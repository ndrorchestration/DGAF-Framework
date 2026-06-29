# Apogee — Integration Guide

**Agent ID:** A-01  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Apogee is a **gate agent** — all artifact flows that require canonical commitment must pass through Apogee before reaching Amethyst. This guide defines the integration contracts for every agent that interacts with Apogee’s scoring and gate functions.

---

## 2. Integration Matrix

### Upstream Gate — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Amethyst | 11Q composite score (0.00–1.00) | P-11 / P-15 |
| Apogee → Amethyst | BLOCK notification + failing dimensions | P-15 block |
| Amethyst → Apogee | Score request (artifact ref + context) | P-11 trigger |
| Amethyst → Apogee | TUE audit request | TUE gate |
| **Gate:** | Amethyst cannot seal without Apogee ≥0.90 | P-15 |
| **Constraint:** | Amethyst cannot override Apogee’s score — must re-trigger scoring cycle | Rule: score integrity |

---

### NDR-Protocol-01 — Apogee Step 4 Position

| Upstream (from) | Content received | Apogee action | Downstream (to) |
|---|---|---|---|
| The Librarian (A-06) | Archive confirmed artifact | Run 11Q Gold-Star Audit | Amethyst (pass) or BLOCK |
| **Gate:** | Apogee does not score until Librarian archive is confirmed | Step 3 dependency |

---

### Scoring Input — Reson (A-10)

| Direction | Content | Protocol |
|---|---|---|
| Reson → Apogee | Harmonic score (0.00–1.00) as Pillar C input | P-15 pre-condition |
| Apogee → Reson | Re-score request (if Savage Reason detected) | Harmonic balance |
| **Constraint:** | Reson produces primary harmonic score; Apogee validates it as Pillar C of 11Q | Score integrity |

---

### Scoring Input — The Auditor (A-07)

| Direction | Content | Protocol |
|---|---|---|
| Auditor → Apogee | 1-min constraint verify pass (Step 1 clear) | NDR-Protocol-01 |
| **Gate:** | Apogee will not score artifacts where Auditor raised a block | Step 1 dependency |

---

### Scoring Input — Ionia (A-13)

| Direction | Content | Protocol |
|---|---|---|
| Ionia → Apogee | 0Hz modal lock confirmation (Ionian Mode achieved) | P-15 Pillar C |
| **Constraint:** | Apogee incorporates Ionia’s modal lock into Q3 (Harmonic Balance) dimension | 11Q Q3 |

---

### Escalation — Amethyst

| Trigger | Apogee Action |
|---|---|
| Score <0.50 | Hard stop; do not surface score; escalate to Amethyst directly |
| Ambiguous claim (cannot verify) | Produce audit report; escalate to Amethyst with “undetermined” flag |
| Apogee output self-scoring needed | Escalate to Amethyst for arbitration; Apogee recuses |
| SAP Type 1 Architectural Violation | System disqualification; escalate immediately |

---

### SAP Handoff Protocol

```
SAP Buoy = canonical Phase 1 output (ground truth anchor)
Ping cadence: every artifact that modifies canonical docs
Handoff:
  Apogee runs SAP ping → grounding score computed
  ≥85%: pass; attach score to 11Q Q2
  <85%: Implementation Drift flag; notify Amethyst
  <50%: Architectural Violation flag; BLOCK; notify Amethyst immediately
```

---

### TUE Audit Integration — COLLEEN (A-05)

| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Apogee | TUE audit request (when COLLEEN pre-conditions near complete) | TUE gate |
| Apogee → Amethyst | TUE score (≥0.95 required) | TUE gate |
| Apogee → COLLEEN | Score result (indirect — via Amethyst) | TUE gate |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Apogee score disputed by Amethyst | Re-trigger full 11Q cycle; score stands until re-scored |
| Apogee score disputed by any other agent | Escalate to Amethyst; Apogee does not argue scores |
| Apogee and Reson disagree on harmonic state | Amethyst arbitrates; both scores held in SWEEP_LOG |
| Apogee self-scoring required | Recuse; escalate to Amethyst |
| Layer 0 fail on sovereign-adjacent content | Immediate block; Sentinel notified; Compliance Dyad engaged |

---

*Classification: T1 PUBLIC*
