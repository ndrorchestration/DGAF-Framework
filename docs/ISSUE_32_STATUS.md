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

## Exact-tree repository-native verification

Governance CI run `33162492796` completed **SUCCESS** on exact tree `061286b1c17fe671cd5c58df025767befbeb55cd` and retained:

- `role_boundary_coherence`: 10/10, score `1.0`
- `governance_schema_conformance`: 1000/1000, score `1.0`, fixed seed `20260828`
- `contraction_proof_fidelity`: 100/100, score `1.0`

Retained artifact: `dgaf-evaluation-evidence`.

All three records identify the same exact source commit and workflow run. They are **SYNTHETIC** repository-authored mechanism/evaluator evidence only.

## Evaluation-integrity fixture track (#64)

The separate #64 fixture suite is also verified on the same exact run:

- fixture: `evaluations/evaluation_integrity_fixture_suite.py`
- regression coverage: `tests/test_evaluation_integrity_fixture_suite.py`
- 12 cases
- 12/12 correct, accuracy `1.0`
- six registered threat classes

## Task 4 evaluator contract

The `audit_hallucination_rate` runner is required to compare independently generated audit events against provenance-controlled ground-truth events on six declared fields: `role`, `curvature`, `contraction`, `gate_result`, `timestamp`, and `session_id`.

The previous runner implementation accepted ground-truth/client parameters but ignored them and synthesized stochastic scores from published benchmark baselines. That behavior was not part of the retained Governance-CI evidence above, but it was too permissive for a direct evidence-gated runner.

The current hardening change makes Task 4 fail closed unless both ground-truth events and independently produced audit-event outputs are supplied. It removes baseline-derived/random scoring from Task 4 and uses deterministic exact field comparison. The legacy `herald_client` parameter is not auto-invoked with expected events, preventing the evaluator from leaking answers into generation.

Regression coverage is provided by `tests/test_audit_hallucination_rate.py` and checks missing evidence, exact matches, deterministic mismatches, malformed ground truth, insufficient sample pairs, non-invocation of the legacy client, and the BF16 policy gate.

This hardens the **evaluator mechanism only**. It does not create the required provenance-controlled corpus, independently generate Herald/model outputs, or establish a hallucination-rate result.

## Remaining slices

- `audit_hallucination_rate`: **BLOCKED ON FIXTURE / OUTPUT CORPUS** — provenance-controlled ground-truth audit events and independently generated corresponding outputs are required before a performance result exists.
- `taubench_banking_mitigation`: CONDITIONAL — reproducible external benchmark/data required.
- Real-workload evaluation remains a separate evidence track.

## Evidence boundary

The verified results establish evaluator/scoring behavior under repository-authored deterministic synthetic conditions. They do not establish model capability, DGAF efficacy, production reliability, adversarial robustness, or real-world performance.

The successful Governance CI run also emitted exact-run E2b/M6, P-42, P8, formal-model, and provenance artifacts. Those are not automatically transferable to later commits.

Task 4 hardening must itself pass current exact-head CI before being treated as merged repository behavior. Even after that, Task 4 remains blocked until a provenance-controlled fixture/output corpus is supplied and retained.

**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0  
**Freeze:** NOT CREATED
