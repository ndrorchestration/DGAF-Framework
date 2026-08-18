---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 2dc0ce49c30b06807f3d57ce3eac775620b31eb5
---

# PDMAL Current Control State

This document is the detailed operational gate record. GitHub Actions evidence is authoritative for execution state; historical runs are never promoted to current-head evidence. Use `docs/CURRENT_STATE.md` for the concise snapshot and `docs/evidence/PDMAL_EVIDENCE_INDEX.md` for evidence mapping.

## Current branch and implementation

- Branch: `epistemic/evidence-architecture-v1`
- Current head at this synchronization: `2dc0ce49c30b06807f3d57ce3eac775620b31eb5`
- Authoritative task specification: `v0.7.4`
- ConsensusTask implementation: CI-verified by Run #74 on `08500a7`
- Runtime characterization harness/workflow: implemented, execution evidence still open

## Gate board

| Control | State | Evidence / blocker |
|---|---|---|
| Environment lock | CLOSED | Runs #67/#68 passed; genuine resolver lock generation and locked installation observed |
| Fresh contract verification | CLOSED | Run #74 passed after circular-import correction |
| Topology provenance | VERIFIED | Fingerprint/reproducibility tests exercised in the PDMAL CI series |
| Artifact schema/integrity | VERIFIED | Schema versioning, fail-closed validation, and current pre-freeze artifact checks |
| Task specification | APPROVED | v0.7.4 approved for implementation |
| ConsensusTask | VERIFIED | Run #74, commit `08500a7` |
| Runtime characterization | OPEN | Dedicated workflow exists; no characterization execution/artifact observed |
| 300-second seed ceiling | NOT VERIFIED | Must be supported by runtime characterization evidence |
| Blinding custody | OPEN | Protected mapping, separation of duties, and dry-run evidence pending |
| Long-term retention | OPEN | 30-day Actions retention documented; durable policy pending |
| Freeze packet | PENDING | Dependent on remaining controls |
| Protocol freeze | BLOCKED | Not all required controls closed |
| Pilot authorization | NOT GRANTED | Requires explicit post-freeze authorization |
| Empirical data | 0 | No empirical execution authorized |

## Evidence boundaries

Run #67 (`32108612515`) executed SHA `584862645ea9e033ac6e33b0dc6364c731eba7b0` and passed. Run #68 (`32108821363`) executed SHA `46c0d4b04025983e1d997094a4d9d404ace31928` and passed. Both are valid historical evidence for the environment/infrastructure state they tested; they are not evidence for the later current branch head.

Run #73 (`32111238613`) failed because of a circular import during test collection. Run #74 (`32111556449`) passed on `08500a7` and closes that implementation defect.

The runtime characterization harness is an implementation artifact until a dedicated workflow run generates and validates its runtime artifact. Its presence does not close the runtime gate.

## Critical path

1. Execute dedicated runtime characterization.
2. Review runtime artifact and 300-second ceiling verdict.
3. Complete blinding operational verification.
4. Resolve long-term retention.
5. Assemble freeze packet.
6. Freeze protocol/implementation/environment/analysis plan with exact SHAs and timestamp.
7. Explicitly authorize the pilot.
8. Execute empirical work only after authorization.

No empirical execution is authorized by this state record.
