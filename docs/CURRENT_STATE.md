---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The **pre-correction restored apparatus source** is `d56b5b3c44e39ddb8c883259584432ab39259306`, the signed squash merge of PR #170. A subsequent adversarial review found that its canonical provenance identity omitted five restored gate-state substrates. PR #172 is therefore the active corrective apparatus lane.
>
> **Candidate status:** `d56b5b3c…` is **not an execution-valid candidate** while #172 remains unresolved. If #172 merges, a new apparatus SHA, candidate identity, and deployment must be established; no evidence from the pre-correction boundary transfers.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No candidate-runtime or experimental evidence is valid from the pre-correction boundary.

## Identity roles

- `d56b5b3c44e39ddb8c883259584432ab39259306` — pre-correction restored apparatus source from PR #170; candidate promotion is blocked by the provenance defect found after merge.
- `3c489459e09d2d9fb9d31239d9bae05df4b3548b` — active PR #172 head containing the provenance correction.
- `9123dc4a2b5b9859e3cf0ebde4d18202ba6b01d7` — earlier provenance-integration head absorbed into PR #170; historical lineage only.
- `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` — superseded historical post-#151 candidate; no evidence transfers.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` — prior engineering/runtime source and historical P2/P6a boundary.
- Documentation commits advance `main` control-plane lineage but do not automatically create a new experimental candidate.
- `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — production deployment bound to the pre-correction `d56b5b3c…` source; it is non-closing for any post-#172 candidate.

## Current engineering/control-plane source

PR #170 restored all seven constitutive gates. PR #172 corrects a material provenance defect in that restoration: only P-31/P-33 state was included in `canonicalize_state`; P-29, P-30, DemiJoule, P-27 KAPPA, and P-32 Phi state were omitted. The correction adds canonical state representations and provenance-identity regression tests. This is an apparatus integrity issue, not a runtime execution result.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub; literal tip SHA is not embedded here. |
| Pre-correction apparatus source | HISTORICAL / BLOCKED | `d56b5b3c…`; restored substrate exists, but provenance promotion is blocked pending #172. |
| Active provenance correction | OPEN / NON-DRAFT | PR #172, head `3c489459…`; validation must complete before merge. |
| Pre-correction production deployment | READY / SOURCE-MATCHED / NON-CLOSING | `dpl_76UU8mCm…`; must not close a candidate after #172 if merged. |
| P-31/P-33 | RESTORED / IMPLEMENTED | Historical parity established; current candidate verification paused behind provenance correction. |
| P-27/P-29/P-30/P-32/DemiJoule | RESTORED / IMPLEMENTED | Historical/authorized behavior ported; current candidate promotion paused behind provenance correction. |
| P2 | PAUSED | Fresh run only after new candidate/deployment exists. |
| P6a | PAUSED | Fresh run only after new candidate/deployment exists. |
| P3–P6 | PAUSED / FAIL-CLOSED | Await corrected candidate evidence. |
| P7 | ADOPTED / BINDING PENDING | Bind only to final corrected candidate/freeze identity. |
| P8 | PAUSED / FAIL-CLOSED | Await corrected candidate binding. |
| P9 | PAUSED | Independent verification follows corrected candidate. |
| Freeze | NOT CREATED | No frozen identity is authoritative. |
| Authorization | NOT GRANTED | Separate governance transition required. |
| Empirical N | 0 | No authorized pilot execution. |

## Provenance correction hold

The #170 merge is not a valid final candidate boundary because its canonical identity is non-injective over restored gate state. PR #172 binds the five omitted state blocks into the canonical representation and adds one identity-change test per gate. The initial #172 validator failure was separately identified as a false-positive caused by a literal `main tip` assertion; that validator has been corrected on `main`.

No fresh P2/P6a execution is permitted against `d56b5b3c…` while this correction is unresolved. If #172 merges, the new apparatus SHA supersedes `d56b5b3c…` for all future candidate work and requires a new production deployment.

## Runtime identity

Pre-correction runtime values remain historical/non-closing:

- deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

Fresh P2/P6a inputs must be regenerated from the corrected candidate and its exact deployment.

## Assurance rule

The project distinguishes five layers: **L0 identity, L1 treatment integrity, L2 execution integrity, L3 scientific integrity, and L4 governance integrity**. A failure at any higher layer blocks downstream claims. A green engineering test suite cannot override a provenance-integrity failure.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
