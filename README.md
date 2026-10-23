# A2A or MCP? Compare the Caller Contract

A research and presentation repository for exposing **the same summarization
capability** through two interfaces. This is distinct from the connected
[agent-discovery demo](https://github.com/carlesarnal/agent-discovery-demo/tree/cloud-native-paris-2026),
which invokes different capabilities and cannot establish interface equivalence.

## Evidence first

Run `python3 compare.py` to validate the decision-table records. The initial table
honestly marks paired-runtime observations as untested. `python3 compare.py --require-observed`
is the delivery gate and fails until every claimed comparison has supporting observations.
Do not turn that failure into a green check by changing labels without running the tests.

The lab plan holds input and implementation constant, records SDK/protocol versions,
then compares discovery, output, failed invocation, task progress and cancellation.
The model itself must not be the uncontrolled variable: begin with a deterministic
summary fixture and add a real model only after transport behavior is understood.

The repository currently supplies the evidence schema, comparison method and
presentation plan. It is **not yet a completed side-by-side protocol implementation**.
See `VERIFICATION.md` and `PRESENTATION_GUIDE.md`.

License: Apache-2.0; see LICENSE.
