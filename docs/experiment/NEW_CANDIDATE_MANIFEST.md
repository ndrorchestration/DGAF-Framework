# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 5
designation_event: NEW_CANDIDATE_PENDING_RUNTIME_BINDING
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: PROVISIONAL / POST-PROVENANCE-CORRECTION
candidate_designation_rule: exact merged apparatus source; promotion to execution-valid candidate requires a fresh exact deployment identity and candidate-scoped P1-P9 evidence
restoration_source:
  prior_pr: 170
  prior_merge_commit: d56b5b3c44e39ddb8c883259584432ab39259306
  status: HISTORICAL / SUPERSEDED_BY_PROVENANCE_CORRECTION
provenance_correction:
  pr: 174
  state: MERGED
  merge_commit: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
  scope: bind_all_seven_behavior_affecting_gate_states_into_canonical_identity
  additional_hardening: substrate_driven_p29_regression; manifest_derived_control_state_identity
prior_candidate:
  sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  status: HISTORICAL / SUPERSEDED
  note: no empirical package transfers
displaced_pre_correction_candidate:
  sha: d56b5b3c44e39ddb8c883259584432ab39259306
  status: HISTORICAL / INVALIDATED_BY_PROVENANCE_CORRECTION
  deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
  deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  note: these runtime identities and all evidence derived from them are non-closing for this post-#174 cycle
deployment_binding:
  deployment_id: NONE_YET
  deployment_url: NONE_YET
  deployment_target: NONE_YET
  deployment_state: NOT_YET_ESTABLISHED
  source_sha_match: NOT_YET_CHECKED
  allowed_cors_origin: NONE_YET
  status: BLOCKED_UNTIL_EXACT_DEPLOYMENT_EXISTS

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: NOT_VERIFIED_FOR_THIS_CYCLE
  P6a_CORS: NOT_VERIFIED_FOR_THIS_CYCLE
  P3_P9: NOT_VERIFIED_FOR_THIS_CYCLE
  P9: NOT_EXECUTED

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source from merged PR #174 and the basis for the new candidate cycle.
- `d56b5b3c…` — pre-correction apparatus source; invalidated as an execution candidate when #174 corrected canonical provenance identity.
- `dpl_76UU8mCm…` — pre-correction deployment; historical/non-closing.
- `4e345c03…` — pre-merge #174 head; validation evidence only, not the merged apparatus identity.
- `05fa2866…` — superseded historical candidate; no evidence transfers.

## Promotion rule

This manifest establishes the apparatus identity for the post-#174 candidate cycle but does not create an execution-valid candidate by itself. A fresh production deployment must be created from the exact apparatus source, verified as READY and source-SHA-matched, then bound to candidate-scoped P2/P6a/P3-P9 evidence. No evidence from the pre-correction `d56b5b3c…` deployment transfers.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
