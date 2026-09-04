---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
mainline_tip_at_last_reconciliation: 16d64bd66231b926d923a5eafecb3a75f71fad48
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. The consolidated control-state anchor is `89be386b…`. `16d64bd6…` is the mainline tip at the latest reconciliation point; later updates to this file are documentation/control-plane descendants. Those descendants do not alter executable runtime semantics unless executable surfaces materially change.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Mainline reconciliation anchor | DOCUMENTATION/CONTROL-PLANE | `16d64bd6…` |
| Runtime candidate lineage | PRESENT | candidate identity `7c1cc4…` |
| Deployment reference | HISTORICAL / CURRENT RETRIEVAL UNCONFIRMED | deployment identity `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` |
| P2 runtime | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | Run `33730195621`; artifact `9883521704` |
| P6a CORS | HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED | Run `33728695806`; artifact `9882965299` |
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

The repository preserves P2 and P6a run/artifact identifiers for the exact `7c1cc4…` / `dpl_8Ms…` lineage. The 2026-09-04 verification pass did not independently re-retrieve those Actions records, so they remain historical repository assertions rather than freshly verified current evidence. This does not establish deletion, invalidity, or tampering; it establishes only that fresh retrieval was not achieved through the verification path used.

## Evidence registry hardening

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_REGISTRY_CONTRACT_v1.md` defines the unified immutable evidence-source tuple. Draft PR #236 is the current implementation lane: exact checked-out candidate verification, executed tree capture, producing workflow/run capture, protocol digest capture, and predicate-level candidate/run binding. The first implementation run on predecessor #235 passed the entire PDMAL dry-run, and its artifact was directly inspected; a separate Control-State Consistency mismatch was then corrected without weakening the validator.

## Required closure sequence

`P1/P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
