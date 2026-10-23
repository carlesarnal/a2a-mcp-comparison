"""Validate evidence records without confusing schema validity with observed parity."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--require-observed', action='store_true')
args = parser.parse_args()
data = json.loads(Path(__file__).with_name('comparison.json').read_text())
seen = set()
for row in data['observations']:
    assert row['requirement'] not in seen
    seen.add(row['requirement'])
    for protocol in ('a2a', 'mcp'):
        assert row[protocol] in {'untested', 'observed', 'unsupported'}
    if 'observed' in (row['a2a'], row['mcp']):
        assert row['evidence'], 'observed behavior requires an evidence reference'
    print(f"{row['requirement']}: A2A={row['a2a']}, MCP={row['mcp']}")
    if args.require_observed and ('untested' in (row['a2a'], row['mcp']) or not row['evidence']):
        raise SystemExit('DELIVERY GATE FAILED: paired observations still required')
print('Evidence structure valid; this is not a runtime compatibility test.')
