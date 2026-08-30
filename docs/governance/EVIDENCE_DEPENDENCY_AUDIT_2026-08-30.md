# Evidence Dependency Audit — 2026-08-30

**Status:** CURRENT / NON-AUTHORIZING

## Canonical identity graph

| Node | Identity / role |
|---|---|
| Apparatus candidate | `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` |
| Candidate tree | `dd662325149c42843d5ca99178ca4399fde6f440` |
| Designation/control record | `02c146d1e0cdc423948ac0dfa11e98f812edfb44` |
| Current main documentation lineage | `d58206358803d091073cd61058038ecc6b4ebfdd` |
| Prior production/runtime evidence source | `303f4424d2198f0d0cf76305c589263dd1e417dc` |
| Prior pre-remediation candidate | `c6157158bf0ee4840e99a381a4b99bd2febe2302` |

## Dependency conditions

Current-candidate evidence may close a predicate only when all upstream identities required by that predicate resolve to the same current candidate cycle.

Historical P2/P6a evidence is valid only at `303f4424…` and its exact deployment/run/artifact boundary.

Historical pre-#151 P3–P9 evidence is valid only within its original pre-remediation scope.

The `05fa286…` candidate designation does not inherit any of those historical predicate closures.

## Gate dependencies

P2/P6a → require exact candidate deployment.

P3 → requires current candidate artifact execution and schema/integrity evidence.

P4 → requires current operational custody and blinding separation.

P5 → requires current environment/topology/RNG/provenance evidence.

P6 → requires durable archive/retrieval/hash evidence for current candidate artifacts.

P7 → requires exact scientific binding to current candidate/protocol/analysis/final freeze identity.

P8 → requires current candidate analysis/runner/protocol binding and applicable predicate closure.

P9 → requires independent verification of the complete current evidence graph.

Freeze → requires current P1–P8 + independent P9.

Authorization → separate governance transition after freeze verification.

N>0 → authorized execution only.

## Non-equivalence invariants

`apparatus SHA != designation/control commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

`implemented != wired != candidate-bound != verified != authorized`

`historical evidence != current evidence`

`deployment READY != runtime verified`

## Current disposition

No dependency is promoted across the candidate boundary merely by ancestry, correlation, deployment readiness, CI success, or documentation reference.

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**
