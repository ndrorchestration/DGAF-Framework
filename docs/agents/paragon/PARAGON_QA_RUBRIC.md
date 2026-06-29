# Paragon — QA Rubric v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Audit Coverage (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| No uncommitted output | Zero swarm outputs committed without Paragon audit |
| Benchmark application | Correct benchmark(s) applied to each output type |
| Verdict documentation | Every audit has a documented PASS or HOLD verdict |

**Critical fail:** Swarm output committed without Paragon audit.

### D2 — Gap Identification Accuracy (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Classification accuracy | Every gap correctly classified by type |
| Routing accuracy | Gap routed to correct remediation agent per Gap Routing Table |
| Gap log completeness | All gaps logged in MEMORY.md before remediation routing |

### D3 — Gold Star Threshold Integrity (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Prerequisite evaluation completeness | All Gold Star candidates receive full audit + prerequisite evaluation |
| No premature routing | PREREQUISITE_PASS not issued while quality gaps remain open |
| Evaluation queue currency | MEMORY.md Gold Star queue reflects current state |

### D4 — Benchmark Currency (weight: 0.15)

| Criterion | Pass condition |
|---|---|
| Benchmark review | Benchmarks reviewed at every session open |
| Impact assessment | Benchmark updates assessed for impact on open audits |
| Navigator/Momentum notification | Updated benchmarks communicated within session |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Gold Star evaluations logged | All PREREQUISITE_PASS evaluations referenced in SWEEP_LOG |
| Escalations logged | All Amethyst escalations logged |

---

## Composite Score

```
Paragon QA Score = D1×0.30 + D2×0.25 + D3×0.25 + D4×0.15 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
