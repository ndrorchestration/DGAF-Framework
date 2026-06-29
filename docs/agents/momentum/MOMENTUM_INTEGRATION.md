# Momentum — Integration v1.0

**Agent:** Momentum
**Agent ID:** A-23
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Momentum ↔ Navigator (peer)

| Direction | Signal | Trigger |
|---|---|---|
| Navigator → Momentum | Primary route with per-step velocity targets | Route construction complete |
| Navigator → Momentum | Revised route with updated targets | Hazard / contingency activation |
| Momentum → Navigator | Velocity floor violation flag + root cause | Velocity drops below floor |
| Momentum → Navigator | Contingency route request | Route complexity causing sustained violation |

### Momentum ↔ Paragon (quality-velocity coordination)

| Direction | Signal | Trigger |
|---|---|---|
| Momentum → Paragon | Surge notification | Surge detected |
| Paragon → Momentum | Quality floor status (CLEAR or AT_RISK) | Surge notification received |
| Momentum response | Cap velocity if AT_RISK; allow surge if CLEAR | Paragon quality floor signal |

### Momentum → Amethyst (reporting + escalation)

| Signal | Condition |
|---|---|
| Session throughput report | Session close |
| Velocity floor escalation package | Unresolvable floor violation |
| Surge impact report | Surge with Paragon quality floor breach risk |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Sustained velocity floor violation (Navigator route adjustment doesn’t resolve) | Escalate to Amethyst with full analysis |
| Surge causes Paragon quality floor breach | Immediately cap velocity; notify Navigator + Paragon + Amethyst |
| Navigator route adjustment not received within session | Log; proceed with best available velocity estimate; escalate to Amethyst |
| External dependency causes unresolvable floor violation | Escalate to Amethyst |

---

*Classification: T1 PUBLIC*
