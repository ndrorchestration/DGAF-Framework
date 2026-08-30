# Branch / Dependency Lifecycle Map — 2026-08-30

**Status:** CURRENT / NON-AUTHORIZING
**Purpose:** Prevent historical or stale branches from being interpreted as active dependencies of the current PDMAL evidence cycle.

## Canonical identities

- Apparatus candidate/source: `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
- Candidate designation/control record: `02c146d1e0cdc423948ac0dfa11e98f812edfb44`
- Current documentation/evidence lineage: `main`
- Prior engineering/runtime source: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Prior pre-remediation candidate: `c6157158bf0ee4840e99a381a4b99bd2febe2302`

## Dependency classes

### CURRENT

`main` is the current documentation/evidence lineage. The post-#151 apparatus candidate is `05fa286…`. The designation record is `02c146d1…`.

### HISTORICAL / PRESERVED

Prior production/runtime evidence bound to `303f4424…`, prior experimental evidence bound to `c6157158…`, and historical verification/freeze identities remain retained for provenance.

### STALE INTEGRATION CANDIDATE

Open branches/PRs based on older mainline snapshots are not current dependencies. They require rebase/reconciliation and fresh validation before any artifact can be used in the current evidence graph.

Observed examples include PR #140, PR #146, and PR #147.

### HISTORICAL REMEDIATION

Older candidate/P7/P8/P2/TGL branches are preserved as historical implementation work and must not be treated as current candidate evidence solely because their names or commits resemble current terminology.

Observed examples include:

- `candidate/p7-binding-reconciliation-clean-20260828`
- `candidate/p7-binding-remediation-20260828`
- `docs/p8-corrected-candidate-basis`
- `verification/p2-candidate-83e1678f`
- `verify/e2b-current-candidate-20260828`
- `engineering/pdmal-tgl-integrity-20260828`
- `engineering/tgl-hpg-regression-20260828`
- `engineering/tgl-p8-p6a-20260828`
- `engineering/tgl-skip-semantics-20260829`
- `fix/tgl-contract-repair-132`
- `fix/tgl-contract-repair-main-20260829`
- `fix/tgl-contract-repair-mainline-20260830`
- `fix/tgl-orchestrator-contract-20260827`

This inventory reflects branches observed during the 2026-08-30 audit and is not asserted to be exhaustive.

## Non-equivalence rules

The following identities are distinct:

`apparatus SHA != candidate designation commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

Likewise:

`historical evidence != current evidence`

`deployment READY != runtime verified`

`implemented != wired != candidate-bound != verified != authorized`

## Promotion rule

A branch becomes an active evidence dependency only after:

1. exact ancestry and executable-change scope are established;
2. candidate identity is explicit;
3. affected predicates are re-identified;
4. current candidate-scoped verification is produced;
5. historical evidence is prevented from crossing the new boundary.

## Current experimental boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
