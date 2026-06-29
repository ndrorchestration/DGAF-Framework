# Zenith — QA Rubric

**Agent:** Zenith (A-09)
**Classification:** T2 FRAMEWORK
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## Evaluation Dimensions

### D-1: Symmetry Accuracy
**Question:** Did Zenith correctly detect all symmetry breaches (≤1/5 threshold per node)?

| Score | Criteria |
|---|---|
| 1.0 | All breaches detected and logged; zero missed |
| 0.7 | One marginal breach detected late but logged |
| 0.4 | One breach missed; detected retrospectively by DemiJoule |
| 0.0 | Multiple breaches undetected; session ran with unacknowledged asymmetry |

---

### D-2: Failover Timeliness
**Question:** Did Zenith trigger GCP failover immediately on node failure?

| Score | Criteria |
|---|---|
| 1.0 | Failover triggered immediately; Amethyst notified in same session step |
| 0.7 | Failover triggered; Amethyst notification delayed one step |
| 0.4 | Failover delayed; session continued with failed node |
| 0.0 | No failover triggered; node failure unacknowledged |

---

### D-3: DemiJoule Alignment
**Question:** Did Zenith’s compute load reports align with DemiJoule’s token spend tracking?

| Score | Criteria |
|---|---|
| 1.0 | Zenith report and DemiJoule spend consistent; no discrepancy |
| 0.7 | Minor discrepancy identified and resolved |
| 0.4 | Discrepancy unresolved for one session |
| 0.0 | Systematic misalignment between Zenith load and DemiJoule spend |

---

### D-4: Silent Compute Debt Detection
**Question:** Did Zenith detect any accumulating compute debt masked by balanced load metrics?

| Score | Criteria |
|---|---|
| 1.0 | Cross-check performed each session; debt detected if present |
| 0.7 | Cross-check performed; minor debt missed then caught next session |
| 0.4 | Cross-check not performed in one session |
| 0.0 | No cross-check performed; compute debt accumulated undetected |

---

### D-5: SWEEP_LOG Completeness
**Question:** Were all symmetry, failover, and escalation events logged?

| Score | Criteria |
|---|---|
| 1.0 | All events logged with required fields |
| 0.7 | One entry missing |
| 0.4 | Multiple entries missing |
| 0.0 | No SWEEP_LOG entries |

---

## Composite Score

```
Composite = (D-1 × 0.30) + (D-2 × 0.25) + (D-3 × 0.20) + (D-4 × 0.15) + (D-5 × 0.10)
Pass threshold: ≥0.80
Critical fail:  D-2 = 0.0 (node failure not acknowledged)
```

---

*Classification: T2 FRAMEWORK*
