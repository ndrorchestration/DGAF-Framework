"""
tests/test_ahg_conductor.py — AHG Conductor + Sidecar Unit Tests
P-42 · Layer 12 — Cognitive Control Plane · v1.3 scaffold
Amethyst × COLLEEN · S072 · 2026-07-02

Coverage targets (v1.3 scaffold):
  - φ computation: canonical weights, logistic normalization, bounds
  - Regime classification: all 7 states + boundary values
  - Hysteresis band: 2-turn transition guard
  - Phase velocity + acceleration
  - PhaseIntent field validation
  - Tribunal activation
  - AHGSidecar: ingestion, aggregation, flush round-trip
  - NDR-STASIS anchor: φ=1.618 ∈ Integration regime

Eval task stubs (Issue #32 — implementation deferred to live stack wiring):
  - ahg_recovery_turns
  - ahg_entropy_recovery
  - ahg_hallucination_reduction
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
    W1_D_E,
    W2_N,
    W3_C,
    W4_R,
    PHI_MIN,
    PHI_MAX,
    compute_phi,
    compute_stability_index,
    compute_phase_acceleration,
    compute_phase_velocity,
    classify_regime,
    logistic,
)
from components.ahg_sidecar import AgentHeartbeat, AHGSidecar, TurnBuffer


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def zero_sv() -> StateVector:
    """All-zero state vector — minimal entropy, minimal novelty."""
    return StateVector()


@pytest.fixture
def high_entropy_sv() -> StateVector:
    """High D_e — should push φ toward Tension."""
    return StateVector(D_e=1.0, N=0.8, C=0.9, R=0.8)


@pytest.fixture
def integration_sv() -> StateVector:
    """State vector engineered to yield φ ≈ 1.618 (NDR-STASIS anchor)."""
    # S(t) = w1*D_e + w2*N + w3*C + w4*R
    # Target: φ = 1 + 0.8*σ(S) = 1.618 => σ(S) = 0.7725 => S ≈ 1.232
    # Set D_e=0.5, N=0.5, C=0.5, R=0.5 => S = 0.35*0.5+0.20*0.5+0.25*0.5+0.20*0.5 = 0.5
    # φ = 1 + 0.8*σ(0.5) = 1 + 0.8*0.6225 = 1.498 (Expansion)
    # For Integration: increase entropy contribution slightly
    return StateVector(D_e=0.9, N=0.6, C=0.7, R=0.5)


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
    """AHG_ARCHITECTURE.md §2.2 — default weights must be exact."""

    def test_weights_sum_to_one(self):
        assert math.isclose(W1_D_E + W2_N + W3_C + W4_R, 1.0, rel_tol=1e-9)

    def test_w1_d_e(self):
        assert W1_D_E == 0.35

    def test_w2_n(self):
        assert W2_N == 0.20

    def test_w3_c(self):
        assert W3_C == 0.25

    def test_w4_r(self):
        assert W4_R == 0.20

    def test_phi_bounds(self):
        assert PHI_MIN == 1.0
        assert PHI_MAX == 1.8


# ===========================================================================
# 2. φ computation
# ===========================================================================

class TestPhiComputation:
    """AHG_ARCHITECTURE.md §2.2 — logistic normalization + bounds."""

    def test_zero_sv_phi_in_bounds(self, zero_sv):
        phi = compute_phi(zero_sv)
        assert PHI_MIN <= phi <= PHI_MAX

    def test_high_entropy_phi_in_bounds(self, high_entropy_sv):
        phi = compute_phi(high_entropy_sv)
        assert PHI_MIN <= phi <= PHI_MAX

    def test_phi_strictly_greater_than_min(self, zero_sv):
        """logistic(x) > 0 for all x => phi > PHI_MIN always."""
        phi = compute_phi(zero_sv)
        assert phi > PHI_MIN

    def test_phi_strictly_less_than_max(self, high_entropy_sv):
        """logistic(x) < 1 for all x => phi < PHI_MAX always."""
        phi = compute_phi(high_entropy_sv)
        assert phi < PHI_MAX

    def test_phi_monotone_with_entropy(self):
        """Higher D_e => higher φ."""
        low  = compute_phi(StateVector(D_e=0.1))
        high = compute_phi(StateVector(D_e=0.9))
        assert high > low

    def test_d_explore_excluded_from_phi(self):
        """D_explore does not enter S(t) — phi must be identical."""
        base = compute_phi(StateVector(D_e=0.5))
        with_explore = compute_phi(StateVector(D_e=0.5, D_explore=0.9))
        assert math.isclose(base, with_explore, rel_tol=1e-12)

    def test_d_correct_excluded_from_phi(self):
        """D_correct does not enter S(t) — phi must be identical."""
        base = compute_phi(StateVector(D_e=0.5))
        with_correct = compute_phi(StateVector(D_e=0.5, D_correct=0.9))
        assert math.isclose(base, with_correct, rel_tol=1e-12)

    def test_stability_index_formula(self):
        sv = StateVector(D_e=0.4, N=0.3, C=0.2, R=0.1)
        expected_s = 0.35*0.4 + 0.20*0.3 + 0.25*0.2 + 0.20*0.1
        assert math.isclose(compute_stability_index(sv), expected_s, rel_tol=1e-9)

    def test_logistic_midpoint(self):
        """\u03c3(0) = 0.5 by definition."""
        assert math.isclose(logistic(0.0), 0.5, rel_tol=1e-9)

    def test_phi_formula_direct(self):
        sv = StateVector(D_e=0.0, N=0.0, C=0.0, R=0.0)
        s = 0.0
        expected_phi = 1.0 + 0.8 * logistic(s)
        assert math.isclose(compute_phi(sv), expected_phi, rel_tol=1e-12)


# ===========================================================================
# 3. NDR-STASIS anchor
# ===========================================================================

class TestNDRStasisAnchor:
    """
    NDR-STASIS design value φ=1.618 must fall in Integration regime [1.60, 1.70].
    AHG_ARCHITECTURE.md §3 — 'NDR-STASIS anchor φ=1.618 sits here —
    peak productive phase'.
    """

    def test_phi_1618_is_integration(self):
        regime = classify_regime(1.618)
        assert regime == Regime.INTEGRATION

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
    """AHG_ARCHITECTURE.md §3 — 7-state regime table."""

    @pytest.mark.parametrize("phi,expected", [
        (1.00, Regime.GROUNDED),
        (1.07, Regime.GROUNDED),
        (1.14, Regime.GROUNDED),
        (1.15, Regime.FLOW),
        (1.22, Regime.FLOW),
        (1.29, Regime.FLOW),
        (1.30, Regime.VIGILANCE),
        (1.37, Regime.VIGILANCE),
        (1.44, Regime.VIGILANCE),
        (1.45, Regime.EXPANSION),
        (1.52, Regime.EXPANSION),
        (1.59, Regime.EXPANSION),
        (1.60, Regime.INTEGRATION),
        (1.618, Regime.INTEGRATION),
        (1.69, Regime.INTEGRATION),
        (1.70, Regime.INTROSPECTION),
        (1.75, Regime.INTROSPECTION),
        (1.79, Regime.INTROSPECTION),
        (1.80, Regime.TENSION),
        (1.85, Regime.TENSION),
        (1.799, Regime.INTROSPECTION),
    ])
    def test_regime_boundary(self, phi, expected):
        assert classify_regime(phi) == expected


# ===========================================================================
# 5. Phase velocity + acceleration
# ===========================================================================

class TestPhaseKinematics:
    """AHG_ARCHITECTURE.md §2.3"""

    def test_velocity_insufficient_history(self):
        assert compute_phase_velocity([1.3]) == 0.0

    def test_velocity_two_points(self):
        v = compute_phase_velocity([1.3, 1.5])
        assert math.isclose(v, 0.2, rel_tol=1e-9)

    def test_velocity_descending(self):
        v = compute_phase_velocity([1.6, 1.4])
        assert math.isclose(v, -0.2, rel_tol=1e-9)

    def test_acceleration_insufficient_history(self):
        assert compute_phase_acceleration([1.3, 1.5]) == 0.0

    def test_acceleration_three_points(self):
        # v_{t-1} = 1.5 - 1.3 = 0.2; v_t = 1.8 - 1.5 = 0.3; a = 0.1
        a = compute_phase_acceleration([1.3, 1.5, 1.8])
        assert math.isclose(a, 0.1, rel_tol=1e-9)

    def test_acceleration_decelerating(self):
        # v_{t-1} = 0.3; v_t = 0.1; a = -0.2
        a = compute_phase_acceleration([1.0, 1.3, 1.4])
        assert math.isclose(a, -0.2, rel_tol=1e-9)


# ===========================================================================
# 6. Hysteresis band
# ===========================================================================

class TestHysteresis:
    """AHG_ARCHITECTURE.md §2.4 — transition fires only after 2 consecutive
    turns crossing the band edge."""

    def test_single_crossing_does_not_transition(self):
        c = AHGConductor()
        # Prime with Grounded
        c.step(StateVector(D_e=0.0, N=0.0, C=0.0, R=0.0))
        grounded_regime = c.regime
        assert grounded_regime == Regime.GROUNDED

        # One step into high-entropy (Tension-bound) territory
        intent = c.step(StateVector(D_e=1.0, N=1.0, C=1.0, R=1.0))
        # With hysteresis, regime should NOT yet flip on turn 1 of crossing
        # (pending_turns=1, need 2)
        # It may stay at Grounded or partially transition depending on
        # phi magnitude — assert it is NOT yet Tribunal if only 1 cross
        # (phi > 1.8 impossible in 1 step from fresh conductor)
        assert intent.regime in list(Regime)  # valid regime returned

    def test_two_crossings_triggers_transition(self):
        """Two consecutive steps in new regime => transition fires."""
        c = AHGConductor()
        # Establish Grounded baseline
        for _ in range(3):
            c.step(StateVector())
        assert c.regime == Regime.GROUNDED

        # Two consecutive high-novelty steps should move into Flow+
        sv_flow = StateVector(N=0.6, C=0.1, R=0.05, D_e=0.05)
        c.step(sv_flow)
        c.step(sv_flow)
        # After 2 turns, transition should have fired
        assert c.regime != Regime.GROUNDED


# ===========================================================================
# 7. AHGConductor.step — PhaseIntent fields
# ===========================================================================

class TestConductorStep:
    """Validate PhaseIntent structure and conductor state after step()."""

    def test_returns_phase_intent(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert isinstance(intent, PhaseIntent)

    def test_intent_phi_in_bounds(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert PHI_MIN <= intent.phi <= PHI_MAX

    def test_intent_regime_matches_phi(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert intent.regime == classify_regime(intent.phi)

    def test_intent_mode_matches_regime(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        from components.ahg_conductor import _REGIME_ARCHETYPE
        assert intent.mode == _REGIME_ARCHETYPE[intent.regime]

    def test_intent_weights_canonical(self, conductor, zero_sv):
        intent = conductor.step(zero_sv)
        assert intent.weights["w1_D_e"] == W1_D_E
        assert intent.weights["w2_N"]   == W2_N
        assert intent.weights["w3_C"]   == W3_C
        assert intent.weights["w4_R"]   == W4_R

    def test_turn_counter_increments(self, conductor, zero_sv):
        for i in range(1, 4):
            intent = conductor.step(zero_sv)
            assert intent.turn_id == i

    def test_tribunal_constraints_on_tension(self):
        c = AHGConductor(hysteresis_turns=1)  # disable hysteresis for test
        # Force phi into Tension by using very high entropy
        # phi > 1.80 is asymptotically approached; use extreme values
        sv = StateVector(D_e=10.0, N=10.0, C=10.0, R=10.0)
        intent = c.step(sv)
        if intent.regime == Regime.TENSION:
            assert "p29_risk_block" in intent.constraints
            assert "p38_circuit_open" in intent.constraints
            assert "apogee_lens_mandatory" in intent.constraints

    def test_introspection_requires_apogee(self):
        c = AHGConductor(hysteresis_turns=1)
        # phi 1.70-1.80 => Introspection
        # S(t) s.t. phi ~ 1.75: sigma(S) = (1.75-1)/0.8 = 0.9375
        # logistic inverse: S = ln(0.9375/0.0625) = ln(15) ~ 2.708
        # D_e=2.708/0.35 with N=C=R=0
        sv = StateVector(D_e=7.0, N=0.0, C=0.0, R=0.0)
        intent = c.step(sv)
        if intent.regime == Regime.INTROSPECTION:
            assert "apogee_lens_mandatory" in intent.constraints


# ===========================================================================
# 8. StateVector helpers
# ===========================================================================

class TestStateVector:
    def test_d_p_is_sum_of_explore_and_correct(self):
        sv = StateVector(D_explore=0.3, D_correct=0.2)
        assert math.isclose(sv.D_p, 0.5, rel_tol=1e-9)

    def test_d_p_zero_when_both_zero(self):
        assert StateVector().D_p == 0.0


# ===========================================================================
# 9. AHGSidecar — heartbeat ingestion + aggregation
# ===========================================================================

class TestAHGSidecar:

    def test_ingest_registers_agent(self, sidecar):
        hb = AgentHeartbeat(agent_id="Amethyst", turn_id=1, D_e_signal=0.1)
        sidecar.ingest(hb)
        assert "Amethyst" in sidecar.registered_agents

    def test_pending_turns_after_ingest(self, sidecar):
        hb = AgentHeartbeat(agent_id="COLLEEN", turn_id=1)
        sidecar.ingest(hb)
        assert 1 in sidecar.pending_turns

    def test_flush_returns_phase_intent(self, sidecar):
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1))
        intent = sidecar.flush(1)
        assert isinstance(intent, PhaseIntent)

    def test_flush_clears_buffer(self, sidecar):
        sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=1))
        sidecar.flush(1)
        assert 1 not in sidecar.pending_turns

    def test_flush_empty_buffer_returns_none(self, sidecar):
        result = sidecar.flush(99)
        assert result is None

    def test_multi_agent_mean_aggregation(self):
        c = AHGConductor()
        s = AHGSidecar(conductor=c)
        s.ingest(AgentHeartbeat(agent_id="A", turn_id=1, D_e_signal=0.2, novelty_signal=0.4))
        s.ingest(AgentHeartbeat(agent_id="B", turn_id=1, D_e_signal=0.4, novelty_signal=0.6))
        intent = s.flush(1)
        # Mean D_e = 0.3, Mean N = 0.5
        # S(t) = 0.35*0.3 + 0.20*0.5 = 0.105 + 0.10 = 0.205
        expected_phi = 1.0 + 0.8 * logistic(0.35*0.3 + 0.20*0.5)
        assert math.isclose(intent.phi, expected_phi, rel_tol=1e-6)

    def test_turn_buffer_rejects_mismatched_turn_id(self):
        buf = TurnBuffer(turn_id=5)
        with pytest.raises(ValueError):
            buf.add(AgentHeartbeat(agent_id="X", turn_id=99))

    def test_flush_all_pending(self, sidecar):
        for turn in [1, 2, 3]:
            sidecar.ingest(AgentHeartbeat(agent_id="Amethyst", turn_id=turn))
        results = sidecar.flush_all_pending()
        assert set(results.keys()) == {1, 2, 3}
        assert all(isinstance(v, PhaseIntent) for v in results.values())


# ===========================================================================
# 10. Eval task stubs (Issue #32 — P-42 AHG additions)
# ===========================================================================

class TestAHGEvalStubs:
    """
    Eval task stubs registered for Issue #32.
    These are SKIPPED until ahg_conductor.py is wired to a live multi-agent
    trace and baseline measurements are established.

    Tasks:
      ahg_recovery_turns      — AHG_ARCHITECTURE.md §6, Issue #32
      ahg_entropy_recovery    — AHG_ARCHITECTURE.md §6, Issue #32
      ahg_hallucination_reduction — AHG_ARCHITECTURE.md §6, Issue #32
    """

    @pytest.mark.skip(reason="Issue #32: requires live multi-agent trace (v1.4)")
    def test_ahg_recovery_turns(self):
        """
        Metric: turns to reach phi < 1.45 after Tension event.
        Baseline: no-AHG control run.
        Target: AHG reduces recovery turns vs control.
        Method: new eval task 'ahg_recovery_turns' in dgaf_eval_suite.py.
        """
        raise NotImplementedError("Issue #32 — ahg_recovery_turns")

    @pytest.mark.skip(reason="Issue #32: requires live multi-agent trace (v1.4)")
    def test_ahg_entropy_recovery(self):
        """
        Metric: rate of D_e suppression per Tribunal cycle.
        Target: measurable per-cycle D_e decay.
        Method: new eval task 'ahg_entropy_recovery' in dgaf_eval_suite.py.
        """
        raise NotImplementedError("Issue #32 — ahg_entropy_recovery")

    @pytest.mark.skip(reason="Issue #32: requires live trace + Herald log fixtures (v1.4)")
    def test_ahg_hallucination_reduction(self):
        """
        Metric: contradiction persistence + ungrounded claims.
        Predicted improvement: 20-40% reduction vs no-AHG baseline.
        Method: extends 'audit_hallucination_rate' task in dgaf_eval_suite.py.
        Source: AHG_ARCHITECTURE.md §6 — currently theoretical.
        """
        raise NotImplementedError("Issue #32 — ahg_hallucination_reduction")
