# A2A or MCP? Choosing an Interface for the Same Capability

Official SDK loopback integration passed. Both interfaces returned the same eight-word fixture. Blank input produced a failed A2A task and an MCP error result. A2A exposed working/canceled task states; MCP exposed progress notifications and client-request cancellation with a usable subsequent session.

## Run

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python integration.py
.venv/bin/python compare.py --require-observed
```

## Evidence and boundaries

A2A SDK 0.3.22 / protocol 0.3.0; MCP SDK 1.26.0 / protocol 2025-11-25. Python implementation, not the previously proposed Quarkus comparison. MCP server-side compute cessation is not proven by client cancellation; neither implementation persists tasks across restart. No auth or production inference benchmark.

Observed machine-readable results: [observations.json](observations.json).

All containers/processes created by the runner are cleaned up on normal completion and handled failures. An externally killed process may need the explicit Compose cleanup command. Use only disposable local test resources.

## Present

Open `presentation.html`; arrows/Page keys navigate and N toggles notes. Use `PRESENTATION_GUIDE.md` for timing and the actual commands.
