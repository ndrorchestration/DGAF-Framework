---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 458bb346569937455b796977dc571af17b64da65
verification_evidence: Runtime Run #14 (32112658368)
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
| Runtime characterization | OPERATIONALLY CHARACTERIZED | 72/72 matrix trials completed; dedicated artifact validated | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` | Run #14 `32112658368`; artifact `9315467977` |
| 300-second ceiling | VERIFIED FOR CHARACTERIZATION MATRIX | All measured seed runtimes below 300 seconds | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` | Artifact digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Blinding operational verification | OPEN | Synthetic dry-run workflow implemented; execution evidence not yet observed | — | Workflow pending execution |
| Long-term retention | OPEN | Retention policy decided; durable research archive not yet established/verified | `004ec9aa6b3ee1fc30b6f0fa22098be5cdedf0fa` | Policy document |
| Freeze packet | PENDING | Upstream controls remain open | — | — |
| Protocol freeze | BLOCKED | Freeze prerequisites remain open | — | — |
| Pilot authorization | NOT GRANTED | Requires explicit post-freeze authorization | — | — |

## Runtime characterization details

Run #14 executed on `a0ff248eadb736f9b5835f2436791dc6abf66cc` and completed 72/72 expected trials. The dedicated workflow validated `protocol_status=PRE-FREEZE`, `empirical_data_collection=false`, artifact completeness, and the 300-second ceiling predicate before upload. Artifact `9315467977` has digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27`.

## Historical evidence

- Run #73 (`32111238613`) failed on `0e7ecd03` due to a circular import during test collection. It remains diagnostic history and does not represent the current implementation after `08500a7`.
- Earlier CI remains scoped to its own executed source and is never silently promoted to current-head verification.

## Evidence classes

Use the repository's evidence ladder policy in `docs/evidence/EVIDENCE_LADDER_POLICY.md` when assigning or promoting labels.
