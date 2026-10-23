# Evidence

Official SDK loopback integration passed. Both interfaces returned the same eight-word fixture. Blank input produced a failed A2A task and an MCP error result. A2A exposed working/canceled task states; MCP exposed progress notifications and client-request cancellation with a usable subsequent session.

A2A SDK 0.3.22 / protocol 0.3.0; MCP SDK 1.26.0 / protocol 2025-11-25. Python implementation, not the previously proposed Quarkus comparison. MCP server-side compute cessation is not proven by client cancellation; neither implementation persists tasks across restart. No auth or production inference benchmark.

See `observations.json` and the runner assertions. Results are observed fixture behavior, not acceptance predictions.
