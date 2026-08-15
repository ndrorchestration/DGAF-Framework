# Issue #32 — Status Tracker

**Issue:** EVAL-001 — DGAF reproducible evaluation suite — baseline and evidence protocol  
**Last updated:** 2026-08-15  
**Status:** OPEN / EMPIRICAL EVIDENCE GATE

---

## Epistemic boundary

Issue #32 no longer treats external Nemotron or other published benchmark scores as DGAF validation. External benchmarks are contextual baselines only.

The repository-native protocol separates:

`IMPLEMENTATION TESTS → SYNTHETIC EVALUATION → MODEL-SPECIFIC RESULTS → REAL-WORKLOAD EVIDENCE`

A result is not promoted to `VERIFIED` without reproducible inputs, expected results, command/environment provenance, retained machine-readable output, and failure analysis.

---

## First reproducible slice — implemented

### `role_boundary_coherence`

| Deliverable | Location | Status |
|---|---|---|
| Deterministic fixture corpus | `evaluations/fixtures/role_boundary_coherence_v1.json` | ✅ Implemented |
| Independent expected labels | fixture corpus | ✅ Implemented |
| Canonical protocol | 50-turn trace / turn-48 probe | ✅ Defined |
| Scoring | exact role match / target 0.95 | ✅ Implemented |
| Provenance | fixture SHA-256 + source metadata | ✅ Implemented |
| Failure analysis | per-case machine-readable results | ✅ Implemented |
| Regression test | `tests/test_role_boundary_coherence.py` | ✅ Implemented |
| CI execution | `.github/workflows/governance-ci.yml` | ✅ Implemented |
| Retained result | CI artifact `dgaf-role-boundary-coherence` | 🟡 Pending successful workflow run |
| DGAF/model performance claim | — | 🔴 Not established |
| Real-world efficacy | — | 🔴 Not established |

The current predictions are explicit evaluator inputs, not model-generated outputs. A passing fixture run therefore establishes evaluator reproducibility, not DGAF role-boundary efficacy.

---

## Remaining slices

1. `contraction_proof_fidelity` — deterministic specification corpus with independently computed spectral expected results.
2. `governance_schema_conformance` — schema corpus/fuzz cases with explicit valid/invalid labels.
3. `audit_hallucination_rate` — ground-truth audit fixture corpus before any rate is reported.
4. `taubench_banking_mitigation` — only if the external benchmark/data are available and reproducible in the repository environment.
5. Real-workload evaluation — separate evidence track after repository-native synthetic slices are stable.

The historical AHG Tasks 6–8 remain separate empirical claims and must not inherit validation merely because the deterministic evaluator infrastructure passes.

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
```

The evaluator emits a machine-readable result containing the fixture hash, protocol metadata, score, target, per-case results, failure analysis, evidence classification, and limitations.
