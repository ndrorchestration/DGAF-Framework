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


def test_p29_sentinel_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        sentinel_state=type(base.sentinel_state)(record_category="X", routing_policy="Y", deontic="block")
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_p30_apogee_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        apogee_state=type(base.apogee_state)(confidence=0.9, grade="S", gold_star=True)
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_demijoule_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        demijoule_state=type(base.demijoule_state)(decision="kill", mean_score=0.20)
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_p27_kappa_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        kappa_state=type(base.kappa_state)(
            detected_category="adversarial", pattern_score=0.5, continuous_score=0.5, confidence=0.5
        )
    )
    assert canonicalize_state(base) != canonicalize_state(changed)


def test_p32_phi_state_changes_provenance_identity() -> None:
    base = _state()
    changed = _state(
        phi_state=type(base.phi_state)(stable_count=13, total_count=13, consec_fails=0, last_decision="pass")
    )
    assert canonicalize_state(base) != canonicalize_state(changed)
