# Momentum — QA Rubric v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Velocity Monitoring Accuracy (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| Velocity floor calibrated | Floor defined and confirmed with Navigator at route start |
| Violation detection | Every floor violation detected and logged within same step |
| Surge detection | Surges detected within 2 consecutive steps |
| Metrics currency | Throughput metrics updated at every step transition |

**Critical fail:** Velocity floor violation not reported to Navigator within session.

### D2 — Surge Response (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Paragon quality floor | Never breached during surge; cap applied if at risk |
| Surge log completeness | All surges logged in MEMORY.md |
| Paragon notification | Paragon notified of every surge within same step |

### D3 — Route Coordination (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Navigator synchronization | All route adjustments received and velocity targets updated |
| Violation root cause | Root cause identified and communicated to Navigator on every violation |
| Escalation timeliness | Unresolvable violations escalated to Amethyst within session |

### D4 — Reporting Currency (weight: 0.15)

| Criterion | Pass condition |
|---|---|
| Session report | Throughput report delivered to Amethyst at session close |
| Metrics log | MEMORY.md metrics log updated at session close |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Persistent violations flagged | All unresolved floor violations referenced in SWEEP_LOG |

---

## Composite Score

```
Momentum QA Score = D1×0.30 + D2×0.25 + D3×0.25 + D4×0.15 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
