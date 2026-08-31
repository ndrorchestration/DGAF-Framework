# Dependency Consistency Rules — 2026-08-31

## Identity tuple

Current post-#174 corrected apparatus candidate/source:
`2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`

Current apparatus tree:
`973c92335caf84f37fc2b3c4df6dd83b3b855087`

Prior restoration source from PR #170:
`d56b5b3c44e39ddb8c883259584432ab39259306`

Prior pre-remediation candidate:
`05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`

Current `main` is documentation/control-plane lineage; documentation-only commits do not silently redefine the apparatus source.

## Dependency rules

1. An apparatus-changing commit creates a new candidate cycle.
2. A documentation/control commit does not change apparatus identity unless executable apparatus behavior changes.
3. Evidence binds to the exact source/deployment/run/artifact that produced it.
4. Deployment readiness does not imply runtime verification.
5. Runtime verification does not imply P3–P9 closure.
6. Historical evidence does not transfer across candidate boundaries.
7. P9 depends on the complete current evidence chain and must remain independent of candidate self-validation.
8. Freeze depends on current P1–P8 plus independent P9; authorization remains separate.
9. N may increase only after the authorized frozen apparatus produces an accepted empirical observation.
10. If any upstream identity changes, affected downstream predicates require re-identification and re-verification.
11. Operational dispatch documents must never present a superseded or non-matching deployment as current candidate input.
12. Historical SHA/deployment references may remain when explicitly scoped as historical/non-closing; they must not be globally deleted merely to remove stale-looking identifiers.
13. A deployment provenance claim must bind source SHA, deployment identity, target/state, effective behavior-affecting configuration, and retained evidence in one auditable chain.

## Non-equivalence invariant

`apparatus SHA != designation commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

`implemented != wired != candidate-bound != verified != authorized`

`historical evidence != current evidence`

`deployment READY != runtime verified`

## Current dependency state

- Current corrected apparatus: `2a54a67d…`; provisional, not frozen.
- Current apparatus tree: `973c9233…`.
- Current candidate deployment: **NONE YET** for exact source `2a54a67d…`.
- Observed READY production deployment at `a7079f51…`: valid deployment evidence but non-matching to the current candidate and therefore non-closing.
- Pre-correction deployment `dpl_76UU8mCm…` / `d56b5b3c…`: historical and invalidated.
- P2/P6a: blocked until an exact-source deployment exists and effective runtime configuration is attested.
- P3–P8: current-candidate evidence-gated.
- P9: not executed for current candidate.
- Freeze: not created.
- Authorization: not granted.
- Empirical N: 0.

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
