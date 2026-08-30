---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_ref: main
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it.

> **Current boundary:** `main` is the current documentation/evidence lineage. PR #151 has merged as `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` and changes apparatus behavior. The post-#151 apparatus identity is therefore the new candidate boundary; subsequent documentation/control commits do not redefine the apparatus. Prior P2/P6a evidence remains exact for `303f4424…` and is not transferred. No freeze or authorization follows from merge or deployment readiness.

## Current identity roles

- `2a80f819…` — historical P8 checklist ancestor.
- `303f4424…` — integrated DGAF v1 engineering/production source and prior P2/P6a evidence boundary.
- `ac8ea267…` — prior historical experimental verification boundary.
- `c6157158…` — superseded pre-remediation candidate; retained for provenance only.
- `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` — **post-#151 apparatus commit / candidate source boundary**.
- `02c146d1…` — subsequent candidate-designation/control commit; not the apparatus identity itself.
- `8625238bb47b9c1c68fcfe8e4a06ce205578d8bd` — current `main` documentation/evidence lineage at last verification.

## Current engineering/control-plane source

PR #151 hardens the apparatus boundary by making required unwired DGAF/TGL gates fail closed, binding TGL turn identity to semantic iteration, and retaining governance traces in pilot results/artifacts. Its merge commit `05fa286…` is therefore a substantive apparatus change and starts a new candidate cycle. The merge is not itself experimental authorization.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Current `main` | CURRENT DOCUMENTATION/EVIDENCE LINEAGE | `8625238…`; resolve `main` directly for latest repository state |
| Prior engineering/runtime source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior production deployment and P2/P6a evidence |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…`; evidence does not transfer post-#151 |
| **Post-#151 apparatus candidate** | **DESIGNATED / NOT FROZEN** | `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`; exact candidate identity for the new cycle |
| Candidate designation/control commit | CONTROL RECORD | `02c146d1…`; records designation, not apparatus source identity |
| Candidate deployment provenance | VERIFIED | Post-#151 deployment/source identity must be checked against the exact candidate before runtime gates are closed |
| P2 runtime verification | PRIOR VERIFIED / NEW CANDIDATE OPEN | Prior run `33300481208` is exact for `303f4424…`; fresh execution required for `05fa286…` |
| P6a CORS verification | PRIOR VERIFIED / NEW CANDIDATE OPEN | Prior run `33302495240` is exact for `303f4424…`; fresh execution required for `05fa286…` |
| P3–P6 | OPEN / FAIL-CLOSED | Candidate-scoped evidence required |
| P7 | ADOPTED / BINDING PENDING | Must bind to the new final candidate/freeze |
| P8 | OPEN / FAIL-CLOSED | New candidate analysis/apparatus binding required |
| P9 | NOT EXECUTED FOR NEW CANDIDATE | Independent verification required |
| Freeze | NOT CREATED | No freeze identity is currently authoritative |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No authorized pilot execution |

## Evidence boundary

CI success, deterministic tests, deployment readiness, synthetic evaluator results, governance documentation, and engineering PRs do not constitute PDMAL efficacy evidence or experimental authorization. Historical evidence remains exact-SHA/run/deployment scoped.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
