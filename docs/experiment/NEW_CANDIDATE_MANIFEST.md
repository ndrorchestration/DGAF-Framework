# NEW CANDIDATE MANIFEST — post-#174 provenance-corrected apparatus cycle

```yaml
manifest_version: 12
designation_event: CURRENT_RUNTIME_EVIDENCE_RECONCILED_AFTER_P4_ARCHITECTURE_UPDATE
state: PRE-FREEZE / FAIL-CLOSED
reconciliation_source_boundary: a3bafa6fca8599df479a685828f5fdddb6bae589
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
  reconciliation_source_boundary: a3bafa6fca8599df479a685828f5fdddb6bae589
  status: DOCUMENTATION / EVALUATOR / CONTROL-PLANE LINEAGE
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
  P4: OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED
  P5: CLOSED / VERIFIED
  P6: CLOSED / VERIFIED
  P6a_CORS: CLOSED / VERIFIED
  P7: ADOPTED / FINAL BINDING OPEN
  P8: OPEN / FAIL-CLOSED
  P9: NOT EXECUTED / OPEN

authorization: NOT GRANTED
empirical_n: 0
freeze_status: NOT_ESTABLISHED
```

## Identity and evidence rules

- `2a54a67d…` is the corrected apparatus provenance anchor.
- `7c1cc4bb…` / tree `586c00d6…` is the designated executable runtime candidate.
- `dpl_8Msuf…` is the READY production deployment bound to that candidate at its scoped runtime evidence boundary.
- `a3bafa6f…` is the immutable control-plane source boundary used for this documentation reconciliation; it is deliberately not labeled “current main.”
- P2 and P6a were executed on 2026-09-03 and their candidate-bound artifacts were successfully re-retrieved on 2026-09-05. Retrieval does not constitute re-execution.
- P1, P2, P3, P5, P6, and P6a are closed within their explicitly bounded engineering/governance evidence contracts.
- P4 remains operationally open because no real admissible H/I/T custody mode has been instantiated and verified.
- P7 remains final-binding open; P8 remains fail-closed; final P9 is not executed.
- No closed engineering/governance predicate is efficacy evidence or authorization.

## P4 architecture and lifecycle boundary

PR #286 merged as `a3bafa6fca8599df479a685828f5fdddb6bae589` and generalized P4 from mandatory distinct-human custody to effective control separation. Modes H, I, and T are admissible in principle under the canonical procedure.

This manifest does not infer a real custody instance from that architecture change. Issue #285 is completed as the architecture correction; Issue #255 is superseded historical context. Issue #287 is the active design/threat-model lane for a possible zero-human Mode T lifecycle and explicitly does not establish an accepted technical custody implementation.

## Later control-plane/evaluation work

PR #268 corrected the documented Sentinel/AOGA runtime boundary: AOGA runtime is separately implemented/evidenced, while direct Sentinel→AOGA integration is not implemented/evidenced.

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` and made Issue #32 Task 4 fail closed without provenance-controlled ground truth plus independently generated outputs. This is evaluator-mechanism hardening only and does not create a model-performance result or alter the PDMAL candidate.

Issue #270 is now CLOSED / COMPLETED after the current-lineage flake8/Black/isort/mypy baseline was repaired and converted to fail-closed workflow gates. Issue #277 separately tracks the still-unestablished branch-protection/ruleset requirement for the Python quality matrix. Neither control changes this candidate manifest's scientific state.

## Mathematical identity boundary

Current PDMAL authority distinguishes the plastic constant `ρ ≈ 1.3247179572447454` from DGAF-specific Platinum Mean `pP = 1/(2 sin(π/11)) ≈ 1.774732842`. The exact dodecahedral Cheeger constant is `0.6`; unweighted Forman–Ricci curvature is `-2` on every edge and currently provides no discriminating audit signal on the unweighted graph.

## Descendant interpretation

This manifest does not treat later repository descendants as experimentally equivalent to the designated candidate. Historical provider/deployment incidents, quality findings, or custody assumptions remain scoped to the SHAs and records on which they occurred; they are not promoted into current-state claims without fresh observation or explicit supersession.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
