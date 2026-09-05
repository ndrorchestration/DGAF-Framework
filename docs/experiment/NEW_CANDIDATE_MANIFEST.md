# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 9
designation_event: CURRENT_RUNTIME_EVIDENCE_RECONCILED
state: PRE-FREEZE / FAIL-CLOSED
mainline_commit_at_last_reconciliation: 8ae37faee637d3992dfec2f635ea4d1d9252ef2d
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: DESIGNATED EXECUTABLE RUNTIME CANDIDATE
candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
candidate_designation_rule: later documentation/control-plane descendants do not replace this executable identity or inherit its evidence without an explicit provenance transition
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8

control_plane:
  consolidated_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
  main_at_last_reconciliation: 8ae37faee637d3992dfec2f635ea4d1d9252ef2d
  status: DOCUMENTATION / CONTROL-PLANE LINEAGE
  runtime_evidence_inherited: false

provenance_correction:
  pr: 174
  state: MERGED
  merge_commit: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
  scope: bind_all_seven_behavior_affecting_gate_states_into_canonical_identity

deployment_binding:
  deployment_id: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
  deployment_url: https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: READY
  git_source_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
  source_sha_match: MATCHED
  allowed_cors_origin: https://dynamicgovernanceagenticformation.vercel.app

runtime_evidence:
  P2:
    state: CLOSED / VERIFIED
    run: 33730195621
    artifact: 9883521704
    digest: sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d
    retrieved_on: 2026-09-05
    scope: exact_candidate_deployment_five_case_runtime_predicates
  P6a:
    state: CLOSED / VERIFIED
    run: 33728695806
    artifact: 9882965299
    digest: sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f
    retrieved_on: 2026-09-05
    scope: exact_candidate_deployment_four_case_cors_predicates

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P1: CLOSED / VERIFIED
  P2_RUNTIME: CLOSED / VERIFIED
  P3: CLOSED / VERIFIED
  P4: OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT
  P5: OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT
  P6: CLOSED / VERIFIED
  P6a_CORS: CLOSED / VERIFIED
  P7: ADOPTED / FINAL BINDING OPEN
  P8: OPEN / FAIL-CLOSED
  P9: OPEN

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_ESTABLISHED
```

## Identity and evidence rules

- `2a54a67d…` is the corrected apparatus provenance anchor.
- `7c1cc4bb…` / tree `586c00d6…` is the designated executable runtime candidate.
- `dpl_8Msuf…` is the READY production deployment bound to that candidate.
- `8ae37fa…` is a later documentation/control-plane reconciliation commit, not a replacement runtime candidate.
- P2 and P6a were executed on 2026-09-03 and their candidate-bound artifacts were successfully re-retrieved on 2026-09-05. Retrieval does not constitute re-execution.
- P3 and P6 are closed within their defined engineering contracts.
- P4 and P5 retain substantive open prerequisites. P7–P9, freeze, and authorization remain open or absent.

## Current-main deployment limitation

The Vercel workflow did not create a deployment for `8ae37fa…` because the free-plan deployment quota was exceeded. Current-main deployment identity and live regression are therefore not executed and do not inherit the `7c1cc4bb…` result.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
