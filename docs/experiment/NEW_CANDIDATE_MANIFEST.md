# NEW CANDIDATE MANIFEST — current-main P-35-integrated candidate

```yaml
manifest_version: 7
designation_event: P35_INTEGRATED_CURRENT_MAIN_CANDIDATE
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
parent_runtime_candidate_sha: 275756fd81c975f17ae3d16d24e599db0617cf85
candidate_designation: P-35-INTEGRATED PILOT CANDIDATE / NOT FROZEN
candidate_sha: PENDING_EXACT_HEAD_AFTER_FINAL_CANDIDATE_DOC_UPDATE
candidate_tree_sha: PENDING_EXACT_HEAD_AFTER_FINAL_CANDIDATE_DOC_UPDATE
candidate_designation_rule: exact candidate commit/tree selected for fresh current-cycle verification; no historical evidence transfers across SHA changes
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 275756fd81c975f17ae3d16d24e599db0617cf85 -> P-35-integrated candidate
remediation_source:
  pr: 188
  verified_remediation_head: f5461ec6e3737c805ea210603ed6f757f49adb3d
  scope: explicit P-35 premise-hook dependency at DGAF/TGL/ConsensusTask boundary
  status: ENGINEERING / PRE-FREEZE VERIFIED
  evidence: exact-head runner validation, runtime characterization, and independent verification

prior_runtime_candidate:
  sha: 92ff830b1c67413df745e37087e6447c9c251b9a
  tree_sha: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
  deployment_id: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
  status: HISTORICAL / SUPERSEDED_FOR_THIS_CANDIDATE
  note: P2/P6a evidence remains exact-scoped to the prior runtime candidate and does not transfer

prior_candidate:
  sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
  status: HISTORICAL / SUPERSEDED
  note: no empirical package transfers

displaced_pre_correction_candidate:
  sha: d56b5b3c44e39ddb8c883259584432ab39259306
  status: HISTORICAL / INVALIDATED_BY_PROVENANCE_CORRECTION
  deployment_id: dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
  deployment_url: https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
  allowed_cors_origin: https://dynamicgovernanceagenticformation-ndrorchestration-ndrorchestration.vercel.app
  note: non-closing historical evidence only

deployment_binding:
  deployment_id: NONE_YET
  deployment_url: NONE_YET
  deployment_target: NONE_YET
  deployment_state: NOT_ESTABLISHED
  source_sha_match: NONE_YET
  allowed_cors_origin: NONE_YET
  status: CURRENT-CANDIDATE DEPLOYMENT PENDING

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: REQUIRES CURRENT-CANDIDATE VERIFICATION
  P6a_CORS: REQUIRES CURRENT-CANDIDATE VERIFICATION
  P3: CURRENT-CANDIDATE EVIDENCE REQUIRED
  P4: CURRENT-CYCLE BLINDING/CUSTODY EVIDENCE REQUIRED
  P5: CURRENT-CYCLE REPRODUCIBILITY EVIDENCE REQUIRED
  P6: CURRENT-CYCLE DURABLE CUSTODY EVIDENCE REQUIRED
  P7: TECHNICALLY ADJUDICATED / FORMALLY OPEN — EXACT BINDING REQUIRED
  P8: OPEN / FAIL-CLOSED — CURRENT-CANDIDATE TGL/P-35 AND ANALYSIS BINDING REQUIRED
  P9: FRESH INDEPENDENT VERIFICATION REQUIRED

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus provenance anchor.
- `275756fd…` — exact current-main parent from which this candidate is derived.
- `f5461ec6…` — independently verified P-35 engineering remediation head.
- Candidate identity is intentionally left pending final document update so this manifest cannot make a moving SHA look frozen.
- The previous runtime candidate `92ff830b…` and deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` are historical for this candidate and do not transfer P2/P6a evidence.

## Promotion / binding rule

The corrected apparatus source establishes scientific apparatus provenance. The selected candidate establishes the exact executable identity. A current-candidate runtime result must identify the exact candidate commit/tree and exact deployment identity. P2/P6a, P3/P4/P5/P6, P7, P8, and P9 must all be regenerated or revalidated against that exact candidate before freeze transitions.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
