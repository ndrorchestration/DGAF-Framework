---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The restored apparatus source from PR #170 is `d56b5b3c44e39ddb8c883259584432ab39259306`. Independent review identified a material provenance-integrity defect in that restored source: only P-31/P-33 state was bound into canonical identity while five additional restored gate-state blocks were omitted. PR #172 is the corrective apparatus change.
>
> **Candidate status:** `d56b5b3c…` is **SUSPENDED / PRE-CANDIDATE** pending completion and merge of PR #172. It must not be used for fresh P2/P6a or downstream candidate evidence while the provenance correction is unresolved.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No prior runtime or experimental evidence transfers across the provenance-correction boundary.

## Identity roles

- `d56b5b3c44e39ddb8c883259584432ab39259306` — restored seven-gate apparatus source from PR #170; **provisionally suspended** as an execution candidate because PR #172 identifies an incomplete canonical identity binding.
- `07bda8b740ab99762334f073eda1bd84b0c6e2db` — current PR #172 correction head; not yet merged and therefore not yet the final apparatus source.
- `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` — superseded historical post-#151 candidate; no evidence transfers.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` — prior engineering/runtime source and historical P2/P6a boundary.
- `c6157158…` — superseded pre-remediation candidate; retained for provenance only.
- `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — deployment bound to `d56b5b3c…`; because the source candidate is suspended, this deployment is **historical/pre-correction runtime identity only** and cannot supply current-candidate P2/P6a evidence.
- Documentation commits advance `main` documentation lineage but do not silently redefine apparatus identity.

## Current engineering/control-plane source

PR #170 completed the seven-gate restoration. Independent review then found the canonical provenance omission described above. PR #172 carries the bounded correction: bind Sentinel, Apogee, DemiJoule, KAPPA, Phi, plus the existing P-31/P-33 state, into canonical identity and test those bindings.

The correction is being held fail-closed until its fresh validation wave is complete. The prior `d56b5b3c…` deployment and all evidence derived from it are non-transferable across the correction boundary.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for the latest control state. |
| PR #170 apparatus source | CORRECTION-HELD | `d56b5b3c…`; seven-gate restoration exists, but canonical identity was incomplete. |
| PR #172 correction | ACTIVE / VALIDATION IN PROGRESS | `07bda8b…`; binds all seven restored gate states into canonical identity. |
| Current candidate basis | SUSPENDED / PRE-CANDIDATE | `d56b5b3c…`; cannot be used for fresh runtime evidence until #172 merges. |
| Current production deployment | HISTORICAL / PRE-CORRECTION | `dpl_76UU8mCm…`; bound to suspended `d56b5b3c…`. |
| P2 runtime verification | BLOCKED / DO NOT RUN | Must wait for post-#172 final apparatus/deployment identity. |
| P6a CORS verification | BLOCKED / DO NOT RUN | Must wait for post-#172 final apparatus/deployment identity. |
| P3–P6 | BLOCKED / FAIL-CLOSED | Current candidate does not yet have valid post-correction identity. |
| P7 | ADOPTED / BINDING PENDING | Bind only to final post-correction candidate/freeze. |
| P8 | BLOCKED / FAIL-CLOSED | Await final candidate identity. |
| P9 | NOT EXECUTED FOR CURRENT VALID CANDIDATE | Independent verification follows final candidate formation. |
| Freeze | NOT CREATED | No freeze identity is authoritative. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## Known runtime inputs from pre-correction deployment

The prior deployment inputs were:

- Candidate source SHA: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- Deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

These inputs remain useful historical provenance only. They must not be treated as fresh P2/P6a inputs after the provenance correction merges.

## Documentation and provenance control rule

This document distinguishes four identities: **`main` tip, apparatus source, candidate identity, and deployment identity**. When apparatus state changes, including provenance semantics, the candidate cycle resets. Documentation-only commits do not create a candidate, but an apparatus/provenance correction does.

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. A provenance correction invalidates execution evidence for the pre-correction apparatus as a current candidate, even when the underlying application behavior is unchanged.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
