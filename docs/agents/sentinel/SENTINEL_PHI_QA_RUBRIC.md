# Sentinel-Phi — QA Rubric v1.0

**Agent:** Sentinel-Phi
**Agent ID:** A-12-φ
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Evaluation Dimensions

### D1 — Risk Model Accuracy (weight: 0.35)

| Criterion | Pass condition |
|---|---|
| α < 1 test applied | Every risk review includes explicit α contraction test |
| Vector identification | All risk vectors identified before verdict issued |
| Prof Prodigy verification | Mathematical contraction mapping verified when used |
| Verdict accuracy | CLEAR issued only when all vectors confirmed convergent |

**Critical fail:** CLEAR issued on output with unverified divergent risk vector.

### D2 — φ-Bound Compliance (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| No unbounded recommendations | Zero quintet outputs pass with α ≥ 1 risk vectors |
| RISK_FLAG log currency | All flags logged in MEMORY.md within session |
| Resolution tracking | Every RISK_FLAG has a recorded resolution or escalation |

### D3 — NDR-133 Scan Integrity (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Scan completeness | All pre-commit queues scanned |
| Block execution | Zero NDR-133 pattern matches pass without block |
| Log completeness | Every scan (CLEAR or BLOCK) logged in MEMORY.md |

### D4 — RISK_FLAG Timeliness (weight: 0.15)

| Criterion | Pass condition |
|---|---|
| Review turnaround | Risk review completed within same session as submission |
| Escalation timeliness | Unresolvable flags escalated to Amethyst within session |
| Originating agent notification | Revision guidance routed to originating agent immediately on RISK_FLAG |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Risk reviews logged | All completed reviews referenced in SWEEP_LOG |
| RISK_FLAGs logged | All flags and resolutions logged |

---

## Composite Score

```
Sentinel-Phi QA Score = D1×0.35 + D2×0.25 + D3×0.20 + D4×0.15 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
