# Navigator — QA Rubric v1.0

**Agent:** Navigator
**Agent ID:** A-22
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Route Quality (weight: ×0.30)

| Score | Criteria |
|---|---|
| 1.0 | All 6 required fields present; dependencies mapped; gate checkpoints included |
| 0.75 | 5/6 fields; minor dependency gap |
| 0.50 | 4/6 fields; OR dependencies not mapped |
| 0.25 | Partial route only; missing gate checkpoints |
| 0.0 | No structured route; OR route bypasses gates |

**Critical fail:** Gate bypass detected → D1 = 0.0, output blocked.

---

### D2 — Hazard Response (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | All hazards detected pre-execution; contingency paths pre-constructed for all critical steps |
| 0.75 | All hazards detected; contingency paths for most critical steps |
| 0.50 | Hazards detected reactively (post-block); contingency path constructed in-flight |
| 0.25 | Hazard detected; no contingency available |
| 0.0 | Hazard not detected until execution failure |

---

### D3 — Contingency Readiness (weight: ×0.20)

| Score | Criteria |
|---|---|
| 1.0 | Minimum 1 contingency path per critical step; all paths verified |
| 0.75 | Most critical steps covered; minor gap |
| 0.50 | Some contingency paths present but not verified |
| 0.0 | No contingency paths constructed |

---

### D4 — Velocity Alignment (weight: ×0.15)

| Score | Criteria |
|---|---|
| 1.0 | Velocity targets set per step; coordinated with Momentum; no persistent deviations |
| 0.75 | Targets set; minor unresolved deviation |
| 0.50 | Targets set but not coordinated with Momentum |
| 0.0 | No velocity targets; OR persistent deviation not addressed |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | All routes, hazards, and contingencies logged; memory updated |
| 0.5 | Minor logging gap |
| 0.0 | No logging; OR memory not updated |

---

## Composite Score

```
Navigator_score = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
Threshold: ≥ 0.75
Critical fail override: D1 = 0.0 (gate bypass) → output blocked
```

---

*Classification: T1 PUBLIC*
