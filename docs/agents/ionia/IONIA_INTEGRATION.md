# Ionia — Integration Guide

**Agent:** Ionia (A-13)
**Classification:** T2 FRAMEWORK
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Ionia sits at the **end of the Resonance Cluster sequence** — it receives Reson's score and Echolette's amplified signal, then issues the 0Hz lock confirmation that clears Amethyst's harmonic seal gate. Its integrations are tightly sequenced: Reson → Echolette → Ionia → Amethyst.

---

## 2. Integration Matrix

### Primary — Reson (Score Coupling)

| Direction | Content | Protocol |
|---|---|---|
| Reson → Ionia | Harmonic score (≥0.75 required for lock) | Per session |
| Ionia → Reson | Lock withheld notification (if score <0.75) | On withhold |
| **Constraint:** | Reson scores; Ionia locks. No lock without traceable Reson score | Coupling integrity |

---

### Primary — Amethyst (Seal Gate)

| Direction | Content | Protocol |
|---|---|---|
| Ionia → Amethyst | Lock confirmation (IONIA_LOCK_CONFIRMED) | Pre-seal |
| Ionia → Amethyst | Lock failure / lock withheld notification | On failure |
| Amethyst → Ionia | Seal proceed clearance (post lock confirmation) | Post-confirmation |
| **Constraint:** | Amethyst cannot seal harmonic-sensitive commits without Ionia lock confirmation | Seal gate |

---

### Primary — Echolette (Amplification Target)

| Direction | Content | Protocol |
|---|---|---|
| Echolette → Ionia | Amplified signal (Ionia locks the amplified state to 0Hz) | Cluster sequence |
| Ionia → Echolette | Re-stabilization request (on lock failure) | On failure |
| **Constraint:** | Echolette amplifies; Ionia provides the stable 0Hz convergence target | Lane separation |

---

### Lateral — The Auditor (False-Positive Cross-Check)

| Direction | Content | Protocol |
|---|---|---|
| Auditor → Ionia | 1-min constraint verify request | Suspected false-positive |
| Ionia → Auditor | Modal state evidence (Hz reading + Reson score) | Cross-check response |
| **Constraint:** | Auditor's verdict is binding; VERIFIED → seal proceeds; FALSE_POSITIVE → lock failure protocol | Audit authority |

---

### Lateral — Resonance Cluster Quorum

| Direction | Content | Protocol |
|---|---|---|
| Ionia ↔ Cluster | 3/4 quorum participation for cluster-level decisions | Quorum vote |
| **Constraint:** | Ionia holds one quorum vote; cannot unilaterally determine cluster outcome | Quorum integrity |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Reson score ≥0.75 but Ionia cannot reach 0Hz | Lock failure protocol; Resonance Cluster full activation |
| Ionia claims 0Hz; Auditor finds false-positive | Auditor verdict stands; lock failure protocol triggered |
| Amethyst proceeds with seal before Ionia confirmation | Sentinel flags commit; Apogee Q2 evidence integrity fail |
| Ionia lock failure unresolvable in session | Njineer authorizes or blocks seal; seal blocked by default |

---

*Classification: T2 FRAMEWORK*
