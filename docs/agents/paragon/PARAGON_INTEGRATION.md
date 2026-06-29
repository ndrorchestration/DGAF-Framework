# Paragon — Integration v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Paragon ↔ Navigator (route quality)

| Direction | Signal | Trigger |
|---|---|---|
| Paragon → Navigator | Quality gap signal + affected route step | Route/execution path gap identified |
| Navigator → Paragon | Route adjustment (remediation step added) | Gap signal received |
| Paragon → Navigator | Quality clearance | Output passes audit |
| Navigator → Paragon | Route change notification | Contingency activated |

### Paragon ↔ Momentum (quality floor protection)

| Direction | Signal | Trigger |
|---|---|---|
| Momentum → Paragon | Surge notification | Surge detected |
| Paragon → Momentum | Quality floor status (CLEAR or AT_RISK) | Surge notification received |
| Paragon → Momentum | Velocity cap directive | Quality floor at risk from surge |

### Paragon → Prof Prodigy (gap remediation)

| Signal | Condition |
|---|---|
| Gap package (description + benchmark + output) | Mathematical or logical error identified |
| Prof Prodigy → Paragon: CORRECTED or UNRESOLVABLE | Remediation complete |

### Paragon → Lyra (gap remediation)

| Signal | Condition |
|---|---|
| Gap package | Synthesis or narrative incoherence identified |
| Lyra → Paragon: CORRECTED or UNRESOLVABLE | Remediation complete |

### Paragon → Apogee (Gold Star gate)

| Signal | Condition |
|---|---|
| Output + PREREQUISITE_PASS evaluation | Gold Star candidate; all gaps resolved |
| Apogee → Paragon: VERIFIED or HOLD | Evidence gate result |

### Paragon → Reson (harmonic score)

| Signal | Condition |
|---|---|
| Candidate output (via Apogee routing) | Apogee VERIFIED; harmonic score required |
| Reson → Paragon: score value | Score returned |

### Paragon → Amethyst (escalation)

| Signal | Condition |
|---|---|
| Quality escalation package (gap log + audit history + remediation attempts) | Gap unresolvable after remediation |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Remediation agent cannot resolve gap | Escalate to Amethyst with full gap analysis |
| Velocity pressure causes quality floor breach | Immediately cap velocity (Momentum directive); log; escalate to Amethyst |
| Gold Star candidate fails Apogee gate | Return to Paragon; identify evidence gap; re-route to Apogee |
| Gold Star candidate fails Reson score | Return to Paragon; identify harmonic gap; re-route to Reson |

---

*Classification: T1 PUBLIC*
