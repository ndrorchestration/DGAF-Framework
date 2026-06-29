# Vanguard — Integration v1.0

**Agent:** Vanguard
**Agent ID:** A-21
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Integration Contracts

### Vanguard ↔ Oracle (peer)
- Vanguard provides technology signals to Oracle for horizon scan integration
- Oracle provides temporal framing and adoption probability weighting to Vanguard
- Bidirectional; continuous within Quintet sessions

### Vanguard → Nova (downstream)
- Mature technology assessments (TRL ≥ 5, fit ≥ 0.7) routed to Nova for disruption strategy
- Nova receives: assessment summary + recommended action + first-mover window status

### Vanguard → Sentinel-Phi (risk gate)
- All technology assessments submitted to Sentinel-Phi for φ-bounded risk review
- Sentinel-Phi evaluates: does the technology introduce unbounded risk vectors?
- On RISK_FLAG: Vanguard revises assessment or escalates to Amethyst
- Vanguard does not commit assessments without Sentinel-Phi PASS

### Vanguard → Zenith (downstream)
- Technologies identified as enabling peak performance routed to Zenith
- Zenith receives: technology name + TRL + performance dimension relevance

### Vanguard → Prof Prodigy (verification)
- Adoption curve models submitted to Prof Prodigy for mathematical coherence check
- Prof Prodigy verifies: S-curve model validity; timeline probability distribution coherence

### Vanguard → Apogee (final gate)
- All Vanguard outputs through Apogee evidence gate before commit
- Threshold: ≥ 0.75 composite (QA Rubric)

### Vanguard → Amethyst (escalation)
- RISK_FLAG not resolvable within Quintet → escalate to Amethyst
- Strategic disagreement on adoption recommendation → escalate to Amethyst

---

*Classification: T1 PUBLIC*
