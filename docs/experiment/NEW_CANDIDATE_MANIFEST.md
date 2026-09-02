# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 7
designation_event: P35_REMEDIATION_CANDIDATE_REBOUND
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: ACTIVE P-35 REMEDIATION / PRE-FREEZE CANDIDATE
candidate_sha: fcdfa0180625c413e692d7fa405ea361c05dc53f
candidate_tree_sha: a81faf976de029734772b81a3615e3316ddf7641
candidate_designation_rule: exact current PR #199 head used by the active pre-freeze validation wave; it must remain traceable to the corrected apparatus source
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> fcdfa0180625c413e692d7fa405ea361c05dc53f
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
  deployment_target: production
  deployment_state: NOT_ESTABLISHED
  source_sha_match: NOT_ESTABLISHED
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  status: NO_EXACT_CANDIDATE_DEPLOYMENT_CLAIMED

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: HISTORICAL VERIFIED / RE-RUN REQUIRED
  P6a_CORS: HISTORICAL VERIFIED / RE-RUN REQUIRED
  P3: HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED
  P4: OPEN
  P5: OPEN
  P6: OPEN / FAIL-CLOSED
  P7: ADOPTED / FINAL BINDING OPEN
  P8: OPEN / FAIL-CLOSED
  P9: HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source and canonical provenance anchor.
- `973c9233…` — exact tree of the corrected apparatus source.
- `fcdfa018…` — active PR #199 P-35 remediation candidate used by the current pre-freeze validation wave.
- `a81faf97…` — exact tree of the active candidate.
- `92ff830b…` — superseded runtime candidate; P2/P6a evidence remains bound to its exact tree/deployment.
- `a43219b…` — superseded completion candidate; PDMAL/P9 evidence remains bound to its exact tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — historical deployment for `92ff830b…`.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — historical preview deployment for `a43219b…`.
- `9b104b28…` — PR #199 merge-ref workflow execution identity for the superseded validation attempt; it is not the candidate SHA.

## Promotion / binding rule

The corrected apparatus source establishes scientific apparatus provenance. The active candidate establishes the exact executable candidate identity. A candidate-bound runtime result must identify the exact candidate commit/tree and exact deployment identity before P2/P6a closure; downstream evidence must then be bound to that same candidate lineage before P7/P8/P9/freeze transitions can occur.

No historical runtime, completion, deployment, or P9 evidence transfers to `fcdfa018…`. The current pre-freeze wave is validation evidence only; it does not create a freeze, authorization, or empirical data.

## Documentation hygiene

Older documents stating that inline artifact validation is missing are historical/stale observations, not current defects. Historical documents remain preserved; this manifest records the active candidate state separately.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
