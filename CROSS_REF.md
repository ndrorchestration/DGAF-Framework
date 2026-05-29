# CROSS_REF.md

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Last updated:** 2026-05-29  
> **Anchor:** S043

Canonical cross-reference index for patterns, files, agents, and ecosystem components.
All NDR patterns, governance gates, and framework bindings are registered here.

---

## NDR Pattern Registry

| Pattern ID | Name | File | Turn Sequence Step | Status |
|---|---|---|---|---|
| NDR-001 | PDMAL Convergence Proof | `components/pdmal_convergence.py` | Pre-turn (substrate) | ✅ Stable |
| NDR-002 | Semantic Control-Plane Translation | `docs/semantic_controlplane.md` | N/A (design pattern) | ✅ Stable |
| NDR-003 | Governance-First Constraint Stack | `components/governance_stack.py` | Steps 4–6 | ✅ Stable |
| NDR-004 | Domain Expert Governance Overlay | `components/domain_overlay.py` | Step 3 | ✅ Stable |
| NDR-005 | Structural Context Pruning Engine (SCPE) | `components/scpe_ensemble_v14.py` | Step 1 | ✅ Locked (threshold=0.15) |
| NDR-006 | Fibonacci Phi-Closure Gate | `components/phi_closure_gate.py` | Step 5 | ✅ Wired |
| NDR-007 | HPG Ionian Gate | `components/hpg_ionian_gate.py` | Step 6 | ✅ Stable |
| NDR-008 | Orchestration Firewall | `components/orchestration_firewall.py` | All steps (boundary) | ✅ Active |
| NDR-009 | Topology Router | `components/topology_router.py` | Post-HPG | 🔄 TC1/TC2/TC7/TC8 bug |
| NDR-010 | DGAF 6-Axis Semantic Scoring | `components/dgaf_semantic_gate.py` | Step 4 | ✅ Stable |
| NDR-011 | Amethyst Dual-Lock | `components/amethyst_dual_lock.py` | Step 8 | ✅ Stable |
| NDR-012 | Lifecycle Phase Harness | `docs/lifecycle_harness_v2.md` | Meta (lifecycle) | 🔄 In Progress |

---

## Turn Sequence Cross-Reference

| Step | Gate / Component | Pattern | File | Notes |
|---|---|---|---|---|
| 1 | SCPE.prune() | NDR-005 | `scpe_ensemble_v14.py` | T0 immune, T3 eliminates in ~1 turn |
| 2 | COLLEEN.schema_diff_check() | NDR-002 | `colleen_schema_diff.py` | SHA-256 state hash vs SSoT |
| 3 | RECIPROCITY.arbitrate() | NDR-004 | `reciprocity_arbiter.py` | PDMAL reweight, Apogee floater |
| 4 | DEMIJOUL.safety_gate() | NDR-010 | `dgaf_semantic_gate.py` | Layer1 syntactic, Layer2 DGAF 6-axis |
| 5 | PHI-CLOSURE GATE | NDR-006 | `phi_closure_gate.py` | Fib[13,21,34,55]; φ*=0.618; ±0.05 |
| 6 | HPG.gate() | NDR-007 | `hpg_ionian_gate.py` | Only if Phi-closure PASS |
| 7 | PRODIGY.verify() | NDR-003 | `prodigy_verifier.py` | Mandatory on conf<0.85 |
| 8 | APOGEE.review_artifact_seal() | NDR-011 | `amethyst_dual_lock.py` | Evidence grade → Gold Star gate |
| 9 | AMETHYST.seal() | NDR-008 | `orchestration_firewall.py` | SHA-256 TurnAuditRecord → audit_log |

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

### components/

| File | Pattern | Status |
|---|---|---|
| `scpe_ensemble_v14.py` | NDR-005 SCPE | ✅ Locked |
| `phi_closure_gate.py` | NDR-006 Phi-Closure | ✅ Wired |
| `hpg_ionian_gate.py` | NDR-007 HPG | ✅ Stable |
| `orchestration_firewall.py` | NDR-008 Firewall | ✅ Active |
| `topology_router.py` | NDR-009 Router | 🔄 Bug TC1/2/7/8 |
| `dgaf_semantic_gate.py` | NDR-010 DGAF | ✅ Stable |
| `amethyst_dual_lock.py` | NDR-011 Dual-Lock | ✅ Stable |

### registry/

| File | Purpose | Status |
|---|---|---|
| `ensemble_v16_manifest.json` | V16 full manifest with all gate bindings | ✅ Created S043 |
| `lifecycle_stability_report.json` | Phase stability metrics | 🔄 Pending |

### tests/

| File | Coverage | Status |
|---|---|---|
| `test_orchestration_firewall.py` | Invariants 1–5, happy+attack path | ✅ Created S043 |
| `test_router_coverage.py` | TC1–TC8 | 🔄 TC1/2/7/8 failing |
| `test_scpe_thresholds.py` | Threshold sweep, T0 guard | ✅ Stable |
| `test_phi_closure.py` | 16-turn sim, checkpoint fire | ✅ Stable |

---

## Agent × Pattern Matrix

| Agent | Patterns Owned / Enforced |
|---|---|
| Amethyst | NDR-008 (firewall), NDR-011 (dual-lock), NDR-012 (lifecycle harness) |
| COLLEEN | NDR-002 (schema diff), all archive and registry patterns |
| Sentinel-Phi | NDR-006 (Phi-closure), NDR-007 (HPG), NDR-003 (constraint stack) |
| Reciprocity | NDR-004 (domain overlay), arbitration logic |
| Sonar | Evidence grounding for all patterns |
| Reson | NDR-009 (router topology), NDR-001 (PDMAL substrate) |
| Prodigy | NDR-010 (claim verification, confidence) |
| Apogee | NDR-011 (Gold Star gate), QA rubrics |

---

## State Anchor Cross-Reference

| Goal | Enforced By | File |
|---|---|---|
| zero_open_blg | Orchestration Firewall | `orchestration_firewall.py` |
| single_authority_chain | `authority_chain_valid()` | `orchestration_firewall.py` |
| append_only_log | Rollback on invariant failure | `orchestration_firewall.py` |
| observable_invariants_only | All invariants tested at boundary | `test_orchestration_firewall.py` |
| procluding_premise_first | SCPE.ingest() tier classification | `scpe_ensemble_v14.py` |
