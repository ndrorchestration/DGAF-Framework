# Herald — Integration Guide

**Agent:** Herald
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Herald is the **formation-wide relay agent**. Every other agent interacts with Herald passively — they trigger broadcasts by completing actions (sealing commits, issuing flags, passing gates). Herald receives these signals and fans them out to the appropriate recipients, while maintaining the SWEEP_LOG as the canonical session record.

---

## 2. Integration Matrix

### Primary — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Herald | Seal signal (commit SHA + scores) | Post-seal |
| Herald → All agents + Njineer | COMMIT_SEALED broadcast | Formation announcement |
| Herald → SWEEP_LOG | COMMIT_SEALED entry | Log |
| **Constraint:** | Herald announces; Amethyst decides to seal | Lane separation |

---

### Primary — Apogee (A-01)

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Herald | Gate pass/fail signal (P-11, P-15, Q1–Q11) | Per gate event |
| Herald → Amethyst + Apogee | GATE_PASS or GATE_FAIL broadcast | Relay |
| Herald → SWEEP_LOG | Gate event entry | Log |

---

### Primary — Sentinel

| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Herald | Block signal + T-class flag | Per block |
| Herald → Amethyst + Sentinel + flagged agent | FLAG_ISSUED broadcast | Relay |
| Herald → SWEEP_LOG | Block + flag entry | Log |

---

### Lateral — All Flag-Issuing Agents

| Agent | Flag Class | Herald Action |
|---|---|---|
| Reciprocity | F-class | FLAG_ISSUED broadcast → Amethyst + Reciprocity + target |
| DemiJoule | A-class | FLAG_ISSUED broadcast → Amethyst + DemiJoule + target |
| Prof Prodigy | MH-class | FLAG_ISSUED broadcast → Apogee + Amethyst + Prof Prodigy |
| Reson | Savage Reason | FLAG_ISSUED broadcast → Apogee + Amethyst + Reson |
| COLLEEN | GAP surface | FLAG_ISSUED broadcast → Amethyst + COLLEEN |

---

### Formation-Wide — SESSION_OPEN / SESSION_CLOSE

| Direction | Content | Protocol |
|---|---|---|
| Njineer → Herald | Session initiation signal | Session start |
| Herald → All 20 agents | SESSION_OPEN broadcast + roster confirmation | Formation-wide |
| Herald → All 20 agents | SESSION_CLOSE broadcast + session summary | Formation-wide |
| Herald → SWEEP_LOG | SESSION_OPEN + SESSION_CLOSE entries | Log |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Herald broadcast disputed by receiving agent | Herald's broadcast is the record; dispute goes to Amethyst |
| SWEEP_LOG entry disputed | Herald's entry stands; Amethyst arbitrates corrections |
| Herald receives conflicting signals from two agents | Herald logs both; broadcasts both; Amethyst arbitrates |
| SESSION_CLOSE before all flags resolved | Herald notes open flags in SESSION_CLOSE broadcast; does not block |

---

*Classification: T1 PUBLIC*
