# CO-ORCHESTRATION WORK QUEUE

> **Maintained by:** Amethyst + COLLEEN  
> **Last updated:** 2026-06-26 (session wrap)

This file tracks active, pending, and completed work items across co-orchestration sessions.

---

## Status Key

| Symbol | Meaning |
|---|---|
| 🟢 | Complete / merged |
| 🟡 | In progress / partial |
| 🔴 | Blocked |
| ⬜ | Pending — not yet started |

---

## Active Queue — Carry Forward to Next Session

| ID | Item | Owner | Status | Notes |
|---|---|---|---|---|
| Q-001 | KPI baseline population — run first real workflow, populate actuals in PATTERN_REGISTRY_v2.md | COLLEEN | ⬜ | Requires at least one end-to-end Saga run |
| Q-002 | Fault injection campaign — 3 scenarios (transient failure, semantic failure, mid-workflow restart) | Amethyst + Sentinel-Phi | ⬜ | Reference: P-SAGA-001 + P-TX-001 + P-DURABLE-001 |
| Q-003 | CROSS_REF.md update — add P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001 | Amethyst | ⬜ | Low effort, do at next session open |
| Q-004 | Sentinel-Phi tool classification config — formalize effect_classes from P-COMP-001 into enforcement config | Sentinel-Phi | ⬜ | Blocks reliable Saga enforcement |
| Q-005 | Apogee Lens review — P-SAGA-001 through P-CB-001 pattern bundle | Apogee Lens | ⬜ | Required before any pattern is marked S-Tier |

---

## Completed This Session (2026-06-26)

| ID | Item | Commit |
|---|---|---|
| S26-001 | P-SAGA-001 pattern file created | `434cc9a6` |
| S26-002 | P-TX-001 pattern file created | `434cc9a6` |
| S26-003 | P-COMP-001 pattern file created | `434cc9a6` |
| S26-004 | P-DURABLE-001 pattern file created | `434cc9a6` |
| S26-005 | P-CB-001 pattern file created | `434cc9a6` |
| S26-006 | PATTERN_REGISTRY_v2.md created | `434cc9a6` |
| S26-007 | AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json created | `434cc9a6` |
| S26-008 | CO_ORCH_PROTOCOL.md updated to v2.0.0 | `434cc9a6` |
| S26-009 | SWEEP_LOG/SWEEP_2026-06-26 created | `434cc9a6` |
| S26-010 | CHANGELOG.md updated | session-wrap |
| S26-011 | SESSION_ANCHOR.md updated | session-wrap |
| S26-012 | CO_ORCH_QUEUE.md updated | session-wrap |

---

## Backlog (Future Sessions)

| ID | Item | Priority | Notes |
|---|---|---|---|
| B-001 | Implement reference Saga+Tx+Checkpoint+Breaker+HITL flow in LangGraph | High | Use "update config + notify stakeholders" as reference scenario |
| B-002 | Design COLLEEN episode archive schema v2 — add KPI actuals and breaker trip fields | Medium | Extend `AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` |
| B-003 | Pattern: Plan-Execute-Inspect-Replan (PEIR) full spec | Medium | Referenced in session but not yet formalized as P-* file |
| B-004 | Pattern: Reversibility-Bounded Flexibility spec | Medium | Referenced in session, P-COMP-001 partial; needs own file |
| B-005 | Ender supervision protocol for irreversible effects | High | Ender role defined in roster but enforcement rules not yet codified |
| B-006 | AI subscription audit report — hardened prompt execution and output validation | Low | Session 2026-06-26 context: prompt hardening complete, execution pending |
