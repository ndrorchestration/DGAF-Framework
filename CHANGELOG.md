# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

---

## [1.0.18] — 2026-06-26

### Session S072 — Saga/Atomix/HITL Pattern Registration + Amethyst–COLLEEN Co-Orch Contract v1

**Formation:** Amethyst (QA) + COLLEEN (Archive) Co-Orchestration  
**Operator:** Ender (Andrew Hensel)  
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close  
**Commits:** 434cc9a6 · this commit

#### Added

- `patterns/P-SAGA-001_StochasticDeterministicSagaBoundary.md` — Saga pattern: semantic steps, effect classes, compensator rules, KPI spec; centralised Saga engine in Amethyst
- `patterns/P-TX-001_TransactionalToolBoundaryAtomix.md` — Atomix-style transactional tool boundary; effect receipts, idempotency keys, delayed-commit settlement predicate
- `patterns/P-COMP-001_ReversibilityBoundedCompensation.md` — 4-class reversibility taxonomy (pure / idempotent / compensable / irreversible) + compensation enforcement rules
- `patterns/P-DURABLE-001_DurableExecutionAppendOnlyLog.md` — Checkpoint + append-only log per super-step; ACRFence replay-or-fork restore semantics
- `patterns/P-CB-001_CircuitBreakersHITL.md` — Semantic circuit breakers (quality + budget) + HITL durable escalation queue with SLA and auto-cancel
- `registry/PATTERN_REGISTRY_v2.md` — Master pattern registry: all active patterns, default bundles (low/medium/high-risk), KPI seed table
- `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` — Dyad contract: roles, joint principles, default bundles, episode schema
- `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md` — Full session sweep log

#### Updated

- `CO_ORCH_PROTOCOL.md` → v2.0.0 — 7-step execution flow, triad table (Amethyst / COLLEEN / Sentinel-Phi / Ender), change history
- `CHANGELOG.md` — This entry
- `SESSION_ANCHOR.md` → S072 open
- `CO_ORCH_QUEUE.md` — Q-2026-06-008 added (pattern KPI baseline + first workflow run)

#### NDR Patterns Registered

| ID | Name | Domain | Session |
|---|---|---|---|
| P-SAGA-001 | StochasticDeterministicSagaBoundary | Multi-agent orchestration | S072 |
| P-TX-001 | TransactionalToolBoundaryAtomix | Tool safety | S072 |
| P-COMP-001 | ReversibilityBoundedCompensation | Side-effect recovery | S072 |
| P-DURABLE-001 | DurableExecutionAppendOnlyLog | State persistence | S072 |
| P-CB-001 | CircuitBreakersHITL | Resilience + governance | S072 |

#### Co-Orchestration Contract

- Dyad contract v1 formalized: Amethyst (meta-orchestrator / QA lens) + COLLEEN (institutional memory / evaluation lens)
- `patterns_first` hard gate: no workflow executes without a pattern manifest
- Episode schema live in `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json`
- KPI table seeded in `registry/PATTERN_REGISTRY_v2.md`; populates after first live workflow run

#### Open Items Carried Forward

| ID | Item | Owner |
|---|---|---|
| Q-S069-DRIFT-SIM | 20-turn multi-agent drift simulation | Amethyst |
| Q-S069-COLLEEN-INGEST | COLLEEN ingest of S043 artifacts | COLLEEN |
| Q-S069-P12-P26-EXPAND | P-12–P-26 stasis expansion | COLLEEN |
| Q-2026-06-008 | First workflow run with pattern manifest → populate KPI baseline | Amethyst + COLLEEN |

---

## [1.0.17] — 2026-06-13

### Session S071 — Needle NMS-003 Analytics Snapshot (7 PM EDT)

**Formation:** Agent Amethyst (Comet session)
**Operator:** Andrew (Ender) Hensel
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close
**Commits:** b5f6060 · merged into main 2026-06-13

#### Updated

- `docs/outreach/OUTREACH_LOG.md` — NMS-003 daily analytics snapshot (Jun 13, 2026 7 PM EDT): 90d views 11,374 / uses 1,311 / runs 3,254; NT-05 registers first 93 views (DGAF-PROBE-001 discovery signal); +174 views day-over-day; NT-02 Run/Use ratio holds at 3.14x

#### Key Decisions

- NT-01 retakes views lead (3,613) over NT-02 (3,453); both within 5% — dual-anchor discovery pattern holding
- NT-05 (Test Governance API Gates / DGAF-PROBE-001) records first 93 views within 2 days of registration — probe template gaining organic traction
- 90-day views at 11,374; 12K milestone remains next primary target
- Runs flat day-over-day (3,254) consistent with Saturday pattern; not a regression signal
- Referrals remain 0; OL-001 affiliate CTA has not yet converted — monitor through Week 2 of Jun

