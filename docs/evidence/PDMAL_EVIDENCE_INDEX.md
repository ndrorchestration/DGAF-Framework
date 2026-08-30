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
| Independent verification | NOT EXECUTED | P9 design | Must verify candidate-scoped evidence independently |

## Production provenance

- Main merge SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel production deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Source Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`
- Selected production log window: no error/warning entries returned

This is verified deployment/source evidence only. It does not close P2/P6a or authorize experimental execution.

## Evidence boundary

Historical acceptance, characterization, synthetic blinding, topology, and security evidence may establish engineering or operational properties. None establishes empirical PDMAL efficacy. Empirical N remains `0` until the explicit authorization chain is completed and a valid paired pilot observation is accepted.

## TGL/P-35 boundary

The TGL/P-35 remediation is now integrated into the current production engineering source. Historical PR #132/#133/#134 records remain provenance only. Current governance validation demonstrates the repaired semantics; they do not redefine the experimental apparatus or authorize execution.

## Remaining gate sequence

1. Establish final experimental apparatus identity atop `303f4424…`.
2. Authenticated P2 five-case runtime verification.
3. Authenticated P6a four-case CORS verification.
4. P3 candidate-scoped artifact-contract execution evidence.
5. P4 operational blinding/custody evidence.
6. P5 environment/topology/RNG reproducibility.
7. P6 durable archive/retrieval/hash evidence.
8. P7 exact scientific/protocol/apparatus binding.
9. P8 exact analysis lock and closure.
10. Independent P9 verification.
11. New immutable freeze and independent freeze verification.
12. Explicit pilot authorization.
13. Authorized blinded pilot execution.

**Empirical N: 0. Pilot authorization: NOT GRANTED. Freeze: NOT CREATED.**
