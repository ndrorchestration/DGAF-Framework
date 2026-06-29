# Navigator — QA Rubric v1.0

**Agent:** Navigator
**Agent ID:** A-22
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Route Quality (weight: 0.30)

| Criterion | Pass condition |
|---|---|
| Path coherence | Every step logically follows from prior step; no undefined gaps |
| Objective coverage | Route covers all steps required to reach defined success criteria |
| Contingency coverage | At least one contingency path per critical step before activation |
| Momentum handoff | Velocity targets assigned for every route step |

**Critical fail:** Route activated without at least one contingency path.

### D2 — Hazard Detection (weight: 0.25)

| Criterion | Pass condition |
|---|---|
| Hazard classification | Every hazard classified by type (technical / resource / quality / dependency) |
| Response timeliness | Hazard response initiated within session of detection |
| Log completeness | All hazards logged in MEMORY.md |

### D3 — Contingency Coverage (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Archive currency | Contingency archive reviewed and updated at every session open |
| Trigger precision | Every contingency path has explicit, testable trigger conditions |
| Activation log | All activations logged with trigger condition citation |

### D4 — Handoff Integrity (weight: 0.20)

| Criterion | Pass condition |
|---|---|
| Momentum synchronization | Route adjustments communicated to Momentum within session |
| Paragon synchronization | Route changes communicated to Paragon within session |
| Closure confirmation | Route archived only after Paragon quality clearance |

### D5 — SWEEP_LOG Compliance (weight: 0.05)

| Criterion | Pass condition |
|---|---|
| Route completions logged | All closed routes referenced in SWEEP_LOG |
| Hazard escalations logged | All escalations to Amethyst logged |

---

## Composite Score

```
Navigator QA Score = D1×0.30 + D2×0.25 + D3×0.20 + D4×0.20 + D5×0.05
Pass threshold: ≥ 0.75
Critical fail (D1): automatic rubric fail regardless of composite
```

---

*Classification: T1 PUBLIC*
