"""Final-branch provenance binding tests for restored P-31/P-33 state.

These tests are pre-freeze only. They verify that behavior-affecting restored
state changes the canonical input identity and that fixed historical invariants
cannot silently drift.
"""
from __future__ import annotations

from dgaf_tgl_adapter import ConsensusState, canonicalize_state


def _state(**overrides) -> ConsensusState:
    values = dict(
        seed_id=1,
        iteration=1,
        agent_values=(0.1, 0.2),
        alive=(True, True),
        original_neighbors=((1,), (0,)),
        active_neighbors=((1,), (0,)),
        failure_history=((), ()),
        failure_count_current=0,
        failure_count_total=0,
        current_final_std=0.05,
        current_mean=0.15,
        runtime_budget_remaining_ms=1000,
        protocol_id="PDMAL-V1",
    )
    values.update(overrides)
    return ConsensusState(**values)


def test_p31_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        scpe_state=type(base.scpe_state)(
            tokens=[{"token_id": "t1", "tier": "T2", "content": "x", "inserted_at": 1.0, "has_trust_edge": False}],
            threshold=0.15,
            trust_edge_boost=0.15,
            last_k_anchor=3,
        )
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_p33_weights_change_provenance_identity() -> None:
    base = _state()
    changed = _state(
        convergence_state=type(base.convergence_state)(
            weights={("0", "1"): 0.5},
            prev_weights={("0", "1"): 0.4},
        )
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_historical_p31_invariants_are_enforced() -> None:
    base = _state()
    bad = type(base.scpe_state)(
        tokens=[], threshold=0.15, trust_edge_boost=0.20, last_k_anchor=3
    )
    try:
        _state(scpe_state=bad).validate()
    except ValueError:
        pass
    else:
        raise AssertionError("historical trust_edge_boost drift was not rejected")
