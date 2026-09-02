# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 7
designation_event: CURRENT_RUNTIME_CANDIDATE_BOUND
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: CURRENT PRODUCTION/RUNTIME CANDIDATE
candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
candidate_tree_sha: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
candidate_designation_rule: exact runtime candidate commit/tree used by current candidate-bound execution evidence; it must remain traceable to the corrected apparatus source
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 92ff830b1c67413df745e37087e6447c9c251b9a
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
  deployment_id: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
  deployment_url: https://dynamicgovernanceagenticformation-3y3d8o5dp-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: READY_AS_RECORDED_BY_RUNTIME_VERIFICATION_SCOPE
  source_sha_match: candidate_bound_in_p2_p6a_runtime_artifacts
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  status: CURRENT_CANDIDATE_RUNTIME_EVIDENCE

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: VERIFIED
  P6a_CORS: VERIFIED
  P3: IMPLEMENTED / OPEN
  P4: OPEN
  P5: OPEN
  P6: OPEN / FAIL-CLOSED
  P7: TECHNICALLY ADJUDICATED / FORMALLY OPEN
  P8: OPEN / FAIL-CLOSED
  P9: NOT YET REVERIFIED FOR THIS RUNTIME CANDIDATE

controlled_completion_candidate:
  sha: a43219b4ed91fff8615f6c655ab3d17ca871fc29
  branch: completion/2026-09-01-exact-candidate
  status: CONTROLLED / NOT FROZEN / HISTORICAL FOR FUTURE SUCCESSOR CANDIDATES
  p3_run: 33572123862
  p9_run: 33572123857
  p9_artifact: 9825660346

superseded_completion_candidate:
  sha: 562753b3053b3566b0fcad1b0b1df151d7de119a
  status: HISTORICAL / SUPERSEDED
  p9_run: 33567199896
  p9_artifact: 9823570326
  evidence_transfer: PROHIBITED

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source from merged PR #174 and canonical provenance anchor.
- `973c9233…` — exact tree of the corrected apparatus source.
- `92ff830b…` — current production/runtime candidate used by P2/P6a.
- `73cf3ad…` — exact tree of the current runtime candidate.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — production deployment recorded by both current runtime evidence artifacts.
- `a43219b…` — controlled completion candidate with scoped P3/P9 evidence; remains non-frozen and evidence does not transfer to successor candidates.
- `562753b…` — superseded historical completion candidate; its P9 evidence remains provenance only.
- `d56b5b3c…` — pre-correction apparatus source; invalidated as an execution candidate when #174 corrected canonical provenance identity.
- `dpl_76UU8mCm…` — pre-correction deployment; historical/non-closing.
- `4e345c03…` — pre-merge #174 head; validation evidence only, not the merged apparatus identity.
- `05fa2866…` — superseded historical candidate; no evidence transfers.

## Promotion / binding rule

The corrected apparatus source establishes scientific apparatus provenance. The runtime candidate establishes the exact executable candidate identity. A candidate-bound runtime result must identify the exact candidate commit/tree and exact deployment identity; downstream evidence must then be bound to that same candidate lineage before P7/P8/P9/freeze transitions can occur.

P2 and P6a are verified for the recorded runtime evidence scope only. Their closure does not create a freeze, authorization, or empirical data. P3–P6, final P7 binding, P8, and current-candidate independent P9 remain outstanding for any eventual pilot candidate.

## Documentation hygiene

This manifest is a living current-cycle manifest. Superseded candidates may be retained only as explicitly historical records. In particular, `562753b…` is historical and `a43219b…` is the prior controlled completion candidate; neither is the current runtime candidate.

The current P7 state is **TECHNICALLY ADJUDICATED / FORMALLY OPEN**. The scientific specification has been adjudicated, but exact final-candidate/freeze binding remains open.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
