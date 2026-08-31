"""Semantic-parity and preflight safety tests for restored P-31/P-33 state.

These tests do not authorize pilot execution or generate empirical evidence.
They verify historical parity plus the provenance/determinism invariants required
before a future candidate can be frozen.
"""
from __future__ import annotations

import os
import sys
import math

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import pytest

from components.ensemble_v16 import (
    ConvergenceStatus,
    ContextToken,
    PDMALConvergenceMonitor,
    PDMALGraph,
    StructuralContextPruningEngine,
    Tier,
)
from dgaf_tgl_adapter import ConsensusState, canonicalize_state
from pdmaltgl_gate_binding import (
    GateResult,
    SCPEState,
    ConvergenceState,
    build_pdmal_hook,
    build_scpe_hook,
)

FIXED_NOW = 1_750_000_000.0


def _reference_scpe_prune(tokens, now=FIXED_NOW):
    """Run the historical reference engine at an explicit deterministic time."""
    eng = StructuralContextPruningEngine(threshold=0.15)
    for t in tokens:
        eng.ingest(t)
    import components.ensemble_v16 as reference_module
    original_time = reference_module.time.time
    reference_module.time.time = lambda: now  # type: ignore[assignment]
    try:
        result = eng.prune()
    finally:
        reference_module.time.time = original_time
    return result, eng


def test_p31_reference_quick_check():
    ref_tokens = [
        ContextToken("ax1", "rule", Tier.AXIOM, inserted_at=FIXED_NOW - 100),
        ContextToken("ex1", "noise", Tier.EXPLORATORY, inserted_at=FIXED_NOW - 100),
    ]
    result, _ = _reference_scpe_prune(ref_tokens)
    assert result["axiom_count"] == 1
    assert result["exploratory_count"] == 0


def test_p31_restored_hook_matches_reference_tier_table():
    tokens = [
        {"token_id": "ax1", "tier": "AXIOM", "content": "rule", "inserted_at": FIXED_NOW - 100, "has_trust_edge": False},
        {"token_id": "ex1", "tier": "EXPLORATORY", "content": "noise", "inserted_at": FIXED_NOW - 100, "has_trust_edge": False},
        {"token_id": "op1", "tier": "OPERATIONAL", "content": "x", "inserted_at": FIXED_NOW - 1, "has_trust_edge": True},
    ]
    ref_tokens = [
        ContextToken(t["token_id"], t["content"], Tier[t["tier"]], inserted_at=t["inserted_at"], has_trust_edge=t["has_trust_edge"])
        for t in tokens
    ]
    _, ref_eng = _reference_scpe_prune(ref_tokens)
    ref_pruned = {e.token_id for e in ref_eng.prune_log}

    st = SCPEState(tokens=[dict(t) for t in tokens], evaluation_time=FIXED_NOW)
    gr = build_scpe_hook(st)("turn-1", {})
    assert gr is GateResult.PASS
    restored_pruned = {t["token_id"] for t in tokens if t["token_id"] not in {s["token_id"] for s in st.tokens}}
    assert restored_pruned == ref_pruned
    assert "ax1" not in restored_pruned


def test_p31_last_k_anchor_preserved():
    tokens = [
        {"token_id": f"op{i}", "tier": "OPERATIONAL", "content": "x", "inserted_at": FIXED_NOW - 1000 + i, "has_trust_edge": False}
        for i in range(5)
    ]
    ref_tokens = [
        ContextToken(t["token_id"], t["content"], Tier.OPERATIONAL, inserted_at=t["inserted_at"])
        for t in tokens
    ]
    _, ref_eng = _reference_scpe_prune(ref_tokens)
    ref_survived = {t.token_id for t in ref_eng._tokens.values()}

    st = SCPEState(tokens=[dict(t) for t in tokens], evaluation_time=FIXED_NOW)
    build_scpe_hook(st)("turn-1", {})
    restored_survived = {s["token_id"] for s in st.tokens}
    assert restored_survived == ref_survived
    assert len(restored_survived) == 3


def test_p31_requires_explicit_evaluation_time_for_token_state():
    with pytest.raises(ValueError, match="evaluation_time"):
        ConsensusState(
            seed_id=1, iteration=1, agent_values=(0.1,), alive=(True,),
            original_neighbors=((),), active_neighbors=((),), failure_history=(),
            failure_count_current=0, failure_count_total=0, current_final_std=0.0,
            current_mean=0.1, runtime_budget_remaining_ms=100, protocol_id="X",
            scpe_state=SCPEState(tokens=[{"token_id": "t", "tier": "OPERATIONAL"}]),
        ).validate()


def test_p31_fixed_contract_constants_cannot_be_rebound():
    with pytest.raises(ValueError, match="trust_edge_boost"):
        ConsensusState(
            seed_id=1, iteration=1, agent_values=(0.1,), alive=(True,),
            original_neighbors=((),), active_neighbors=((),), failure_history=(),
            failure_count_current=0, failure_count_total=0, current_final_std=0.0,
            current_mean=0.1, runtime_budget_remaining_ms=100, protocol_id="X",
            scpe_state=SCPEState(trust_edge_boost=0.20),
        ).validate()

    with pytest.raises(ValueError, match="last_k_anchor"):
        ConsensusState(
            seed_id=1, iteration=1, agent_values=(0.1,), alive=(True,),
            original_neighbors=((),), active_neighbors=((),), failure_history=(),
            failure_count_current=0, failure_count_total=0, current_final_std=0.0,
            current_mean=0.1, runtime_budget_remaining_ms=100, protocol_id="X",
            scpe_state=SCPEState(last_k_anchor=2),
        ).validate()


