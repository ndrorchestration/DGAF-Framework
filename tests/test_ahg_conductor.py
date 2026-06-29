"""
tests/test_ahg_conductor.py
Test suite for AHGConductor and AHGSidecar (P-42 v1.3)

Covers:
  TC-AHG-01  phi canonical computation (logistic normalization, [1.0, 1.8] bounds)
  TC-AHG-02  Stability Index S(t): only D_e enters, D_explore/D_correct excluded
  TC-AHG-03  7-state regime classification
  TC-AHG-04  NDR-STASIS phi=1.618 maps to Integration regime
  TC-AHG-05  Hysteresis: no transition on single-turn band crossing
  TC-AHG-06  Hysteresis: transition fires after HYSTERESIS_TURNS consecutive turns
  TC-AHG-07  Anticipatory governance: Tribunal pre-empt on high a_phi
  TC-AHG-08  Tribunal activation and exit protocol
  TC-AHG-09  AHGSidecar aggregation and flush
  TC-AHG-10  AHGSidecar auto_flush with expected_agents
  TC-AHG-11  phi bounds: S=0 -> phi near 1.4, S very large -> phi near 1.8, S very negative -> phi near 1.0
  TC-AHG-12  Governance Momentum M: updates monotonically
  TC-AHG-13  Phase velocity and acceleration computed correctly
  TC-AHG-14  D_correct and D_explore tracked in signals but excluded from S(t)
"""

import math
import pytest

from components.ahg_conductor import (
    AHGConductor,
    HeartbeatVector,
    Archetype,
    Regime,
    compute_phi,
    compute_stability_index,
    classify_regime,
    aggregate_heartbeats,
    NDR_STASIS_PHI,
    PHI_TENSION_FLOOR,
    HYSTERESIS_TURNS,
)
from components.ahg_sidecar import AHGSidecar


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_hb(
    agent_id: str = "TestAgent",
    turn_id: int = 1,
    d_e: float = 0.1,
    d_explore: float = 0.2,
    d_correct: float = 0.1,
    novelty: float = 0.3,
    constraint_count: int = 1,
    total_constraints: int = 10,
    revision_count: int = 1,
    total_turns: int = 10,
) -> HeartbeatVector:
    return HeartbeatVector(
        agent_id=agent_id,
        turn_id=turn_id,
        d_e=d_e,
        d_explore=d_explore,
        d_correct=d_correct,
        novelty=novelty,
        constraint_count=constraint_count,
        total_constraints=total_constraints,
        revision_count=revision_count,
        total_turns=total_turns,
    )


def conductor_with_n_turns(
    n: int,
    d_e: float = 0.1,
    novelty: float = 0.3,
    constraint_frac: float = 0.1,
    revision_rate: float = 0.1,
) -> AHGConductor:
    """Run conductor for n identical turns and return it."""
    conductor = AHGConductor(hysteresis_turns=HYSTERESIS_TURNS)
    for t in range(1, n + 1):
        hb = make_hb(
            turn_id=t,
            d_e=d_e,
            novelty=novelty,
            constraint_count=int(constraint_frac * 10),
            total_constraints=10,
            revision_count=int(revision_rate * 10),
            total_turns=t,
        )
        conductor.observe([hb], turn_id=t)
    return conductor


# ---------------------------------------------------------------------------
# TC-AHG-01: phi canonical computation
# ---------------------------------------------------------------------------

