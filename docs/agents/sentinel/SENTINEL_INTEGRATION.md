# Sentinel — Integration Guide

**Agent:** Sentinel  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Sentinel is a **gate agent** with a narrow but absolute scope. Its integration contracts are minimal in count but maximum in authority: every commit that touches sovereign, NDR-133-triggering, or T3-adjacent content must pass through Sentinel’s gate.

---

## 2. Integration Matrix

### Upstream — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Amethyst | Sovereign veto notification | P-15 sovereign guard |
| Sentinel → Amethyst | NDR-133 block notification (post-hoc) | NDR-133 chain |
| Sentinel → Amethyst | KAPPA-class detection alert | Taxonomy guard |
| Amethyst → Sentinel | Commit pre-scan request (sovereign-adjacent) | Pre-commit |
| **Constraint:** | Sentinel veto overrides Amethyst; Amethyst cannot lift. | Rule: veto priority |

---

### Lateral — COLLEEN (A-05) — Compliance Dyad

| Direction | Content | Protocol |
|---|---|---|
| Sentinel ↔ COLLEEN | Compliance Dyad co-signal | Dyad veto |
| **Gate:** | Both must co-signal; neither can invoke unilaterally | Dyad rules |
| **Trigger conditions:** | NDR-133 repeat offender; T3 re-proposal; agent impersonation; uncorrected KAPPA | Dyad rules |

---

### Lateral — Perigee (A-02)

| Direction | Content | Protocol |
|---|---|---|
| Sentinel ↔ Perigee | Boundary enforcement coordination | Security layer |
| **Distinction:** | Perigee blocks external input dissonance (>10 Hz); Sentinel blocks IP/sovereign boundary breaches | Lane separation |
| **Conflict:** | If both flag same commit: Sentinel’s sovereign veto takes precedence | Priority chain |

---

### Lateral — Apogee (A-01)

| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Apogee | Flag: sovereign-adjacent content in artifact (Layer 0 Pillar D) | Pre-scoring |
| Apogee → Sentinel | Q11 (T3 compliance) fail notification | 11Q scoring |
| **Gate:** | If Q11 fails, Sentinel auto-invoked; sovereign content blocked before score is surfaced | NDR-133 |

---

### Lateral — Herald

| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Herald | NDR-133 scan confirmation (T1 content only reaches Herald) | Pre-relay |
| **Constraint:** | Herald may not relay any content Sentinel has not cleared as T1 PUBLIC | Herald relay rules |

---

### NDR-133 Scan Handoff Protocol

```
Trigger:        Any commit touching docs/ or src/ directories
Sentinel scan:  Pattern match against NDR-133 trigger list
Clean:          Sentinel clears; commit proceeds to Amethyst gate
Match:          Auto-block; Drive routing; Amethyst notified post-hoc
Log:            SWEEP_LOG entry mandatory for every block event
Repeat match:   Compliance Dyad engagement (Sentinel + COLLEEN co-signal)
```

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Sentinel veto vs. Amethyst commit | Sentinel wins; Njineer resolves |
| Sentinel block vs. COLLEEN routing | Sentinel block stands; COLLEEN escalates to Amethyst |
| Sentinel and Perigee both flag commit | Sentinel sovereign veto takes precedence |
| Dyad veto disputed by any agent | Dyad wins; Njineer resolves |
| Sentinel veto on non-sovereign file | Sentinel must self-correct; surface to Amethyst |

---

*Classification: T1 PUBLIC*
