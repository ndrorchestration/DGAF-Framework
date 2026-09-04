---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
current_main_tip: 08f29b7addab98dbc5460c31f2597d7b29e31e8a
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
verified_runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
verified_runtime_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The consolidated control-state anchor is `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`. The live `main` tip is `08f29b7addab98dbc5460c31f2597d7b29e31e8a`; commits after the consolidated anchor are documentation/control-plane reconciliation and must not be mistaken for a new executable candidate unless executable semantics materially change.

The verified executable runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, with Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to that exact Git SHA. The control-plane/documentation lineage must not be conflated with that separately scoped runtime identity.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Live `main` tip | CURRENT | `08f29b7a…` |
| Verified executable runtime candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Candidate deployment | VERIFIED READY | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to `7c1cc4…` |
| P2 | CLOSED / VERIFIED | run `33730195621`, artifact `9883521704` |
| P6a | CLOSED / VERIFIED | run `33728695806`, artifact `9882965299` |
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

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_PACKET_2026-09-04.md` defines the exact current-candidate P3–P9 packet boundary. It distinguishes retained P2/P6a runtime evidence from the outstanding current-candidate operational, provenance, durable-custody, analysis-lock, and independent-verification predicates.

## Evidence boundary

Closed P2/P6a runtime evidence remains scoped to the verified executable runtime identity above. Documentation/control-plane changes do not reopen those predicates unless the runtime surface or governing acceptance conditions materially change. No empirical efficacy conclusion follows from runtime or CI checks.

The strongest historical completion evidence remains scoped to superseded candidate `a43219b4…` and does not transfer to `7c1cc4…` without an explicit provenance relationship.

## Documentation architecture boundary

Agent-identity, registry-synchronization, numerical-instrument, metrics-provenance, and documentation-integration workstreams remain separately scoped. Their reconciliation artifacts do not silently change experimental authority.

## Current substantive closure work

The remaining task is one-candidate evidence assembly, not additional speculative governance architecture:

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

The active completion control record is GitHub Issue #232. Superseded planning records #184 and #186 remain historical provenance.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
