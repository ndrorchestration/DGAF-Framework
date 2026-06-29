# Sentinel-Phi — QA Rubric v1.0

**Agent:** Sentinel-Phi
**Agent ID:** A-12-φ
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Threat Model Accuracy (weight: ×0.35) — CRITICAL

| Score | Criteria |
|---|---|
| 1.0 | All risk vectors identified; α calculated for each; PASS/FLAG correctly issued |
| 0.75 | All risk vectors identified; α estimated (not fully calculated); correct outcome |
| 0.50 | Major risk vectors identified; minor vectors missed; outcome correct |
| 0.25 | Risk vectors partially identified; outcome uncertain |
| 0.0 | Risk vectors not identified; OR α ≥ 1 scenario cleared as PASS |

**Critical fail:** α ≥ 1 risk vector cleared as PASS → D1 = 0.0, RISK_FLAG mandatory, output blocked.

---

### D2 — Technology Risk Coverage (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | All 4 risk dimensions assessed (adoption / disruption / dependency / security) |
| 0.75 | 3/4 dimensions assessed |
| 0.50 | 2/4 dimensions assessed |
| 0.25 | 1/4 dimensions assessed |
| 0.0 | No technology risk assessment performed |

---

### D3 — NDR-133 Compliance (weight: ×0.20)

| Score | Criteria |
|---|---|
| 1.0 | NDR-133 scan executed every session; zero false negatives |
| 0.75 | Scan executed; one minor false negative (caught by secondary check) |
| 0.50 | Scan executed but not at session opening |
| 0.0 | NDR-133 scan not executed; OR personal document passed through |

---

### D4 — Coherence Gate Compliance (weight: ×0.15)

| Score | Criteria |
|---|---|
| 1.0 | Coherence gate executed pre-commit; result logged; no unbounded risk passed |
| 0.75 | Gate executed; minor logging gap |
| 0.50 | Gate executed post-commit (late) |
| 0.0 | Coherence gate not executed; OR unbounded risk passed |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.05)

| Score | Criteria |
|---|---|
| 1.0 | All flags, clears, and scans logged in memory |
| 0.5 | Minor logging gap |
| 0.0 | No logging |

---

## Composite Score

```
Sentinel_Phi_score = (D1 × 0.35) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.05)
Threshold for Apogee gate: ≥ 0.75
Critical fail override: D1 = 0.0 → RISK_FLAG mandatory; output blocked
```

---

*Classification: T1 PUBLIC*