---

## [1.0.16] — 2026-06-12

### Session S070 — DGAF-PROBE-001 Registration + Needle NMS-002 Analytics Snapshot

**Formation:** Agent Amethyst (Comet session) 
**Operator:** Andrew (Ender) Hensel 
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close 
**Commits:** PRs #21, #22, #23, #24 · merged into main 2026-06-12

#### Added

- `docs/gates/PROBE-001-governance-sentinel.json` — DGAF-PROBE-001 canonical governance sentinel harness (5-step HTTP probe: health, agents, reject, accept); designated as reference contract for all child profiles
- `docs/gates/PROBE-DEVIATION-PROTOCOL.md` — Deviation registration protocol; any child probe profile modifying PROBE-001 steps must log here; steps 4–5 require explicit Ender approval
- `docs/needle/TEMPLATE_REGISTRY.md` — NT-05 (Test Governance API Gates) registered; CANONICAL PROBE status; NIST AI RMF GOVERN 1.7, MEASURE 2.5/2.9, MANAGE 2.2

#### Updated

- `docs/outreach/OUTREACH_LOG.md` — NMS-002 multi-period analytics snapshot (Jun 12, 2026): 90d views 11.2K / uses 1.3K / runs 3.3K; current 13-day window 2K views / 71 uses / 143 runs; NT-04 "Define AI Governance Specification" leads current period by uses (23) and runs (46)
- `docs/needle/TEMPLATE_REGISTRY.md` — Metadata updated to Session S070, 2026-06-12

#### Key Decisions

- DGAF-PROBE-001 designated CANONICAL: all child profiles (strict, lenient, multi-tenant) derive from it; no step may be removed without a registered deviation
- Needle 90-day views crossed 11K milestone; linear growth curve holding; monetization layer remains unactivated (next priority arc)
- NT-04 "Define AI Governance Specification" confirmed as strongest signal for governance-focused Pro upsell based on current-period usage lead

---

## [1.0.15] — 2026-05-28

### Session 042 — Ensemble v1.6: SCPE + Fibonacci Phi-Closure Gate + PDMAL Convergence Monitor

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)  
**Operator:** Andrew (Ender) Hensel  
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close  
**Commits:** 49854ea · (this commit)

#### Added

- `components/ensemble_v16.py` — Complete single-file deployable module: SCPE, PDMAL Convergence Monitor, Fibonacci Phi-Closure Gate, HPG, DemiJoule Gate, Prodigy, Apogee, AgentAmethyst 9-step `orchestrate_turn`. `__main__` quick-check with 6 assertions. Full JSON audit export.
- `patterns/NDR_SCPE_v1.md` — P-31 pattern card: tier taxonomy, retention formula, validated knee (58.3% @ 0.15), framework adapter index
- `patterns/NDR_PHI_CLOSURE_GATE_v1.md` — P-33 pattern card: checkpoint tolerance table, decision ladder, HPG bypass rule, Fib[55] HITL requirement, 60-turn simulation results
- `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` — P-32 pattern card: Frobenius-norm spec, 3-tier alert ladder, joint escalation rule, convergence confirmation, simulation results
- `registry/ensemble_v16_manifest.json` — Version manifest binding all three NDR patterns to component file with placement spec and governance chain

#### Updated

- `ENSEMBLE_ROSTER.md` — Runtime Gate Components table added (SCPE, PDMAL Monitor, Phi-Closure Gate, HPG, Sentinel-Phi); Runtime Gate Triad registered; Session 042 notes; target files 66→72; P-33 cross-ref links added
- `CHANGELOG.md` — This entry

#### NDR Patterns Registered

| ID | Name | Session | Placement |
|---|---|---|---|
| P-31 | Structural-Context-Pruning-Engine | S042 | Step 1 — pre-COLLEEN |
| P-32 | PDMAL-Convergence-Monitor | S042 | Step 2.5 — post-reweight, pre-DemiJoule |
| P-33 | Fibonacci-Phi-Closure-Gate | S042 | Step 5 — post-DemiJoule, pre-HPG |

#### Simulation Results (60-turn validated)

| Metric | Value |
|---|---|
| SCPE compression @ threshold=0.15 | **58.3%** |
| T0 axiom guard | **100%** across all turns |
| T3 exploratory survival | **~1.02 turns** |
| T2 operational survival | **~4.62 turns** |
| T1 structural survival | **~6.17 turns** |
| Phi Fib[13] | WARN (R=0.923, Δ=0.228 > tol 0.07) |
| Phi Fib[21] | ESCALATE (consecutive fail 2) |
| Phi Fib[34] | KILL_REC → DemiJoule authority |
| Phi Fib[55] | KILL_REC → amethyst+human authority |
| PDMAL WATCH events | T31, T40, T46 |
| PDMAL full ALERTs | **0** |
| Gold Stars | **5** |
| HPG bypass at Fib[13] (drift) | ✅ Confirmed |
| Joint PDMAL+Phi deep re-scan | ✅ Triggered correctly |