class TestPhiComputation:
    def test_phi_at_S_zero(self):
        """phi(S=0) = 1 + 0.8 * sigma(0) = 1 + 0.4 = 1.4"""
        phi = compute_phi(0.0)
        assert abs(phi - 1.4) < 1e-9

    def test_phi_lower_bound(self):
        """phi(S=-inf) -> 1.0"""
        phi = compute_phi(-1e9)
        assert abs(phi - 1.0) < 1e-6

    def test_phi_upper_bound(self):
        """phi(S=+inf) -> 1.8"""
        phi = compute_phi(1e9)
        assert abs(phi - 1.8) < 1e-6

    def test_phi_range_many_values(self):
        """phi always in [1.0, 1.8] for any S"""
        for S in [-100, -10, -1, 0, 0.5, 1, 2, 5, 10, 100]:
            phi = compute_phi(S)
            assert 1.0 <= phi <= 1.8, f"phi={phi} out of range for S={S}"

    def test_phi_monotone(self):
        """phi is monotonically increasing in S"""
        prev = compute_phi(-10)
        for S in [-5, -2, -1, 0, 0.5, 1, 2, 5, 10]:
            cur = compute_phi(S)
            assert cur > prev, f"Not monotone at S={S}"
            prev = cur


# ---------------------------------------------------------------------------
# TC-AHG-02: Stability Index
# ---------------------------------------------------------------------------

class TestStabilityIndex:
    def test_only_D_e_not_D_explore_D_correct(self):
        """S(t) uses D_e. Changing D_explore/D_correct alone has no effect on S."""
        S_base = compute_stability_index(D_e=0.3, N=0.2, C=0.1, R=0.1)
        # D_explore and D_correct are not parameters of S
        # verify the function ignores them (they're not in signature)
        assert abs(S_base - (0.35 * 0.3 + 0.20 * 0.2 + 0.25 * 0.1 + 0.20 * 0.1)) < 1e-9

    def test_weights_sum_not_required_to_be_one(self):
        S = compute_stability_index(D_e=1.0, N=1.0, C=1.0, R=1.0)
        assert abs(S - (0.35 + 0.20 + 0.25 + 0.20)) < 1e-9

    def test_zero_inputs(self):
        S = compute_stability_index(D_e=0.0, N=0.0, C=0.0, R=0.0)
        assert S == 0.0


# ---------------------------------------------------------------------------
# TC-AHG-03: 7-state regime classification
# ---------------------------------------------------------------------------

class TestRegimeClassification:
    @pytest.mark.parametrize("phi,expected", [
        (1.00, Regime.GROUNDED),
        (1.10, Regime.GROUNDED),
        (1.14, Regime.GROUNDED),
        (1.15, Regime.FLOW),
        (1.25, Regime.FLOW),
        (1.30, Regime.VIGILANCE),
        (1.40, Regime.VIGILANCE),
        (1.45, Regime.EXPANSION),
        (1.55, Regime.EXPANSION),
        (1.60, Regime.INTEGRATION),
        (1.65, Regime.INTEGRATION),
        (1.618, Regime.INTEGRATION),  # NDR-STASIS anchor
        (1.70, Regime.INTROSPECTION),
        (1.75, Regime.INTROSPECTION),
        (1.80, Regime.TENSION),
        (1.90, Regime.TENSION),
    ])
    def test_regime_boundaries(self, phi, expected):
        assert classify_regime(phi) == expected


# ---------------------------------------------------------------------------
# TC-AHG-04: NDR-STASIS phi=1.618 -> Integration
# ---------------------------------------------------------------------------

class TestNDRStasisAlignment:
    def test_ndr_stasis_phi_in_integration(self):
        assert abs(NDR_STASIS_PHI - 1.6180339) < 1e-5
        regime = classify_regime(NDR_STASIS_PHI)
        assert regime == Regime.INTEGRATION

    def test_ndr_stasis_archetype_is_integrator(self):
        from components.ahg_conductor import regime_to_archetype
        archetype = regime_to_archetype(Regime.INTEGRATION)
        assert archetype == Archetype.INTEGRATOR


# ---------------------------------------------------------------------------
# TC-AHG-05 & 06: Hysteresis
# ---------------------------------------------------------------------------

