# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 8
designation_event: CURRENT_RUNTIME_EVIDENCE_BOUND
state: PRE-FREEZE / FAIL-CLOSED
main_tip_at_reconciliation: 35436f1c95c11e49d8af7603bf914128cf2b4aee
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: VERIFIED EXECUTABLE RUNTIME CANDIDATE
candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
candidate_designation_rule: exact executable candidate commit used by the verified P2/P6a runtime evidence; later documentation-only control-plane commits do not reopen those predicates
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
control_plane_successor:
  sha: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
  status: CONSOLIDATED DOCUMENTATION / CONTROL-PLANE ANCHOR
  main_tip: 35436f1c95c11e49d8af7603bf914128cf2b4aee
  note: later documentation-only descendants remain control-plane lineage and do not alter the runtime surfaces covered by P2/P6a
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
- `586c00d6…` — exact tree of that runtime candidate.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — exact deployment bound to that runtime candidate.
- `89be386b…` — consolidated documentation/control-state anchor.
- `35436f1c…` — present `main` tip, consisting of later documentation-only reconciliation descendants from the consolidated anchor.

## Binding rule

The corrected apparatus source establishes provenance. The verified executable runtime candidate establishes the exact runtime identity. P2 and P6a are closed for that candidate/deployment pair. Later documentation-only control-plane successors do not reopen those predicates. Downstream evidence must remain bound to the exact evidence candidate used for the relevant gate.

P3–P6, final P7 binding, P8, and independent P9 remain outstanding.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**