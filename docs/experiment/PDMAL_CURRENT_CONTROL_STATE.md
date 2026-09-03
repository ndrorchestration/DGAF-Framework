---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_control_plane_head: 637023b28492783f50d77550d4ed8e0867cbcc3d
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_deployment_identity: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_deployment_state: READY
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. The control-plane successor is documentation-only; the verified runtime candidate and its closed P2/P6a evidence remain explicitly identified.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Control-plane mainline | CURRENT | `637023b2…` |
| Executable runtime candidate | VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Candidate deployment | ESTABLISHED / READY | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` |
| P2 runtime | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704` |
| P6a CORS | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299` |
| P3 | OPEN | Current-cycle artifact contract |
| P4 | OPEN | Operational blinding/custody |
| P5 | OPEN | Reproducibility/provenance |
| P6 | OPEN / FAIL-CLOSED | Durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact candidate/protocol/analysis binding |
| P8 | OPEN / FAIL-CLOSED | Analysis lock and prerequisites |
| P9 | OPEN | Independent verification |
| Freeze | NOT ESTABLISHED | No immutable pilot identity |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Runtime evidence boundary

P2 and P6a are closed for the exact `7c1cc4…` / `dpl_8Ms…` runtime binding. The later `637023…` control-plane change is documentation-only with respect to those runtime surfaces, so the closed predicates remain closed.

## Pre-freeze validation

The PDMAL pre-freeze runner validation completed successfully on the governance branch with 44 harness tests passing, contract-mode validation passing, unauthorized pilot mode failing closed, artifact schema/integrity checks passing, and a retained pre-freeze manifest artifact. This is engineering/control evidence, not empirical efficacy evidence.

## Instrumentation workflow isolation

The PDMAL instrumentation workflow is restricted to experiment-path changes and deliberate `workflow_dispatch`, preventing documentation-only changes from becoming experimental candidates. The earlier successful PR instrumentation run remains trigger-isolation validation and does not advance empirical N.

## Required closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
