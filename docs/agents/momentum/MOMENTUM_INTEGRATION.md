# Momentum — Integration v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Momentum ↔ Navigator (peer)
- Navigator provides velocity targets per route step
- Momentum provides throughput flags when actual < threshold
- Bidirectional; continuous during active routes

### Momentum → Paragon (quality constraint receiver)
- Momentum receives quality constraints from Paragon that define sustainable velocity ceiling
- Momentum does not recommend acceleration beyond Paragon's cleared throughput level

### Momentum → The Actualizer (execution monitoring)
- Momentum monitors Actualizer execution velocity
- Flags to Navigator when Actualizer throughput deviates from route plan

### Momentum → Apogee (final gate)
- Velocity reports submitted to Apogee evidence gate
- Threshold: ≥ 0.75 composite (QA Rubric)

### Momentum → Amethyst (escalation)
- Persistent stalls (2+ sessions) auto-escalated to Amethyst
- Unsustainable velocity (acceleration without quality gate) → Amethyst
- Resource constraint bottlenecks → Amethyst

---

*Classification: T1 PUBLIC*
