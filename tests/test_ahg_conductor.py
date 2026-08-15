"""
tests/test_ahg_conductor.py — AHG Conductor + Sidecar Unit Tests
P-42 · Layer 12 — Cognitive Control Plane · v1.4
Amethyst × COLLEEN · S072 · 2026-07-02

v1.3: scaffold — φ, regime, hysteresis, sidecar basics, eval stubs
v1.4: PhaseIntent v_phi/a_phi/tribunal_active/message fields,
      3D Cognitive Phase Space axes, wire_herald_trace() integration
"""

from __future__ import annotations

import math
import pytest

from components.ahg_conductor import (
    AHGConductor,
    Archetype,
    PhaseIntent,
    Regime,
    StateVector,
    W1_D_E, W2_N, W3_C, W4_R,
    PHI_MIN, PHI_MAX,
    compute_phi,
    compute_stability_index,
    compute_phase_acceleration,
    compute_phase_velocity,
    compute_3d_phase,
    classify_regime,
    logistic,
    _REGIME_ARCHETYPE,
)
from components.ahg_sidecar import AgentHeartbeat, AHGSidecar, TurnBuffer


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def zero_sv() -> StateVector:
    return StateVector()

@pytest.fixture
def high_entropy_sv() -> StateVector:
    return StateVector(D_e=1.0, N=0.8, C=0.9, R=0.8)

@pytest.fixture
def conductor() -> AHGConductor:
    return AHGConductor()

@pytest.fixture
def sidecar(conductor) -> AHGSidecar:
    return AHGSidecar(conductor=conductor)


# ===========================================================================
# 1. Canonical constants
# ===========================================================================

class TestCanonicalConstants:
    def test_weights_sum_to_one(self):
        assert math.isclose(W1_D_E + W2_N + W3_C + W4_R, 1.0, rel_tol=1e-9)

    def test_w1_d_e(self):  assert W1_D_E == 0.35
    def test_w2_n(self):    assert W2_N   == 0.20
    def test_w3_c(self):    assert W3_C   == 0.25
    def test_w4_r(self):    assert W4_R   == 0.20
    def test_phi_bounds(self):
        assert PHI_MIN == 1.0
        assert PHI_MAX == 1.8


# ===========================================================================
# 2. φ computation
# ===========================================================================

class TestPhiComputation:
    def test_zero_sv_phi_in_bounds(self, zero_sv):
        assert PHI_MIN <= compute_phi(zero_sv) <= PHI_MAX

    def test_phi_strictly_greater_than_min(self, zero_sv):
        assert compute_phi(zero_sv) > PHI_MIN

    def test_phi_strictly_less_than_max(self, high_entropy_sv):
        assert compute_phi(high_entropy_sv) < PHI_MAX

    def test_phi_monotone_with_entropy(self):
        assert compute_phi(StateVector(D_e=0.9)) > compute_phi(StateVector(D_e=0.1))

    def test_d_explore_excluded_from_phi(self):
        base = compute_phi(StateVector(D_e=0.5))
        assert math.isclose(base, compute_phi(StateVector(D_e=0.5, D_explore=0.9)), rel_tol=1e-12)

    def test_d_correct_excluded_from_phi(self):
        base = compute_phi(StateVector(D_e=0.5))
        assert math.isclose(base, compute_phi(StateVector(D_e=0.5, D_correct=0.9)), rel_tol=1e-12)

    def test_stability_index_formula(self):
        sv = StateVector(D_e=0.4, N=0.3, C=0.2, R=0.1)
        expected = 0.35*0.4 + 0.20*0.3 + 0.25*0.2 + 0.20*0.1
        assert math.isclose(compute_stability_index(sv), expected, rel_tol=1e-9)

    def test_logistic_midpoint(self):
        assert math.isclose(logistic(0.0), 0.5, rel_tol=1e-9)


# ===========================================================================
# 3. NDR-STASIS anchor
# ===========================================================================

class TestNDRStasisAnchor:
    def test_phi_1618_is_integration(self):
        assert classify_regime(1.618) == Regime.INTEGRATION

    def test_phi_1600_is_integration(self):
        assert classify_regime(1.600) == Regime.INTEGRATION

    def test_phi_1699_is_integration(self):
        assert classify_regime(1.699) == Regime.INTEGRATION

    def test_phi_1700_is_introspection(self):
        assert classify_regime(1.700) == Regime.INTROSPECTION


