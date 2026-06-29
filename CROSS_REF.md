# CROSS_REF.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-06-29  
> **Anchor:** Post-S077 autonomous sprint — AHG/P-42 filing + P-35 collision fix

Canonical cross-reference index for patterns, files, agents, and ecosystem components.

> ⚠️ **Registry path:** All pattern references point to `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` (P-01 through P-42+).

---

## NDR Pattern Registry

**Canonical source:** [`docs/NDR_PATTERN_REGISTRY_UNIFIED.md`](docs/NDR_PATTERN_REGISTRY_UNIFIED.md)

| Pattern ID | Name | Layer | Status |
|---|---|---|---|
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | 1 — Trace & Audit | ✅ Stable |
| P-02 | Async-Persist Ring Buffer | 1 — Trace & Audit | ✅ Stable |
| P-03 | Governance Contract Test | 2 — Testing & CI | ✅ Stable |
| P-04 | Parametrized Corpus | 2 — Testing & CI | ✅ Stable |
| P-05 | Tri-Phase CI Gate | 2 — Testing & CI | ✅ Stable |
| P-06 | Topology × Orchestration Matrix Lab | 3 — Architecture Lab | ✅ Stable |
| P-07 | Dual-Agent Persistent Sweep Loop | 4 — Governance Formation | ✅ Stable |
| P-08 | Triad Taxonomy | 4 — Governance Formation | ✅ Stable |
| P-09 | Triumvirate Mandate Schema | 4 — Governance Formation | ✅ Stable |
| P-10 | Session Graduation Check | 4 — Governance Formation | ✅ Stable |
| P-11 | 11Q Attestation Scoring | 5 — Quality Gate | ✅ Stable |
| P-12–P-26 | Stasis Patterns (133 entries) | 6 — Stasis | ✅ STASIS-CANONICAL |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | 7 — Router Calibration | ✅ Stable |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | 7 — Router Calibration | ✅ Stable |
| P-29 | Sentinel-Annotated Risk Pass | 8 — Safety & Sentinel | ✅ Stable |
| P-30 | Apogee-Attestation-Gate | 5 — Quality Gate | ✅ Stable |
| P-31 | SCPE — Structural Context Pruning Engine | 9 — Long-Context Safety | ✅ Locked |
| P-32 | Fibonacci Phi-Closure Gate | 9 — Long-Context Safety | ✅ Wired |
| P-33 | PDMAL Convergence Monitor | 9 — Long-Context Safety | ✅ Stable |
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | 7 — Router Calibration | ✅ A-TIER |
| **P-35** | **Procluding Premise Gate** | **0 — Pre-Admissibility** | **✅ CANONICAL — Ender ratified S069** |
| P-36 | Gate Priority Schema | 0.5 — Stack Architecture | ✅ CANONICAL — Ender ratified S069 |
| P-37 | Stochastic-Deterministic Saga Boundary | 10 — Resilience & Recovery | ✅ Registered S071 |
| P-38 | Circuit-Breaker with HITL Escalation | 10 — Resilience & Recovery | ✅ Registered S071 |
| P-39 | ACRFence — Atomic Checkpoint-Restore with Effect Fence | 10 — Resilience & Recovery | ✅ Registered S071 |
| P-40 | Atomix — Transactional Tool Boundary | 11 — Transactional Integrity | ✅ Registered S071 |
| P-41 | Sentinel-Phi HITL Durable Queue | 11 — Transactional Integrity | ✅ Registered S071 |
| **P-42** | **Adaptive Harmonic Governance (AHG)** | **12 — Cognitive Control Plane** | **🟡 Specified — Implementation Pending** |

---

## AHG Vocabulary Index — P-42 (Added 2026-06-29)

> Source: [docs/theory/AHG_ARCHITECTURE.md](docs/theory/AHG_ARCHITECTURE.md) | [patterns/P-42_AHG.md](patterns/P-42_AHG.md)

