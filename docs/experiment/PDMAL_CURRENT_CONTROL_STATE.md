---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
current_mainline_commit_at_last_reconciliation: 90dab43838810cf73fac626c6268ab81ac4972b0
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. The consolidated control-state anchor is `89be386b…`. `90dab438…` records the mainline at the last reconciliation point; subsequent commits to this file are documentation/control-plane descendants. Those descendants do not alter executable runtime semantics unless executable surfaces materially change.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Mainline reconciliation anchor | DOCUMENTATION/CONTROL-PLANE | `90dab438…` |
| Runtime candidate lineage | PRESENT | `7c1cc4…` |
| Deployment reference | HISTORICAL / CURRENT RETRIEVAL UNCONFIRMED | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` |
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

## Current-candidate evidence packet

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_PACKET_2026-09-04.md` defines the remaining P3–P9 evidence boundary and explicitly distinguishes historical repository-recorded P2/P6a identifiers from currently retrievable evidence.

## Evidence registry hardening

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_REGISTRY_CONTRACT_v1.md` defines a unified immutable evidence-source tuple. Draft PR #236 is the current implementation lane: it adds exact checked-out candidate verification, executed tree capture, producing workflow/run capture, protocol digest capture, and predicate-level candidate/run binding to the PDMAL dry-run registry. Its predecessor #235 was superseded after CI exposed and corrected a validator-compatible control-state labeling mismatch.

## Pre-freeze validation

The PDMAL pre-freeze runner validation completed successfully on the governance branch with 44 harness tests passing, contract-mode validation passing, unauthorized pilot mode failing closed, artifact schema/integrity checks passing, and a retained pre-freeze manifest artifact. This is engineering/control evidence, not empirical efficacy evidence.

## Instrumentation workflow isolation

The PDMAL instrumentation workflow is restricted to experiment-path changes and deliberate `workflow_dispatch`, preventing documentation-only changes from becoming experimental candidates. Earlier successful instrumentation runs remain trigger-isolation validation and do not advance empirical N.

## Matrix-control disposition

PRs #220, #230, and #231 were closed without merge. Review established that the proposed additional per-condition matrix-equality assertion was logically implied by the existing canonical coordinate membership, exact per-condition cardinality, and duplicate `(condition, topology, failure_count)` rejection. No active matrix-hardening blocker remains.

## Required closure sequence

`P1/P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
