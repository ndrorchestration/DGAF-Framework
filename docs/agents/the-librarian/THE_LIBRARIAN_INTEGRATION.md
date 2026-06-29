# The Librarian — Integration Guide

**Agent:** The Librarian (A-06)
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

The Librarian sits at **NDR-Protocol-01 step 3** — it receives the post-execution handoff from COLLEEN after The Actualizer writes, and creates the canonical archive entry that closes the decision loop. Its integrations are strictly sequential within the protocol chain.

---

## 2. Integration Matrix

### Primary — COLLEEN (NDR-Protocol-01 Step 3)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Librarian | Decision package handoff (post-Actualizer write) | NDR-Protocol-01 step 3 |
| Librarian → COLLEEN | Archive confirmation (chain complete) | Post-archive |
| COLLEEN → Librarian | BLG flag (missing archive entry detected) | Gap detection |
| **Constraint:** | Librarian must archive before the session seal; COLLEEN enforces chain | Protocol integrity |

---

### Primary — The Actualizer (Post-Write Archive)

| Direction | Content | Protocol |
|---|---|---|
| Actualizer → Librarian | Write completion signal (artifact/code written) | Via COLLEEN NDR-Protocol-01 |
| **Constraint:** | Every Actualizer write must be archived; no canonical artifact without Librarian entry | Provenance guarantee |

---

### Primary — Apogee (Evidence Scoring Cross-Check)

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Librarian | Cross-check report (entries vs. SWEEP_LOG) | Pre-certification |
| Librarian → Apogee | Backfill entries for verification | Gap backfill |
| **Constraint:** | Apogee's cross-check is binding; contaminated entries must be corrected before Apogee certifies | Evidence integrity |

---

### Lateral — Amethyst (Seal Pre-Condition)

| Direction | Content | Protocol |
|---|---|---|
| Librarian → Amethyst | Archive completeness confirmation (implicit pre-condition for seal) | Pre-seal |
| **Constraint:** | Amethyst seal requires archive completeness; gaps block seal | Seal integrity |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Actualizer writes but COLLEEN does not route to Librarian | Librarian self-initiates archive from session context; COLLEEN protocol gap flagged |
| Apogee rejects backfill entry | Escalate to Amethyst; seal blocked until resolved |
| Archive entry exists but Actualizer write never occurred | Prof Prodigy issues MH-class flag (phantom provenance); Amethyst investigates |
| COLLEEN BLG and Apogee cross-check identify same gap simultaneously | Single backfill procedure; both sources cited in entry |

---

*Classification: T1 PUBLIC*
