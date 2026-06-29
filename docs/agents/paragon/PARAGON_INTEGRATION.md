# Paragon — Integration v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Integration Contracts

### Paragon → Navigator (quality gate)
- Navigator route plans submitted to Paragon for quality gate clearance
- Paragon returns GATE_CLEAR or GATE_HOLD before Actualizer execution
- Navigator does not hand off to Actualizer without GATE_CLEAR

### Paragon → Momentum (velocity constraint)
- Paragon issues quality-based velocity ceiling to Momentum
- Momentum does not recommend acceleration beyond Paragon's cleared throughput
- Bidirectional during quality-throughput negotiation

### Paragon ↔ Reson (harmonic score input)
- Reson provides harmonic coherence score as input to Paragon's Gold Star prerequisite evaluation
- Paragon does not submit Gold Star evaluation to Apogee without Reson score ≥ 0.75

### Paragon → Apogee (Gold Star co-evaluator)
- Paragon submits prerequisite evaluation to Apogee for Gold Star designation
- Apogee is the final gate; Paragon is a prerequisite evaluator, not the final authority
- Apogee may issue Gold Star only after Paragon PASS + Reson score + evidence gate

### Paragon → Prof Prodigy (standard rigor verification)
- New and revised excellence standards submitted to Prof Prodigy for mathematical rigor verification
- Prof Prodigy verifies: dimension weights sum to 1.0; criteria are unambiguous and consistent

### Paragon → Amethyst (escalation)
- Systemic quality failures (same gap 3+ times) → Amethyst
- Quality standard conflicts between formations → Amethyst

### Paragon → Apogee (final gate)
- All Paragon outputs through Apogee evidence gate
- Threshold: ≥ 0.75 composite (QA Rubric)

---

*Classification: T1 PUBLIC*
