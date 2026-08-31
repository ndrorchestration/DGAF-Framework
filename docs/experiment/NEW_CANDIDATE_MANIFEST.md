# NEW CANDIDATE MANIFEST — post-#170 restoration cycle

```yaml
manifest_version: 4
designation_event: NEW_CANDIDATE
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: d56b5b3c44e39ddb8c883259584432ab39259306
apparatus_source_tree_sha: 8c13900c4ce2a503414f9dddf1d7ef7debead57e
candidate_designation: BLOCKED / PRE-CORRECTION
candidate_designation_rule: exact restored apparatus source; candidate promotion prohibited while provenance identity is incomplete
restoration_source:
  pr: 170
  pr_state: MERGED
  merge_commit: d56b5b3c44e39ddb8c883259584432ab39259306
provenance_correction:
  pr: 172
  state: OPEN / NON-DRAFT / VALIDATION IN PROGRESS
  head: 3c489459e09d2d9fb9d31239d9bae05df4b3548b
  reason: five restored gate-state substrates were omitted from canonical provenance identity in #170
  candidate_promotion_blocked: true
  consequence_if_merged: new apparatus SHA and new candidate cycle required
prior_candidate:
  sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  status: HISTORICAL / SUPERSEDED
  note: no prior empirical package transfers
deployment_binding:
  deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
  deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: READY
  source_sha_match: true
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  status: PRE-CORRECTION / NON-CLOSING
  note: deployment is bound to d56b5b3c and must not be used for the post-#172 candidate if #172 merges
gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_CORRECTION_PENDING
  P2_RUNTIME: PAUSED_UNTIL_NEW_CANDIDATE
  P6a_CORS: PAUSED_UNTIL_NEW_CANDIDATE
  P3_P9: PAUSED_UNTIL_NEW_CANDIDATE
authorization: NOT GRANTED
empirical_n: 0
```

## Identity roles

- `d56b5b3c…` — pre-correction restored apparatus source; not an execution-valid candidate while #172 remains unresolved.
- `3c489459…` — provenance-correction PR head; if merged, creates the next executable apparatus boundary.
- `dpl_76UU8mCm…` — production deployment bound to the pre-correction apparatus; non-closing for any post-#172 candidate.
- `05fa2866…` — superseded historical candidate; no evidence transfers.

## Promotion rule

This record intentionally does **not** promote `d56b5b3c…` to an execution-valid candidate. The five omitted gate-state substrates must first be incorporated into canonical provenance identity and independently validated. If #172 merges, all candidate runtime identity, deployment, P2/P6a, and downstream P3–P9 work must restart from the resulting new apparatus SHA.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
