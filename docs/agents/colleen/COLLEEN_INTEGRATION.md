# COLLEEN — Integration Guide

**Agent ID:** A-05  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

This document defines COLLEEN's integration contracts with every agent in the 20-agent taxonomy. COLLEEN is a hub agent — it interfaces upstream with Amethyst, downstream with the four Swarm members, and laterally with Sentinel (Dyad), Reson (harmonic gate), and Herald (relay).

---

## 2. Integration Matrix

### Upstream — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Amethyst | BLG queue (session open) | P-02 |
| COLLEEN → Amethyst | GAP surfaces (all classes) | GAP taxonomy |
| COLLEEN → Amethyst | TUE signal (when L5 conditions met) | TUE gate |
| COLLEEN → Amethyst | NDR-Protocol-01 Step 3 archive confirm | NDR-Protocol-01 |
| Amethyst → COLLEEN | Session open instruction | P-02 |
| Amethyst → COLLEEN | Normative decisions on surfaces | Rule 3 |
| Amethyst → COLLEEN | Swarm task routing instructions | Amethyst normative |
| **Constraint:** | COLLEEN never decides — only surfaces to Amethyst | Rule 3 |

---

### Swarm — The Librarian (A-06)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Librarian | Archive task assignment | NDR-Protocol-01 Step 3 |
| Librarian → COLLEEN | Archive confirmation + provenance entry ref | Step 3 confirm |
| **Gate:** | COLLEEN confirms archive is coherent with trunk before routing to Apogee | Step 3 |

---

### Swarm — The Auditor (A-07)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Auditor | Initiate constraint verify cycle | NDR-Protocol-01 Step 1 |
| Auditor → COLLEEN | Pass / BLOCK result | Step 1 |
| **Gate:** | COLLEEN cannot route to Actualizer until Auditor passes | NDR-Protocol-01 |
| **Conflict:** | COLLEEN cannot override Auditor block — escalate to Amethyst | Rule 3 |

---

### Swarm — The Actualizer (A-08)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Actualizer | Execution task (post Auditor pass only) | NDR-Protocol-01 Step 2 |
| Actualizer → COLLEEN | Artifact delivery confirmation | Step 2 output |
| **Constraint:** | COLLEEN must not route to Actualizer without Auditor clearance | NDR-Protocol-01 |

---

### Swarm — Zenith (A-09)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Zenith | System state query (load, symmetry) | Swarm coordination |
| Zenith → COLLEEN | System High alert (if imbalance) | Escalation |
| **Route:** | COLLEEN escalates Zenith alerts to Amethyst — does not authorize pause unilaterally | Rule 3 |

---

### Lateral — Sentinel

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN ↔ Sentinel | Compliance Dyad co-signal | Dyad veto |
| **Gate:** | Dyad veto requires both COLLEEN + Sentinel co-signal; overrides all formations | Compliance Dyad |
| **Constraint:** | COLLEEN cannot invoke Dyad unilaterally — Sentinel co-signal required | Dyad rules |

---

### Lateral — Apogee (A-01)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Apogee | Route artifact for scoring (post Step 3) | NDR-Protocol-01 Step 4 |
| Apogee → COLLEEN | Score result (pass to Amethyst for seal) | P-11 / P-15 |
| **Constraint:** | COLLEEN does not interpret the score — routes to Amethyst | Rule 3 |

---

### Lateral — Herald

| Direction | Content | Protocol |
|---|---|---|
| Amethyst → COLLEEN → Herald | State confirmation before relay | Herald Relay activation |
| **Constraint:** | COLLEEN confirms T1 classification of relay content before Herald receives it; strips T2/T3 markers | NDR-133 |

---

### Nova Gate (A-03)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Amethyst | TUE signal (L5 Executor achieved) | TUE gate |
| Amethyst → Nova | Activation (post COLLEEN TUE signal) | Amethyst normative |
| **Constraint:** | COLLEEN never directly activates Nova — signals Amethyst who executes | TUE gate |

---

## 3. BLG Handoff Matrix

| BLG Class | COLLEEN Action | Routed To | Closed By |
|---|---|---|---|
| BLOCKING | Immediate surface; halt non-critical writes | Amethyst | Amethyst (pre-TUE) / COLLEEN (post-TUE) |
| NON-BLOCKING | Surface at next session open | Amethyst | Amethyst (pre-TUE) |
| GAP-04 (protocol break) | Immediate surface + Auditor engage | Amethyst + Auditor | Amethyst |
| GAP-05 (taxonomy drift) | Hard stop; cite ROSTER | Amethyst | Amethyst |
| GAP-06 (sovereign breach) | NDR-133; Sentinel notified | Amethyst + Sentinel | Compliance Dyad |
| GAP-08 (Ceremonialization) | Proof-of-action request | Agent that claimed completion | Amethyst confirms |

---

## 4. Conflict Resolution

| Conflict | Resolution |
|---|---|
| COLLEEN surface vs. Amethyst decision conflict | Amethyst decides — COLLEEN defers (Rule 3) |
| COLLEEN Dyad veto vs. Amethyst commit | Dyad wins — Njineer resolves |
| Auditor block vs. COLLEEN routing | Auditor wins — COLLEEN escalates to Amethyst |
| Swarm member refuses COLLEEN direction | COLLEEN surfaces to Amethyst; Amethyst arbitrates |
| TUE conditions disputed | Amethyst re-verifies all 7 pre-conditions; COLLEEN surfaces evidence |

---

*Classification: T1 PUBLIC*
