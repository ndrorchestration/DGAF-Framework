"""Test-only alternate method-of-steps integrator for numerical cross-checks.

This explicit-Euler oracle is intentionally separate from the production
sandbox's RK4 stage/interpolation implementation. It checks a narrow smooth
fixed-delay numerical fixture, not independent scientific validation,
proof of 4th-order convergence, or PDMAL topology effectiveness.
"""

import math

from tools.pdmal.delay_sandbox import simulate_delayed_kuramoto

GRAPH = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))
INITIAL = (0.2, -0.8, 1.4, -0.4)
FREQUENCIES = (0.13, -0.17, 0.31, 0.08)
PHYSICAL_DELAYS = {
    (0, 1): 0.12,
    (1, 0): 0.06,
    (2, 1): 0.04,
    (3, 2): 0.08,
    (0, 3): 0.10,
}
COUPLING = 1.1
HORIZON = 0.8


def _independent_euler_method_of_steps(step_size):
    """Euler method at fine resolution, using only previously stored samples.

    The positive physical delays are integer multiples of step_size; there is
    no RK4 stage, history interpolation, or call to the sandbox's derivative.
    For edges with zero delay, use the current state. Before t=0, use the
    constant initial history. This checks an independently coded integrator
    rather than an independent scientist's reproduction.
    """
    graph_neighbors: dict[int, list[int]] = {i: [] for i in range(len(INITIAL))}
    for u, v in GRAPH:
        graph_neighbors[u].append(v)
        graph_neighbors[v].append(u)

    lags: dict[tuple[int, int], int] = {}
    for edge, delay in PHYSICAL_DELAYS.items():
        count = round(delay / step_size)
        assert math.isclose(count * step_size, delay, abs_tol=1e-12)
        lags[edge] = count

    trajectory = [INITIAL]
    number_of_steps = round(HORIZON / step_size)
    for t_index in range(number_of_steps):
        current = trajectory[t_index]
        slope = []
        for receiver, neighborhood in graph_neighbors.items():
            interaction = 0.0
            for sender in neighborhood:
                source_index = t_index - lags.get((receiver, sender), 0)
                old_phase = INITIAL[sender] if source_index < 0 else trajectory[source_index][sender]
                interaction += math.sin(old_phase - current[receiver])
            slope.append(FREQUENCIES[receiver] + COUPLING * interaction / len(neighborhood))
        trajectory.append(tuple(current[i] + step_size * slope[i] for i in range(len(INITIAL))))
    return tuple(trajectory)


def _rk4_terminal_state(time_step=0.02):
    integer_lags = {edge: round(delay / time_step) for edge, delay in PHYSICAL_DELAYS.items()}
    assert all(
        math.isclose(integer_lags[edge] * time_step, delay, abs_tol=1e-12) for edge, delay in PHYSICAL_DELAYS.items()
    )
    return simulate_delayed_kuramoto(
        GRAPH,
        INITIAL,
        FREQUENCIES,
        delays=integer_lags,
        coupling=COUPLING,
        dt=time_step,
        steps=round(HORIZON / time_step),
    )[-1]


def _maximum_phase_difference(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def test_heterogeneous_directed_delay_matches_independently_coded_euler_oracle():
    """Cross-integrator agreement on a fixed verification fixture, not topology evidence."""
    rk4 = _rk4_terminal_state()
    reference = _independent_euler_method_of_steps(0.0005)[-1]
    assert _maximum_phase_difference(rk4, reference) < 0.001


def test_euler_reference_refinement_converges_toward_sandbox_solution():
    """Heuristic sanity check; does not establish RK4/DDE convergence order."""
    rk4 = _rk4_terminal_state()
    coarse = _independent_euler_method_of_steps(0.001)[-1]
    fine = _independent_euler_method_of_steps(0.0005)[-1]
    assert _maximum_phase_difference(rk4, fine) < _maximum_phase_difference(rk4, coarse)


def test_delay_direction_affects_solution_without_changing_initial_state():
    """Directed lag (receiver,sender) must not silently become undirected."""
    left = simulate_delayed_kuramoto(GRAPH, INITIAL, FREQUENCIES, delays={(0, 1): 6}, dt=0.02, steps=40)
    right = simulate_delayed_kuramoto(GRAPH, INITIAL, FREQUENCIES, delays={(1, 0): 6}, dt=0.02, steps=40)
    assert left[0] == right[0] == INITIAL
    assert _maximum_phase_difference(left[-1], right[-1]) > 0.001


def test_entire_trajectory_agrees_with_separate_euler_reference():
    """Compare every RK4 sample, including all first-delay crossing instants."""
    reference = _independent_euler_method_of_steps(0.0005)
    lag_counts = {edge: round(delay / 0.02) for edge, delay in PHYSICAL_DELAYS.items()}
    solution = simulate_delayed_kuramoto(
        GRAPH,
        INITIAL,
        FREQUENCIES,
        delays=lag_counts,
        coupling=COUPLING,
        dt=0.02,
        steps=40,
    )
    assert len(solution) == 41
    assert len(reference) == 1601
    # Same physical-time grid; 0.02 seconds = 40 reference steps.
    worst_difference = max(
        _maximum_phase_difference(state, reference[index * 40]) for index, state in enumerate(solution)
    )
    # Numerical smoke bound only: not a general solver error guarantee.
    assert worst_difference < 0.002


def test_nonuniform_stationary_state_balances_nonzero_coupling():
    """Exact fixed-history equilibrium with nontrivial phases and frequencies."""
    neighbors: dict[int, list[int]] = {i: [] for i in range(len(INITIAL))}
    for u, v in GRAPH:
        neighbors[u].append(v)
        neighbors[v].append(u)

    balanced_frequencies = tuple(
        -COUPLING / len(neighbors[i]) * sum(math.sin(INITIAL[j] - phase) for j in neighbors[i])
        for i, phase in enumerate(INITIAL)
    )
    assert any(abs(w) > 0.01 for w in balanced_frequencies)
    delays = {edge: round(physical / 0.02) for edge, physical in PHYSICAL_DELAYS.items()}
    trajectory = simulate_delayed_kuramoto(
        GRAPH, INITIAL, balanced_frequencies, delays=delays, coupling=COUPLING, dt=0.02, steps=40
    )
    assert max(
        _maximum_phase_difference(INITIAL, state) for state in trajectory
    ) < 1e-12