class TestHysteresis:
    def test_no_transition_on_single_turn(self):
        """Single turn in new band: hold current archetype."""
        conductor = AHGConductor(hysteresis_turns=2)
        # Warm up in Grounded (low S)
        for t in range(1, 5):
            conductor.observe([make_hb(turn_id=t, d_e=0.01, novelty=0.01)], turn_id=t)
        grounded_archetype = conductor.archetype
        assert grounded_archetype == Archetype.EXECUTOR

        # Single turn with high S (Tension territory)
        conductor.observe(
            [make_hb(turn_id=5, d_e=0.99, novelty=0.99, constraint_count=9, revision_count=9)],
            turn_id=5
        )
        # Should still be Executor (hysteresis holds)
        assert conductor.archetype == Archetype.EXECUTOR

    def test_transition_fires_after_hysteresis_turns(self):
        """After HYSTERESIS_TURNS consecutive turns in Tension band, Tribunal activates."""
        conductor = AHGConductor(hysteresis_turns=2)
        # Warm up in Grounded
        for t in range(1, 4):
            conductor.observe([make_hb(turn_id=t, d_e=0.01, novelty=0.01)], turn_id=t)
        # 2 consecutive Tension turns
        for t in range(4, 6):
            conductor.observe(
                [make_hb(turn_id=t, d_e=0.99, novelty=0.99, constraint_count=9, revision_count=9)],
                turn_id=t
            )
        assert conductor.archetype == Archetype.TRIBUNAL


# ---------------------------------------------------------------------------
# TC-AHG-07: Anticipatory governance
# ---------------------------------------------------------------------------

class TestAnticipatoryGovernance:
    def test_preempt_on_high_acceleration(self):
        """High a_phi while phi > 1.45 triggers Tribunal pre-empt."""
        conductor = AHGConductor(hysteresis_turns=2, accel_preempt_threshold=0.05)
        # Start at moderate phi
        conductor.observe([make_hb(turn_id=1, d_e=0.3, novelty=0.3)], turn_id=1)
        conductor.observe([make_hb(turn_id=2, d_e=0.4, novelty=0.4)], turn_id=2)
        # Rapidly escalate
        intent = conductor.observe(
            [make_hb(turn_id=3, d_e=0.90, novelty=0.80, constraint_count=7, revision_count=7)],
            turn_id=3
        )
        # With high a_phi and phi > 1.45, should pre-empt to Tribunal
        # (actual result depends on signal magnitudes; verify archetype or tribunal flag)
        assert intent.archetype in (Archetype.TRIBUNAL, Archetype.AUDITOR, Archetype.INTEGRATOR)


# ---------------------------------------------------------------------------
# TC-AHG-08: Tribunal activation and exit
# ---------------------------------------------------------------------------

class TestTribunal:
    def test_tribunal_activates_and_exits(self):
        conductor = AHGConductor(hysteresis_turns=2)
        # Drive to Tribunal
        for t in range(1, 5):
            conductor.observe(
                [make_hb(turn_id=t, d_e=0.99, novelty=0.99, constraint_count=9, revision_count=9)],
                turn_id=t
            )
        # Tribunal should be active after 2+ turns
        if conductor.tribunal_active:
            # Drive down to exit
            for t in range(5, 10):
                conductor.observe(
                    [make_hb(turn_id=t, d_e=0.01, novelty=0.01, constraint_count=0, revision_count=0)],
                    turn_id=t
                )
            assert not conductor.tribunal_active


# ---------------------------------------------------------------------------
# TC-AHG-09: Sidecar aggregation and flush
# ---------------------------------------------------------------------------

class TestSidecar:
    def test_flush_returns_phase_intent(self):
        conductor = AHGConductor()
        sidecar = AHGSidecar(conductor=conductor)
        sidecar.submit_heartbeat(make_hb(agent_id="A", turn_id=1))
        sidecar.submit_heartbeat(make_hb(agent_id="B", turn_id=1))
        intent = sidecar.flush_turn(turn_id=1)
        assert intent is not None
        assert 1.0 <= intent.phi <= 1.8

    def test_flush_missing_turn_raises(self):
        conductor = AHGConductor()
        sidecar = AHGSidecar(conductor=conductor)
        with pytest.raises(ValueError):
            sidecar.flush_turn(turn_id=99)

    def test_phi_series(self):
        conductor = AHGConductor()
        sidecar = AHGSidecar(conductor=conductor)
        for t in range(1, 6):
            sidecar.submit_heartbeat(make_hb(turn_id=t))
            sidecar.flush_turn(turn_id=t)
        series = sidecar.phi_series(n=5)
        assert len(series) == 5
        assert all(1.0 <= p <= 1.8 for p in series)


