# Issue #64 — Evaluation Integrity & Adversarial Measurement Tests

**Last updated:** 2026-09-05  
**Status:** OPEN / EVALUATION-INTEGRITY TRACK

## Historical exact verified fixture result

Governance CI run `33162492796` completed **SUCCESS** on exact commit `061286b1c17fe671cd5c58df025767befbeb55cd`.

Retained `dgaf-evaluation-evidence` includes `evaluation_integrity_fixture_suite.json` with:

- 12 deterministic cases
- 12/12 correct
- accuracy `1.0`
- six registered threats: benchmark gaming, measurement leakage, evaluator awareness, test-set contamination, stochastic seed artifacts, and topology specificity

The same historical artifact also retains the three repository-native Issue #32 deterministic slices:

- `role_boundary_coherence`: 10/10, score `1.0`
- `governance_schema_conformance`: 1000/1000, score `1.0`
- `contraction_proof_fidelity`: 100/100, score `1.0`

## Task 4 integrity hardening — merged current behavior

PR #269 merged to protected `main` as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` after all 17 returned exact-head workflows succeeded on head `d6b6fb640e6d310ff31c4a31d08541821824c412`.

The `audit_hallucination_rate` runner now:

- requires provenance-controlled ground-truth audit events;
- requires independently generated corresponding audit-event outputs;
- performs deterministic comparison of the six declared audit fields;
- emits no synthetic/random performance score when required evidence is absent, malformed, or insufficient;
- deliberately does not pass expected answers into the legacy Herald client path;
- preserves BF16 as the required precision policy.

Regression evidence from Python Tests & Quality Checks run `33957199893`:

- all seven Task-4 integrity regressions were collected and passed;
- Python 3.12 overall: 190 passed / 4 skipped;
- Python 3.10 and 3.11 test jobs also completed successfully.

Governance CI `33957199870` and PDMAL Pre-Freeze Runner Validation `33957199849` also completed successfully for the PR head.

## Evidence boundary

The historical fixture result is **SYNTHETIC** repository-authored evaluator/mechanism evidence for its exact executed tree. The current Task-4 change verifies a fail-closed deterministic comparison mechanism and answer-leakage prevention behavior.

Neither establishes model-facing adversarial robustness, resistance to benchmark gaming in actual model execution, contamination resistance, topology invariance, DGAF efficacy, hallucination rate, or real-world performance.

## Remaining work

- provenance-controlled ground-truth corpus for `audit_hallucination_rate`;
- independently generated corresponding model/Herald outputs;
- model-facing adversarial execution if robustness claims are pursued;
- reproducible external benchmark execution where applicable;
- independent verification where required by the applicable governance predicate.

## Quality diagnostic boundary

Python workflow run `33957199893` records non-blocking Black/isort/mypy debt on the later lineage. Those diagnostics are currently configured `continue-on-error`, so a green workflow cannot be promoted into a claim that formatting/import/type checks are clean.

That current-lineage quality regression is tracked separately in Issue #270.

## Control boundary

No freeze, authorization, unblinding, or empirical-N change follows from this evaluator work.

**Current protected main:** `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`  
**Fixture status:** VERIFIED / SYNTHETIC / historical exact tree `061286b1…` / Governance CI `33162492796`  
**Task-4 evaluator:** MERGED / FAIL-CLOSED MECHANISM / NO PERFORMANCE RESULT  
**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0  
**Freeze:** NOT CREATED
