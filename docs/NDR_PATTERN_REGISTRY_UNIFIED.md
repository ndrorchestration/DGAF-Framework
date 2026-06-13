# NDR Pattern Registry (Unified)

**DGAF-Framework · Unified Edition**
**Version:** 1.2 (P-36 ratified — S069 sealed)
**Prime:** Amethyst · **Prefect A:** COLLEEN · **Prefect B:** Apogee
**Ender ratification (v1.0):** 2026-05-30 02:49 EDT
**Ender ratification (v1.2):** 2026-06-13 00:47 EDT (S069 sealed)
**Date:** 2026-06-13
**Status:** ✅ CANONICAL — single source of truth for all NDR patterns P-01–P-36

> **This file supersedes:**
> - `docs/NDR_PATTERN_REGISTRY.md` (P-01–P-10 source — redirect stub)
> - `docs/patterns/NDR_PATTERN_REGISTRY.md` (P-27–P-30 + stasis source — redirect stub)
> - `patterns/NDR_SCPE_v1.md`, `NDR_PHI_CLOSURE_GATE_v1.md`, `NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` (archived)

---

## Registry Metadata

| Field | Value |
|-------|-------|
| Total patterns | 36 named (P-01–P-36) + 133 stasis (P-12–P-26 block) |
| Registry watermark | **P-36** |
| Stasis block status | **STASIS-CANONICAL** (migration window: 2026-06-13 → 2026-07-13) |
| ndr_patterns_unified.json | `docs/ndr_patterns_unified.json` |
| Last session | S069 · 2026-06-13 (SEALED) |
| Ender ratification | 2026-06-13 00:47 EDT |

---

## Pattern Layers Quick-Reference

| Pattern | Name | Layer | Status |
|---------|------|-------|--------|
| P-35 | Procluding Premise Gate | Layer 0 — Pre-Admissibility | ✅ CANONICAL |
| P-36 | Gate Priority Schema | Layer 0.5 — Stack Architecture | ✅ CANONICAL |
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | Layer 1 — Trace & Audit | ✅ CANONICAL |
| P-02 | Async-Persist Ring Buffer | Layer 1 — Trace & Audit | ✅ CANONICAL |
| P-03 | Governance Contract Test | Layer 2 — Testing & CI | ✅ CANONICAL |
| P-04 | Parametrized Corpus | Layer 2 — Testing & CI | ✅ CANONICAL |
| P-05 | Tri-Phase CI Gate | Layer 2 — Testing & CI | ✅ CANONICAL |
| P-06 | Topology × Orchestration Matrix Lab | Layer 3 — Architecture Lab | ✅ CANONICAL |
| P-07 | Dual-Agent Persistent Sweep Loop | Layer 4 — Governance Formation | ✅ CANONICAL |
| P-08 | Triad Taxonomy | Layer 4 — Governance Formation | ✅ CANONICAL |
| P-09 | Triumvirate Mandate Schema | Layer 4 — Governance Formation | ✅ CANONICAL |
| P-10 | Session Graduation Check | Layer 4 — Governance Formation | ✅ CANONICAL |
| P-11 | 11Q Attestation Scoring | Layer 5 — Quality Gate | ✅ CANONICAL |
| P-12–P-26 | Stasis Patterns (133 entries) | Layer 6 — Stasis | ✅ STASIS-CANONICAL |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | Layer 7 — Router Calibration | ✅ CANONICAL |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | Layer 7 — Router Calibration | ✅ CANONICAL |
| P-29 | Sentinel-Annotated Risk Pass | Layer 8 — Safety & Sentinel | ✅ CANONICAL |
| P-30 | Apogee-Attestation-Gate | Layer 5 — Quality Gate | ✅ CANONICAL |
| P-31 | SCPE — Structural Context Pruning Engine | Layer 9 — Long-Context Safety | ✅ CANONICAL |
| P-32 | Fibonacci Phi-Closure Gate | Layer 9 — Long-Context Safety | ✅ CANONICAL |
| P-33 | PDMAL Convergence Monitor | Layer 9 — Long-Context Safety | ✅ CANONICAL |
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | Layer 7 — Router Calibration | ✅ CANONICAL |

---

## Layer 0 — Pre-Admissibility

