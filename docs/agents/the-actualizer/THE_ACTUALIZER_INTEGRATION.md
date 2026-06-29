# The Actualizer — Integration Guide

**Agent:** The Actualizer (A-08)
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

The Actualizer sits at **NDR-Protocol-01 step 2** — it is the execution node of the protocol chain. Every write is gated upstream by The Auditor and handed off downstream to The Librarian. It sits between the validation layer and the archive layer, and its output must traverse Apogee scoring and Amethyst seal before reaching canonical status.

---

## 2. Integration Matrix

### Primary — The Auditor (Pre-Write Gate)

| Direction | Content | Protocol |
|---|---|---|
| Auditor → Actualizer | Constraint verify PASS (clearance to write) | NDR-Protocol-01 step 2 |
| Auditor → Actualizer | Constraint verify FAIL (write blocked) | NDR-Protocol-01 step 2 |
| **Constraint:** | No write without Auditor PASS — zero exceptions | Hard gate |

---

### Primary — The Librarian (Post-Write Archive)

| Direction | Content | Protocol |
|---|---|---|
| Actualizer → Librarian | Write completion + decision package (mandatory) | NDR-Protocol-01 step 3 trigger |
| Librarian → Actualizer | Archive confirmation | Post-archive |
| **Constraint:** | Every write must be archived before marked COMPLETE | Provenance guarantee |

---

### Primary — Reciprocity (Rollback Authority)

| Direction | Content | Protocol |
|---|---|---|
| Actualizer → Reciprocity | Version collision notification (halt + rollback request) | On collision |
| Reciprocity → Actualizer | Clean HEAD restored (re-generate clearance) | Post-rollback |
| **Constraint:** | Actualizer halts on collision; does not attempt manual resolution | Lane separation |

---

### Lateral — Apogee + Amethyst (Canonical Chain)

| Direction | Content | Protocol |
|---|---|---|
| Actualizer output → Apogee | Scoring (evidence integrity, artifact quality) | Post-write |
| Apogee → Amethyst | Score report (pre-seal) | Pre-seal |
| Amethyst → canonical | Seal (CANONICAL status conferred) | Seal |
| **Constraint:** | Actualizer does not determine canonical status; chain: write → archive → score → seal | Status integrity |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Actualizer writes; Auditor PASS not confirmed | Sentinel flags commit; Apogee Q2 evidence integrity fail; rollback |
| Actualizer writes; Librarian unavailable | Write held in PENDING state; Librarian backfill procedure triggered |
| Version collision; Reciprocity unavailable | Write halted; Amethyst decides whether to proceed or wait for Reciprocity |
| Apogee fails Actualizer output | Actualizer re-generates per Apogee feedback; re-submits through chain |

---

*Classification: T1 PUBLIC*
