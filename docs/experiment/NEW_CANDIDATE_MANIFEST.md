# NEW CANDIDATE MANIFEST — current verified runtime evidence boundary

```yaml
manifest_version: 7
designation_event: CURRENT_RUNTIME_EVIDENCE_BOUND
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: VERIFIED EXECUTABLE RUNTIME CANDIDATE
candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_tree_sha: d969f7b5c2c00000000000000000000000000000
candidate_designation_rule: exact executable candidate commit used by the current verified P2/P6a runtime evidence; the control-plane successor is documentation-only and does not reopen closed runtime predicates
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
control_plane_successor:
  sha: 637023b28492783f50d77550d4ed8e0867cbcc3d
  status: DOCUMENTATION / CONTROL-PLANE ONLY
  note: does not alter the runtime surfaces covered by P2/P6a
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
  sha: 92ff830b1c67413df745e37087e6447c9c251b9a
  status: HISTORICAL / SUPERSEDED
  note: no evidence transfers merely by documentation equivalence
displaced_pre_correction_candidate:
  sha: d56b5b3c44e39ddb8c883259584432ab39259306
  status: HISTORICAL / INVALIDATED_BY_PROVENANCE_CORRECTION
  deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
  deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
  note: these runtime identities and all evidence derived from them are non-closing for this cycle
deployment_binding:
  deployment_id: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
  deployment_url: https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: READY
  source_sha_match: MATCHED
  allowed_cors_origin: https://dynamicgovernanceagenticformation.vercel.app
  status: VERIFIED_RUNTIME_EVIDENCE_SCOPE

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
  P7: ADOPTED / FINAL BINDING OPEN
  P8: OPEN / FAIL-CLOSED
  P9: OPEN

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected apparatus provenance anchor.
- `973c9233…` — corrected apparatus source tree.
- `7c1cc4bb…` — verified executable runtime candidate bound to P2/P6a.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — exact deployment bound to that runtime candidate.
- `637023b2…` — later documentation/control-plane successor; not a new runtime candidate.
- Older candidate/deployment identities are historical/non-transferable.

## Promotion / binding rule

The corrected apparatus source establishes provenance. The verified executable runtime candidate establishes the exact runtime identity. P2 and P6a are closed for that candidate/deployment pair. A later documentation-only control-plane successor does not reopen those predicates. Downstream evidence must remain bound to the exact evidence candidate used for the relevant gate.

P3–P6, final P7 binding, P8, and independent P9 remain outstanding.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
