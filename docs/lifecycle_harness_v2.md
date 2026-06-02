# Lifecycle Harness v2

> **Steward:** COLLEEN  
> **Orchestrator:** Amethyst  
> **Created:** 2026-06-01 — Session S044  
> **Ensemble:** v1.6  
> **NDR Patterns:** P-31 (SCPE) · P-32 (PDMAL Monitor) · P-33 (Phi-Closure Gate)  
> **Governed by:** DGAF-Framework · Apache 2.0

---

## Purpose

The Lifecycle Harness v2 defines the executable phase exit criteria for the Ensemble v1.6 orchestration pipeline.
Each phase must satisfy all listed invariants before the pipeline may advance.
The harness produces `registry/lifecycle_stability_report.json` as its terminal artifact.

---

## Phase Definitions

### Phase 0 — Initialization

**Gate:** State anchor assertion

| Invariant | Check | Pass Condition |
|---|---|---|
| zero_open_blgs | `len(open_blgs) == 0` | 0 open bug/limitation gates |
| state_anchor_loaded | `SESSION_ANCHOR.md` present and current session stamped | Session ID matches |
| procluding_premise_fires_before_routing | Intake gate classifies premise before any routing occurs | Classification event logged pre-route |

**Stability target:** N/A (binary gate)  
**Artifacts:** `SESSION_ANCHOR.md`, `CO_ORCH_QUEUE.md`

---

### Phase I — Ingest

**Gate:** SCPE compression and topological preflight

| Invariant | Check | Pass Condition |
|---|---|---|
| da_preflight_passes | `topology.node_count >= 10` | Dimensional anchors sufficient |
| scpe_compression_within_bounds | `0.50 <= compression_ratio <= 0.65` | Near 58.3% validated baseline |
| t0_immune | T0 axiom guard tier never pruned | 100% T0 preservation |

**Stability target:** ≥ 0.618  
**Artifacts:** `components/scpe_ensemble_v14.py`

---

### Phase II — Route

**Gate:** Topology router NDR P-02 predicate order invariant

| Invariant | Check | Pass Condition |
|---|---|---|
| predicate_order_correct | SEQUENTIAL resolves before HIERARCHICAL | `route(SEQUENTIAL) is SequentialRouter` |
| no_shadow_bugs | FAN_OUT resolves before HIERARCHICAL | `route(FAN_OUT) is FanOutRouter` |
| 8_of_8_tc_pass | Full TC1–TC8 pytest suite | 10/10 tests pass |

**Stability target:** ≥ 0.618  
**Artifacts:** `components/topology_router.py`, `tests/test_topology_router.py`

---

### Phase III — Execute

**Gate:** Orchestration firewall 5-invariant check

| Invariant | Check | Pass Condition |
|---|---|---|
| all_5_invariants_hold | `all_invariants_hold()` returns True | Both happy and attack paths |
| authority_chain_valid | `authority_chain_valid()` returns True | Single authority chain |
| attack_path_blocked | DEPLOY_SUCCESS rolled back on attack path | 1 committed event only |

**Stability target:** ≥ 0.618  
**Artifacts:** `components/orchestration_firewall.py`, `tests/test_orchestration_firewall.py`

---

### Phase IV — Verify

**Gate:** PDMAL Monitor + Phi-Closure Gate + DemiJoule safety

| Invariant | Check | Pass Condition |
|---|---|---|
| pdmal_no_full_alerts | 3-consecutive ALERT threshold not met | 0 full PDMAL alerts |
| phi_closure_passes | `phi_score >= phi_star - tolerance` | φ* = 0.6180 ± 0.05 |
| demijule_ethics_clear | DemiJoule gate returns PASS | No GDPR Art 22, no cost overrun |

**Stability target:** ≥ 0.618  
**Convergence bound:** ≤ Fib[34] = 34 turns  
**Artifacts:** `components/ensemble_v16.py`, `registry/ensemble_v16_manifest.json`

---

### Phase V — Archive

**Gate:** COLLEEN 1-1-1-1 Alignment Gate

| Invariant | Check | Pass Condition |
|---|---|---|
| colleen_1_1_1_1_gate_pass | All 4 COLLEEN alignment checks pass | Librarian · Auditor · Actualizer · Anchor all PASS |
| cross_ref_updated | `CROSS_REF.md` reflects all new patterns and files | Zero stale cross-references |
| sweep_log_appended | `SWEEP_LOG.md` has current sweep entry | Append-only invariant holds |

**Stability target:** ≥ 0.618  
**Artifacts:** `SWEEP_LOG.md`, `CROSS_REF.md`, `CO_ORCH_QUEUE.md`

---

### Phase VI — Close

**Gate:** Amethyst terminal attestation

| Invariant | Check | Pass Condition |
|---|---|---|
| amethyst_signed | Terminal attestation JSON present and signed | `orchestrator: Agent Amethyst` |
| terminal_attestation_present | `terminal_attestation.json` committed to branch | File exists in repo root |
| issue_closed | Tracking issue marked closed | GitHub issue state = CLOSED |

**Stability target:** N/A (binary gate)  
**Artifacts:** `terminal_attestation.json`

---

## Aggregate Stability Index

Computed after all phases run:

```
overall_stability_index = stable_phases / total_phases
target: >= 0.618 (Fibonacci phi-complement)
```

If `overall_stability_index < 0.618`, the sweep **FAILS** and must be re-run from the first failing phase.

---

## Execution Instructions

1. Run `pytest tests/test_topology_router.py` — Phase II gate
2. Run `pytest tests/test_orchestration_firewall.py` — Phase III gate
3. Run `python scripts/run_lifecycle_harness.py` — Phases 0–VI, outputs `registry/lifecycle_stability_report.json`
4. Review report: all 7 phases must show `status: PASS` and `stability_index >= 0.618`
5. COLLEEN executes Phase V archive ingest
6. Amethyst issues terminal attestation JSON — Phase VI

---

*All agents operate under the DGAF governance framework.*  
*NDR Patterns P-01 through P-33 active.*  
*Lifecycle Harness v2 · Ensemble v1.6 · φ = 1.61818 · θ = 0.009*
