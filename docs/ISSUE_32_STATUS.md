# Issue #32 — Status Tracker

**Issue:** EVAL-001 — DGAF reproducible evaluation suite — baseline and evidence protocol  
**Last updated:** 2026-09-05  
**Status:** OPEN / EMPIRICAL EVIDENCE GATE

---

## Epistemic boundary

Issue #32 does not treat external benchmarks as DGAF validation. External benchmarks are contextual baselines only.

The repository-native protocol separates:

`IMPLEMENTATION TESTS → SYNTHETIC EVALUATION → MODEL-SPECIFIC RESULTS → REAL-WORKLOAD EVIDENCE`

A result is not promoted to `VERIFIED` without reproducible inputs, expected results, command/environment provenance, retained machine-readable output, and failure analysis.

## Historical exact-tree repository-native verification

Governance CI run `33162492796` completed **SUCCESS** on exact tree `061286b1c17fe671cd5c58df025767befbeb55cd` and retained:

- `role_boundary_coherence`: 10/10, score `1.0`
- `governance_schema_conformance`: 1000/1000, score `1.0`, fixed seed `20260828`
- `contraction_proof_fidelity`: 100/100, score `1.0`

Retained artifact: `dgaf-evaluation-evidence`.

All three records identify the same exact source commit and workflow run. They are **SYNTHETIC** repository-authored mechanism/evaluator evidence only.

## Evaluation-integrity fixture track (#64)

The separate #64 fixture suite remains verified on the same historical exact run:

- fixture: `evaluations/evaluation_integrity_fixture_suite.py`
- regression coverage: `tests/test_evaluation_integrity_fixture_suite.py`
- 12 cases
- 12/12 correct, accuracy `1.0`
- six registered threat classes

## Task 4 evaluator contract — merged current behavior

PR #269 hardened `audit_hallucination_rate` and merged to protected `main` as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` from exact PR head `d6b6fb640e6d310ff31c4a31d08541821824c412`.

Before merge, all 17 returned exact-head workflows completed successfully. Key evidence includes:

- Python Tests & Quality Checks run `33957199893`: SUCCESS.
- Governance CI run `33957199870`: SUCCESS.
- PDMAL Pre-Freeze Runner Validation run `33957199849`: SUCCESS.
- Python 3.12 pytest: 190 passed / 4 skipped overall.
- All seven `tests/test_audit_hallucination_rate.py` regressions were collected and passed.
- Python 3.10 and Python 3.11 test jobs also completed successfully.

The Task 4 runner now requires both provenance-controlled ground-truth audit events and independently generated corresponding audit-event outputs. It deterministically compares six declared fields:

- `role`
- `curvature`
- `contraction`
- `gate_result`
- `timestamp`
- `session_id`

If required evidence is absent, malformed, or insufficient, the task fails closed and emits no synthetic/random performance result. The legacy `herald_client` parameter is retained for compatibility but is deliberately not auto-invoked with expected answers, preventing answer leakage into the generation path. BF16 remains the required precision policy.

This establishes the **evaluator mechanism hardening only**. It does not create the required provenance-controlled corpus, independently generate Herald/model outputs, or establish a hallucination-rate result.

## Remaining slices

- `audit_hallucination_rate`: **BLOCKED ON FIXTURE / OUTPUT CORPUS** — provenance-controlled ground-truth audit events and independently generated corresponding outputs are required before a model-performance result exists.
- `taubench_banking_mitigation`: CONDITIONAL — reproducible external benchmark/data required.
- Real-workload evaluation remains a separate evidence track.

## Quality diagnostic boundary

Python workflow run `33957199893` also recorded current-lineage formatting/import/type debt. Black, isort, mypy, and broad lint diagnostics are presently configured `continue-on-error`, so workflow SUCCESS must not be represented as a clean formatting/type baseline.

That later quality regression is tracked separately in Issue #270. The Task-4 regression tests themselves passed across the supported Python matrix.

## Evidence boundary

The historical verified results establish evaluator/scoring behavior under repository-authored deterministic synthetic conditions. The Task-4 merge establishes fail-closed deterministic comparison mechanics and leakage prevention. Neither establishes model capability, DGAF efficacy, production reliability, adversarial robustness, hallucination rate, or real-world performance.

The successful PR-head Governance CI and PDMAL Pre-Freeze runs are engineering/governance compatibility evidence only. They do not alter PDMAL scientific gate state.

**Current protected main:** `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`  
**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0  
**Freeze:** NOT CREATED
