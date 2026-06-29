# Vanguard — QA Rubric v1.0

**Agent:** Vanguard
**Agent ID:** A-21
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Technology Identification Accuracy (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| TRL classification | Every pipeline item has explicit TRL 1–9 assignment with cited evidence |
| Signal source | Identification source documented for each technology |
| Strategic fit | High / medium / low assignment with rationale |
| Adoption timeline | Near / mid / long horizon assigned and Oracle-confirmed |

**Critical fail:** TRL unassigned on committed pipeline item.

### D2 — Readiness Assessment Quality (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Four-dimension coverage | All assessments cover maturity, strategic fit, risk profile, timeline |
| Sentinel-Phi gate | No assessment routed to Nova without Sentinel-Phi CLEAR |
| Prof Prodigy verification | Adoption curve models verified before commit |

### D3 — First-Mover Window Modeling (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Window calculation | Emergence point and adoption threshold explicitly defined |
| Oracle integration | Window estimate routed to Oracle for scenario weighting |
| Urgent flag | Windows < near-term horizon flagged to Amethyst within session |

### D4 — Pipeline Integrity (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Pipeline currency | Pipeline reviewed and updated at every session open |
| No orphaned items | No item remains at same TRL for 3+ sessions without update rationale |
| Archive completeness | All completed assessments logged in MEMORY.md archive |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Assessments logged | All committed assessments referenced in SWEEP_LOG |
| Gate verifications logged | Sentinel-Phi CLEAR + Apogee gate recorded |

---

## Composite Score

```
Vanguard QA Score = D1×0.30 + D2×0.25 + D3×0.20 + D4×0.20 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
