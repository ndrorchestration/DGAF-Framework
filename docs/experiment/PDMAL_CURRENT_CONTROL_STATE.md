---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: 303f4424d2198f0d0cf76305c589263dd1e417dc
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
| Current engineering/production source | VERIFIED | `303f4424d2198f0d0cf76305c589263dd1e417dc`; production Vercel deployment is READY and exact SHA-bound |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`; not silently promoted |
| **Current pre-freeze candidate** | **DESIGNATED / NOT FROZEN** | `c6157158bf0ee4840e99a381a4b99bd2febe2302` on `experimental-candidate/2026-08-30-reconciled`; requires candidate-scoped verification |
| Corrected runner | IMPLEMENTED / EVIDENCE GATED | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates implemented; candidate execution evidence remains required |
| TGL contract | VERIFIED ENGINEERING CONTROL | Current integrated implementation has required-gate SKIP escalation, fail-closed handling, authority semantics, and final audit sealing; current exact engineering CI passed |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING | `dgaf` vs `null`, FFCR, paired root-seed estimand adopted; exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation exists; complete final-apparatus evidence package remains incomplete |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` enforces structure/hash/matrix/FFCR integrity; fresh candidate execution evidence required |
| Blinding custody | OPEN | Operational custody evidence and separation still required |
| Durable retention | OPEN | Archive destination plus independent retrieval/hash proof required |
| P2 runtime | VERIFIED / PRIOR CANDIDATE-SCOPED | Authenticated run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; all five cases passed. Fresh exact-candidate execution required for `c6157158…`. |
| P6a CORS | VERIFIED / PRIOR CANDIDATE-SCOPED | Run `33302495240`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; artifact `9729387603`; four live cases passed. Fresh exact-candidate execution required for `c6157158…`. |
| P9 independent verification | NOT EXECUTED | Independent audit/reproduction still required |
| New freeze | NOT CREATED | `c6157158…` is a designated pre-freeze candidate, not a freeze |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate identity reconciliation

The apparent discrepancy among `2a80f819…`, `303f4424…`, and the current `main` lineage has been reconciled.

- `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is the P8 checklist ancestor.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` is a descendant of `2a80f819…` and the integrated DGAF v1 engineering/production source.
- Current `main` observed during reconciliation was `255d76f6775caf40e758de4d41920f9ce40fda0c`, itself a descendant of `303f4424…`; the comparison contained documentation/evidence-surface changes only.
- The reconciled mainline was then preserved as a dedicated candidate cycle at `c6157158bf0ee4840e99a381a4b99bd2febe2302` on `experimental-candidate/2026-08-30-reconciled`.

The candidate is designated for verification only. It is not a freeze. No downstream gate may be treated as closed merely because the underlying executable source is ancestral to a previously verified runtime.

## P2 evidence boundary

P2 is **VERIFIED** for the exact production runtime boundary exercised by authenticated workflow run `33300481208`. The `p2-runtime` job `99227568599` completed successfully and retained artifact `9728767844` with digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`. The artifact records `evidence_class = P2_RUNTIME_EXECUTION`, source commit `303f4424d2198f0d0cf76305c589263dd1e417dc`, deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`, endpoint `https://project-7ybao.vercel.app/api/orchestrate`, and `all_pass = true` for the five specified cases.

This evidence remains valid at `303f4424…` and is retained. Because the designated pre-freeze candidate is now `c6157158…`, the evidence must not be relabeled as exact-candidate evidence without a fresh candidate-scoped P2 execution or an explicitly documented equivalence rule that satisfies the governing contract.

## P6a evidence boundary

P6a is **VERIFIED** for the exact deployment boundary exercised by run `33302495240`, candidate `303f4424…`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. The run executed four live CORS cases and retained artifact `9729387603` with digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`.

This evidence remains exact for `303f4424…`. It is not silently transferred to `c6157158…`; fresh exact-candidate execution is required before treating P6a as verified for the designated pre-freeze candidate.

## Production provenance

- Main merge SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`

Production provenance is CLOSED. This does not authorize experimental execution.

## TGL / P-35 remediation boundary

Historical PR #132/#133/#134 records remain diagnostic/provenance records. The repaired semantics are integrated in current main and were validated in current engineering CI. No historical record is promoted across SHA boundaries.

## Required next evidence events

1. Fresh P2 runtime verification against exact pre-freeze candidate `c6157158…` using the candidate's exact deployment identity.
2. Fresh P6a runtime/CORS verification against the exact candidate/deployment boundary, unless the governing contract explicitly permits an equivalence determination.
3. Complete P3 candidate-scoped artifact execution evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Bind P7 to the exact final protocol/apparatus/analysis/freeze identity.
8. Close P8 from candidate-scoped evidence, including all remaining applicable predicates.
9. Prepare and execute independent P9 verification.
10. Create and independently verify a new immutable freeze.
11. Obtain explicit pilot authorization.
12. Only then perform the blinded pilot.

**P2 VERIFIED at `303f4424…`; P6a VERIFIED at `303f4424…`; pre-freeze candidate `c6157158…` designated but not yet execution-verified; P3–P6 remain evidence-gated; P8 remains OPEN / FAIL-CLOSED; no empirical execution is authorized; N = 0; authorization is NOT GRANTED.**
