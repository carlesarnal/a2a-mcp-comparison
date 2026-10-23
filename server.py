"""The same deterministic capability served by the official A2A and MCP SDKs."""
import argparse
import asyncio
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCard, AgentCapabilities, AgentSkill, Part, TextPart, TaskState
from a2a.utils import new_task, new_agent_text_message
from mcp.server.fastmcp import FastMCP, Context
import uvicorn


def summarize(text):
    if not text.strip():
        raise ValueError('text must not be blank')
    return ' '.join(text.split()[:8])


class Executor(AgentExecutor):
    def __init__(self):
        self.stops = {}

    async def execute(self, context: RequestContext, event_queue):
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        stop = self.stops[task.id] = asyncio.Event()
        try:
            payload = json.loads(context.get_user_input())
            result = summarize(payload['text'])
            delay = min(max(float(payload.get('delay', 0)), 0), 5)
            await updater.update_status(TaskState.working)
            try:
                await asyncio.wait_for(stop.wait(), timeout=delay or 0.001)
                return  # cancel() publishes the terminal event
            except asyncio.TimeoutError:
                pass
            await updater.add_artifact([Part(root=TextPart(text=result))], name='summary')
            await updater.complete()
        except (ValueError, KeyError, TypeError) as error:
            await updater.update_status(TaskState.failed, new_agent_text_message(str(error)), final=True)
        finally:
            self.stops.pop(task.id, None)

    async def cancel(self, context, event_queue):
        stop = self.stops.get(context.task_id)
        if stop:
            stop.set()
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.update_status(TaskState.canceled, final=True)


def a2a_app(port):
    card = AgentCard(name='Same summarizer', description='Deterministic first-eight-word fixture',
                     url=f'http://127.0.0.1:{port}/', version='1.0.0',
                     capabilities=AgentCapabilities(streaming=True),
                     default_input_modes=['text/plain'], default_output_modes=['text/plain'],
                     skills=[AgentSkill(id='summary', name='Summary', description='First eight words', tags=['summary'])])
    return A2AStarletteApplication(agent_card=card, http_handler=DefaultRequestHandler(
        agent_executor=Executor(), task_store=InMemoryTaskStore())).build()


def mcp_server(port):
    app = FastMCP('Same summarizer', host='127.0.0.1', port=port, json_response=True)

    @app.tool()
    async def summary(text: str, ctx: Context, delay: float = 0) -> str:
        result = summarize(text)
        await ctx.report_progress(0, 1, 'working')
        await asyncio.sleep(min(max(delay, 0), 5))
        await ctx.report_progress(1, 1, 'complete')
        return result

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('protocol', choices=['a2a', 'mcp'])
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    if args.protocol == 'a2a':
        uvicorn.run(a2a_app(args.port), host='127.0.0.1', port=args.port)
    else:
        mcp_server(args.port).run(transport='streamable-http')
