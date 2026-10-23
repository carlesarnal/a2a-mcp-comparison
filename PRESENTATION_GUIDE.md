# Presentation guide

A2A or MCP? Choosing an Interface for the Same Capability

## 0:00 — One capability, two actual transports

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 4:00 — Identical output is only the starting point

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 9:00 — Failed task versus tool error result

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 15:00 — Progress and cancellation expose different caller contracts

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 21:00 — A canceled request is not proof of durable recovery

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 26:00 — Questions and buffer

A2A SDK 0.3.22 / protocol 0.3.0; MCP SDK 1.26.0 / protocol 2025-11-25. Python implementation, not the previously proposed Quarkus comparison. MCP server-side compute cessation is not proven by client cancellation; neither implementation persists tasks across restart. No auth or production inference benchmark.

## Commands

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python integration.py
.venv/bin/python compare.py --require-observed
```

## Observed result

Official SDK loopback integration passed. Both interfaces returned the same eight-word fixture. Blank input produced a failed A2A task and an MCP error result. A2A exposed working/canceled task states; MCP exposed progress notifications and client-request cancellation with a usable subsequent session.

For 25 minutes, shorten setup and keep one trace plus the failure result. A backup recording must show a real run, not synthetic output.
