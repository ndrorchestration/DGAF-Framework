---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: 303f4424d2198f0d0cf76305c589263dd1e417dc
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is provenance only |
| Current engineering/production source | VERIFIED | `303f4424d2198f0d0cf76305c589263dd1e417dc`; production Vercel deployment is READY and exact SHA-bound |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`; not silently promoted |
| Corrected runner | IMPLEMENTED / EVIDENCE GATED | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates implemented; authorized execution evidence absent |
| TGL contract | VERIFIED ENGINEERING CONTROL | Current integrated implementation has required-gate SKIP escalation, fail-closed handling, authority semantics, and final audit sealing; current exact engineering CI passed |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING | `dgaf` vs `null`, FFCR, paired root-seed estimand adopted; exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation exists; complete final-apparatus evidence package remains incomplete |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` enforces structure/hash/matrix/FFCR integrity; fresh authorized execution evidence required |
| Blinding custody | OPEN | Operational custody evidence and separation still required |
| Durable retention | OPEN | Archive destination plus independent retrieval/hash proof required |
| P2 runtime | BLOCKED / OPEN | Authenticated workflow dispatch required against exact production deployment |
| P6a CORS | BLOCKED / OPEN | Authenticated workflow dispatch required against same deployment |
| P9 independent verification | NOT EXECUTED | Independent audit/reproduction still required |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Production provenance

- Main merge SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`

Production provenance is CLOSED. This does not close P2/P6a or authorize experimental execution.

## TGL / P-35 remediation boundary

Historical PR #132/#133/#134 records remain diagnostic/provenance records. The repaired semantics are integrated in current main and were validated in current engineering CI. No historical record is promoted across SHA boundaries.

## Required next evidence events

1. Execute authenticated P2 against the exact production deployment.
2. Execute authenticated P6a against the same deployment identity.
3. Retain and independently inspect P2/P6a artifacts/logs.
4. Complete P3 candidate-scoped artifact execution evidence.
5. Complete P4 operational blinding/custody evidence.
6. Complete P5 environment/topology/RNG reproducibility evidence.
7. Complete P6 durable archive/retrieval/hash evidence.
8. Bind P7 to the exact final protocol/apparatus/analysis/freeze identity.
9. Close P8 from candidate-scoped evidence.
10. Prepare and execute independent P9 verification.
11. Create and independently verify a new immutable freeze.
12. Obtain explicit pilot authorization.
13. Only then perform the blinded pilot.

**No empirical execution is authorized by this record. N = 0. Authorization is NOT GRANTED.**
