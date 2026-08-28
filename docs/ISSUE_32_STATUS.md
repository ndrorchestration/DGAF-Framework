# Issue #32 — Status Tracker

**Issue:** EVAL-001 — DGAF reproducible evaluation suite — baseline and evidence protocol  
**Last updated:** 2026-08-28  
**Status:** OPEN / EMPIRICAL EVIDENCE GATE

---

## Epistemic boundary

Issue #32 does not treat external benchmarks as DGAF validation. External benchmarks are contextual baselines only.

The repository-native protocol separates:

`IMPLEMENTATION TESTS → SYNTHETIC EVALUATION → MODEL-SPECIFIC RESULTS → REAL-WORKLOAD EVIDENCE`

A result is not promoted to `VERIFIED` without reproducible inputs, expected results, command/environment provenance, retained machine-readable output, and failure analysis.

## Repository-native slices

| Slice | Status | Scope |
|---|---|---|
| `role_boundary_coherence` | IMPLEMENTED | deterministic synthetic fixture/evaluator |
| `governance_schema_conformance` | IMPLEMENTED | deterministic 1,000-case schema classification; fixed seed `20260828` |
| `contraction_proof_fidelity` | IMPLEMENTED | deterministic 100-case analytic spectral-radius fixture/evaluator |
| `audit_hallucination_rate` | BLOCKED ON FIXTURE | requires provenance-controlled ground-truth audit corpus |
| `taubench_banking_mitigation` | CONDITIONAL | requires reproducible external benchmark/data |
| Real-workload evaluation | LATER | separate evidence track |

### Governance schema conformance

Implemented in `evaluations/governance_schema_conformance.py` with regression coverage in `tests/test_governance_schema_conformance.py`.

- fixed seed: `20260828`
- cases: `1000` (`500` expected-valid / `500` expected-invalid)
- validator: versioned `schemas/governance.yml.schema.json` via `jsonschema.Draft7Validator`
- metric: correct accept/reject classification
- evidence class: `SYNTHETIC`

### Contraction proof fidelity

Implemented in `evaluations/contraction_proof_fidelity.py` with fixture `evaluations/fixtures/contraction_proof_fidelity_v1.json` and regression coverage in `tests/test_contraction_proof_fidelity.py`.

- cases: `100`
- construction: deterministic diagonal matrices with independently specified spectral radii
- metric: correct contraction/non-contraction classification
- evidence class: `SYNTHETIC`

## CI verification state

A prior schema-conformance run on `6093673…` failed at test collection because `jsonschema` was absent from `requirements-ci.txt`. The dependency contract was corrected in commit `e46ffb3913794b506bf413e837fcf5be99d8f426` by adding `jsonschema==4.26.0` and constraining `setuptools>=83.0.0,<84`.

The combined evaluator tree at `352dd166…` and the corrected dependency tree at `e46ffb3…` must be evaluated on their exact current commits before the new slices are promoted to `VERIFIED`. Subsequent P-42 metadata normalization advanced `main` again to `bcc893f6…`; no earlier CI result is transferred automatically to that later tree.

## Evidence boundary

Repository-native fixtures validate evaluator/scoring behavior under synthetic conditions. They do not establish model capability, DGAF efficacy, production reliability, or real-world performance. No result is promoted beyond its actual execution scope.

## Reproducibility commands

```bash
python -m pytest -q tests/test_role_boundary_coherence.py
python -m pytest -q tests/test_governance_schema_conformance.py
python -m pytest -q tests/test_contraction_proof_fidelity.py
python evaluations/role_boundary_coherence.py --output artifacts/role_boundary_coherence.json
python evaluations/governance_schema_conformance.py --output artifacts/governance_schema_conformance.json
python evaluations/contraction_proof_fidelity.py --output artifacts/contraction_proof_fidelity.json
```

**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0  
**Freeze:** NOT CREATED