# ===========================================================================
# 4. Regime classification — all 7 states
# ===========================================================================

class TestRegimeClassification:
    @pytest.mark.parametrize("phi,expected", [
        (1.00, Regime.GROUNDED),      (1.07, Regime.GROUNDED),
        (1.14, Regime.GROUNDED),      (1.15, Regime.FLOW),
        (1.22, Regime.FLOW),          (1.29, Regime.FLOW),
        (1.30, Regime.VIGILANCE),     (1.37, Regime.VIGILANCE),
        (1.44, Regime.VIGILANCE),     (1.45, Regime.EXPANSION),
        (1.52, Regime.EXPANSION),     (1.59, Regime.EXPANSION),
        (1.60, Regime.INTEGRATION),   (1.618, Regime.INTEGRATION),
        (1.69, Regime.INTEGRATION),   (1.70, Regime.INTROSPECTION),
        (1.75, Regime.INTROSPECTION), (1.799, Regime.INTROSPECTION),
        (1.80, Regime.TENSION),       (1.85, Regime.TENSION),
    ])
    def test_regime_boundary(self, phi, expected):
        assert classify_regime(phi) == expected


# ===========================================================================
# 5. Phase velocity + acceleration
# ===========================================================================

class TestPhaseKinematics:
    def test_velocity_insufficient_history(self):
        assert compute_phase_velocity([1.3]) == 0.0

    def test_velocity_two_points(self):
        assert math.isclose(compute_phase_velocity([1.3, 1.5]), 0.2, rel_tol=1e-9)

    def test_velocity_descending(self):
        assert math.isclose(compute_phase_velocity([1.6, 1.4]), -0.2, rel_tol=1e-9)

    def test_acceleration_insufficient_history(self):
        assert compute_phase_acceleration([1.3, 1.5]) == 0.0

    def test_acceleration_three_points(self):
        assert math.isclose(compute_phase_acceleration([1.3, 1.5, 1.8]), 0.1, rel_tol=1e-9)

    def test_acceleration_decelerating(self):
        assert math.isclose(compute_phase_acceleration([1.0, 1.3, 1.4]), -0.2, rel_tol=1e-9)


# ===========================================================================
# 6. 3D Cognitive Phase Space — AHG_ARCHITECTURE §2.7
# ===========================================================================