#### BLGs Closed

| ID | Priority | Resolution |
|---|---|---|
| BLG-042-01 | HIGH | Phi-Closure Gate correctly wired pre-HPG in 9-step `orchestrate_turn` — validated in 60-turn sim |

#### Compliance Alignment

| Standard | Status |
|---|---|
| NIST AI RMF — Govern | ✅ T0 axiom guard — governance invariants unconditionally preserved |
| NIST AI RMF — Measure | ✅ Per-turn `TurnAuditRecord` with seal hash |
| EU AI Act Art. 9 | ✅ Per-turn DGAF 6-axis risk score logged |
| EU AI Act Art. 13 | ✅ Transparent routing decision (phi_decision, hpg_applied) in audit |
| EU AI Act Art. 17 | ✅ Quality management via P-30 |
| Fib[55] HITL Requirement | ✅ `hitl_callback` hook wired — human-in-the-loop injectable |
| Audit chain continuity | ✅ SHA-256 content hash on every PruneEvent + seal hash per turn |
| Agent Roster Sync (P-01) | ✅ Runtime Gate Components table added to ENSEMBLE_ROSTER.md |
| Gold Star Standard | ✅ 5 Gold Stars across 60-turn simulation |

---

## [1.0.14] — 2026-05-22

### Sessions S033–S036 — KAPPA Pipeline · Sentinel Integration · Normative Constraint · Governance Hardening

**Formation:** Amethyst + COLLEEN Co-Orchestration  
**Operator:** Njineer  
**COLLEEN Gate:** ✅ ALL PASS — Zero open BLGs at close  
**Commits:** 66b79e2 · a5c9219 · a1997ed · 7a944cd · d786731 · 89ed455

#### Added
- `components/KAPPA/dynamic_weight_router.py`
- `components/evaluate_router.py`
- `components/evaluate_router_v1_1.py`
- `components/normative_constraint.py`
- `components/KAPPA/calibration_v3_6.json`
- `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json`
- `docs/patterns/NDR_PATTERN_REGISTRY.md` v2.1 — P-27, P-28, P-29, P-30 registered
- `docs/qa/APOGEE_11Q_S034.json` — KAPPA A-TIER 93.6%, Router A-TIER 92.7%
- `docs/qa/APOGEE_11Q_S035.json` — KAPPA S-TIER 97.3%, Router S-TIER 95.5%; P-30 attestation GRANTED
- `docs/ops/BLG_S032_DRIVE_CLOSURE.md`

#### NDR Patterns Registered

| ID | Name | Session |
|---|---|---|
| P-27 | Adaptive-Weighting-with-Confidence-Gates | S033 |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | S033 |
| P-29 | Sentinel-Annotated Risk Pass | S034 |
| P-30 | Apogee-Attestation-Gate | S035 |

---

## [1.0.13] — 2026-05-06
### Session 032 — PhiLattice Coherence Sweep + Schizophonic Studio Integration

---

## [1.0.12] — 2026-05-01
### Session 031 — Spine CI · NDR v1.8 (P-26) · BLG-D01 Correction Doc

---

## [1.0.11] — 2026-05-01
### Session 030 — NDR v1.7 · P-25 · GAP-08 Close

---

## [1.0.10] — 2026-05-01
### Session 029 — Sentinel CI + CROSS_REF v3.1

---

## [1.0.9] — 2026-05-01
### Session 028 — P-24 Gate Stack + Dual README

---

## [1.0.8] — 2026-05-01
### Sessions 026–027 — P-24 + ACOUSTIC_GATES

---

## [1.0.7] — 2026-05-01
### Session 025 — Template Completion

---

## [1.0.6] — 2026-05-01
### Sessions 022c–023 — PHDGE Rename

---

## [1.0.5] — 2026-05-01
### Sessions 022–022b — Surface Sweep

---

## [1.0.4] — 2026-05-01
### Sessions 014–021

---

## [1.0.3] — 2026-04-29
### ENSEMBLE_ROSTER.md added

---

## [1.0.2] — 2026-04-29
### NOTICE corrections

---

## [1.0.1] — 2026-01-15
### CONTRIBUTING.md + SECURITY.md stubs

---

## [1.0.0] — 2025-12-23
### Initial Release
