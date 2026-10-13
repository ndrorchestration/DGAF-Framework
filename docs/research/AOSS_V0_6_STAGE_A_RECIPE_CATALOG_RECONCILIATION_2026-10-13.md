# AOSS Stage-A recipe-catalog reconciliation — 2026-10-13

Controller: #901  
Defect: #1349  
Classification: candidate correction / non-collecting / no authority effect

## Observed inconsistency

Protected main `aabf1163515af291dc564bd7564fd12762a898c8` bound the Stage-A recipe
catalog to frozen ACP source `dbab7c1afafec524ce7c18157de2089cafe79c87`.
For `suppressed_budget_exception_fail_closed`, the catalog recorded
`task.failed`, while three retained sources agree on `task.budget_exhausted`:

- `registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json`;
- `tests/resources/aoss_v0_6_acp_fixture_bundle.json`;
- frozen ACP `tests/test_core.py` plus `ControlPlane.dispatch()` /
  `_mark_budget_exhausted()`.

A static comparison of all 16 recipe classes found no second terminal-event mismatch.

## TDD evidence

Test-only RED commit: `cc5592947322cace19a01bc21d1e6368defd7746`.

Observed RED result:
`suppressed_budget_exception_fail_closed: task.failed != task.budget_exhausted`.

Candidate correction changes only that terminal-event value. The same static
cross-contract test then passes 2/2.

Historical catalog identity:
- Git blob: `178471a6a871fec5d5a7a6349f6f439af8667284`
- raw SHA-256: `1c93843dd03cf1e75fff8c390d3ef125d73f3215f77efb0465e19d5998910715`

Candidate catalog identity:
- Git blob: `6382a36a3b2bba25c4e152f475e9dbfb232d3a70`
- raw SHA-256: `b3c0d883cd9463ec558ee8a3fab3376641b2603eb474a745c119a28d1cd15d77`

## Handoff boundary

The accepted independent-validation handoff remains historical evidence bound
to the old catalog blob. This candidate does not rewrite that record or imply
that external reviewers received the corrected catalog. If this correction is
admitted, any current review packet that requires the catalog identity must be
explicitly refreshed and re-bound.

No ACP driver was imported or executed. No study attempt, outcome, acceptance,
readiness transition, or scientific-N increment was created.

`SOURCE_DRIVER_BINDING=NOT_ESTABLISHED`  
`EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED`  
`execution_allowed=false`  
`COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED`  
`SCIENTIFIC_N_INCREMENT=0`  
`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`  
`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`  
`HIGH_ASSURANCE=NOT_AUTHORIZED`
