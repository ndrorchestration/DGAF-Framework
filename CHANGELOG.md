# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

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
| EU AI Act Art. 17 | ✅ Gold Star gate via Apogee S-Tier review |
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
- `components/KAPPA/dynamic_weight_router.py` — DGAF-GATE-KAPPA-v3.5; per-input category detection, confidence-gated weight selection; 100-pass validation 95% accuracy
- `components/evaluate_router.py` — DGAF-EVALUATE-ROUTER-v1.0; raw_batch → KAPPA detect → apply_weights → ranked report
- `components/evaluate_router_v1_1.py` — Sentinel integration; `sentinel_review()` at 3 hook points; `p10_deontic_gate()`; per-record audit log (EU AI Act Art.9)
- `components/normative_constraint.py` — Full `NormativeConstraint` class; deontic logic (permitted / obligated / forbidden / escalate); score_ceiling optimization constraint; epistemic integrity meta-constraint
- `components/KAPPA/calibration_v3_6.json` — KAPPA v3.6; `governance_clear` 100% (STRONG=0.22, BLENDED=0.18)
- `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` — CPU-compliant component card
- `docs/patterns/NDR_PATTERN_REGISTRY.md` v2.1 — P-27, P-28, P-29, P-30 registered; 30 named + 133 stasis
- `docs/qa/APOGEE_11Q_S034.json` — KAPPA A-TIER 93.6%, Router A-TIER 92.7%
- `docs/qa/APOGEE_11Q_S035.json` — KAPPA S-TIER 97.3%, Router S-TIER 95.5%; P-30 attestation GRANTED
- `docs/ops/BLG_S032_DRIVE_CLOSURE.md` — S032-DRIVE closure; all 4 Drive templates executed

#### Updated
- `SESSION_ANCHOR.md` → S036 (zero open BLGs)
- `SWEEP_LOG.md` → S033–S035 wave sealed

#### NDR Patterns Registered

| ID | Name | Session |
|---|---|---|
| P-27 | Adaptive-Weighting-with-Confidence-Gates | S033 |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | S033 |
| P-29 | Sentinel-Annotated Risk Pass | S034 |
| P-30 | Apogee-Attestation-Gate | S035 |

#### BLGs Closed

| ID | Priority | Resolution |
|---|---|---|
| S033-BLG-01 | HIGH | `governance_clear` 100% — KAPPA v3.6 |
| S033-BLG-02 | LOW | `p10_deontic_gate()` wired |
| S033-BLG-03 | LOW | Apogee 11Q S-TIER both components |
| S032-DRIVE | MEDIUM | Njineer executed all 4 Drive templates (P-01, P-20) |

#### Compliance Alignment

| Standard | Status |
|---|---|
| NIST AI RMF — Measure | ✅ Per-record audit log |
| NIST AI RMF — Govern | ✅ P-10 deontic gate + P-30 attestation |
| EU AI Act Art. 9 | ✅ Risk management per-record log |
| EU AI Act Art. 13 | ✅ Transparent routing decision log |
| EU AI Act Art. 17 | ✅ Quality management via P-30 |
| Normative Constraint (P-10) | ✅ Full NormativeConstraint class |
| Gold Star Standard | ✅ S-TIER — KAPPA 97.3% · Router 95.5% |
| Drive–GitHub Sync (P-20) | ✅ |
| Agent Roster Sync (P-01) | ✅ |

---

## [1.0.13] — 2026-05-06

### Session 032 — PhiLattice Coherence Sweep + Schizophonic Studio Integration

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)  
**Operator:** Amethyst (Meta-Orchestrator) + COLLEEN (Institutional Anchor)  
**COLLEEN 1-1-1-1 Gate:** ✅ ALL PASS — 0 Hz Ionian Mode

#### Added
- `docs/agents/colleen-l5-governance-protocol.md`
- `docs/architecture/platinum-convergence-audit-v1.md`
- `docs/frameworks/awcp-symphony-cross-ref.md`
- `docs/agents/canonical-agent-registry.md`
- `docs/governance/ndr-pattern-registry-v3.md`
- `SWEEP_LOG.md` — Session 032 entry

#### Updated
- `README.md` — Brand corrected, PhiLattice links added
- `ENSEMBLE_ROSTER.md` — Schizophonic Studio trio added
- `CONTRIBUTING.md` — PhiLattice attribution

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
