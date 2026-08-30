---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
pre_freeze_candidate_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
pre_freeze_candidate_ref: experimental-candidate/2026-08-30-reconciled
candidate_status: DESIGNATED / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is provenance only |
| Current engineering/production source | VERIFIED | `303f4424d2198f0d0cf76305c589263dd1e417dc`; prior production Vercel deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` is READY and exact SHA-bound |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`; not silently promoted |
| **Current pre-freeze candidate** | **DESIGNATED / NOT FROZEN** | `c6157158bf0ee4840e99a381a4b99bd2febe2302` on `experimental-candidate/2026-08-30-reconciled`; candidate deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` is now READY and exact SHA-bound |
| Corrected runner | IMPLEMENTED / EVIDENCE GATED | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates implemented; candidate execution evidence remains required |
| TGL contract | VERIFIED ENGINEERING CONTROL | Current integrated implementation has required-gate SKIP escalation, fail-closed handling, authority semantics, and final audit sealing; current exact engineering CI passed |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING | `dgaf` vs `null`, FFCR, paired root-seed estimand adopted; exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation exists; complete final-apparatus evidence package remains incomplete |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` enforces structure/hash/matrix/FFCR integrity; fresh candidate execution evidence required |
| Blinding custody | OPEN | Operational custody evidence and separation still required |
| Durable retention | OPEN | Archive destination plus independent retrieval/hash proof required |
| P2 runtime | VERIFIED / PRIOR CANDIDATE-SCOPED | Run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; all five cases passed. Fresh exact-candidate execution required for `c6157158…`. |
| P6a CORS | VERIFIED / PRIOR CANDIDATE-SCOPED | Run `33302495240`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; artifact `9729387603`; four live cases passed. Fresh exact-candidate execution required for `c6157158…`. |
| P9 independent verification | NOT EXECUTED | Independent audit/reproduction still required |
| New freeze | NOT CREATED | `c6157158…` is a designated pre-freeze candidate, not a freeze |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate identity reconciliation

The previous SHA discrepancy has been explicitly reconciled.

- `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is the P8 checklist ancestor.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` is a descendant of `2a80f819…` and the integrated DGAF v1 engineering/production source.
- `255d76f6775caf40e758de4d41920f9ce40fda0c` was the `main` tip observed during the reconciliation and is a descendant of `303f4424…`; the interval compared contained documentation/evidence-surface changes only.
- `c6157158bf0ee4840e99a381a4b99bd2febe2302` is the explicitly designated pre-freeze candidate for the next evidence cycle.

These identities must remain distinct by role. Historical P2/P6a evidence at `303f4424…` is retained and cannot be relabeled as `c6157158…` evidence without fresh candidate-scoped verification.

## Candidate deployment provenance

The designated candidate now has a READY Vercel production deployment:

- Candidate: `c6157158bf0ee4840e99a381a4b99bd2febe2302`
- Deployment: `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`
- Vercel Git source SHA: exact match to candidate
- Target: `production`
- State: `READY`

This closes only candidate deployment/source provenance. It does not execute or close P2/P6a.

## P2 evidence boundary

P2 is **VERIFIED** for the exact production runtime boundary exercised by authenticated workflow run `33300481208`. The artifact records `evidence_class = P2_RUNTIME_EXECUTION`, source commit `303f4424d2198f0d0cf76305c589263dd1e417dc`, deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`, and `all_pass = true` for the five specified cases.

This evidence remains valid at `303f4424…`. Because the designated pre-freeze candidate is `c6157158…`, fresh exact-candidate P2 execution is required before P2 can be promoted from prior candidate-scoped evidence to current-candidate verification. The candidate deployment is now READY and supplies the exact deployment boundary needed for that run, but no current-candidate P2 run is yet recorded.

## P6a evidence boundary

P6a is **VERIFIED** for the exact runtime boundary exercised by run `33302495240`, candidate `303f4424…`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. The retained artifact is `9729387603` with recorded digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`.

This evidence remains exact for `303f4424…`. It is not silently transferred to `c6157158…`. The candidate deployment is now READY, so fresh exact-candidate P6a execution can be bound to it; no such current-candidate run is yet recorded.

## Production provenance

- Mainline engineering source: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Prior Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`

Production provenance is CLOSED for the engineering source. Candidate deployment provenance is separately CLOSED for `c6157158…` via `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`. Neither provenance result authorizes experimental execution.

## Required next evidence events

1. Execute fresh P2 runtime verification against candidate `c6157158…` and deployment `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`.
2. Execute fresh P6a runtime/CORS verification against the same exact candidate/deployment boundary.
3. Complete P3 candidate-scoped artifact-contract execution evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Bind P7 to the exact final protocol/apparatus/analysis/freeze identity.
8. Close P8 from candidate-scoped evidence, including all remaining applicable predicates.
9. Prepare and execute independent P9 verification.
10. Create and independently verify a new immutable freeze.
11. Obtain explicit pilot authorization.
12. Only then perform the blinded pilot.

**Prior P2/P6a verified at `303f4424…`; current pre-freeze candidate `c6157158…` is designated and deployment-provenanced but not yet runtime-verified; P3–P6 remain evidence-gated; P8 remains OPEN / FAIL-CLOSED; no empirical execution is authorized; N = 0; authorization is NOT GRANTED.**
