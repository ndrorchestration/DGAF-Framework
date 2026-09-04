# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 8
designation_event: CURRENT_RUNTIME_EVIDENCE_BOUND
state: PRE-FREEZE / FAIL-CLOSED
mainline_commit_at_last_reconciliation: a17aee4a97fc8159361bdc0b30c6039b19752c07
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
apparatus_source_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
candidate_designation: RUNTIME CANDIDATE REFERENCED BY HISTORICAL P2/P6a EVIDENCE
candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
candidate_designation_rule: exact executable candidate commit referenced by the recorded P2/P6a runtime evidence; later documentation-only control-plane commits do not change that historical identity
candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
control_plane_successor:
  sha: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
  status: CONSOLIDATED DOCUMENTATION / CONTROL-PLANE ANCHOR
  last_reconciled_mainline: a17aee4a97fc8159361bdc0b30c6039b19752c07
  note: later documentation-only descendants remain control-plane lineage and do not alter the runtime surfaces covered by the recorded P2/P6a evidence
provenance_correction:
  pr: 174
  state: MERGED
  merge_commit: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
  scope: bind_all_seven_behavior_affecting_gate_states_into_canonical_identity
deployment_binding:
  deployment_id: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
  deployment_url: https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app
  deployment_target: production
  deployment_state: HISTORICAL REFERENCE / CURRENT RETRIEVAL UNCONFIRMED
  source_sha_match: HISTORICALLY RECORDED MATCH
  allowed_cors_origin: https://dynamicgovernanceagenticformation.vercel.app
  status: HISTORICAL_RUNTIME_EVIDENCE_SCOPE

gate_ledger:
  P31_SCPE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P33_CONVERGENCE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P29_SENTINEL: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P30_APOGEE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  DEMIJOULE: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P27_KAPPA: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P32_PHI: RESTORED_IMPLEMENTED_PROVENANCE_COMPLETE
  P2_RUNTIME: HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED
  P6a_CORS: HISTORICAL RECORD / CURRENT RETRIEVAL UNCONFIRMED
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
- `7c1cc4bb…` — runtime candidate referenced by the historical P2/P6a evidence records.
- `586c00d6…` — exact tree of that runtime candidate.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — deployment referenced by those historical runtime records; current retrieval is unconfirmed.
- `89be386b…` — consolidated documentation/control-state anchor.
- `a17aee4a…` — latest mainline reconciliation commit at this record's update; documentation/control-plane lineage.

## Binding rule

The corrected apparatus source establishes provenance. The runtime candidate establishes the exact identity referenced by the recorded P2/P6a evidence. The current verification pass did not independently re-retrieve the cited Actions records, so those predicates remain historical repository assertions rather than freshly verified evidence. Later documentation-only control-plane successors do not retroactively change the runtime identity or create new runtime evidence.

P1/P3–P6, final P7 binding, P8, and independent P9 remain outstanding for the current closure cycle.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