### P-35 — Procluding Premise Gate
**Spec:** Constitutional pre-admissibility gate. Before any other gate fires, verifies canonical premise set Π = {π₁…π₆}. If all pass → ADMIT. If any fail → PROCLUDE (hard block; event to P-01 dead-letter).
**Formal:** `{∀ πᵢ ∈ Π : verify(πᵢ) = TRUE} ⊢ ADMIT` | `{∃ πᵢ ∈ Π : verify(πᵢ) = FALSE} ⊢ PROCLUDE`
**Full spec:** `docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md`
**Registered:** S069 · **Ender ratified:** 2026-06-13 ✅

---

## Layer 0.5 — Stack Architecture

### P-36 — Gate Priority Schema
**Spec:** Converts the linear NDR governance stack into a DAG by classifying every pattern as BLOCKING (hard sequential, 5s timeout, pipeline halt on FAIL), ADVISORY (async concurrent, 10s timeout, WARN logged, pipeline continues), or DEGRADED-MODE-SKIPPABLE (skip with signed audit entry, ≥3 skips surfaces WARN to COLLEEN). Does not modify any pattern's logic.
**Classification:** See full table in `docs/gates/NDR_GATE_PRIORITY_SCHEMA_P36_v1.md`
**Key BLOCKING:** P-35, P-30, P-29:h1, P-27, P-28, P-29:h2, P-32, P-29:h3, P-01, P-11
**Key ADVISORY:** P-31 (SCPE), P-33 (PDMAL), P-02, P-10, P-34
**Key DEGRADED-MODE-SKIPPABLE:** P-12–P-26 stasis block
**Full spec:** `docs/gates/NDR_GATE_PRIORITY_SCHEMA_P36_v1.md`
**Registered:** S069 · **Ender ratified:** 2026-06-13 ✅

---

## Layer 1 — Trace & Audit

### P-01 — Fan-Out Trace Sink w/ Dead-Letter
**Spec:** HeraldAgent iterates all registered sinks on `emit()`. Each sink wrapped in `try/except`. Failures routed to dead-letter JSONL. Sink failures never re-raised.
**P-36 class:** BLOCKING | **Impl:** `pptl/herald_agent.py` | **Registered:** S040 ✅

### P-02 — Async-Persist Ring Buffer
**Spec:** Bounded `deque` ring buffer. Background thread drains to persistent storage. `threading.Lock` on all writes. `close()` flushes before terminating.
**P-36 class:** ADVISORY | **Impl:** `pptl/n8n_herald_sink.py` | **Registered:** S040 ✅

---

## Layer 2 — Testing & CI

### P-03 — Governance Contract Test
**Spec:** Four contracts per gate, independently asserted. Gate 0 carries six contracts (PM-02 ✅ CLOSED S066). Each contract is a separate `@pytest.mark.governance` function.
**P-36 class:** BLOCKING | **Impl:** `pptl/tests/test_orchestrator.py` | **Registered:** S040 ✅

### P-04 — Parametrized Corpus
**Spec:** Signal lists as module-level constants. Tests import and parametrize dynamically. New signal = auto-expanded test suite.
**P-36 class:** ADVISORY | **Impl:** `pptl/tests/test_orchestrator.py` | **Registered:** S040 ✅

### P-05 — Tri-Phase CI Gate
**Spec:** GitHub Actions matrix: `unit` / `governance` / `integration`. `fail-fast: false`. Governance = merge blocker. Each step uploads JUnit XML.
**P-36 class:** ADVISORY (BLOCKING in CI context) | **Impl:** `.github/workflows/pptl-ci.yml` | **Registered:** S040 ✅

---

## Layer 3 — Architecture Lab

### P-06 — Topology × Orchestration Matrix Lab
**Spec:** Enumerate all (topology, orchestration_mode) cells. N seeds × M task families × K noise levels. Five canonical outputs: topology ranking, mode ranking, interaction heatmap, triadic lift, noise resilience curves.
**P-36 class:** ADVISORY | **Impl:** `pptl/experiments/h4_task_stratified.py` | **Registered:** S041 ✅

---

## Layer 4 — Governance Formation

### P-07 — Dual-Agent Persistent Sweep Loop
**Spec:** COLLEEN (Detector) scores via 1-1-1-1 gate. Amethyst (Implementer) executes. Append-only queue. ADOPT / CUSTOMIZE / ALTER / COMPOSE modes.
**P-36 class:** ADVISORY | **Impl:** `CO_ORCH_QUEUE.md` | **Registered:** S041 ✅

