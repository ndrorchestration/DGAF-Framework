# Oracle — Integration v1.0

**Agent:** Oracle
**Agent ID:** A-20
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Integration Contracts

### Oracle ↔ Vanguard (peer)
- Vanguard provides technology signals to Oracle for horizon scanning integration
- Oracle provides temporal framing to Vanguard's technology readiness assessments
- Signal exchange is bidirectional and continuous within Quintet sessions

### Oracle → Nova (downstream)
- Oracle routes completed scenario sets to Nova for innovation response generation
- Nova receives: scenario set reference + strategic implication + recommended response
- Nova does not modify Oracle scenario content — generates innovation responses independently

### Oracle → Zenith (downstream)
- Oracle routes completed scenario sets to Zenith for performance optimization response
- Zenith receives: scenario set reference + strategic implication + performance dimension

### Oracle ↔ Sentinel-Phi (parallel gate)
- All Oracle scenario sets submitted to Sentinel-Phi for φ-bounded risk review before commit
- Sentinel-Phi issues RISK_FLAG if any scenario introduces unbounded risk vector (α ≥ 1)
- On RISK_FLAG: Oracle revises scenario or escalates to Amethyst
- Oracle does not commit scenario sets without Sentinel-Phi PASS

### Oracle → Prof Prodigy (verification)
- Oracle submits probability weight distributions to Prof Prodigy for mathematical coherence verification
- Prof Prodigy verifies: weights sum to 1.0; distributions are well-specified; no logical contradictions
- Prof Prodigy issues PASS or FAIL with root cause
- Oracle does not commit probability weights without Prof Prodigy PASS

### Oracle → Apogee (final gate)
- All Oracle outputs pass through Apogee evidence gate before formation commit
- Apogee evaluates: evidence grounding, scenario coherence, gate compliance
- Oracle score threshold: ≥ 0.75 composite (QA Rubric)

### Oracle → Amethyst (escalation)
- Unresolvable temporal conflicts (e.g. RISK_FLAG cannot be resolved within Quintet)
- Persistent temporal myopia or paralysis not corrected by Procedure 4
- Escalation logged in ORACLE_MEMORY.md

---

## NDR-Protocol-01 Position

Oracle is not in the Archive Trio write chain. Oracle outputs are:
1. Reviewed by Sentinel-Phi (risk gate)
2. Verified by Prof Prodigy (probability coherence)
3. Gated by Apogee (evidence gate)
4. Routed to Nova + Zenith (downstream)
5. Archived by The Librarian after Apogee PASS

---

*Classification: T1 PUBLIC*