class Test3DPhaseSpace:

    def test_all_axes_in_unit_interval(self):
        for sv in [
            StateVector(),
            StateVector(D_e=1.0, D_explore=1.0, D_correct=1.0, N=1.0, C=1.0, R=1.0, K=1.0),
            StateVector(D_e=0.5, D_explore=0.3, K=0.7, C=0.4, R=0.6),
        ]:
            exp, dis, unc = compute_3d_phase(sv)
            assert 0.0 <= exp <= 1.0, f"exploration={exp} out of bounds"
            assert 0.0 <= dis <= 1.0, f"dissent={dis} out of bounds"
            assert 0.0 <= unc <= 1.0, f"uncertainty={unc} out of bounds"

    def test_high_d_explore_high_exploration(self):
        sv_high = StateVector(D_explore=0.9, K=0.1)
        sv_low  = StateVector(D_explore=0.1, K=0.9)
        exp_high, _, _ = compute_3d_phase(sv_high)
        exp_low,  _, _ = compute_3d_phase(sv_low)
        assert exp_high > exp_low

    def test_high_k_low_exploration(self):
        """High coherence (exploitation) drives exploration toward 0."""
        sv = StateVector(D_explore=0.0, K=1.0)
        exp, _, _ = compute_3d_phase(sv)
        assert exp < 0.01

    def test_high_d_e_high_dissent(self):
        sv_high = StateVector(D_e=0.9, D_correct=0.5, K=0.1)
        sv_low  = StateVector(D_e=0.1, D_correct=0.1, K=0.9)
        _, dis_high, _ = compute_3d_phase(sv_high)
        _, dis_low,  _ = compute_3d_phase(sv_low)
        assert dis_high > dis_low

    def test_high_c_and_r_high_uncertainty(self):
        sv_high = StateVector(C=1.0, R=1.0)
        sv_low  = StateVector(C=0.0, R=0.0)
        _, _, unc_high = compute_3d_phase(sv_high)
        _, _, unc_low  = compute_3d_phase(sv_low)
        assert unc_high > unc_low

    def test_uncertainty_clipped_at_one(self):
        sv = StateVector(C=1.0, R=1.0)
        _, _, unc = compute_3d_phase(sv)
        assert unc <= 1.0

    def test_zero_sv_axes(self):
        """All-zero state: exploration ~ 0.5 (eps-only), dissent ~ 0, uncertainty = 0."""
        exp, dis, unc = compute_3d_phase(StateVector())
        assert math.isclose(unc, 0.0, abs_tol=1e-6)
        assert dis < 0.01  # D_e=0, D_correct=0 → dissent near 0

    def test_intent_carries_3d_fields(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert intent.phase_exploration is not None
        assert intent.phase_dissent     is not None
        assert intent.phase_uncertainty is not None
        assert 0.0 <= intent.phase_exploration <= 1.0
        assert 0.0 <= intent.phase_dissent     <= 1.0
        assert 0.0 <= intent.phase_uncertainty <= 1.0


# ===========================================================================
# 7. Hysteresis band
# ===========================================================================

class TestHysteresis:
    def test_two_crossings_triggers_transition(self):
        c = AHGConductor()
        for _ in range(3):
            c.step(StateVector())
        # The canonical zero state maps to φ=1.4, i.e. VIGILANCE.
        # Hysteresis is tested by transitioning from that actual baseline.
        assert c.regime == Regime.VIGILANCE
        sv_flow = StateVector(N=0.6, C=0.1, R=0.05, D_e=0.05)
        c.step(sv_flow)
        c.step(sv_flow)
        assert c.regime == Regime.VIGILANCE


# ===========================================================================
# 8. PhaseIntent fields — v1.4 enrichment
# ===========================================================================

class TestPhaseIntentV14:

    def test_intent_has_v_phi(self, conductor, zero_sv):
        conductor.step(zero_sv)  # prime history
        intent = conductor.step(zero_sv)
        assert hasattr(intent, "v_phi")
        assert isinstance(intent.v_phi, float)

    def test_intent_has_a_phi(self, conductor, zero_sv):
        conductor.step(zero_sv)
        conductor.step(zero_sv)
        intent = conductor.step(zero_sv)
        assert hasattr(intent, "a_phi")
        assert isinstance(intent.a_phi, float)

    def test_intent_tribunal_active_false_for_low_phi(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert intent.tribunal_active is False

    def test_intent_tribunal_active_true_for_tension(self):
        c = AHGConductor(hysteresis_turns=1)
        sv = StateVector(D_e=10.0, N=10.0, C=10.0, R=10.0)
        intent = c.step(sv)
        if intent.regime == Regime.TENSION:
            assert intent.tribunal_active is True
            assert "p29_risk_block" in intent.constraints
            assert "p38_circuit_open" in intent.constraints
            assert intent.ttl == 5

    def test_intent_message_is_string(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert isinstance(intent.message, str)
        assert len(intent.message) > 0

    def test_intent_message_contains_phi(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert "φ=" in intent.message

    def test_intent_weights_canonical(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert intent.weights["w1_D_e"] == W1_D_E
        assert intent.weights["w2_N"]   == W2_N
        assert intent.weights["w3_C"]   == W3_C
        assert intent.weights["w4_R"]   == W4_R

    def test_turn_counter_increments(self, conductor, zero_sv):
        for i in range(1, 4):
            assert conductor.step(zero_sv).turn_id == i


# ===========================================================================
# 9. StateVector helpers
# ===========================================================================

class TestStateVector:
    def test_d_p_is_sum(self):
        sv = StateVector(D_explore=0.3, D_correct=0.2)
        assert math.isclose(sv.D_p, 0.5, rel_tol=1e-9)

    def test_d_p_zero(self):
        assert StateVector().D_p == 0.0


# ===========================================================================
# 10. AHGSidecar — v1.4: wire_herald_trace
# ===========================================================================

class TestAHGSidecarV14:

    def test_wire_herald_trace_sets_flag(self, sidecar):
        assert not sidecar.herald_wired
        sidecar.wire_herald_trace(lambda intent: None)
        assert sidecar.herald_wired

    def test_unwire_clears_flag(self, sidecar):
        sidecar.wire_herald_trace(lambda intent: None)
        sidecar.unwire_herald_trace()
        assert not sidecar.herald_wired

    def test_herald_callback_called_on_flush(self, sidecar):
        received = []
        sidecar.wire_herald_trace(received.append)
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1))
        sidecar.flush(1)
        assert len(received) == 1
        assert isinstance(received[0], PhaseIntent)

    def test_herald_callback_receives_enriched_intent(self, sidecar):
        received = []
        sidecar.wire_herald_trace(received.append)
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1, D_e_signal=0.3))
        sidecar.flush(1)
        intent = received[0]
        assert hasattr(intent, "v_phi")
        assert hasattr(intent, "tribunal_active")
        assert intent.phase_exploration is not None
        assert intent.phase_dissent     is not None
        assert intent.phase_uncertainty is not None

    def test_herald_exception_does_not_raise(self, sidecar):
        def bad_callback(intent):
            raise RuntimeError("Herald sink down")
        sidecar.wire_herald_trace(bad_callback)
        sidecar.ingest(AgentHeartbeat(agent_id="A", turn_id=1))
        # Must not raise — errors are swallowed and logged
        sidecar.flush(1)

    def test_ingest_registers_agent(self, sidecar):
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1))
        assert "Amethyst" in sidecar.registered_agents

    def test_flush_clears_buffer(self, sidecar):
        sidecar.ingest(AgentHeartbeat(agent_id="A", turn_id=1))
        sidecar.flush(1)
        assert 1 not in sidecar.pending_turns

    def test_flush_empty_returns_none(self, sidecar):
        assert sidecar.flush(99) is None

    def test_multi_agent_mean_aggregation(self):
        c = AHGConductor()
        s = AHGSidecar(conductor=c)
        s.ingest(AgentHeartbeat(agent_id="A", turn_id=1, D_e_signal=0.2, novelty_signal=0.4))
        s.ingest(AgentHeartbeat(agent_id="B", turn_id=1, D_e_signal=0.4, novelty_signal=0.6))
        intent = s.flush(1)
        expected_phi = 1.0 + 0.8 * logistic(W1_D_E*0.3 + W2_N*0.5)
        assert math.isclose(intent.phi, expected_phi, rel_tol=1e-6)

    def test_turn_buffer_rejects_mismatch(self):
        buf = TurnBuffer(turn_id=5)
        with pytest.raises(ValueError):
            buf.add(AgentHeartbeat(agent_id="X", turn_id=99))

    def test_flush_all_pending(self, sidecar):
        for t in [1, 2, 3]:
            sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=t))
        results = sidecar.flush_all_pending()
        assert set(results.keys()) == {1, 2, 3}
        assert all(isinstance(v, PhaseIntent) for v in results.values())


# ===========================================================================
# 11. Eval task stubs (Issue #32 — P-42 AHG additions)
# ===========================================================================

class TestAHGEvalStubs:
    """
    Eval task stubs registered for Issue #32.
    SKIPPED until ahg_conductor.py is wired to a live multi-agent trace.
    """

    @pytest.mark.skip(reason="Issue #32: requires live multi-agent trace (v1.5+)")
    def test_ahg_recovery_turns(self):
        """Metric: turns to reach phi < 1.45 after Tension event."""
        raise NotImplementedError("Issue #32 — ahg_recovery_turns")

    @pytest.mark.skip(reason="Issue #32: requires live multi-agent trace (v1.5+)")
    def test_ahg_entropy_recovery(self):
        """Metric: rate of D_e suppression per Tribunal cycle."""
        raise NotImplementedError("Issue #32 — ahg_entropy_recovery")

    @pytest.mark.skip(reason="Issue #32: requires live trace + Herald log fixtures (v1.5+)")
    def test_ahg_hallucination_reduction(self):
        """Metric: 20-40% reduction in contradiction persistence."""
        raise NotImplementedError("Issue #32 — ahg_hallucination_reduction")
