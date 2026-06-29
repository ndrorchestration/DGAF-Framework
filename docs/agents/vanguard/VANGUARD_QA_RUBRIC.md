# Vanguard — QA Rubric v1.0

**Agent:** Vanguard
**Agent ID:** A-21
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Scouting Coverage (weight: ×0.30)

| Score | Criteria |
|---|---|
| 1.0 | TRL 1–4 technologies identified from ≥3 source types; pipeline current |
| 0.75 | ≥2 source types; pipeline current |
| 0.50 | 1 source type only; OR pipeline has stale entries |
| 0.25 | Ad-hoc scouting only; no systematic coverage |
| 0.0 | No scouting activity; OR only mainstream (TRL 7+) technologies identified |

---

### D2 — TRL Assessment Accuracy (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | All TRL ratings evidence-cited; Prof Prodigy adoption curve PASS |
| 0.75 | TRL ratings cited; minor gap in evidence quality |
| 0.50 | TRL ratings present but assertion-only (no evidence cited) |
| 0.25 | TRL estimates only (no full assessment) |
| 0.0 | No TRL ratings; OR TRL ratings without any justification |

**Critical fail:** Technology advocacy without completed assessment → D2 = 0.0, output blocked.

---

### D3 — First-Mover Window Modeling (weight: ×0.20)

| Score | Criteria |
|---|---|
| 1.0 | Window calculated for all TRL ≤ 5 / fit ≥ 0.7 technologies; Oracle temporal framing applied |
| 0.75 | Window calculated; minor temporal framing gap |
| 0.50 | Window estimated but not formally calculated |
| 0.0 | No window modeling for eligible technologies |

---

### D4 — Pipeline Hygiene (weight: ×0.15)

| Score | Criteria |
|---|---|
| 1.0 | No stale entries; all entries prioritized; top-3 current |
| 0.75 | Minor staleness; top-3 current |
| 0.50 | Some stale entries; top-3 present |
| 0.0 | Pipeline not maintained; OR >50% stale |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | All assessments logged; pipeline updated; anomalies recorded |
| 0.5 | Minor logging gap |
| 0.0 | No logging; OR memory not updated |

---

## Composite Score

```
Vanguard_score = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
Threshold for Apogee gate: ≥ 0.75
Critical fail override: D2 = 0.0 → output blocked regardless of composite
```

---

*Classification: T1 PUBLIC*
