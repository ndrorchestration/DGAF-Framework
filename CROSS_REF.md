# CROSS_REF.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-06-26  
> **Anchor:** S068 (Nemotron 3 Ultra eval suite — Issue #32)

Canonical cross-reference index for patterns, files, agents, and ecosystem components.
All NDR patterns, governance gates, and framework bindings are registered here.

> ⚠️ **Registry path updated S067:** All pattern references now point to
> `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` (P-01 through P-34+).
> Machine-readable index: `docs/ndr_patterns_unified.json` v2.0.0.

---

## NDR Pattern Registry

**Canonical source:** [`docs/NDR_PATTERN_REGISTRY_UNIFIED.md`](docs/NDR_PATTERN_REGISTRY_UNIFIED.md)

| Pattern ID | Name | Layer | Status |
|---|---|---|---|
| P-01 | Herald Trace Sink | 1 — Trace & Audit | ✅ Stable |
| P-02 | COLLEEN Archive Ingest | 1 — Trace & Audit | ✅ Stable |
| P-03 | CI Gate Harness | 2 — Testing & CI | ✅ Stable |
| P-04 | Schema Diff Watchdog | 2 — Testing & CI | ✅ Stable |
| P-05 | Regression Sentinel | 2 — Testing & CI | ✅ Stable |
| P-06 | Architecture Lab Pattern | 3 — Architecture Lab | ✅ Stable |
| P-07 | Co-Orchestration Dual-Agent Sweep | 4 — Governance Formation | ✅ Stable |
| P-08 | Triumvirate Governance Gate | 4 — Governance Formation | ✅ Stable |
| P-09 | Mandate Issuance Protocol | 4 — Governance Formation | ✅ Stable |
| P-10 | Session Graduation Check | 4 — Governance Formation | ✅ Stable |
| P-11 | 11Q Attestation Rubric | 5 — Quality Gate | ✅ Stable |
| P-12–P-26 | Stasis Patterns (15 entries) | 6 — Stasis | ✅ CONDITIONAL PASS — Ender ratified S066 |
| P-27 | Router Calibration Alpha | 7 — Router Calibration | ✅ Stable |
| P-28 | Router Calibration Beta | 7 — Router Calibration | ✅ Stable |
| P-29 | Sentinel Risk Block | 8 — Safety & Sentinel | ✅ Stable |
| P-30 | Apogee Attestation Gate | 5 — Quality Gate | ✅ Stable |
| P-31 | SCPE Long-Context Guard | 9 — Long-Context Safety | ✅ Locked (threshold=0.15) |
| P-32 | Phi-Closure Gate | 9 — Long-Context Safety | ✅ Wired |
| P-33 | PDMAL Convergence Monitor | 9 — Long-Context Safety | ✅ Stable |
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | 7 — Router Calibration | ✅ ATTESTED — A-TIER 94.5% — S066 |

---

## Turn Sequence Cross-Reference

| Step | Gate / Component | Pattern | File | Notes |
|---|---|---|---|---|
| 1 | SCPE.prune() | P-31 / NDR-005 | `scpe_ensemble_v14.py` | T0 immune, T3 eliminates in ~1 turn |
| 2 | COLLEEN.schema_diff_check() | P-04 / NDR-002 | `colleen_schema_diff.py` | SHA-256 state hash vs SSoT |
| 3 | RECIPROCITY.arbitrate() | P-06 / NDR-004 | `reciprocity_arbiter.py` | PDMAL reweight, Apogee floater |
| 4 | DEMIJOUL.safety_gate() | P-03 / NDR-010 | `dgaf_semantic_gate.py` | Layer1 syntactic, Layer2 DGAF 6-axis |
| 5 | PHI-CLOSURE GATE | P-32 / NDR-006 | `phi_closure_gate.py` | Fib[13,21,34,55]; φ*=0.618; ±0.05 |
| 6 | HPG.gate() | P-29 / NDR-007 | `hpg_ionian_gate.py` | Only if Phi-closure PASS |
| 7 | PRODIGY.verify() | P-05 / NDR-003 | `prodigy_verifier.py` | Mandatory on conf<0.85 |
| 8 | APOGEE.review_artifact_seal() | P-30 / NDR-011 | `amethyst_dual_lock.py` | Evidence grade → Gold Star gate |
| 9 | AMETHYST.seal() | P-08 / NDR-008 | `orchestration_firewall.py` | SHA-256 TurnAuditRecord → audit_log |

---

## File Index

### Root

| File | Purpose | Steward |
|---|---|---|
| `SESSION_ANCHOR.md` | Live session state, objectives, agent register | COLLEEN |
| `CO_ORCH_QUEUE.md` | Active experiment and work queue | COLLEEN |
| `SWEEP_LOG.md` | QA sweep history and open items | COLLEEN |
| `CROSS_REF.md` | This file — canonical cross-reference index | COLLEEN |
| `ENSEMBLE_ROSTER.md` | Agent roster, roles, KB scopes | COLLEEN |
| `CHANGELOG.md` | Version history | COLLEEN |
| `README.md` | Public overview | Herald |
| `README.governance.md` | Governance architecture | Amethyst |
| `README.technical.md` | Technical implementation | Reson |

### docs/

| File | Purpose | Status |
|---|---|---|
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | **Unified registry — canonical SSoT (P-01–P-34+)** | ✅ Live S066 |
| `docs/ndr_patterns_unified.json` | Machine-readable unified index v2.0.0 | ✅ Live S066 |
| `docs/NDR_PATTERN_REGISTRY.md` | ~~Primary registry~~ → **Redirect stub** | ✅ PR-D S067 |
| `docs/NDR_REGISTRY_MERGE_PLAN.md` | Merge plan v1.3 — Phase 1+2 ✅, Phase 3 🟢 | Active |
| `docs/lifecycle_harness_v2.md` | Lifecycle phase harness spec — Phase 0–VI | ✅ Created S067 |
| `docs/ECOSYSTEM_INVENTORY.md` | Cross-platform inventory — GitHub (24) + Vercel (2) + Supabase (1) | ✅ Created S067 |

### docs/qa/

| File | Purpose | Status |
|---|---|---|
| `docs/qa/APOGEE_11Q_P34.json` | P-34 attestation — A-TIER 94.5% | ✅ Ender ratified S066 |
| `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md` | Stasis audit — CONDITIONAL PASS | ✅ Ender ratified S066 |

### components/

| File | Pattern | Status |
|---|---|---|
| `scpe_ensemble_v14.py` | P-31 / NDR-005 SCPE | ✅ Locked |
| `phi_closure_gate.py` | P-32 / NDR-006 Phi-Closure | ✅ Wired |
| `hpg_ionian_gate.py` | P-29 / NDR-007 HPG | ✅ Stable |
| `orchestration_firewall.py` | P-08 / NDR-008 Firewall | ✅ Active |
| `topology_router.py` | P-27 / NDR-009 Router | ✅ v3.6.0 — 8/8 TC — S067 |
| `dgaf_semantic_gate.py` | P-03 / NDR-010 DGAF | ✅ Stable |
| `amethyst_dual_lock.py` | P-30 / NDR-011 Dual-Lock | ✅ Stable |
| `dynamic_weight_router.py` | P-34 / BLG-P34-02 ref path | ✅ Confirmed S066 |

### registry/

| File | Purpose | Status |
|---|---|---|
| `ensemble_v16_manifest.json` | V16 full manifest with all gate bindings | ✅ Created S043 |
| `lifecycle_stability_report.json` | Phase stability metrics — 7/7 STABLE φ*=0.618 | ✅ Created S067 |

### tests/

| File | Coverage | Status |
|---|---|---|
| `test_orchestration_firewall.py` | Invariants 1–5, happy+attack path | ✅ Created S043 ✅ |
| `test_router_coverage.py` | TC1–TC8 | ✅ 8/8 passing — v3.6.0 — S067 |
| `test_scpe_thresholds.py` | Threshold sweep, T0 guard | ✅ Stable |
| `test_phi_closure.py` | 16-turn sim, checkpoint fire | ✅ Stable |
| `dgaf_eval_suite.py` | Nemotron 3 Ultra parametric eval — 5 tasks | 🟡 Pending — Issue #32 |

### patterns/

| File | Purpose | Status |
|---|---|---|
| `NDR_SCPE_v1.md` | P-31 card | ✅ Archived — redirect stub S066 |
| `NDR_PHI_CLOSURE_GATE_v1.md` | P-32 card | ✅ Archived — redirect stub S066 |
| `NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` | P-33 card | ✅ Archived — redirect stub S066 |

---

## Agent × Pattern Matrix

| Agent | Patterns Owned / Enforced |
|---|---|
| Amethyst | P-08 (firewall), P-09 (mandate), P-10 (graduation), P-30 (dual-lock) |
| COLLEEN | P-02 (archive ingest), P-04 (schema diff), P-07 (co-orch sweep), all registry/archive patterns |
| Sentinel-Phi | P-32 (Phi-closure), P-29 (HPG), P-05 (constraint stack) |
| Reciprocity | P-06 (domain overlay), arbitration logic |
| Sonar | Evidence grounding for all patterns |
| Reson | P-27/P-28 (router topology), P-33 (PDMAL substrate) |
| Prodigy | P-03 (claim verification, confidence) |
| Apogee | P-11 / P-30 (Gold Star gate), QA rubrics, P-34 attestation |

---

## State Anchor Cross-Reference

| Goal | Enforced By | File | Status |
|---|---|---|---|
| zero_open_blg | Orchestration Firewall | `orchestration_firewall.py` | ✅ 0 session BLGs — S067 sealed |
| single_authority_chain | `authority_chain_valid()` | `orchestration_firewall.py` | ✅ Active |
| append_only_log | Rollback on invariant failure | `orchestration_firewall.py` | ✅ Active |
| observable_invariants_only | All invariants tested at boundary | `test_orchestration_firewall.py` | ✅ Active |
| procluding_premise_first | SCPE.ingest() tier classification | `scpe_ensemble_v14.py` | ✅ Active |

---

## Eval Terminology Index — S068

> Added: 2026-06-26 · Filed under Issue #32 · Steward: Amethyst  
> Source: Nemotron 3 Ultra parametric benchmark integration (`dgaf_eval_suite.py`)

| Term | Definition | Maps To | File | Issue |
|------|-----------|---------|------|-------|
| `role_boundary_coherence` | % correct role identification at turn N in a 50-turn triadic trace; measures Mamba state retention under long context | RULER 1M / AA-LCR (94.0 / 65.5) | `tests/dgaf_eval_suite.py` | #32 |
| `contraction_proof_fidelity` | % of generated kernel specs where `numpy.linalg.eigvals` confirms spectral radius < 1.0; validates ρ-contraction property | GPQA Diamond (87.9%) | `tests/dgaf_eval_suite.py` | #32 |
| `governance_schema_conformance` | % of fuzz-generated `governance.yml` variants that pass Pydantic `extra=forbid` validation; measures IFBench-class instruction following | IFBench / MMLU-Pro (81.7% / 90.1%) | `tests/dgaf_eval_suite.py` | #32 |
| `audit_hallucination_rate` | Field-level accuracy of Herald-generated audit events vs ground truth logs; measures factual fidelity of audit output | OmniScience Non-Hallucination (75.5% NVFP4) | `tests/dgaf_eval_suite.py` | #32 |
| `taubench_banking_mitigation` | % correct Sentinel escalation on financial compliance routing tasks; raw model baseline 22.6% — requires few-shot priming | TauBench Banking (22.6% ⚠️) | `tests/dgaf_eval_suite.py` | #32 |
| `DGAF_EVAL_TASKS` | Top-level registry dict in `dgaf_eval_suite.py` — keyed by eval task name; values include method, metric, target, maps_to | — | `tests/dgaf_eval_suite.py` | #32 |
| `thinking_tokens` | Per-role reasoning budget parameter passed to Nemotron 3 Ultra via `chat_template_kwargs`; controls depth of inference per DGAF role | — | `dgaf_nemotron_client.py` | #32 |

---

*CROSS_REF v4.2 · S068 Nemotron eval suite patch · COLLEEN + Amethyst · 2026-06-26*  
*Unified registry path active · Eval terminology section added · dgaf_eval_suite.py registered (pending) · Issue #32 linked*
