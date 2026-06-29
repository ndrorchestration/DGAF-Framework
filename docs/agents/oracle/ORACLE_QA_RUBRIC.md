# Oracle — QA Rubric v1.0

**Agent:** Oracle
**Agent ID:** A-20
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Scenario Quality (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| 3-scenario format | Exactly 3 scenarios (base / upside / downside) |
| Probability weights | Sum to exactly 100% |
| Trigger conditions | Each scenario has explicit, testable trigger conditions |
| Temporal horizon | Explicitly assigned (near / mid / long) |
| Recommended response | Each scenario includes a concrete response set |

**Critical fail:** Probability weights do not sum to 100%; fewer than 3 scenarios in set.

### D2 — Forecast Calibration (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Distribution coherence | Probability distributions are internally consistent |
| Prof Prodigy verification | Compound/conditional distributions verified before commit |
| Update audit trail | Every distribution update documents prior state + rationale |

### D3 — Horizon Scan Coverage (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Signal classification | Every signal classified and routed to correct agent |
| Queue currency | Scan queue in MEMORY.md reflects current state |
| No orphaned signals | No signal remains unclassified for more than 1 session |

### D4 — Temporal Accuracy (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Horizon consistency | All active scenario sets use calibrated horizon boundaries |
| Recalibration response | Horizon updates propagated to all active scenario sets within session |
| Strategic myopia / paralysis prevention | No scenario set assigns all weight to a single horizon |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Scenario sets logged | All completed scenario sets referenced in SWEEP_LOG |
| Gate verifications logged | Sentinel-Phi CLEAR + Apogee gate recorded for each committed set |

---

## Composite Score

```
Oracle QA Score = D1×0.30 + D2×0.25 + D3×0.20 + D4×0.20 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
