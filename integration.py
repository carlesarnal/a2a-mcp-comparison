"""Real loopback HTTP calls; assert output, errors, progress and cancellation."""
import asyncio
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

ROOT = Path(__file__).resolve().parent
TEXT = 'One implementation can expose multiple interfaces without changing the underlying work.'
EXPECTED = 'One implementation can expose multiple interfaces without changing'


async def rpc(client, method, params):
    response = await client.post('http://127.0.0.1:18201/', json={
        'jsonrpc': '2.0', 'id': uuid.uuid4().hex, 'method': method, 'params': params})
    response.raise_for_status()
    value = response.json()
    assert 'error' not in value, value
    return value['result']


def message(text, delay=0, blocking=True):
    return {'message': {'role': 'user', 'messageId': uuid.uuid4().hex,
                        'parts': [{'kind': 'text', 'text': json.dumps({'text': text, 'delay': delay})}]},
            'configuration': {'blocking': blocking}}


async def check():
    observations = {}
    async with httpx.AsyncClient(timeout=15) as client:
        card = (await client.get('http://127.0.0.1:18201/.well-known/agent-card.json')).json()
        assert card['skills'][0]['id'] == 'summary'
        good = await rpc(client, 'message/send', message(TEXT))
        assert good['status']['state'] == 'completed', good
        assert good['artifacts'][0]['parts'][0]['text'] == EXPECTED, good
        bad = await rpc(client, 'message/send', message(''))
        assert bad['status']['state'] == 'failed', bad
        slow = await rpc(client, 'message/send', message(TEXT, 4, False))
        task_id = slow['id']
        for _ in range(30):
            state = await rpc(client, 'tasks/get', {'id': task_id})
            if state['status']['state'] == 'working':
                break
            await asyncio.sleep(.05)
        assert state['status']['state'] == 'working', state
        canceled = await rpc(client, 'tasks/cancel', {'id': task_id})
        assert canceled['status']['state'] == 'canceled', canceled
        await asyncio.sleep(.1)
        after = await rpc(client, 'tasks/get', {'id': task_id})
        assert after['status']['state'] == 'canceled' and not after.get('artifacts'), after
        observations['a2a'] = {'protocol': card.get('protocolVersion'), 'output': EXPECTED,
                               'invalid_input': 'failed task', 'progress': 'working via tasks/get',
                               'cancel': 'canceled task, no artifact'}
    async with streamablehttp_client('http://127.0.0.1:18202/mcp') as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            tools = await session.list_tools()
            assert tools.tools[0].name == 'summary'
            progress = []

            async def on_progress(value, total, detail):
                progress.append(value)

            good = await session.call_tool('summary', {'text': TEXT}, progress_callback=on_progress)
            assert not good.isError and good.content[0].text == EXPECTED, good
            assert progress == [0, 1], progress
            bad = await session.call_tool('summary', {'text': ''})
            assert bad.isError, bad
            # MCP cancellation is a request notification, not a persisted task state.
            # Cancel the client operation; the SDK emits notifications/cancelled.
            progress.clear()
            task = asyncio.create_task(session.call_tool('summary', {'text': TEXT, 'delay': 4},
                                                        progress_callback=on_progress))
            for _ in range(100):
                if progress:
                    break
                await asyncio.sleep(.02)
            assert progress == [0], progress
            task.cancel()
            try:
                await task
                raise AssertionError('canceled request returned successfully')
            except asyncio.CancelledError:
                pass
            # Session remains usable after cancellation.
            again = await session.call_tool('summary', {'text': TEXT})
            assert again.content[0].text == EXPECTED and not again.isError
            observations['mcp'] = {'protocol': initialized.protocolVersion, 'output': EXPECTED,
                                   'invalid_input': 'isError tool result', 'progress': progress,
                                   'cancel': 'client request canceled; next request succeeds; no durable task store'}
    return observations


def main():
    processes, logs = [], []
    target = ROOT / 'target'
    target.mkdir(exist_ok=True)
    try:
        for protocol, port in [('a2a',18201),('mcp',18202)]:
            log = open(target/f'{protocol}.log', 'w')
            logs.append(log)
            processes.append(subprocess.Popen([sys.executable,str(ROOT/'server.py'),protocol,'--port',str(port)], stdout=log, stderr=log))
        for _ in range(60):
            try:
                if httpx.get('http://127.0.0.1:18201/.well-known/agent-card.json').status_code == 200:
                    httpx.get('http://127.0.0.1:18202/mcp')
                    break
            except httpx.HTTPError:
                pass
            if any(p.poll() is not None for p in processes):
                raise RuntimeError('server exited; see target logs')
            time.sleep(.25)
        result = asyncio.run(check())
        (ROOT/'observations.json').write_text(json.dumps(result, indent=2)+'\n')
        comparison = json.loads((ROOT/'comparison.json').read_text())
        for row in comparison['observations']:
            row.update(a2a='observed',mcp='observed',evidence=['observations.json'])
        comparison['boundary'] = 'Loopback official SDKs, deterministic fixture; MCP cancellation is client-observed, not a durable task guarantee.'
        (ROOT/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
        print(json.dumps(result, indent=2))
    finally:
        for process in processes:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        for log in logs:
            log.close()


if __name__ == '__main__':
    main()