| Term | Symbol | Definition |
|---|---|---|
| Cognitive Phase Energy | φ | Central governance signal — continuous measure of the collective harmonic regime. Extends P-32 from binary to continuous. |
| Phase Velocity | v_φ | Directional rate of change of φ |
| Phase Acceleration | a_φ | Second derivative — enables predictive intervention before threshold breach |
| State Vector | x_t | D, N, C, R, M, K (Divergence, Novelty, Constraint Pressure, Revision Pressure, Governance Momentum, Coherence) |
| Productive Divergence | D_p | Useful disagreement that increases Mission Utility J — to be preserved |
| Destabilizing Entropy | D_e | Harmful disagreement leading to hallucination or deadlock — to be suppressed |
| Conductor Archetype | — | Governance regime selector: Executor, Explorer, Sentinel, Synthesizer, Auditor, Tribunal |
| Phase Intent | I_t | Broadcast packet (mode, weights, constraints, TTL) issued by the Conductor |
| Compliance Coefficient | α_i | Per-agent conformance weight: π_i' = (1−α_i)π_i + α_i·I_t |
| Mission Utility Function | J | λ_Q·Q + λ_E·E + λ_N·N + λ_S·S − λ_G·G |
| Recovery Score | R_c | Tribunal exit criterion |
| Governance Momentum | M | Hysteresis term preventing mode thrashing |
| Hysteresis Band | — | Threshold buffer — φ must cross band for ≥2 turns before archetype transition fires |
| Sidecar Monitor | — | O(n) observability — reads Heartbeat signals only, not full agent context |
| Heartbeat | — | Compressed cognitive signal emitted by each agent to the Sidecar Monitor |
| MPHG | — | Model Predictive Harmonic Governance — P-42 v2.0 roadmap |
| Cognitive Control Plane | — | Governance abstraction above task execution — answers "what mode should the collective operate in?" |

---

## Conductor Archetype × Agent Mapping (P-42)

| Archetype | DGAF Agent | Primary Bias |
|---|---|---|
| Executor | Professor Prodigy | Low novelty, precision execution |
| Explorer | Herald | High novelty, hypothesis generation |
| Sentinel | DemiJoule | Validation, constraint enforcement |
| Synthesizer | Herald / COLLEEN | Integration, coherence |
| Auditor | Apogee Lens | Contradiction discovery, logic review |
| Tribunal | Amethyst | Convergence, de-escalation, failure resolution |

---

## AHG φ Range Reference (P-42)

| φ Range | Energy Level | Cognitive Mode | DGAF Notes |
|---|---|---|---|
| 1.0 – 1.15 | Low | Convergent / Execution | Executor archetype preferred |
| 1.15 – 1.45 | Medium | Adaptive / Vigilant | Sentinel or Synthesizer |
| 1.45 – 1.70 | High | Divergent / Exploratory | Explorer; NDR-STASIS anchor φ=1.618 sits here |
| > 1.70 | Extreme | Unstable / Tension | Tribunal required |

---

## Turn Sequence Cross-Reference

| Step | Gate / Component | Pattern | File | Notes |
|---|---|---|---|---|
| 0 | Procluding Premise Gate | P-35 | `docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md` | Pre-admissibility; Ender ratified S069 |
| 1 | SCPE.prune() | P-31 | `scpe_ensemble_v14.py` | T0 immune |
| 2 | COLLEEN.schema_diff_check() | P-04 | `colleen_schema_diff.py` | SHA-256 state hash |
| 3 | RECIPROCITY.arbitrate() | P-06 | `reciprocity_arbiter.py` | PDMAL reweight |
| 4 | DEMIJOUL.safety_gate() | P-03 | `dgaf_semantic_gate.py` | Layer1 syntactic, Layer2 DGAF 6-axis |
| 5 | PHI-CLOSURE GATE | P-32 | `phi_closure_gate.py` | Fib[13,21,34,55]; φ*=0.618; ±0.05 |
| 6 | HPG.gate() | P-29 | `hpg_ionian_gate.py` | Only if Phi-closure PASS |
| 7 | PRODIGY.verify() | P-05 | `prodigy_verifier.py` | Mandatory on conf<0.85 |
| 8 | APOGEE.review_artifact_seal() | P-30 | `amethyst_dual_lock.py` | Evidence grade → Gold Star gate |
| 9 | AMETHYST.seal() | P-08 | `orchestration_firewall.py` | SHA-256 TurnAuditRecord → audit_log |
| 10 | AHG.phase_observe() | P-42 (future) | `ahg_conductor.py` (planned) | φ estimation, archetype dispatch, Phase Intent broadcast |

