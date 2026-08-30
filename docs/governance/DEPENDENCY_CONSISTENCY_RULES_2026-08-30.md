# Dependency Consistency Rules — 2026-08-30

## Identity tuple

Current post-#151 apparatus candidate/source:
`05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`

Candidate designation/control record:
`02c146d1e0cdc423948ac0dfa11e98f812edfb44`

Prior runtime evidence boundary:
`303f4424d2198f0d0cf76305c589263dd1e417dc`

Prior pre-remediation candidate:
`c6157158bf0ee4840e99a381a4b99bd2febe2302`

## Dependency rules

1. An apparatus-changing commit creates a new candidate cycle.
2. A documentation/control commit does not change the apparatus identity unless executable apparatus behavior changes.
3. Evidence binds to the exact source/deployment/run/artifact that produced it.
4. Deployment readiness does not imply runtime verification.
5. Runtime verification does not imply P3–P9 closure.
6. Historical evidence does not transfer across candidate boundaries.
7. P9 depends on the complete current evidence chain and must remain independent of candidate self-validation.
8. Freeze depends on current P1–P8 plus independent P9; authorization remains separate.
9. N may increase only after the authorized frozen apparatus produces an accepted empirical observation.
10. If any upstream identity changes, affected downstream predicates require re-identification and re-verification.

## Non-equivalence invariant

`apparatus SHA != designation commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

`implemented != wired != candidate-bound != verified != authorized`

`historical evidence != current evidence`

`deployment READY != runtime verified`

## Current dependency state

- Current candidate: designated, not frozen.
- Current candidate deployment: exact-source provenance must be re-verified before current P2/P6a closure.
- Prior P2/P6a: verified only at `303f4424…`.
- P3–P8: current evidence-gated.
- P9: not executed for current candidate.
- Freeze: not created.
- Authorization: not granted.
- Empirical N: 0.

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
