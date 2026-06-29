# Vanguard — Integration v1.0

**Agent:** Vanguard
**Agent ID:** A-21
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Integration Contracts

### Vanguard ↔ Oracle (peer)

| Direction | Signal | Trigger |
|---|---|---|
| Vanguard → Oracle | Technology signal (name, TRL, strategic fit, first-mover window estimate) | New technology identified |
| Oracle → Vanguard | Temporal framing (horizon assignment + adoption probability window) | Technology signal received |
| Oracle → Vanguard | Active scenario set context | Scenario construction initiated |

### Vanguard → Nova (downstream)

| Signal | Condition |
|---|---|
| Full technology readiness assessment | TRL 5+; Sentinel-Phi CLEAR; Apogee gate passed |
| First-mover window alert | Window < near-term horizon; urgent disruption opportunity |

### Vanguard ↔ Sentinel-Phi (risk gate)

| Direction | Signal | Trigger |
|---|---|---|
| Vanguard → Sentinel-Phi | Technology assessment for φ-bounded risk review | Assessment complete |
| Sentinel-Phi → Vanguard | CLEAR or RISK_FLAG + rationale | Risk review complete |
| Vanguard response to RISK_FLAG | Revise assessment risk profile OR escalate to Amethyst | RISK_FLAG received |

### Vanguard → Zenith (downstream)

| Signal | Condition |
|---|---|
| Technology assessment with performance optimization application | Sentinel-Phi CLEAR; Apogee gate passed |

### Vanguard ↔ Prof Prodigy (verification)

| Direction | Signal | Trigger |
|---|---|---|
| Vanguard → Prof Prodigy | Adoption curve model for mathematical verification | Model involves compound/conditional relationships |
| Prof Prodigy → Vanguard | VERIFIED or CORRECTION | Verification complete |

### Vanguard → Apogee (final gate)

| Signal | Condition |
|---|---|
| Full assessment + Sentinel-Phi CLEAR + Prof Prodigy VERIFIED (if applicable) | Pre-commit |
| Apogee HOLD | Assessment held; evidence gap addressed; re-submitted |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Sentinel-Phi RISK_FLAG | Revise risk profile; re-submit |
| Prof Prodigy CORRECTION | Revise adoption curve model; re-submit |
| Apogee HOLD | Do not route to Nova/Zenith; address gap; re-submit |
| First-mover window < near-term | Immediate flag to Amethyst; expedite assessment |
| Oracle temporal framing not received within session | Proceed with default horizon estimates; note in MEMORY.md |

---

*Classification: T1 PUBLIC*
