# Momentum — QA Rubric v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Evaluation Dimensions

### D1 — Throughput Accuracy (weight: ×0.30)

| Score | Criteria |
|---|---|
| 1.0 | Throughput measured per session; actual vs. target reported; deviation calculated |
| 0.75 | Measurement present; minor calculation gap |
| 0.50 | Throughput estimated, not measured |
| 0.25 | Throughput referenced without measurement |
| 0.0 | No throughput tracking |

---

### D2 — Bottleneck Resolution (weight: ×0.25)

| Score | Criteria |
|---|---|
| 1.0 | Bottleneck type correctly classified; resolution routed to correct agent; resolved within 1 session |
| 0.75 | Correctly classified; resolution in progress |
| 0.50 | Bottleneck identified; type classification incorrect; resolution delayed |
| 0.25 | Bottleneck identified; not classified or routed |
| 0.0 | Bottleneck not detected; OR persistent stall not escalated |

**Critical fail:** Persistent stall (2+ sessions) not escalated to Amethyst → D2 = 0.0.

---

### D3 — Acceleration Model Quality (weight: ×0.20)

| Score | Criteria |
|---|---|
| 1.0 | Acceleration modeled with quality gate confirmation; sustainable rate identified |
| 0.75 | Acceleration modeled; minor quality confirmation gap |
| 0.50 | Acceleration proposed without modeling |
| 0.0 | Acceleration recommended without quality gate check |

---

### D4 — Swarm Synchronization (weight: ×0.15)

| Score | Criteria |
|---|---|
| 1.0 | Coordination pulse issued every session; Navigator velocity targets current |
| 0.75 | Pulse issued; minor target staleness |
| 0.50 | Pulse issued but incomplete |
| 0.0 | No coordination pulse |

---

### D5 — SWEEP_LOG Compliance (weight: ×0.10)

| Score | Criteria |
|---|---|
| 1.0 | All velocity records, bottlenecks, and stalls logged |
| 0.5 | Minor logging gap |
| 0.0 | No logging |

---

## Composite Score

```
Momentum_score = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
Threshold: ≥ 0.75
Critical fail: D2 = 0.0 (persistent stall not escalated) → output blocked
```

---

*Classification: T1 PUBLIC*
