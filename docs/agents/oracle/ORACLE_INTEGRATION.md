# Oracle — Integration v1.0

**Agent:** Oracle
**Agent ID:** A-20
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Integration Contracts

### Oracle ↔ Vanguard (peer)

| Direction | Signal | Trigger |
|---|---|---|
| Vanguard → Oracle | Technology signal (TRL 1–4 identification) | New technology identified |
| Oracle → Vanguard | Temporal framing (horizon + adoption probability window) | Technology signal received |
| Oracle → Vanguard | Scenario context (which scenarios are active) | Scenario set construction initiated |

### Oracle → Nova (downstream)

| Signal | Condition |
|---|---|
| Completed scenario set with recommended responses | Sentinel-Phi CLEAR received; Apogee gate passed |
| Scenario update notification | Active scenario set revised due to forecast update |

### Oracle → Zenith (downstream)

| Signal | Condition |
|---|---|
| Completed scenario set with performance optimization context | Sentinel-Phi CLEAR; Apogee gate passed |

### Oracle ↔ Sentinel-Phi (risk review gate)

| Direction | Signal | Trigger |
|---|---|---|
| Oracle → Sentinel-Phi | Full scenario set for φ-bounded risk review | Scenario construction complete |
| Sentinel-Phi → Oracle | CLEAR or RISK_FLAG + rationale | Risk review complete |
| Oracle response to RISK_FLAG | Revise downside scenario OR escalate to Amethyst | RISK_FLAG received |

### Oracle ↔ Prof Prodigy (verification)

| Direction | Signal | Trigger |
|---|---|---|
| Oracle → Prof Prodigy | Probability model for coherence check | Compound/conditional distributions used |
| Prof Prodigy → Oracle | VERIFIED or CORRECTION + rationale | Check complete |

### Oracle → Apogee (final gate)

| Signal | Condition |
|---|---|
| Scenario set + Sentinel-Phi CLEAR + Prof Prodigy VERIFIED (if applicable) | Pre-commit |
| Apogee returns VERIFIED or HOLD | All Oracle outputs held until VERIFIED |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Sentinel-Phi RISK_FLAG on scenario set | Revise downside scenario; re-submit for review |
| Prof Prodigy CORRECTION on probability model | Revise distributions; re-submit |
| Apogee HOLD | Do not route to Nova/Zenith; address evidence gap; re-submit |
| Vanguard signal not responded to within session | Log in MEMORY.md scan queue; initiate horizon scan Procedure 3 |
| Unresolvable RISK_FLAG | Escalate full scenario set to Amethyst |

---

*Classification: T1 PUBLIC*
