---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the documentation/control-plane lineage. The **current restored apparatus source** is `d56b5b3c44e39ddb8c883259584432ab39259306`, the signed squash merge of PR #170, which integrates the complete seven-gate constitutive substrate plus P-31/P-33 provenance binding. Later documentation-only commits do not redefine that apparatus source.
>
> **Candidate status:** `d56b5b3c…` is the provisional candidate designation basis for the new post-restoration cycle. Fresh candidate-scoped runtime evidence is required; no prior P2/P6a/P3–P9 evidence transfers.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. Merge, CI success, deployment readiness, or provisional candidate designation do not create a freeze or authorize execution.

## Identity roles

- `d56b5b3c44e39ddb8c883259584432ab39259306` — current restored apparatus source and provisional candidate designation basis after PR #170.
- `9123dc4a2b5b9859e3cf0ebde4d18202ba6b01d7` — provenance-integration head absorbed into PR #170; not a current apparatus identity.
- `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` — superseded historical post-#151 candidate; no evidence transfers.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` — prior engineering/runtime source and historical P2/P6a boundary.
- `c6157158…` — superseded pre-remediation candidate; retained for provenance only.
- Documentation commits after `d56b5b3c…` advance `main` documentation lineage but do not automatically create a new apparatus candidate.
- `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` — exact production deployment currently bound to `d56b5b3c…`; deployment identity is separate from Git identity.

## Current engineering/control-plane source

PR #170 is merged. It integrates the authorized P-27, P-29, P-30, P-32, DemiJoule, P-31, and P-33 restoration work, including historical parity and provenance binding. This is engineering completion only; candidate-scoped runtime and experimental verification remain outstanding.

The candidate manifest records the exact apparatus source and exact current deployment inputs. Prior empirical/runtime evidence remains historical and non-transferable.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` ref | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly in GitHub for the latest documentation/control state. The literal tip SHA is not embedded here to avoid self-staleness after doc-only commits. |
| Current apparatus source | CURRENT POST-RESTORE APPARATUS | `d56b5b3c…`; complete seven-gate constitutive substrate and provenance integration merged by PR #170 |
| Current candidate basis | PROVISIONAL / PRE-FREEZE | `d56b5b3c…`; requires fresh candidate-scoped runtime and evidence verification |
| Current production deployment | READY / SOURCE-MATCHED | `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`; Vercel reports READY/production and exact Git source SHA match |
| Prior runtime source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior P2/P6a evidence does not transfer |
| Prior post-#151 candidate | SUPERSEDED / HISTORICAL | `05fa286…`; evidence does not transfer |
| P-31 | RESTORED / IMPLEMENTED | Historical substrate restored and provenance-bound; candidate-scoped verification required |
| P-33 | RESTORED / IMPLEMENTED | Historical substrate restored and provenance-bound; candidate-scoped verification required |
| P-27 | RESTORED / IMPLEMENTED | Historical v3.5 behavior ported with parity tests; candidate-scoped verification required |
| P-29 | RESTORED / IMPLEMENTED | Authorized Sentinel risk/halt behavior ported; candidate-scoped verification required |
| P-30 | RESTORED / IMPLEMENTED | Authorized acceptance schema and gold-star behavior ported; candidate-scoped verification required |
| P-32 | RESTORED / IMPLEMENTED | Historical PHI_STAR/KILL_REC behavior ported with direct parity; candidate-scoped verification required |
| DemiJoule | RESTORED / IMPLEMENTED | Authorized six-axis semantic-safety behavior ported; historical WARN-unreachable property remains documented |
| P2 runtime verification | NOT VERIFIED FOR CURRENT CANDIDATE | Workflow requires exact candidate SHA + deployment ID + deployment URL; fresh execution required |
| P6a CORS verification | NOT VERIFIED FOR CURRENT CANDIDATE | Workflow additionally binds the configured allowed CORS origin; fresh execution required |
| P3–P6 | OPEN / FAIL-CLOSED | Fresh candidate-scoped evidence required |
| P7 | ADOPTED / BINDING PENDING | Must bind to the final candidate/freeze |
| P8 | OPEN / FAIL-CLOSED | New candidate analysis/apparatus binding required |
| P9 | NOT EXECUTED FOR CURRENT CANDIDATE | Independent verification required |
| Freeze | NOT CREATED | No freeze identity is authoritative |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No authorized pilot execution |

## Deployment identity for fresh runtime verification

- Candidate apparatus SHA: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Production deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- Production deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`
- Historical P6a evidence used the same configured origin but a different candidate/deployment and is therefore non-transferable.

## Documentation and provenance control rule

This document distinguishes four identities: **`main` tip, apparatus source, candidate identity, and deployment identity**. Documentation-only changes advance the first but do not automatically alter the second or create a new experimental candidate. Runtime evidence is valid only when its deployment and source identity are explicitly bound to the candidate under evaluation.

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
