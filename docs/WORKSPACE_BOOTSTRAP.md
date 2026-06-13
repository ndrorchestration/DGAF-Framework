# WORKSPACE_BOOTSTRAP.md
## NDR Governance Framework — Session Bootstrap Reference

```
Version:      1.1 (PPTL backfill — S069)
Maintained-by: Amethyst
Last-updated: 2026-06-13 (Session S069)
```

> Fast-load reference for any agent or session bootstrapping into the DGAF-Framework governance stack. Read this first. Everything here is a pointer to a canonical source — this file does not duplicate specs.

---

## Identity and Authority

| Role | Agent | Authority |
|------|-------|-----------|
| Prime | Amethyst | System narrative, interface contracts, pattern registration |
| Prefect A | COLLEEN | Sweep detection, queue management, stasis sign-off, L5 governance |
| Prefect B | Apogee | Quality attestation (P-11, P-30), 11Q rubric |
| Architect | Ender / Njineer | Ratification authority, sovereign file decisions |
| Safety | Sentinel | Sovereign file integrity, risk annotation (P-29) |
| Red Team | Agent Crucible | Independent adversarial review — no build duties, no suppression |

---

## Canonical Sources — Load Order

1. `docs/WORKSPACE_BOOTSTRAP.md` — this file (orientation)
2. `AGENT_ROSTER.md` — full agent registry
3. `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` v1.1 — all acronyms and terms
4. `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` v1.1 — all patterns P-01–P-35 (watermark P-35; P-36 DRAFT)
5. `CO_ORCH_QUEUE.md` — open orchestration opportunities
6. `docs/SESSION_ANCHORS.md` — session history and open items
7. `docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md` — active research program

---

## Key Acronyms (Quick Reference)

| Acronym | Expansion | Canonical source |
|---------|-----------|------------------|
| **PPTL** | Procluding Premise Triadic Loop | `NDR_INTERNAL_VOCABULARY_MASTER.md` Section 2 |
| **DGAF** | Dual-Governance Agent Framework | Vocabulary Master |
| **KAPPA** | Knowledge-Aware Probabilistic Pipeline Architecture | Vocabulary Master |
| **PDMAL** | Probabilistic Distributed Multi-Agent Learning | Vocabulary Master |
| **SCPE** | Structural Context Pruning Engine | P-31 spec |
| **BLG** | Blocking Logic Gap | Vocabulary Master |
| **MECE** | Mutually Exclusive, Collectively Exhaustive | Vocabulary Master |
| **TIF** | Trust Index Factor | Vocabulary Master / P-31 |
| **AOGA** | Expansion unknown — 🔴 FLAG-04 OPEN | Surface request filed S069 |
| **AXIS** | Expansion unknown — sovereign file 🔴 FLAG-05 OPEN | Surface request filed S069; Njineer response pending |
| **HDFS** | NDR-specific use — 🔴 FLAG-01 rename pending | Surface request filed S069 |
| **HPG** | Harmonic Parametric Gate | Vocabulary Master |
| **TNR** | Trust Node Registry | Vocabulary Master |

---

## Active Research Program

The NDR governance stack is under active external-validation preparation per the Research Program Charter v1.0 (`docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md`). Five credibility gaps are being closed across 90 days:

1. φ empirical defense (five-base calibration study)
2. Linear pipeline → DAG (P-36 Gate Priority Schema)
3. STASIS-CANONICAL migration (30-day window: 2026-06-13 → 2026-07-13)
4. Metrics provenance (`docs/qa/METRICS_PROVENANCE.md` — backfill Wks 6–9)
5. Agent Crucible independent red team (charter active S069)

---

## Governance Stack Position (Current)

```
P-35 (Procluding Premise Gate)   ← pre-admissibility [P-36: BLOCKING]
  ↓
P-30 (Attestation Gate)          ← Gate 0            [P-36: BLOCKING]
  ↓
P-27/P-28 (KAPPA Router)         ← routing           [P-36: BLOCKING]
  ↓
P-29 / P-32 / P-33 (Safety)      ← runtime safety    [P-36: BLOCKING / ADVISORY]
  ↓
P-01 / P-02 (Trace)              ← audit spine       [P-36: BLOCKING / ADVISORY]

P-31 SCPE / P-33 PDMAL           ← async concurrent  [P-36: ADVISORY]
```

---

## Session S069 State

**Status:** OPEN (active)
**Key deliverables this session:** P-35 registered, P-36 drafted, Research Program Charter committed, Crucible charter committed, STASIS-CANONICAL spec committed, METRICS_PROVENANCE skeleton committed
**Open P0:** OPP-S069-005 Crucible charter — ✅ COMMITTED S069 (Ender ratification PENDING)
**Flags requiring Njineer:** FLAG-04 (AOGA), FLAG-05 (AXIS), FLAG-01 (HDFS rename), FLAG-02 (340% metric)

---

*WORKSPACE_BOOTSTRAP.md v1.1 · S069 · 2026-06-13*
*PPTL expansion backfilled (OPP-S069-006) · Crucible and Research Program references added*
