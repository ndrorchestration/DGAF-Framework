---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 08500a7a129a39c21dc890a71a85e5d996e4c4b3
verification_evidence: Run #74 (32111556449)
---

# PDMAL Evidence Index

This index maps material controls to the strongest retained evidence currently available. A passing run is scoped to its exact executed SHA; later commits do not inherit its verification automatically.

| Control | Status | Evidence | Tested SHA | Run / artifact |
|---|---|---|---|---|
| Environment lock | VERIFIED | Resolver-generated full lock produced and locked installation succeeded | `584862645ea9e033ac6e33b0dc6364c731eba7b0` | Run #67 `32108612515`; corroborated by Run #68 `32108821363` |
| Topology provenance | VERIFIED | Fingerprints, integration, and reproducibility tests exercised in fresh PDMAL CI | Run-specific; see CI history | Runs #67/#68 and subsequent pre-freeze evidence |
| Artifact schema/integrity | VERIFIED | Schema versioning, fail-closed checks, artifact validation | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` | Run #74 `32111556449` |
| v0.7.4 task specification | APPROVED | Expert-panel adjudication and repository specification | `e421bb48ae02080119685d0de7241288fafc90d7` | Notion governance record |
| ConsensusTask implementation | VERIFIED | Contract suite passed after implementation and circular-import correction | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` | Run #74 `32111556449` |
| Runtime characterization | OPEN | Dedicated harness/workflow implemented; execution evidence not yet observed | — | — |
| 300-second ceiling | NOT VERIFIED | Requires dedicated characterization artifact | — | — |
| Blinding operational verification | OPEN | Procedural dry-run and custody evidence pending | — | — |
| Long-term retention | OPEN | 30-day workflow retention documented; durable long-term decision pending | — | — |
| Freeze packet | PENDING | Upstream controls remain open | — | — |
| Protocol freeze | BLOCKED | Freeze prerequisites remain open | — | — |
| Pilot authorization | NOT GRANTED | Requires explicit post-freeze authorization | — | — |

## Historical evidence

- Run #73 (`32111238613`) failed on `0e7ecd03` due to a circular import during test collection. It is retained as diagnostic history and does not represent the current implementation after `08500a7`.
- Earlier historical CI remains scoped to its own executed source and is never silently promoted to current-head verification.

## Evidence classes

Use the repository's evidence ladder policy in `docs/evidence/EVIDENCE_LADDER_POLICY.md` when assigning or promoting labels.
