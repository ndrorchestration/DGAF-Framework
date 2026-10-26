"""Contract tests only: neither empirical PDMAL data nor efficacy evidence."""
import math

import pytest

from tools.pdmal.delay_sandbox import circular_order_parameter, simulate_delayed_kuramoto
from tools.pdmal.lattice_harness import DODECAHEDRAL_EDGES


EDGES = ((0, 1), (1, 2), (2, 0))
INITIAL = (0.0, 0.8, -0.6)
OMEGA = (0.1, -0.2, 0.3)


def run(**kwargs):
    options = {"dt": 0.04, "steps": 25, **kwargs}
    return simulate_delayed_kuramoto(EDGES, INITIAL, OMEGA, **options)


def test_deterministic_replay_and_immutable_trace():
    delay = {(0, 1): 2, (2, 1): 5}
    a = run(delays=delay)
    assert a == run(delays=delay)
    assert len(a) == 26
    assert a[0] == INITIAL
    assert all(len(state) == 3 for state in a)


def test_zero_coupling_has_exact_uncoupled_analytic_reference():
    result = run(delays={(0, 1): 9}, coupling=0.0)
    for k, state in enumerate(result):
        for j, theta in enumerate(state):
            assert theta == pytest.approx(INITIAL[j] + OMEGA[j] * k * 0.04, abs=1e-13)


def test_uniform_equilibrium_is_stationary_even_with_delay():
    states = simulate_delayed_kuramoto(
        EDGES, (0.5,) * 3, (0.0,) * 3,
        delays={(0, 1): 3, (2, 1): 7}, steps=40,
    )
    assert all(x == pytest.approx(0.5) for state in states for x in state)
    assert circular_order_parameter(states[-1]) == pytest.approx(1.0)


def test_delays_affect_numerical_trajectory_without_changing_initial_condition():
    delayed = run(delays={(0, 1): 3})
    instantaneous = run()
    assert delayed[0] == instantaneous[0]
    assert max(abs(a - b) for a, b in zip(delayed[-1], instantaneous[-1])) > 1e-5


def test_constant_global_phase_shift_is_invariant():
    lag = {(0, 1): 2, (1, 2): 1, (2, 0): 4}
    base = run(delays=lag)
    shifted = simulate_delayed_kuramoto(
        EDGES, tuple(x + 1.7 for x in INITIAL),
        OMEGA, delays=lag, dt=0.04, steps=25,
    )
    for state_a, state_b in zip(base, shifted):
        for a, b in zip(state_a, state_b):
            assert b - a == pytest.approx(1.7, abs=1e-12)


def test_zero_lag_explicit_map_equals_default():
    assert run() == run(delays={(0, 1): 0, (1, 0): 0})


def test_dodecahedral_proxy_can_run_without_extra_dependencies():
    theta = tuple(0.1 * i for i in range(20))
    traces = simulate_delayed_kuramoto(
        DODECAHEDRAL_EDGES, theta, (0.0,) * 20,
        delays={(0, 1): 2, (10, 0): 1}, dt=0.05, steps=2,
    )
    assert len(traces[-1]) == 20
    assert len(traces) == 3


@pytest.mark.parametrize("changes", [
    {"delays": {(0, 2): -1}},
    {"delays": {(0, 5): 1}},
    {"delays": {(0, 1): 1.5}},
    {"delays": {(0, 1): True}},
    {"dt": 0.0},
    {"dt": math.inf},
    {"coupling": math.nan},
    {"steps": -1},
    {"steps": 3.0},
])
def test_invalid_inputs_fail_closed(changes):
    with pytest.raises(ValueError):
        run(**changes)


def test_graph_rejects_duplicate_and_isolated_vertices():
    with pytest.raises(ValueError):
        simulate_delayed_kuramoto(((0, 1), (1, 0), (1, 2)), INITIAL, OMEGA)
    with pytest.raises(ValueError):
        simulate_delayed_kuramoto(((0, 1),), INITIAL, OMEGA)


def test_order_parameter_does_not_conflate_phase_wrap_with_failure():
    assert circular_order_parameter((0.0, 2 * math.pi)) == pytest.approx(1.0)
    assert circular_order_parameter((0.0, math.pi)) == pytest.approx(0.0, abs=1e-12)
    with pytest.raises(ValueError):
        circular_order_parameter(())


def test_step_refinement_reduces_error_against_finer_reference():
    # Physical delay tau=0.12 throughout: lag integer changes with time step.
    # Heuristic numerical consistency check, not a convergence-order proof.
    def endpoint(dt):
        return simulate_delayed_kuramoto(
            EDGES, INITIAL, OMEGA, delays={(0, 1): round(0.12 / dt)},
            dt=dt, steps=round(1.2 / dt),
        )[-1]

    ref = endpoint(0.005)
    coarse = endpoint(0.04)
    fine = endpoint(0.02)
    err_coarse = max(abs(a - b) for a, b in zip(coarse, ref))
    err_fine = max(abs(a - b) for a, b in zip(fine, ref))
    assert err_fine < err_coarse
