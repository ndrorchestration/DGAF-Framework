# CO_ORCH_QUEUE.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-30  
> **Anchor:** S067

This file is the active experiment and work queue for the co-orchestration pipeline.
All items must have an owner, checks, artifacts, and metrics before execution.

---

## Queue — S067 Active

### [Q-S066-01] Router TC1/TC2/TC7/TC8 Shadow Bug Fix

- **Owner:** Reson
- **Priority:** P1
- **Status:** 🔲 Queued
- **Context:** Sequential and fan-out predicates in topology router are shadowed by hierarchical catch-all. TC1, TC2, TC7, TC8 currently fail (5/8 pass rate). Tracked from S043 Q-S043-04.
- **Checks:**
  - [ ] Reorder predicates so SEQUENTIAL and FAN-OUT match before HIERARCHICAL catch-all
  - [ ] All 8 TCs pass: TC1 SEQUENTIAL, TC2 SEQUENTIAL, TC3 REFLEXIVE, TC4 HIERARCHICAL, TC5 REJECTED, TC6 REJECTED, TC7 FAN-OUT, TC8 FAN-OUT
  - [ ] Regression: TC3–TC6 still pass after reorder
  - [ ] CI green on `tests/test_router_coverage.py`
- **Artifacts:** `components/topology_router.py`, `tests/test_router_coverage.py`
- **Metrics:** 8/8 TC pass rate (up from 5/8)

---

### [Q-S066-04] Lifecycle Harness — Phase 0–VI Executable (Carry-Forward)

- **Owner:** Amethyst + COLLEEN
- **Priority:** P1
- **Status:** 🔲 Queued (carry-forward from S043 Q-S043-05)
- **Checks:**
  - [ ] Executable phase harness produces `lifecycle_stability_report.json`
  - [ ] Stability index per phase ≥ 0.618
  - [ ] Time-to-convergence ≤ Fib[34] turns
  - [ ] COLLEEN archive ingest of all phase artifacts
- **Artifacts:** `registry/lifecycle_stability_report.json`, `docs/lifecycle_harness_v2.md`
- **Metrics:** Stability index ≥ 0.618 per phase, convergence ≤ Fib[34]

---

### [PM-04] P-07 COMPOSE Mode Note (Non-Blocking)

- **Owner:** Amethyst
- **Priority:** Medium
- **Status:** 🔲 Deferred (non-blocking, any session)
- **Context:** Update P-07 COMPOSE mode note re: issue-resolution source.

---

## Completed Queue Items — S067

| ID | Name | Owner | Status |
|----|------|-------|--------|
| PR-D | `docs/NDR_PATTERN_REGISTRY.md` → redirect stub | Amethyst | ✅ Done S067 |
| PR-E (partial) | CROSS_REF → unified path + S067 anchor | COLLEEN | ✅ Done S067 |

---

## Completed Queue Items — S066

| ID | Name | Owner | Status |
|----|------|-------|--------|
| Q-S066-02 | COLLEEN stasis audit P-12–P-26 (PM-05) | COLLEEN | ✅ CLOSED — Ender ratified 2026-05-30 02:49 EDT |
| Q-S066-03 | Apogee P-34 attestation (PM-07) | Apogee | ✅ CLOSED — A-TIER 94.5% — Ender ratified 2026-05-30 02:49 EDT |
| Q-S066-P34-REG | Register P-34 COMPOSE entry | Amethyst | ✅ Done |
| Q-S066-JSON-SYNC | Sync ndr_patterns.json v0.3.0 | Amethyst | ✅ Done |
| Q-S066-DIFF | Create NDR_REGISTRY_DIFFERENTIATION.md | Amethyst | ✅ Done |
| Q-S066-MERGE-PLAN | Create NDR_REGISTRY_MERGE_PLAN.md | Amethyst | ✅ Done |
| Q-S066-PM01 | PM-01: Phi-Closure card P-29 cross-ref | Amethyst | ✅ Done |
| Q-S066-PM02 | PM-02: P-03 ALTER note P-30 ref | Amethyst | ✅ Done |

---

## Completed Queue Items — Prior Sessions

| ID | Name | Session | Status |
|---|---|---|---|
| Q-S043-01 | Intake Gate Hardening | S043 | ✅ Done |
| Q-S043-02 | Phi-Closure Gate — HPG Wiring | S043 | ✅ Done |
| Q-S043-03 | Orchestration Firewall | S043 | ✅ Done |
| Q-S043-06 | Archive and Registry Sync | S043 | ✅ Done |
| Q-S038-01 | SCPE threshold calibration | S038 | ✅ Done |
| Q-S039-01 | PDMAL convergence proof | S039 | ✅ Done |
| Q-S040-01 | HPG Ionian gate implementation | S040 | ✅ Done |
| Q-S041-01 | DGAF 6-axis semantic scoring | S041 | ✅ Done |
| Q-S042-01 | Amethyst dual-lock logic | S042 | ✅ Done |
