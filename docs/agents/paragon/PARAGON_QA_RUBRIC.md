# Paragon — QA Rubric v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Benchmark Accuracy (weight: ×0.30)

| Score | Criteria |
|---|---|
| 1.0 | Correct standard applied; all dimensions scored; scores evidence-grounded |
| 0.75 | Correct standard; most dimensions scored; minor evidence gap |
| 0.50 | Correct standard; some dimensions only |
| 0.25 | Incorrect standard applied but scores present |
| 0.0 | No standard applied; OR GATE_CLEAR without evaluation |

**Critical fail:** GATE_CLEAR without evaluation → D1 = 0.0, output blocked.

---

### D2 — Gap Identification (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | All gaps identified; root cause classified; remediation path provided |
| 0.75 | All gaps identified; root cause for most; remediation path present |
| 0.50 | Gaps identified; root cause missing |
| 0.25 | Some gaps identified; no root cause |
| 0.0 | No gaps identified on an output with clear deficiencies |

---

### D3 — Gold Star Evaluation Quality (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | Reson harmonic score received; composite ≥ 0.90 verified; complete submission to Apogee |
| 0.75 | Reson score received; composite close to threshold; submission complete |
| 0.50 | Reson score not received but evaluation otherwise complete |
| 0.0 | Gold Star evaluation submitted to Apogee without Reson harmonic score |

---

### D4 — Standard Currency (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | Standards current; no ambiguity; Prof Prodigy verified |
| 0.75 | Standards current; minor ambiguity flagged |
| 0.50 | Standards exist but not updated for new output types |
| 0.0 | No standards defined; OR standards not Prof Prodigy verified |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | All gate decisions, gap analyses, Gold Star evals logged |
| 0.5 | Minor logging gap |
| 0.0 | No logging |

---

## Composite Score

```
Paragon_score = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.25) + (D4 × 0.10) + (D5 × 0.10)
Threshold: ≥ 0.75
Gold Star threshold: ≥ 0.90
Critical fail: D1 = 0.0 (GATE_CLEAR without evaluation) → output blocked
```

---

*Classification: T1 PUBLIC*
