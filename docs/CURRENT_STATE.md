---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it. A repository record of prior verification is distinct from successful current retrieval of the underlying evidence artifact.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The consolidated control-state anchor is `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`. `main` now contains subsequent documentation/control-plane descendants; those descendants do not alter executable runtime semantics unless executable surfaces materially change.

The current **candidate identity** record for the runtime lineage referenced by historical P2/P6a evidence is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`. The current **deployment identity** record referencing that runtime is `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. The present verification pass did not independently re-retrieve the cited Actions records, so those runtime results are not promoted here as freshly verified evidence.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Runtime candidate lineage | PRESENT | candidate identity `7c1cc4bb…` |
| Deployment reference | HISTORICAL / CURRENT RETRIEVAL UNCONFIRMED | deployment identity `dpl_8Msuf…` |
| P2 | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | run `33730195621`, artifact `9883521704` |
| P6a | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | run `33728695806`, artifact `9882965299` |
| P3 | OPEN / CURRENT EVIDENCE REQUIRED | artifact-contract closure |
| P4 | OPEN | operational blinding/custody |
| P5 | OPEN | reproducibility/provenance closure |
| P6 | OPEN / FAIL-CLOSED | durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | exact final candidate/protocol/analysis binding |
| P8 | OPEN / FAIL-CLOSED | exact prerequisites and analysis lock |
| P9 | OPEN | independent verification |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized pilot execution |

## Current-candidate evidence packet

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_PACKET_2026-09-04.md` is present in the current GitHub `main` tree and defines the exact P3–P9 evidence boundary. It explicitly distinguishes historical repository-recorded P2/P6a identifiers from currently retrievable evidence.

## Evidence boundary

The P2/P6a run and artifact identifiers remain preserved as provenance records. Their present verification state is **not currently retrievable through the verification path used in the 2026-09-04 pass**. This does not establish deletion, invalidity, or tampering; it establishes only that fresh retrieval was not achieved.

The strongest historical completion evidence remains scoped to superseded candidate `a43219b4…` and does not transfer to `7c1cc4…` without an explicit provenance relationship.

## Documentation architecture boundary

Agent-identity, registry-synchronization, numerical-instrument, and documentation-integration reconciliation work remains separately scoped. These controls do not resolve disputed authority or change experimental state by themselves.

## Current substantive closure work

The remaining task is one-candidate evidence assembly, not additional speculative governance architecture:

`P1/P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

The active completion control record is GitHub Issue #232. Superseded planning records #184 and #186 remain historical provenance.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