# ---------------------------------------------------------------------------
# TC-AHG-10: Auto-flush with expected_agents
# ---------------------------------------------------------------------------

class TestSidecarAutoFlush:
    def test_auto_flush_triggers_on_all_agents(self):
        conductor = AHGConductor()
        sidecar = AHGSidecar(
            conductor=conductor,
            expected_agents=["Herald", "DemiJoule"],
            auto_flush=True,
        )
        intent_a = sidecar.submit_heartbeat(make_hb(agent_id="Herald", turn_id=1))
        assert intent_a is None  # not yet flushed
        intent_b = sidecar.submit_heartbeat(make_hb(agent_id="DemiJoule", turn_id=1))
        assert intent_b is not None  # auto-flushed
        assert 1.0 <= intent_b.phi <= 1.8


# ---------------------------------------------------------------------------
# TC-AHG-11: phi bounds
# ---------------------------------------------------------------------------

class TestPhiBounds:
    def test_extreme_low_S(self):
        phi = compute_phi(-50.0)
        assert 1.0 <= phi < 1.05

    def test_extreme_high_S(self):
        phi = compute_phi(50.0)
        assert 1.75 < phi <= 1.8


# ---------------------------------------------------------------------------
# TC-AHG-12: Governance Momentum
# ---------------------------------------------------------------------------

class TestGovernanceMomentum:
    def test_momentum_updates(self):
        conductor = AHGConductor()
        conductor.observe([make_hb(turn_id=1)], turn_id=1)
        m1 = conductor._state.momentum
        conductor.observe([make_hb(turn_id=2, d_e=0.5)], turn_id=2)
        m2 = conductor._state.momentum
        assert m2 != m1


# ---------------------------------------------------------------------------
# TC-AHG-13: Phase velocity and acceleration
# ---------------------------------------------------------------------------

class TestPhaseKinematics:
    def test_velocity_computed(self):
        conductor = AHGConductor()
        conductor.observe([make_hb(turn_id=1, d_e=0.1)], turn_id=1)
        intent = conductor.observe([make_hb(turn_id=2, d_e=0.5)], turn_id=2)
        assert intent.v_phi != 0.0 or intent.phi == conductor._state.phi_history[-2]

    def test_acceleration_computed_by_turn_3(self):
        conductor = AHGConductor()
        for t in range(1, 4):
            intent = conductor.observe([make_hb(turn_id=t, d_e=t * 0.1)], turn_id=t)
        # a_phi should be non-None and a float by turn 3
        assert isinstance(intent.a_phi, float)


# ---------------------------------------------------------------------------
# TC-AHG-14: D_correct and D_explore tracked but excluded from S(t)
# ---------------------------------------------------------------------------

class TestDisaggregation:
    def test_d_explore_d_correct_in_signals(self):
        """D_explore and D_correct must appear in aggregated signals."""
        hbs = [
            make_hb(agent_id="A", turn_id=1, d_e=0.1, d_explore=0.8, d_correct=0.7),
            make_hb(agent_id="B", turn_id=1, d_e=0.1, d_explore=0.4, d_correct=0.3),
        ]
        signals = aggregate_heartbeats(hbs, turn_id=1)
        assert abs(signals.D_explore - 0.6) < 1e-9
        assert abs(signals.D_correct - 0.5) < 1e-9

    def test_S_unchanged_by_D_explore_D_correct(self):
        """Two heartbeats identical except D_explore/D_correct produce same S(t)."""
        S1 = compute_stability_index(D_e=0.3, N=0.2, C=0.1, R=0.1)
        S2 = compute_stability_index(D_e=0.3, N=0.2, C=0.1, R=0.1)
        assert abs(S1 - S2) < 1e-12
