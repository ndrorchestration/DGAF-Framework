# Test Execution Readiness — 2026-08-21

## Purpose

This record inventories the tests that must execute before freeze readiness can be advanced. It does not claim execution merely because tests exist.

## Repository test surfaces identified

- `pptl/pytest.ini`
- `pptl/tests/`
- `tests/`
- `experiments/pdmal_pilot/test_execution_contract.py`
- `experiments/pdmal_topology/test_experiment.py`
- artifact/schema validation tests and supporting governance scripts
- full-repository audit workflow

The pilot execution-contract tests explicitly verify fail-closed behavior, fixed two-seed contract mode, explicit pilot preconditions, exact frozen-SHA enforcement, executor-path presence, sample-size validation, and deviation serialization. fileciteturn97file0

## Required execution tiers

### Tier 1 — deterministic / unit / contract

Run the complete pytest suite and the pilot execution-contract suite against the exact candidate SHA. These tests must establish that implementation behavior matches the documented preconditions and invariants.

### Tier 2 — repository/governance QA

Run `scripts/full_repo_audit.py`, `scripts/freeze_consistency_check.py`, the propagation checker, artifact schema/sidecar validation, and negative-path governance tests.

### Tier 3 — candidate deployment verification

Run current-candidate P2 runtime verification and P6a CORS verification against the deployment whose metadata exactly matches the candidate SHA. Historical deployment evidence is not substitutable.

### Tier 4 — operational security/custody

Run synthetic blinding operational verification and perform the real archive/retrieve/hash custody round trip.

### Tier 5 — independent verification

After P7/P8 are locked, an independent verifier must execute P9. This cannot be self-certified by the implementation authoring path.

## Current execution limitation

The connected GitHub interface does not expose a workflow-dispatch action, and current push-triggered workflow execution has not produced an accessible run for the latest audit candidate. Therefore this document records **execution required**, not **execution passed**.

## Safety boundary

Do not run the 50-seed empirical pilot before P1–P9 closure, a new immutable freeze, and explicit authorization. Empirical N remains `0`.
