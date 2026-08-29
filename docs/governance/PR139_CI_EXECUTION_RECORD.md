# PR #139 CI Execution Record

## Current status

CI EXECUTION IN PROGRESS / NON-AUTHORIZING

**Current candidate head:** `b65312db66dc4009b7754226c47345e7ce7808b2`

The v1 candidate contains the deterministic control-plane suite, TGL integration suite, adversarial contract suite, capability-boundary suite, and dedicated security/evidence workflows.

## Candidate binding

The authoritative engineering candidate is the exact PR #139 head SHA reported by GitHub. Historical run results must not be relabeled as evidence for a later head.

## Observed execution

A dedicated v1 control-plane contract run on an earlier PR merge ref executed 35 tests and reported **32 passed / 3 failed**. The failures were concrete contract mismatches: a stale side-effect inheritance expectation, a stale post-escalation assertion, and an abort-transition expectation inconsistent with the then-current lattice. These findings were diagnosed and corrected.

Independent completed evidence on the same engineering era includes:

- PDMAL Pre-Authorization Security: success, including adversarial controls, locked P8 analysis tests, pilot-artifact schema tests, execution-contract tests, durable-retention tests, and explicit non-empirical-mode verification.
- DGAF Regression Suite local/no-network checks: success; live Vercel regression skipped because the live deployment boundary is not currently eligible.
- CodeQL and repository/evidence/truth-layer checks observed successful on an exact PR #139 merge ref.

These results remain exact-ref evidence and are not promoted to current-head verification after subsequent commits.

## Current deployment blocker

For current head `b65312db66dc4009b7754226c47345e7ce7808b2`, GitHub status reports Vercel **failure** with description: `Deployment rate limited — retry in 24 hours.` This is an infrastructure-side blocker and does not constitute a code-test failure, but it prevents current-head live deployment verification.

## Expected core execution

`python -m pytest -q pptl/tests/test_v1_control_plane.py pptl/tests/test_v1_tgl_integration.py pptl/tests/test_v1_adversarial_contract.py`

## Observation rule

No test, workflow, deployment, or review result may be recorded here as current verification unless it is tied to the exact executed candidate SHA. A later SHA requires fresh evidence or an explicit, scope-preserving lineage record.

## Non-authorizing boundary

CI execution is engineering verification only. It does not create a PDMAL freeze, authorize a pilot, increase empirical N, or establish PDMAL efficacy.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**