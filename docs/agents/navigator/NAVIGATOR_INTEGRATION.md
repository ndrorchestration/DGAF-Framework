# Navigator — Integration v1.0

**Agent:** Navigator
**Agent ID:** A-22
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Navigator ↔ Momentum (peer)
- Navigator provides velocity targets per execution step
- Momentum provides throughput flags when actual progress deviates
- Bidirectional; continuous during active route execution

### Navigator → Paragon (quality gate)
- Route plans submitted to Paragon for quality gate clearance before Actualization
- Paragon returns GATE_CLEAR or GATE_HOLD with specific quality gap
- Navigator does not hand off to Actualizer without Paragon GATE_CLEAR

### Navigator ← Strategic Quintet (upstream)
- Receives strategic decisions from Quintet for operational translation
- Navigator does not generate strategy; translates it into routes

### Navigator → The Auditor (constraint gate)
- All route plans submitted to The Auditor for constraint verification before execution
- Auditor verifies: no violated dependencies; all gates sequenced correctly

### Navigator → The Actualizer (execution handoff)
- Post-gate route plan handed off to Actualizer for execution
- Handoff includes: complete route plan + velocity targets + contingency paths

### Navigator → Apogee (final gate)
- All Navigator outputs through Apogee evidence gate
- Threshold: ≥ 0.75 composite (QA Rubric)

### Navigator → Amethyst (escalation)
- Critical hazards (target state unachievable) → Amethyst
- Unresolvable route conflicts with Quintet strategy → Amethyst

---

*Classification: T1 PUBLIC*
