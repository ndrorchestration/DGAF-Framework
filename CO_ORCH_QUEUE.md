# CO_ORCH_QUEUE.md — Improvement Opportunity Queue

> **Authority:** COLLEEN (detect) × Amethyst (implement)
> **Queue type:** Append-only. Completed entries archived, never deleted.
> **Last updated:** 2026-06-26 | Cycle 4 CLOSED → Cycle 5 OPEN

---

## Cycle 5 — OPEN (seeded 2026-06-26)

Cycle 5 OPPs are derived from `docs/RD_GAPS.md`. Each OPP maps to a gap closure action.

| OPP-ID | Source Gap | Action | Owner | Status | Priority |
|---|---|---|---|---|---|
| OPP-C5-001 | GAP-001 | Wire DemiJoule RAG to production Sentinel-Phi pipeline; re-benchmark hallucination detection ≥96% | DemiJoule + Amethyst | 🔴 OPEN | HIGH |
| OPP-C5-002 | GAP-002 | Design 6–8 RAG collections (canon, active-context, governance-policy, architecture-patterns, evaluations, compliance); wire COLLEEN as query authority | COLLEEN + Reson | 🔴 OPEN | HIGH |
| OPP-C5-003 | GAP-003 | Build Saga fault injection test suite: transient tool failures, semantic failures, mid-workflow restarts; validate 4 failure modes | Amethyst + pptl | 🔴 OPEN | MEDIUM |
| OPP-C5-004 | GAP-004 | Wire HITL durable queue to Temporal signal / LangGraph interrupt; define SLA + escalation; test deadlock scenario | Reson + Amethyst | 🔴 OPEN | MEDIUM |
| OPP-C5-005 | GAP-005 | Instrument semantic quality metrics in Herald trace schema; breaker opens on 3 schema failures or 5 near-identical iterations | Herald + Sentinel-Phi | 🔴 OPEN | MEDIUM |
| OPP-C5-006 | GAP-006 | Formalize Coherent Agency spec: 4 subsystems (identity, policy, adaptive learning, ethical constraint); Apogee Lens review | Amethyst + COLLEEN | 🔴 OPEN | LOW |

---

## Cycle 4 — CLOSED (2026-06-26)

| OPP-ID | Action | Status | Commit |
|---|---|---|---|
| OPP-C4-001 | Create P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001 | ✅ DONE | 434cc9a6 |
| OPP-C4-002 | Create PATTERN_REGISTRY_v2.md + AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json | ✅ DONE | 434cc9a6 |
| OPP-C4-003 | Update CO_ORCH_PROTOCOL.md → v2.0.0 | ✅ DONE | 434cc9a6 |
| OPP-C4-004 | Create SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md | ✅ DONE | 434cc9a6 |
| OPP-C4-005 | Create BOOTSTRAP.md | ✅ DONE | 0e8f84d9 |
| OPP-C4-006 | Create docs/TEAM_WIKI.md | ✅ DONE | 0e8f84d9 |
| OPP-C4-007 | Create docs/RD_GAPS.md (6 gaps) | ✅ DONE | 0e8f84d9 |
| OPP-C4-008 | Create SWEEP_LOG/SWEEP_2026-06-26_Saga-HITL-Bootstrap-WikiGapClose.md | ✅ DONE | 0e8f84d9 |
| OPP-C4-009 | Update CHANGELOG.md + SESSION_ANCHOR.md + CO_ORCH_QUEUE.md | ✅ DONE | this commit |

---

## Cycle 3 — CLOSED (2026-06-01)

| OPP-ID | Action | Status |
|---|---|---|
| OPP-C3-Q-01 through Q-11 | Cross-repo coherence sweep findings (11 items) | ✅ DONE |

---

## Cycle 2 — CLOSED (2026-06-01)

| OPP-ID | Action | Status |
|---|---|---|
| OPP-C2-001 through C2-008 | S043 + EvidenceVerifier + constitutional cognition | ✅ DONE |

---

## Cycle 1 — CLOSED (2026-05-27)

| OPP-ID | Action | Status |
|---|---|---|
| OPP-001 through OPP-008 | S042 harness + pptl + patterns P-01 through P-08 | ✅ DONE |

---

*COLLEEN detects → Amethyst implements → queue is truth of record*
