# Oracle — QA Rubric v1.0

**Agent:** Oracle
**Agent ID:** A-20
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Scenario Quality (weight: ×0.30)

| Score | Criteria |
|---|---|
| 1.0 | All 5 required fields present; 3+ scenarios; internally consistent; no logical contradictions |
| 0.75 | 4/5 fields present; minor internal tension (resolvable) |
| 0.50 | 3/5 fields present; OR only 2 scenarios constructed |
| 0.25 | 2/5 fields; OR scenarios are not meaningfully distinct |
| 0.0 | Single scenario / single-point prediction; OR missing trigger + implication |

**Critical fail:** Single-point prediction with no probability distribution → D1 = 0.0, output blocked.

---

### D2 — Forecast Calibration (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | Probability weights sum to 1.0; Prof Prodigy verification PASS; distributions well-specified |
| 0.75 | Weights sum to 1.0; minor distribution specification gap |
| 0.50 | Weights sum to 1.0 but Prof Prodigy verification pending or minor issue |
| 0.25 | Weights do not sum to 1.0 but error <10% |
| 0.0 | No probability weights; OR Prof Prodigy verification FAIL |

---

### D3 — Horizon Coverage (weight: ×0.20)

| Score | Criteria |
|---|---|
| 1.0 | All three horizon bands addressed; temporal labels on all outputs |
| 0.75 | Two horizon bands addressed; labels present |
| 0.50 | One horizon band only; OR labels missing on some outputs |
| 0.0 | No temporal horizon labels; OR single time horizon only |

---

### D4 — Temporal Accuracy (weight: ×0.15)

| Score | Criteria |
|---|---|
| 1.0 | No temporal myopia or paralysis detected; horizon map current |
| 0.75 | Minor imbalance; self-corrected within session |
| 0.50 | Imbalance detected; correction directive issued but not yet applied |
| 0.0 | Persistent myopia or paralysis; no correction initiated |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | All scenario sets logged; anomalies recorded; memory updated |
| 0.5 | Minor logging gap |
| 0.0 | No logging; OR memory not updated |

---

## Composite Score

```
Oracle_score = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
Threshold for Apogee gate: ≥ 0.75
Critical fail override: D1 = 0.0 → output blocked regardless of composite
```

---

*Classification: T1 PUBLIC*
