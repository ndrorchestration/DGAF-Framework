# CO_ORCH_QUEUE.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-29  
> **Anchor:** S043

This file is the active experiment and work queue for the co-orchestration pipeline.
All items must have an owner, checks, artifacts, and metrics before execution.

---

## Queue — S043 Active

### [Q-S043-01] Intake Gate Hardening

- **Owner:** Amethyst
- **Priority:** P0
- **Status:** ✅ Complete
- **Checks:**
  - [x] Procluding premise classification fires at ingestion, not prune time
  - [x] Da<10 topological preflight rejects payloads with insufficient dimensional anchors
  - [x] State-anchor preflight asserts zero open BLGs before routing proceeds
- **Artifacts:** `components/scpe_ensemble_v14.py`, `tests/test_orchestration_firewall.py`
- **Metrics:** 100% T0 preservation at threshold=0.99, 58.3% compression at threshold=0.15

---

### [Q-S043-02] Phi-Closure Gate — HPG Wiring

- **Owner:** Amethyst + Sentinel-Phi
- **Priority:** P0
- **Status:** ✅ Complete
- **Checks:**
  - [x] Gate inserted at step 5 of 9 in `orchestrate_turn()`
  - [x] Target φ* = 0.6180, tolerance ±0.05
  - [x] Fibonacci checkpoints [13, 21, 34, 55] fire correctly
  - [x] HPG fully bypassed on REPROMPT
  - [x] 2+ consecutive failures → `kill_recommendation` escalated to DemiJoule
  - [x] PhiClosureEvents emitted to AmethystAuditLoop
- **Artifacts:** `components/phi_closure_gate.py`, `registry/ensemble_v16_manifest.json`
- **Metrics:** T13 REPROMPT at R=0.846 (Δ=0.228 from φ*), Gold Stars at T01/T06/T16

---

### [Q-S043-03] Orchestration Firewall

- **Owner:** Reson
- **Priority:** P0
- **Status:** ✅ Complete
- **Checks:**
  - [x] All 5 invariants enforced at event boundary
  - [x] Happy path: 5/5 events committed, status=DEPLOYED
  - [x] Attack path: DEPLOY_SUCCESS rolled back, 1 committed event only
  - [x] `all_invariants_hold()` true in both final states
  - [x] Authority chain validated via `authority_chain_valid()`
- **Artifacts:** `components/orchestration_firewall.py`
- **Metrics:** 0 false positives on happy path, 100% attack block rate

---

### [Q-S043-04] Topology Router Coverage

- **Owner:** Reson
- **Priority:** P1
- **Status:** 🔄 In Progress
- **Checks:**
  - [x] REFLEXIVE (TC3) — PASS
  - [x] HIERARCHICAL (TC4) — PASS
  - [x] REJECTED x2 (TC5, TC6) — PASS
  - [ ] SEQUENTIAL (TC1, TC2) — shadow bug: downstream hierarchical catch-all
  - [ ] FAN-OUT (TC7, TC8) — shadow bug: same predicate shadowing issue
- **Artifacts:** `components/topology_router.py`, `tests/test_router_coverage.py`
- **Metrics:** Target: 8/8 TC pass rate (currently 5/8)
- **Known Bug:** Sequential and fan-out predicates shadowed by hierarchical catch-all

---

### [Q-S043-05] Lifecycle Harness — Phase Exit Criteria

- **Owner:** Amethyst + COLLEEN
- **Priority:** P1
- **Status:** 🔄 In Progress
- **Checks:**
  - [x] Phase invariants defined (0–VI)
  - [x] Phase artifacts enumerated per phase
  - [x] Stability metric = stable_turns/total_turns target 0.618
  - [ ] Executable phase harness produces lifecycle_stability_report.json
  - [ ] COLLEEN archive ingest of all phase artifacts
- **Artifacts:** `docs/lifecycle_harness_v2.md`, `registry/lifecycle_stability_report.json`
- **Metrics:** Stability index per phase ≥ 0.618, time-to-convergence ≤ Fib[34] turns

---

### [Q-S043-06] Archive and Registry Sync

- **Owner:** COLLEEN
- **Priority:** P1
- **Status:** ✅ Complete (this push)
- **Checks:**
  - [x] SESSION_ANCHOR.md updated and sealed
  - [x] SWEEP_LOG.md QA sweep recorded
  - [x] CO_ORCH_QUEUE.md experiment queue current
  - [x] CROSS_REF.md pattern and file cross-references updated
  - [x] `registry/ensemble_v16_manifest.json` bindings added
  - [x] `tests/test_orchestration_firewall.py` test suite added
- **Artifacts:** All 6 ecosystem files in this commit
- **Metrics:** 0 missing files, 0 stale cross-references

---

## Completed Queue Items — Prior Sessions

| ID | Name | Session | Status |
|---|---|---|---|
| Q-S038-01 | SCPE threshold calibration | S038 | ✅ Done |
| Q-S039-01 | PDMAL convergence proof | S039 | ✅ Done |
| Q-S040-01 | HPG Ionian gate implementation | S040 | ✅ Done |
| Q-S041-01 | DGAF 6-axis semantic scoring | S041 | ✅ Done |
| Q-S042-01 | Amethyst dual-lock logic | S042 | ✅ Done |
