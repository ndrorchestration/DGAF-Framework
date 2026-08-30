---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: 303f4424d2198f0d0cf76305c589263dd1e417dc
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically. Production provenance
  is closed for the merged engineering source, but experimental evidence
  remains separately gated.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current repository lineage | CURRENT | `main` / `303f4424…` | Active engineering and documentation lineage |
| Production source provenance | CLOSED / VERIFIED | Vercel `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` | Production target READY; Vercel Git SHA exactly matches `303f4424…`; `/api/health` HTTP 200 |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` | Historical pre-freeze apparatus evidence; not silently promoted |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` | Historical apparatus only |
| Corrected pilot runner | IMPLEMENTED / EVIDENCE GATED | `pilot_artifact_schema.py` + runner controls | Explicit FFCR outcome, schema/sidecar validation, matrix semantics; pilot execution evidence still gated |
| TGL contract | CURRENT ENGINEERING CONTROL / VERIFIED | Merged PR #148 via `303f4424…` | Required-gate SKIP semantics, fail-closed handling, authority semantics, and final audit sealing validated in current engineering CI |
| Environment lock | VERIFY | CI dependency/runtime configuration | Final freeze candidate must bind exact environment fingerprint |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not efficacy evidence |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic/control evidence only |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` + tests | Structural contract implemented; fresh authorized execution evidence required |
| Security controls | VERIFIED FOR ENGINEERING SCOPE | Current Governance/PDMAL security CI | Does not substitute for P4 operational custody |
| Topology provenance | VERIFY | `PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` | Recompute/bind against exact final freeze candidate |
| Durable retention | OPEN | Policy present | Operational archive + independent retrieval/hash proof required |
| Primary contrast | ADJUDICATED / BINDING PENDING | `dgaf` vs `null`; FFCR; paired seed | Scientific target selected; exact freeze binding remains required |
| Analysis lock | OPEN / FAIL-CLOSED | `PDMAL_ANALYSIS_CONTROL_PLAN.md` / P8 | Exact final apparatus/configuration binding required |
| P2 runtime | VERIFIED | Run `33300481208`; job `99227568599`; artifact `9728767844`; digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5` | Authenticated five-case runtime matrix passed against candidate `303f4424d2198f0d0cf76305c589263dd1e417dc` / deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; artifact `all_pass=true` |
| P6a CORS runtime | VERIFIED | Run `33302495240`; artifact `9729387603`; digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c` | Four live CORS cases passed on candidate `303f4424d2198f0d0cf76305c589263dd1e417dc` / deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`; protected Vercel bypass secret consumed; scoped to exact runtime boundary |
| Independent verification | NOT EXECUTED | P9 design | Must verify candidate-scoped evidence independently |

## P2 evidence boundary

P2 is **VERIFIED** for the exact production runtime boundary exercised by authenticated workflow run `33300481208`. The `p2-runtime` job `99227568599` completed successfully and retained artifact `9728767844` with digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`. The artifact records `evidence_class = P2_RUNTIME_EXECUTION`, source commit `303f4424d2198f0d0cf76305c589263dd1e417dc`, deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`, endpoint `https://project-7ybao.vercel.app/api/orchestrate`, and `all_pass = true` for the five specified cases.

This is authenticated runtime-contract evidence only. It does not close P3–P6, P8, or P9, establish empirical PDMAL efficacy, create a freeze, grant pilot authorization, or increase empirical N.

## P6a evidence boundary

P6a is **VERIFIED** for the exact candidate/deployment/origin boundary exercised by run `33302495240`. The retained artifact is `9729387603` with recorded upload digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`.

This is runtime/CORS evidence only. It does not close P3, P4, P5, P6, P8, P9, establish empirical efficacy, create a freeze, or grant pilot authorization.

## Production provenance

- Main merge SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel production deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Source Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`
- Selected production log window: no error/warning entries returned

This is verified deployment/source evidence only. It does not authorize experimental execution.

## Evidence boundary

Historical acceptance, characterization, synthetic blinding, topology, security, P2, and P6a runtime evidence may establish engineering or operational properties. None establishes empirical PDMAL efficacy. Empirical N remains `0` until the explicit authorization chain is completed and a valid paired pilot observation is accepted.

## TGL/P-35 boundary

The TGL/P-35 remediation is now integrated into the current production engineering source. Historical PR #132/#133/#134 records remain provenance only. Current governance validation demonstrates the repaired semantics; they do not redefine the experimental apparatus or authorize execution.

## Remaining gate sequence

1. Establish final experimental apparatus identity atop `303f4424…`.
2. Candidate-scoped P3 artifact-contract execution evidence.
3. P4 operational blinding/custody evidence.
4. P5 environment/topology/RNG reproducibility.
5. P6 durable archive/retrieval/hash evidence.
6. P7 exact scientific/protocol/apparatus binding.
7. P8 exact analysis lock and closure.
8. Independent P9 verification.
9. New immutable freeze and independent freeze verification.
10. Explicit pilot authorization.
11. Authorized blinded pilot execution.

**P2: VERIFIED. P6a: VERIFIED. P3–P6: evidence-gated. P8: OPEN / FAIL-CLOSED. Empirical N: 0. Pilot authorization: NOT GRANTED. Freeze: NOT CREATED.**
