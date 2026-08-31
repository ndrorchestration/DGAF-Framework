# NEW CANDIDATE MANIFEST — post-#170 restoration cycle

```yaml
manifest_version: 2
designation_event: NEW_CANDIDATE
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
apparatus_source_tree_sha: 8c13900c4ce2a503414f9dddf1d7ef7debead57e
candidate_designation: PROVISIONAL / POST-RESTORE
candidate_designation_rule: exact restored apparatus source; no prior empirical evidence transfers
prior_candidate:
  sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  status: HISTORICAL / SUPERSEDED BY #170 RESTORATION
  note: prior P3-P9 package is NOT transferred
restoration_source:
  pr: 170
  pr_state: MERGED
  merge_commit: d56b5b3c44e39ddb8c883259584432ab39259306
  merged_at: 2026-08-31T07:03:16Z
provenance_source:
  pr: 169
  state: ABSORBED INTO #170
  head: 9123dc4a2b5b9859e3cf0ebde4d18202ba6b01d7
gate_ledger:
  P31_SCPE: RESTORED_ON_APPARATUS
  P27_KAPPA: RESTORED_ON_APPARATUS
  P29_SENTINEL: RESTORED_ON_APPARATUS
  P32_PHI: RESTORED_ON_APPARATUS
  P30_APOGEE: RESTORED_ON_APPARATUS
  P33_CONVERGENCE: RESTORED_ON_APPARATUS
  DEMIJOULE: RESTORED_ON_APPARATUS
  P2_RUNTIME: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P6a_CORS: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P3_P9: NOT_VERIFIED_FOR_THIS_CANDIDATE
  P9: NOT_EXECUTED
authorization: NOT GRANTED
empirical_n: 0
```

## Identity roles

- `d56b5b3c…` — current restored apparatus source and provisional candidate designation basis.
- `9123dc4a…` — provenance-integration head absorbed into #170; not the final apparatus identity.
- `05fa2866…` — superseded historical post-#151 candidate; no empirical package transfers.
- Any subsequent documentation-only commit changes `main` documentation lineage, not `apparatus_source_sha`.
- Deployment identity must be recorded separately from both `main` tip and apparatus source SHA.

## Promotion rule

This manifest designates the exact restored apparatus source for the new candidate cycle. It does **not** create a freeze, authorize the pilot, or promote prior P2/P6a/P3-P9 evidence. All runtime and experimental predicates must be freshly established against this exact apparatus and its candidate-bound deployment.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