---

## File Index

### Root

| File | Purpose | Steward |
|---|---|---|
| `SESSION_ANCHOR.md` | Live session state, objectives, agent register | COLLEEN |
| `CO_ORCH_QUEUE.md` | Active experiment and work queue | COLLEEN |
| `SWEEP_LOG/` | QA sweep history | COLLEEN |
| `CROSS_REF.md` | This file — canonical cross-reference index | COLLEEN |
| `ENSEMBLE_ROSTER.md` | Agent roster, roles, KB scopes | COLLEEN |
| `CHANGELOG.md` | Version history | COLLEEN |
| `DEFERRED_ITEMS.md` | Snoozed owner-action items S-01–S-08 | Amethyst |
| `README.md` | Public overview | Herald |
| `README.governance.md` | Governance architecture | Amethyst |
| `README.technical.md` | Technical implementation | Reson |

### docs/

| File | Purpose | Status |
|---|---|---|
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | Unified registry SSoT (P-01–P-42+) | ✅ Provenance entry added 2026-06-29 |
| `docs/ndr_patterns_unified.json` | Machine-readable index | ✅ v2.2 — P-37–P-42 entries added 2026-06-29 |
| `docs/NDR_PATTERN_REGISTRY.md` | Redirect stub | ✅ PR-D S067 |
| `docs/lifecycle_harness_v2.md` | Lifecycle phase harness spec | ✅ Created S067 |
| `docs/ECOSYSTEM_INVENTORY.md` | Cross-platform inventory | ✅ Updated 2026-06-29 |
| `docs/DGAF_RECURSIVE_REFINEMENT_ANALYSIS.md` | Recursive refinement analysis v2 | ✅ 2026-06-29 |

### docs/theory/

| File | Purpose | Status |
|---|---|---|
| `docs/theory/AHG_ARCHITECTURE.md` | P-42 full specification — AHG control-theoretic architecture | ✅ v1.1 — P-42 renumber 2026-06-29 |

### docs/agents/

| File | Purpose | Status |
|---|---|---|
| `docs/agents/PROFESSOR_PRODIGY_KB.md` | Professor Prodigy 3-tier KB | ✅ Filed 2026-06-29 |

### docs/qa/

| File | Purpose | Status |
|---|---|---|
| `docs/qa/APOGEE_11Q_P34.json` | P-34 attestation — A-TIER 94.5% | ✅ Ender ratified S066 |
| `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md` | Stasis audit — CONDITIONAL PASS | ✅ Ender ratified S066 |

### components/

| File | Pattern | Status |
|---|---|---|
| `scpe_ensemble_v14.py` | P-31 | ✅ Locked |
| `phi_closure_gate.py` | P-32 | ✅ Wired |
| `hpg_ionian_gate.py` | P-29 | ✅ Stable |
| `orchestration_firewall.py` | P-08 | ✅ Active |
| `topology_router.py` | P-27 | ✅ v3.6.0 |
| `dgaf_semantic_gate.py` | P-03 | ✅ Stable |
| `amethyst_dual_lock.py` | P-30 | ✅ Stable |
| `dynamic_weight_router.py` | P-34 | ✅ Confirmed S066 |
| `ahg_conductor.py` | P-42 | 🔴 Planned |
| `ahg_sidecar.py` | P-42 Sidecar Monitor | 🔴 Planned |

