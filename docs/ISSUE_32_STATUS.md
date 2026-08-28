# Issue #32 — Status Tracker

**Issue:** EVAL-001 — DGAF reproducible evaluation suite — baseline and evidence protocol  
**Last updated:** 2026-08-28  
**Status:** OPEN / EMPIRICAL EVIDENCE GATE

---

## Epistemic boundary

Issue #32 does not treat external model benchmarks as DGAF validation. External benchmarks are contextual baselines only.

The repository-native protocol separates:

`IMPLEMENTATION TESTS → SYNTHETIC EVALUATION → MODEL-SPECIFIC RESULTS → REAL-WORKLOAD EVIDENCE`

A result is not promoted to `VERIFIED` without reproducible inputs, expected results, command/environment provenance, retained machine-readable output, and failure analysis.

---

## Reproducible slices

### `role_boundary_coherence`

Existing deterministic fixture slice remains implemented. Its evaluator uses explicit expected labels and predictions; it is synthetic reproducibility evidence, not DGAF/model performance evidence.

### `governance_schema_conformance` — newly implemented

| Deliverable | Location | Status |
|---|---|---|
| Deterministic evaluator | `evaluations/governance_schema_conformance.py` | ✅ Implemented |
| Versioned schema under test | `schemas/governance.yml.schema.json` | ✅ Bound |
| Deterministic corpus generator | evaluator, fixed seed `20260828` | ✅ Implemented |
| Corpus size | 1,000 cases (500 expected-valid, 500 expected-invalid) | ✅ Defined |
| Mutation coverage | extra fields, missing fields, type errors, bounds, enum/pattern violations | ✅ Implemented |
| Regression gate | `tests/test_governance_schema_conformance.py` | ✅ Implemented |
| CI execution | Python Tests & Quality / PPTL CI triggered on `60936730824c296725817bccfdfa243513eddba3` | 🟡 RUNNING / QUEUED |
| Retained result | machine-readable evaluator output | 🟡 Pending successful CI execution |
| DGAF/model performance claim | — | 🔴 Not established |
| Real-world efficacy | — | 🔴 Not established |

The conformance metric is **correct accept/reject classification against the versioned JSON Schema**. This avoids treating invalid test fixtures as failed "valid outputs" while still exercising the schema boundary. The evaluator explicitly states that this is synthetic evidence and does not establish production reliability or DGAF efficacy.

---

## Remaining slices

1. `contraction_proof_fidelity` — deterministic specification corpus with independently computed spectral expected results.
2. `audit_hallucination_rate` — ground-truth audit fixture corpus before any rate is reported.
3. `taubench_banking_mitigation` — only if the external benchmark/data are available and reproducible in the repository environment.
4. Real-workload evaluation — separate evidence track after repository-native synthetic slices are stable.

The historical AHG Tasks 6–8 remain separate empirical claims and must not inherit validation merely because deterministic evaluator infrastructure passes.

---

## Closure conditions

Issue #32 remains open until the repository-native evaluation protocol has sufficient executable slices and retained evidence to support the claims being evaluated.

Closure must not be based solely on:

- code existence,
- unit-test success,
- external benchmark scores,
- synthetic fixture success,
- deployment status, or
- historical attestations.

---

## Reproducibility commands

```bash
python -m pytest -q tests/test_role_boundary_coherence.py
python evaluations/role_boundary_coherence.py --output artifacts/role_boundary_coherence.json
python -m pytest -q tests/test_governance_schema_conformance.py
python evaluations/governance_schema_conformance.py --variants 1000 --output artifacts/governance_schema_conformance.json
```

The schema-conformance evaluator emits a machine-readable result containing the schema hash, fixed seed, sample count, correct classifications, score, target, failure analysis, evidence classification, and limitations.
