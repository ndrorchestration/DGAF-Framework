"""Same-author early DDE history-boundary checks, no external solver needed."""

import math

import pytest

from tools.pdmal.delay_sandbox import simulate_delayed_kuramoto
from tools.pdmal.early_window_oracle import (
    EARLIEST_POSITIVE_DELAY,
    analytic_initial_derivatives,
    initial_window_rhs,
    initial_window_trajectory,
)
from tools.pdmal.scipy_reference_probe import COUPLING, DELAYS, FREQUENCIES, GRAPH, INITIAL


def test_first_positive_lag_establishes_exact_ordinary_equation_interval():
    assert EARLIEST_POSITIVE_DELAY == pytest.approx(0.04, abs=1e-14)
    assert min(DELAYS.values()) == EARLIEST_POSITIVE_DELAY
    assert initial_window_rhs(INITIAL) == pytest.approx(analytic_initial_derivatives()[0])


def test_analytic_right_slope_is_pinned_without_numerical_dde_solver():
    slope, _ = analytic_initial_derivatives()
    assert slope == pytest.approx(
        (-0.04382726981975876, 0.7374820637451177, -0.6852738109105043, 0.926169557350277),
        abs=1e-14,
    )


def test_right_acceleration_accounts_for_zero_vs_positive_directed_lags():
    _, acceleration = analytic_initial_derivatives()
    assert acceleration == pytest.approx(
        (-0.06327968042603098, 0.2413565892312074, -0.19689068074438454, -0.32457989538802645),
        abs=1e-13,
    )


def test_short_interval_ode_agrees_with_existing_rk4_at_both_early_samples():
    """Software paths agree on t<=min delay; not an independent scientific result."""
    lag_steps = {edge: round(physical / 0.02) for edge, physical in DELAYS.items()}
    full = simulate_delayed_kuramoto(GRAPH, INITIAL, FREQUENCIES, delays=lag_steps, coupling=COUPLING, dt=0.02, steps=2)
    short = initial_window_trajectory(0.02)
    assert len(full) == len(short) == 3
    for state, expected in zip(short, full):
        assert state == pytest.approx(expected, abs=2e-13)


def test_first_interval_substepping_is_stable_under_halving():
    reference = initial_window_trajectory(0.0025)
    coarse = initial_window_trajectory(0.02)
    medium = initial_window_trajectory(0.01)
    assert len(reference) == 17
    assert len(coarse) == 3
    assert len(medium) == 5
    error_coarse = max(abs(a - b) for a, b in zip(coarse[-1], reference[-1]))
    error_medium = max(abs(a - b) for a, b in zip(medium[-1], reference[-1]))
    assert 0 < error_medium < error_coarse
    assert error_coarse < 1e-9


def test_second_order_initial_taylor_has_small_but_nonzero_remainder():
    slope, acceleration = analytic_initial_derivatives()
    t = 0.02
    taylor = tuple(INITIAL[i] + t * slope[i] + t * t * acceleration[i] / 2 for i in range(4))
    early = initial_window_trajectory(0.0025)[8]
    error = max(abs(a - b) for a, b in zip(taylor, early))
    assert 1e-7 < error < 3e-6


@pytest.mark.parametrize("dt", [0.0, -0.01, True, math.nan, math.inf, 0.03, 0.05])
def test_first_window_ode_rejects_unaligned_or_invalid_timestep(dt):
    with pytest.raises(ValueError):
        initial_window_trajectory(dt)


@pytest.mark.parametrize("bad_state", [(), (1.0,), (math.nan, 0, 0, 0), (0, 0, 0, math.inf)])
def test_analytic_first_window_rejects_wrong_dimension_or_nonfinite_state(bad_state):
    with pytest.raises(ValueError):
        initial_window_rhs(bad_state)