### patterns/

| File | Purpose | Status |
|---|---|---|
| `NDR_SCPE_v1.md` | P-31 card | ✅ Archived |
| `NDR_PHI_CLOSURE_GATE_v1.md` | P-32 card | ✅ Archived |
| `NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` | P-33 card | ✅ Archived |
| `P-42_AHG.md` | P-42 — Adaptive Harmonic Governance | ✅ Filed 2026-06-29 (renumbered from P-35) |
| ~~`P-35_AHG.md`~~ | Stale file — superseded by P-42_AHG.md | ⚠️ Needs deletion |

---

## Agent × Pattern Matrix

| Agent | Patterns Owned / Enforced |
|---|---|
| Amethyst | P-08, P-09, P-10, P-30, P-42 (Tribunal archetype) |
| COLLEEN | P-02, P-04, P-07, all registry/archive patterns |
| Sentinel-Phi / DemiJoule | P-32, P-29, P-05, P-42 (Sentinel archetype) |
| Reciprocity | P-06, arbitration logic |
| Sonar | Evidence grounding for all patterns |
| Reson | P-27, P-28, P-33 |
| Prodigy | P-03, P-42 (Executor archetype) |
| Apogee | P-11, P-30, P-34 attestation, P-42 (Auditor archetype) |
| Herald | P-01, P-42 (Explorer + Synthesizer archetype) |

---

## State Anchor Cross-Reference

| Goal | Enforced By | File | Status |
|---|---|---|---|
| zero_open_blg | Orchestration Firewall | `orchestration_firewall.py` | ✅ 0 BLGs — S067 sealed |
| single_authority_chain | `authority_chain_valid()` | `orchestration_firewall.py` | ✅ Active |
| append_only_log | Rollback on invariant failure | `orchestration_firewall.py` | ✅ Active |
| observable_invariants_only | All invariants tested at boundary | `test_orchestration_firewall.py` | ✅ Active |
| procluding_premise_first | SCPE.ingest() tier classification | `scpe_ensemble_v14.py` | ✅ Active |
| phi_range_monitoring | AHG Sidecar Monitor (planned) | `ahg_conductor.py` (planned) | 🔴 P-42 v1.2 |

---

## Eval Terminology Index — S068

| Term | Definition | Maps To | File | Issue |
|------|-----------|---------|------|-------|
| `role_boundary_coherence` | % correct role identification at turn N in 50-turn triadic trace | RULER 1M / AA-LCR | `tests/dgaf_eval_suite.py` | #32 |
| `contraction_proof_fidelity` | % of kernel specs where eigvals confirms spectral radius < 1.0 | GPQA Diamond (87.9%) | `tests/dgaf_eval_suite.py` | #32 |
| `governance_schema_conformance` | % fuzz-generated governance.yml variants passing Pydantic extra=forbid | IFBench / MMLU-Pro | `tests/dgaf_eval_suite.py` | #32 |
| `audit_hallucination_rate` | Field-level accuracy of Herald audit events vs ground truth | OmniScience Non-Hallucination | `tests/dgaf_eval_suite.py` | #32 |
| `taubench_banking_mitigation` | % correct Sentinel escalation on financial compliance tasks | TauBench Banking (22.6% ⚠️) | `tests/dgaf_eval_suite.py` | #32 |
| `DGAF_EVAL_TASKS` | Top-level registry dict in dgaf_eval_suite.py | — | `tests/dgaf_eval_suite.py` | #32 |
| `thinking_tokens` | Per-role reasoning budget for Nemotron 3 Ultra | — | `dgaf_nemotron_client.py` | #32 |

---

*CROSS_REF v4.4 · 2026-06-29 · P-42 AHG registered (renumbered from collision P-35) · P-35–P-41 added to registry table · COLLEEN + Amethyst*
