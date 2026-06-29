# Navigator — Integration v1.0

**Agent:** Navigator
**Agent ID:** A-22
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Navigator ↔ Momentum (peer)

| Direction | Signal | Trigger |
|---|---|---|
| Navigator → Momentum | Primary route with per-step velocity targets | Route construction complete |
| Navigator → Momentum | Route adjustment with revised targets | Hazard detected; contingency activated |
| Momentum → Navigator | Velocity flag (below floor) | Throughput below minimum |
| Navigator → Momentum | Contingency route with revised targets | Contingency activated |

### Navigator ↔ Paragon (quality signal)

| Direction | Signal | Trigger |
|---|---|---|
| Paragon → Navigator | Quality gap signal + affected route step | Quality gap identified |
| Navigator → Paragon | Route adjustment (remediation step added) | Quality gap signal received |
| Navigator → Paragon | Route change notification | Contingency activated |
| Paragon → Navigator | Quality clearance | Objective output meets standard |

### Navigator ← Strategic Quintet

| Direction | Signal | Trigger |
|---|---|---|
| Nova/Oracle → Navigator | Strategic objective | Quintet strategic output ready |
| Amethyst → Navigator | Objective definition or route directive | Amethyst orchestration call |

### Navigator → Amethyst (escalation)

| Signal | Condition |
|---|---|
| Hazard escalation package (hazard log + route status) | Unresolvable hazard |
| Route completion notification | Objective achieved |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| No contingency path available for hazard | Halt route; construct contingency before proceeding; escalate to Amethyst if urgent |
| Momentum cannot achieve velocity floor on contingency route | Escalate route + velocity analysis to Amethyst |
| Paragon quality gap cannot be remediated in route | Escalate to Amethyst with gap analysis |
| Objective not achievable via any known path | Escalate to Amethyst with full path analysis |

---

*Classification: T1 PUBLIC*