def _reference_convergence(weights_seq, alert=0.08, conv=0.02, n=3):
    cs = {"_prev": {}, "_cd": 0, "_cs": 0, "_turn": 0, "_events": []}
    events = []
    for snap in weights_seq:
        g = PDMALGraph()
        for (s, d), w in snap.items():
            g.add_edge(s, d, w)
        mon = PDMALConvergenceMonitor(g, alert_thresh=alert, conv_thresh=conv, n_consec=n)
        mon._prev_weights = dict(cs["_prev"])
        mon._consec_divergent = cs["_cd"]
        mon._consec_stable = cs["_cs"]
        mon._turn = cs["_turn"]
        mon._events = list(cs["_events"])
        evt = mon.check(turn_id="T")
        cs["_prev"] = dict(mon._prev_weights)
        cs["_cd"] = mon._consec_divergent
        cs["_cs"] = mon._consec_stable
        cs["_turn"] = mon._turn
        cs["_events"] = list(mon._events)
        events.append(evt)
    return events


def test_p33_reference_frobenius_matches_manual():
    w0 = {("a", "b"): 0.5, ("b", "c"): 0.3}
    w1 = {("a", "b"): 0.55, ("b", "c"): 0.31}
    expected = math.sqrt(0.05 ** 2 + 0.01 ** 2)
    events = _reference_convergence([w0, w1])
    assert abs(events[-1].graph_norm_delta - round(expected, 6)) < 1e-6


def test_p33_restored_hook_matches_reference_status_ladder():
    w0 = {("a", "b"): 0.10, ("b", "c"): 0.10}
    w1 = {("a", "b"): 0.30, ("b", "c"): 0.30}
    w2 = {("a", "b"): 0.50, ("b", "c"): 0.50}
    w3 = {("a", "b"): 0.70, ("b", "c"): 0.70}

    ref_events = _reference_convergence([w0, w1, w2, w3])
    ref_codes = [e.status for e in ref_events]

    cs = ConvergenceState()
    results = []
    for i, snap in enumerate([w0, w1, w2, w3]):
        cs.weights = dict(snap)
        context = {"pdmaltgl": {"state": {"seed_id": 7, "iteration": i + 1}}}
        results.append(build_pdmal_hook(cs)("turn", context))
    restored_ladder = [
        GateResult.WARN if c in (ConvergenceStatus.WARN.code, ConvergenceStatus.ALERT.code)
        else GateResult.PASS
        for c in ref_codes
    ]
    assert results == restored_ladder
    assert results[3] is GateResult.WARN
    assert cs._events[-1].turn_id == "seed:7:iteration:4"


def test_p33_w_prev_snapshot_retained_across_turns():
    cs = ConvergenceState()
    w0 = {("a", "b"): 0.10}
    w1 = {("a", "b"): 0.20}
    cs.weights = dict(w0)
    context = {"pdmaltgl": {"state": {"seed_id": 1, "iteration": 1}}}
    build_pdmal_hook(cs)("t0", context)
    assert cs.prev_weights == w0
    cs.weights = dict(w1)
    context["pdmaltgl"]["state"]["iteration"] = 2
    r1 = build_pdmal_hook(cs)("t1", context)
    assert r1 is GateResult.PASS
    assert cs._events[-1].graph_norm_delta > 0


def test_canonical_identity_changes_when_restored_state_changes():
    base = ConsensusState(
        seed_id=1, iteration=1, agent_values=(0.1,), alive=(True,),
        original_neighbors=((),), active_neighbors=((),), failure_history=(),
        failure_count_current=0, failure_count_total=0, current_final_std=0.0,
        current_mean=0.1, runtime_budget_remaining_ms=100, protocol_id="X",
    )
    canonical_base = canonicalize_state(base)
    changed = ConsensusState(
        seed_id=1, iteration=1, agent_values=(0.1,), alive=(True,),
        original_neighbors=((),), active_neighbors=((),), failure_history=(),
        failure_count_current=0, failure_count_total=0, current_final_std=0.0,
        current_mean=0.1, runtime_budget_remaining_ms=100, protocol_id="X",
        scpe_state=SCPEState(threshold=0.16),
    )
    assert canonicalize_state(changed) != canonical_base


def test_consensus_state_accepts_empty_restored_substrate_defaults():
    st = ConsensusState(
        seed_id=1, iteration=1, agent_values=(0.1, 0.2), alive=(True, True),
        original_neighbors=((1,), (0,)), active_neighbors=((1,), (0,)),
        failure_history=(), failure_count_current=0, failure_count_total=0,
        current_final_std=0.1, current_mean=0.15, runtime_budget_remaining_ms=100,
        protocol_id="X",
    )
    st.validate()
    assert isinstance(st.scpe_state, SCPEState)
    assert isinstance(st.convergence_state, ConvergenceState)
