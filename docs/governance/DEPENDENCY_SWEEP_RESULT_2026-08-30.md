# Dependency Sweep Result — 2026-08-30

## Result

Cross-layer dependency hygiene sweep completed across candidate identity, deployment provenance, P1–P9 evidence, N=1, historical recovery, branch/PR lifecycle, and control-plane documentation.

## Canonical identity

- Current apparatus/source candidate: `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
- Candidate tree: `dd662325149c42843d5ca99178ca4399fde6f440`
- Candidate designation/control record: `02c146d1e0cdc423948ac0dfa11e98f812edfb44`
- Current main documentation lineage at sweep completion: `6e674bbb04d9f57fbce72dc8fa02061374dbd8e8`
- Prior P2/P6a evidence source: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Superseded pre-remediation candidate: `c6157158bf0ee4840e99a381a4b99bd2febe2302`

## Cross-layer findings

1. Historical runtime evidence remains exact to `303f4424…`.
2. The post-#151 apparatus candidate is `05fa286…`; designation/control is `02c146d…`.
3. P2/P6a require fresh execution for `05fa286…` and must not inherit prior runs.
4. P3–P8 remain evidence-gated; P9 remains unexecuted for the current candidate.
5. Issue #152 remains the governing recovery/translation workstream for the seven historical TGL gates; FAIL-CLOSED remains correct where substrate or contract reconciliation is incomplete.
6. Historical branches and stale PRs remain provenance/integration candidates, not current evidence dependencies.
7. Documentation-only commits do not redefine the apparatus identity.
8. Substantive executable changes require candidate re-identification and affected-predicate re-verification.

## Invariants enforced

`apparatus SHA != designation commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

`implemented != wired != candidate-bound != verified != authorized`

`historical evidence != current evidence`

`deployment READY != runtime verified`

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
