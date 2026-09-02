# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 7
designation_event: SELECTED_EXPERIMENTAL_CANDIDATE_RECONCILED
state: PRE-FREEZE / FAIL-CLOSED
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: SELECTED EXPERIMENTAL CANDIDATE
candidate_sha: 58ba9a072f40e94638b0332eeec19dd882a7ff95
candidate_tree_sha: abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb
candidate_designation_rule: exact PR #192 head selected for the September 2 pre-freeze verification cycle; candidate identity must remain distinct from workflow merge-ref execution identities
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 58ba9a072f40e94638b0332eeec19dd882a7ff95
candidate_pr: 192
candidate_branch: candidate/p35-integrated-current-20260902
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
  sha: edd3b5c8266e2680b9bb94301c2623a3f1ac0cf0
  status: HISTORICAL / SUPERSEDED_BY_CLEAN_CURRENT_CANDIDATE
  note: predecessor candidate; no empirical package transfers
historical_runtime_candidate:
  sha: 92ff830b1c67413df745e37087e6447c9c251b9a
  tree_sha: 73cf3adcc2fd600eda83b818a681c83a7bb1c2ae
  deployment_id: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
  status: HISTORICAL / NON-TRANSFERABLE_RUNTIME_EVIDENCE
deployment_binding:
  deployment_id: NOT_ESTABLISHED
  deployment_url: NOT_ESTABLISHED
  deployment_target: NOT_ESTABLISHED
  deployment_state: NOT_ESTABLISHED
  source_sha_match: NOT_ESTABLISHED
  status: DEPLOYMENT_EVIDENCE_REQUIRED

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: OPEN / EXACT_DEPLOYMENT_REQUIRED
  P6a_CORS: OPEN / EXACT_DEPLOYMENT_REQUIRED
  P3: VERIFIED / ENGINEERING_CONTROL SCOPE
  P4: OPEN / OPERATIONAL_CLOSURE_REQUIRED
  P5: VERIFIED / VERIFIER_TOOLCHAIN_SCOPE
  P6: OPEN / DURABLE_CUSTODY_REQUIRED
  P7: EXACT_CANDIDATE_BINDING_RECORDED_PRE_FREEZE
  P8: OPEN / FAIL-CLOSED
  P9: OPEN / FRESH_FINAL_CANDIDATE_VERIFICATION_REQUIRED

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
```

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus source from merged PR #174 and canonical provenance anchor.
- `973c9233…` — exact tree of the corrected apparatus source.
- `58ba9a…` — selected September 2 experimental candidate / PR #192 head.
- `abdbc9b…` — exact tree of the selected candidate.
- `92ff830b…` — historical runtime candidate whose P2/P6a evidence remains non-transferable.
- `dpl_Br3muEJ…` — historical production deployment for the `92ff…` runtime evidence scope.
- `edd3b5c…` — immediate predecessor candidate; superseded by clean corrections incorporated into `58ba9a…`.

## Promotion / binding rule

The corrected apparatus source establishes apparatus provenance. The selected candidate establishes the exact executable candidate identity. A candidate-bound runtime result must identify that exact commit/tree and an independently confirmed deployment identity. Downstream evidence must remain bound to the same candidate/deployment lineage before P2/P6a/P7/P8/P9/freeze transitions can close.

The September 2 candidate CI wave is green, but GitHub Actions success does not establish deployment identity, runtime health, durable custody, freeze, authorization, or empirical data.

## Documentation hygiene

The historical runtime manifest and prior candidate records remain preserved as exact-scoped provenance. This manifest is the current selected-candidate control surface and deliberately records deployment identity as unresolved until exact Vercel source-SHA evidence exists.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
