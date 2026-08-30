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
| P2 runtime | VERIFIED | Authenticated run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; all five cases passed |
| P6a CORS | VERIFIED | Run `33302495240`; candidate `303f4424…`; deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; artifact `9729387603`; four live cases passed |
| P9 independent verification | NOT EXECUTED | Independent audit/reproduction still required |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## P2 evidence boundary

P2 is now **VERIFIED** for the exact production runtime boundary exercised by authenticated workflow run `33300481208`. The `p2-runtime` job `99227568599` completed successfully and retained artifact `9728767844` with digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`. The artifact records `evidence_class = P2_RUNTIME_EXECUTION`, source commit `303f4424d2198f0d0cf76305c589263dd1e417dc`, deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`, endpoint `https://project-7ybao.vercel.app/api/orchestrate`, and `all_pass = true` for the five specified cases.

The workflow consumed the protected `VERCEL_AUTOMATION_BYPASS_SECRET` without exposing its value. This is authenticated runtime-contract evidence only. It does not close P3–P6, P8, or P9, establish empirical PDMAL efficacy, create a freeze, grant pilot authorization, or increase empirical N.

## P6a evidence boundary

P6a is **VERIFIED** for the exact deployment boundary exercised by run `33302495240`. The run executed four live CORS cases, consumed the protected `VERCEL_AUTOMATION_BYPASS_SECRET` without exposing its value, and retained artifact `9729387603` with digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`.

This closes only the P6a CORS runtime predicate for that candidate/deployment/origin boundary. It does not imply P3–P6 operational closure, P8 closure, experimental efficacy, freeze, or authorization.

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

1. Retain and independently inspect the P2 artifact and logs as part of the candidate evidence packet.
2. Complete P3 candidate-scoped artifact execution evidence.
3. Complete P4 operational blinding/custody evidence.
4. Complete P5 environment/topology/RNG reproducibility evidence.
5. Complete P6 durable archive/retrieval/hash evidence.
6. Bind P7 to the exact final protocol/apparatus/analysis/freeze identity.
7. Close P8 from candidate-scoped evidence, including P2/P6a and all remaining applicable predicates.
8. Prepare and execute independent P9 verification.
9. Create and independently verify a new immutable freeze.
10. Obtain explicit pilot authorization.
11. Only then perform the blinded pilot.

**P2 VERIFIED. P6a VERIFIED. P3–P6 remain evidence-gated. P8 remains OPEN / FAIL-CLOSED. No empirical execution is authorized by this record. N = 0. Authorization is NOT GRANTED.**