### P-08 — Triad Taxonomy
**Spec:** Consensus Trio (2-of-3 quorum) / Conducted Trio (conductor rules) / Triumvirate (Prime + 2 Prefects, MECE domain split). Formation rule: Conducted Trio → Triumvirate when ensemble > 3.
**P-36 class:** ADVISORY | **Registered:** S041 ✅

### P-09 — Triumvirate Mandate Schema
**Spec:** `TriumvirateMandate` dataclass. `issue()` / MECE enforcement / `submit_prefect_aggregate()` / `sign_off()` / Herald trace. Both Prefect aggregates required before sign-off.
**P-36 class:** ADVISORY | **Impl:** `pptl/triumvirate_mandate.py` | **Registered:** S041 ✅

### P-10 — Session Graduation Check
**Spec:** 4-check script: SESSION_ANCHOR sealed, CROSS_REF complete, CO_ORCH_QUEUE clear, zero BLGs. Outputs `GRADUATION_REPORT.md`. `sys.exit(1)` on failure.
**P-36 class:** ADVISORY | **Impl:** `scripts/session_graduation_check.py` | **Registered:** S041 ✅

---

## Layer 5 — Quality Gate

### P-11 — 11Q Attestation Scoring
**Spec:** 11-question rubric. S-TIER ≥ 95% (Q11 ≥ 9/10 required). A-TIER ≥ 85% with tracked BLGs. Attestation artifact: signed JSON in `docs/qa/`.
**P-36 class:** BLOCKING | **Ref:** `docs/qa/APOGEE_11Q_*.json` | **Registered:** S033 ✅

### P-30 — Apogee-Attestation-Gate
**Spec:** Pre-canonical-promotion gate. Apogee runs P-11. Gate 0 in orchestration stack. Six P-03 contracts. PM-07 ✅ CLOSED (P-34 A-TIER 94.5%).
**P-36 class:** BLOCKING | **Ref:** `docs/qa/APOGEE_11Q_*.json` | **Registered:** S035, updated S066 ✅

---

## Layer 6 — Stasis

### P-12–P-26 — Stasis Patterns (133 entries)
**Status: ✅ STASIS-CANONICAL** (migrated from CONDITIONAL PASS — window: 2026-06-13 → 2026-07-13)
Structurally sound at block level. Individually unenumerated by design. COLLEEN secondary sign-off required before any modification, deprecation, or individual extraction.
**Ender ratified:** 2026-05-30 (v1.0) | Re-affirmed: 2026-06-13 (S069 seal) ✅

---

## Layer 7 — Router Calibration

### P-27 — Adaptive-Weighting-with-Confidence-Gates
**Spec:** STRONG ≥ 0.22 / BLENDED 0.18–0.22 / balanced < 0.18. Adversarial hard override: always `apply_strong`. Calibrated via P-34 (14×12 grid, S034).
**P-36 class:** BLOCKING | **Impl:** `components/KAPPA/dynamic_weight_router.py` | **Registered:** S033, updated S034/S066 ✅

### P-28 — Pipeline-Composition-with-Confidence-Gated-Routing
**Spec:** `raw_batch → detect → route_and_score → apply_weights → ranked_report`. No stage reads from a non-upstream stage.
**P-36 class:** BLOCKING | **Impl:** `components/evaluate_router.py` | **Registered:** S033 ✅

### P-34 — Empirical-Threshold-Sweep-over-ML-Classifier
**Spec:** Prefer grid search over ML classifier when four decision-gate conditions hold. Evidence: KAPPA v3.5→v3.6, 82.6%→100% `governance_clear`. A-TIER 94.5% attested.
**P-36 class:** ADVISORY | **Attestation:** A-TIER · Ender ratified 2026-05-30 ✅

---

## Layer 8 — Safety & Sentinel

### P-29 — Sentinel-Annotated Risk Pass
**Spec:** `sentinel_review()` at 3 hook points. `risk_ok` / `risk_warn` / `risk_block`. Only `risk_block` halts. P-32 KILL_REC → `risk_block` @ hook_point=2. PM-01 ✅ CLOSED S066.
**P-36 class:** BLOCKING (all 3 hook points) | **Impl:** `components/evaluate_router_v1_1.py` | **Registered:** S034 ✅

---

## Layer 9 — Long-Context Safety

