"""Semantic-parity tests: RESTORE of P-31 SCPE + P-33 Convergence.

These tests prove the restored pilot hooks produce results IDENTICAL to the
historical reference implementation in ``components/ensemble_v16.py`` (the v1.0
contract oracle, co-located at historical commit ``49854ea1...``).

They do not authorize pilot execution or generate empirical data. Empirical
N remains 0; the other five required gates remain unwired (FAIL_CLOSED).
"""
from __future__ import annotations

import os
import sys

_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
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
from dgaf_tgl_adapter import ConsensusState
from pdmaltgl_gate_binding import (
    ConvergenceState,
    GateResult,
    SCPEState,
    build_pdmal_hook,
    build_scpe_hook,
)


# ---------------------------------------------------------------------------
# P-31 SCPE parity
# ---------------------------------------------------------------------------

def _reference_scpe_prune(tokens):
    """Run the historical reference engine directly and return (result, engine)."""
    eng = StructuralContextPruningEngine(threshold=0.15)
    for t in tokens:
        eng.ingest(t)
    result = eng.prune()
    return result, eng


def test_p31_reference_quick_check():
    """The contract's own Quick Check: T0 GUARD PASS, T3 ELIMINATED PASS."""
    ref_tokens = [
        ContextToken("ax1", "rule", Tier.AXIOM, inserted_at=__import__("time").time() - 100),
        ContextToken("ex1", "noise", Tier.EXPLORATORY, inserted_at=__import__("time").time() - 100),
    ]
    result, eng = _reference_scpe_prune(ref_tokens)
    assert result["axiom_count"] == 1
    assert result["exploratory_count"] == 0


def test_p31_restored_hook_matches_reference_tier_table():
    """Restored hook prunes exactly what the reference engine prunes."""
    now = __import__("time").time()
    tokens = [
        {"token_id": "ax1", "tier": "AXIOM", "content": "rule", "inserted_at": now - 100, "has_trust_edge": False},
        {"token_id": "ex1", "tier": "EXPLORATORY", "content": "noise", "inserted_at": now - 100, "has_trust_edge": False},
        {"token_id": "op1", "tier": "OPERATIONAL", "content": "x", "inserted_at": now - 1, "has_trust_edge": True},
    ]
    # Reference oracle
    ref_tokens = [ContextToken(t["token_id"], t["content"], Tier[t["tier"]], inserted_at=t["inserted_at"],
                               has_trust_edge=t["has_trust_edge"]) for t in tokens]
    _, ref_eng = _reference_scpe_prune(ref_tokens)
    ref_pruned = {e.token_id for e in ref_eng.prune_log}

    # Restored substrate + hook
    st = SCPEState(tokens=[dict(t) for t in tokens])
    hook = build_scpe_hook(st)
    gr = hook("turn-1", {})
    assert gr is GateResult.PASS
    restored_pruned = {t["token_id"] for t in tokens if t["token_id"] not in {s["token_id"] for s in st.tokens}}
    assert restored_pruned == ref_pruned
    # AXIOM never pruned
    assert "ax1" not in restored_pruned


def test_p31_last_k_anchor_preserved():
    """Last-K (K=3) operational tokens survive regardless of retention."""
    now = __import__("time").time()
    tokens = [
        {"token_id": f"op{i}", "tier": "OPERATIONAL", "content": "x", "inserted_at": now - 1000, "has_trust_edge": False}
        for i in range(5)
    ]
    # Reference: with 5 stale operational tokens, the 3 most-recent survive.
    ref_tokens = [ContextToken(t["token_id"], t["content"], Tier.OPERATIONAL, inserted_at=t["inserted_at"]) for t in tokens]
    _, ref_eng = _reference_scpe_prune(ref_tokens)
    ref_survived = {t.token_id for t in ref_eng._tokens.values()}

    st = SCPEState(tokens=[dict(t) for t in tokens])
    hook = build_scpe_hook(st)
    hook("turn-1", {})
    restored_survived = {s["token_id"] for s in st.tokens}
    assert restored_survived == ref_survived
    assert len(restored_survived) == 3  # exactly last-3 anchored


# ---------------------------------------------------------------------------
# P-33 Convergence parity
# ---------------------------------------------------------------------------

def _reference_convergence(weights_seq, alert=0.08, conv=0.02, n=3):
    """Feed a sequence of W_t snapshots through the reference monitor, carrying
    W_{t-1} AND consecutive counters across turns (mirrors the binding)."""
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
    """Reference Frobenius delta equals manual sqrt(sum squared diffs)."""
    import math
    w0 = {("a", "b"): 0.5, ("b", "c"): 0.3}
    w1 = {("a", "b"): 0.55, ("b", "c"): 0.31}
    expected = math.sqrt((0.05) ** 2 + (0.01) ** 2)
    events = _reference_convergence([w0, w1])
    assert abs(events[-1].graph_norm_delta - round(expected, 6)) < 1e-6


def test_p33_restored_hook_matches_reference_status_ladder():
    """Restored hook returns the same GateResult as the reference status ladder.

    Reference ladder for 3 consecutive divergences (>alert):
      turn0 STABLE, turn1 WATCH, turn2 WARN, turn3 ALERT.
    TGL mapping: WATCH->PASS, WARN->WARN, ALERT->WARN.
    """
    w0 = {("a", "b"): 0.10, ("b", "c"): 0.10}
    w1 = {("a", "b"): 0.30, ("b", "c"): 0.30}  # delta ~0.283 > 0.08
    w2 = {("a", "b"): 0.50, ("b", "c"): 0.50}
    w3 = {("a", "b"): 0.70, ("b", "c"): 0.70}

    ref_events = _reference_convergence([w0, w1, w2, w3])
    ref_codes = [e.status for e in ref_events]

    cs = ConvergenceState()
    results = []
    for snap in [w0, w1, w2, w3]:
        cs.weights = dict(snap)
        results.append(build_pdmal_hook(cs)("turn", {}))
    restored_ladder = [
        GateResult.WARN if c in (ConvergenceStatus.WARN.code, ConvergenceStatus.ALERT.code)
        else GateResult.PASS
        for c in ref_codes
    ]
    assert results == restored_ladder
    # 3rd consecutive divergent turn is ALERT -> WARN
    assert results[3] is GateResult.WARN


def test_p33_w_prev_snapshot_retained_across_turns():
    """Restored hook retains W_{t-1}; the 2nd call computes a real delta."""
    cs = ConvergenceState()
    w0 = {("a", "b"): 0.10}
    w1 = {("a", "b"): 0.20}
    cs.weights = dict(w0)
    build_pdmal_hook(cs)("t0", {})
    # After t0, prev_weights should equal w0 (snapshot retained)
    assert cs.prev_weights == w0
    cs.weights = dict(w1)
    r1 = build_pdmal_hook(cs)("t1", {})
    # Single divergent turn -> WATCH -> GateResult.PASS (not yet WARN)
    assert r1 is GateResult.PASS


# ---------------------------------------------------------------------------
# Integration: wiring does not break ConsensusState contract
# ---------------------------------------------------------------------------

def test_consensus_state_accepts_restored_substrate_defaults():
    """Backward-compatible: existing callers without substrate still validate."""
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
