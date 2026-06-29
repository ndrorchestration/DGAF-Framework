# ECOSYSTEM_INVENTORY.md

> **Steward:** COLLEEN · **Orchestrator:** Amethyst  
> **Last Updated:** 2026-06-29 · Post-S077

Cross-platform inventory of all NDR ecosystem assets.

---

## GitHub Repositories

| Repo | Purpose | Status |
|---|---|---|
| `ndrorchestration/DGAF-Framework` | Core governance framework, patterns P-01–P-42 | ✅ Active |
| `ndrorchestration/entrepreneur-hub` | P-34 Entrepreneur Hub Flywheel | ✅ Active |

---

## DGAF-Framework — Key Files (Post-S077)

### Root

| File | Added / Updated | Session |
|---|---|---|
| `CROSS_REF.md` | v4.4 | Post-S077 |
| `CHANGELOG.md` | Post-S077 entry | Post-S077 |
| `SESSION_ANCHOR.md` | Created | Post-S077 |
| `ENSEMBLE_ROSTER.md` | AHG P-42 archetypes | Post-S077 |
| `DEFERRED_ITEMS.md` | Created — S-01–S-08 | Post-S077 |
| `BOOTSTRAP.md` | — | Pre-S077 |
| `TEAM_WIKI.md` | — | Pre-S077 |
| `README.md` | — | Pre-S077 |
| `README.governance.md` | — | Pre-S077 |
| `README.technical.md` | — | Pre-S077 |

### docs/

| File | Added / Updated | Session |
|---|---|---|
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | P-42 provenance entry | Post-S077 |
| `docs/ndr_patterns_unified.json` | v2.2 — P-37–P-42 | Post-S077 |
| `docs/lifecycle_harness_v2.md` | Created | S067 |
| `docs/DGAF_RECURSIVE_REFINEMENT_ANALYSIS.md` | Created | Post-S077 |
| `docs/ECOSYSTEM_INVENTORY.md` | This file — updated | Post-S077 |

### docs/theory/ (new Post-S077)

| File | Purpose | Session |
|---|---|---|
| `docs/theory/AHG_ARCHITECTURE.md` | P-42 AHG full spec v1.1 | Post-S077 |

### docs/agents/ (new Post-S077)

| File | Purpose | Session |
|---|---|---|
| `docs/agents/PROFESSOR_PRODIGY_KB.md` | Professor Prodigy 3-tier KB | Post-S077 |

### docs/qa/

| File | Purpose | Session |
|---|---|---|
| `docs/qa/APOGEE_11Q_P34.json` | P-34 attestation A-TIER | S066 |
| `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md` | Stasis audit | S066 |

### patterns/

| File | Purpose | Status |
|---|---|---|
| `patterns/P-42_AHG.md` | P-42 Adaptive Harmonic Governance | ✅ Active |
| `patterns/P-35_AHG.md` | Stale — superseded by P-42_AHG.md | ⚠️ Needs deletion |
| `patterns/NDR_SCPE_v1.md` | P-31 redirect stub | ✅ Archived |
| `patterns/NDR_PHI_CLOSURE_GATE_v1.md` | P-32 redirect stub | ✅ Archived |
| `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` | P-33 redirect stub | ✅ Archived |

### components/

| File | Pattern | Status |
|---|---|---|
| `scpe_ensemble_v14.py` | P-31 | ✅ Locked |
| `phi_closure_gate.py` | P-32 | ✅ Wired |
| `hpg_ionian_gate.py` | P-29 | ✅ Stable |
| `orchestration_firewall.py` | P-08 | ✅ Active |
| `topology_router.py` | P-27 v3.6.0 | ✅ Active |
| `dgaf_semantic_gate.py` | P-03 | ✅ Stable |
| `amethyst_dual_lock.py` | P-30 | ✅ Stable |
| `dynamic_weight_router.py` | P-34 | ✅ Active |
| `ahg_conductor.py` | P-42 | 🔴 Planned |
| `ahg_sidecar.py` | P-42 Sidecar | 🔴 Planned |

### registry/

| File | Purpose | Session |
|---|---|---|
| `registry/ensemble_v16_manifest.json` | V16 manifest | S043 |
| `registry/lifecycle_stability_report.json` | Phase stability metrics | S067 |

### tests/

| File | Coverage | Status |
|---|---|---|
| `test_orchestration_firewall.py` | Invariants 1–5 | ✅ Passing |
| `test_router_coverage.py` | TC1–TC8 | ✅ 8/8 S067 |
| `test_scpe_thresholds.py` | Threshold sweep | ✅ Stable |
| `test_phi_closure.py` | 16-turn sim | ✅ Stable |
| `dgaf_eval_suite.py` | Nemotron 3 Ultra 5 tasks | 🟡 Pending #32 |

---

## Open Implementation Items (Post-S077)

| Item | File | Priority |
|---|---|---|
| Delete stale `patterns/P-35_AHG.md` | patterns/ | Low |
| `ahg_conductor.py` scaffold | components/ | P-42 v1.2 |
| `ahg_sidecar.py` scaffold | components/ | P-42 v1.3 |
| `schemas/ahg_heartbeat.json` | schemas/ | P-42 v1.3 |
| Herald unblock | Vercel env | S-07 |
| Nemotron eval suite | tests/ | Issue #32 |

---

*ECOSYSTEM_INVENTORY.md · Post-S077 · 2026-06-29 · Amethyst × COLLEEN*