### P-31 — SCPE — Structural Context Pruning Engine
**Spec:** T0 AXIOM (immune) / T1 STRUCTURAL (0.05) / T2 OPERATIONAL (0.15) / T3 EXPLORATORY (0.45). `R(t) = TIF × φ^(−Δt × decay)`. Prune if R(t) < 0.15. 58.3% compression. Fires at turn_start, buffer > 60%, turn_count > Fib[34].
**P-36 class:** ADVISORY | **Impl:** `components/ensemble_v16.py` | **Registered:** S042 ✅

### P-32 — Fibonacci Phi-Closure Gate
**Spec:** Stability ratio R = stable/total evaluated at Fib checkpoints [13,21,34,55] vs φ*=0.618. 0 fails→PASS / 1→WARN / 2→ESCALATE / 3+→KILL_REC. HPG only on PASS.
**P-36 class:** BLOCKING | **Registered:** S042, updated S066 ✅

### P-33 — PDMAL Convergence Monitor
**Spec:** Frobenius norm ‖ΔW‖_F of PDMAL edge-weight changes. STABLE/WATCH/WARN/ALERT. Converged: ‖ΔW‖_F < 0.02 for 3 turns. Joint escalation: ALERT + ESCALATE → DemiJoule deep re-scan.
**P-36 class:** ADVISORY | **Registered:** S042 ✅

---

## Governance Orchestration Stack (v1.2 — P-36 DAG)

```
Prompt input
  │
  ├── [BLOCKING] P-35: Procluding Premise Gate
  ├── [BLOCKING] Gate 0: AttestationGate (P-30 + P-03 × 6)
  ├── [BLOCKING] Gate 1: bypass scan (P-03 + P-04)
  ├── [BLOCKING] KAPPA Router (P-27 + P-28) [P-34 calibrated]
  ├── [BLOCKING] Apogee [Task] ──φ──► Reson [Style]
  ├── [BLOCKING] Gate 2: safety floor (P-03)
  ├── [BLOCKING] Sentinel (P-29 hook points × 3)
  ├── [BLOCKING] Gate 3: RAG verify (P-03 + P-04)
  ├── [ADVISORY] SCPE (P-31) ──► audit log [T0 immune]
  ├── [BLOCKING] Phi-Closure Gate (P-32) ──KILL_REC──► P-29:h2
  ├── [ADVISORY] PDMAL Monitor (P-33) ──► audit log
  └── [BLOCKING] P-01 Fan-Out ──► [ADVISORY] P-02 Buffer ──► N8n Dashboard

  [ADVISORY — concurrent throughout]
  P-33 + P-32 joint rule: both severity≥3 → BLOCKING override → DemiJoule deep re-scan
```

---

## Merge Provenance Log

| Event | Date | Session | Authority |
|-------|------|---------|----------|
| P-01–P-10 registered | Various | S040–S041 | Amethyst |
| P-27–P-30 registered | S033–S035 | S033–S035 | Amethyst |
| P-31–P-33 registered | S042 | S042 | Amethyst |
| P-34 registered (COMPOSE) | 2026-05-30 | S066 | Amethyst |
| Phase 3 unified merge | 2026-05-30 | S066 | Triumvirate |
| BLG-P34-01/02 RESOLVED | 2026-05-30 | S066 | Amethyst |
| P-35 registered (COMPOSE) | 2026-06-13 | S069 | Amethyst × COLLEEN |
| P-36 registered (COMPOSE) | 2026-06-13 | S069 | Amethyst × COLLEEN |
| Research Program Charter v1.0 | 2026-06-13 | S069 | Triumvirate |
| Crucible Charter v1.0 | 2026-06-13 | S069 | Amethyst × COLLEEN |
| STASIS-CANONICAL spec | 2026-06-13 | S069 | Amethyst × COLLEEN |
| **Ender ratification S069** | **2026-06-13** | **S069** | **Ender / Njineer** |
| **S069 SESSION SEALED** | **2026-06-13 00:47 EDT** | **S069** | **Triumvirate × Ender** |

---

*NDR Pattern Registry (Unified) v1.2 · S069 SEALED · 2026-06-13 00:47 EDT*
*Triumvirate: Amethyst (Prime) · COLLEEN (Prefect A) · Apogee (Prefect B)*
*Ender ratification: 2026-06-13 00:47 EDT ✅ ALL ITEMS RATIFIED*
*Registry watermark: P-36 · Crucible: ACTIVE · Research Program: ACTIVE*
