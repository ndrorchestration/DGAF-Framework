# 2026-09-03 — Current Evidence Execution Record

## Current verified runtime boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Verified executable runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Runtime tree: `586c00d6dedb589e52108279f9759be3c4f927e1`
- Verified deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- Control-plane documentation head: `637023b28492783f50d77550d4ed8e0867cbcc3d`

## Closed gates retained

P2 and P6a remain CLOSED / VERIFIED. The control-plane/documentation successor does not modify the runtime surfaces they test.

- P2 run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`
- P6a run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`

## Engineering evidence completed

The PDMAL pre-freeze runner validation completed successfully with:

- 44 harness contract tests passing;
- contract-mode validation passing;
- unauthorized pilot execution failing closed;
- artifact schema/integrity checks passing;
- pre-freeze manifest generated and uploaded.

The PDMAL instrumentation dry-run suite also completed successfully with 19 structural/artifact tests passing, deterministic smoke reproduction, blinding-secret presence, masked CSV generation, schema validation, and checksum verification.

These are engineering/control evidence and do not advance empirical N.

## Remaining gates

| Gate | State | Remaining requirement |
|---|---|---|
| P3 | OPEN | Current-cycle artifact contract evidence bound to the selected execution candidate |
| P4 | OPEN | Operational blinding/custody, access separation, and custody record |
| P5 | OPEN | Exact candidate reproducibility, environment/toolchain/topology/RNG evidence |
| P6 | OPEN / FAIL-CLOSED | Durable external archive, independent retrieval, SHA-256 recomputation, round-trip proof |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact scientific/protocol/apparatus/candidate binding |
| P8 | OPEN / FAIL-CLOSED | Analysis lock and prerequisite verification |
| P9 | OPEN | Independent verification against the same final evidence set |
| Freeze | NOT ESTABLISHED | Immutable final identity not created |
| Authorization | NOT GRANTED | Separate governance decision required |
| Empirical N | 0 | No authorized pilot execution |

## Execution constraint

The current connected GitHub interface does not expose a deliberate workflow-dispatch operation. Therefore this record does not claim a deliberate current-main experimental run. The experiment workflow itself now has explicit path isolation and `workflow_dispatch` so documentation changes cannot create experimental candidates.

## Next executable operation

Run the PDMAL evidence workflow deliberately against the exact selected candidate after the control-plane fixes are merged. Use its resulting artifact set to close P3/P4/P5, then complete P6 durable custody, P7 binding, P8, and P9 before freeze.

**Boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
