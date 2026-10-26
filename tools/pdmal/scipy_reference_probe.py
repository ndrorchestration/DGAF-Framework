"""Opt-in numerical probe: SciPy ODE core + locally authored DDE history.

This checks a fixed 4-node oscillator *implementation*, not graph superiority,
scientific N, an independently maintained DDE solver, or an outside review.
NO SCIENTIFIC RUNNER. SciPy is optional; none of the CI/production lock sets
is changed. Invoke manually: python -m tools.pdmal.scipy_reference_probe
"""

from __future__ import annotations

import bisect
import hashlib
import json
import math
import sys
from pathlib import Path

from tools.pdmal.delay_sandbox import simulate_delayed_kuramoto

GRAPH = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))
INITIAL = (0.2, -0.8, 1.4, -0.4)
FREQUENCIES = (0.13, -0.17, 0.31, 0.08)
DELAYS = {(0, 1): 0.12, (1, 0): 0.06, (2, 1): 0.04, (3, 2): 0.08, (0, 3): 0.10}
COUPLING = 1.1
HORIZON = 0.8
GRID = 0.02


def _max_phase_difference(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return max(abs(a - b) for a, b in zip(left, right))


def reference_trajectory(segment: float, rtol: float, atol: float) -> tuple[tuple[float, ...], ...]:
    """Author-coded method of steps with SciPy-maintained DOP853 ODE solver.

    Segments of 0.02 or 0.01 s are shorter than the smallest positive delay
    (0.04 s), so every delayed source is in an ALREADY solved segment.
    Zero-delay neighbors use the current ODE stage. Negative time has the
    frozen theta(0) history; no future stage is interpolated.
    """
    try:
        from scipy.integrate import solve_ivp
    except ImportError as exc:
        raise RuntimeError("optional SciPy is needed; no dependency is automatically installed") from exc

    adjacency: list[list[int]] = [[] for _ in INITIAL]
    for u, v in GRAPH:
        adjacency[u].append(v)
        adjacency[v].append(u)

    boundaries: list[float] = []
    dense_segments = []
    states: list[tuple[float, ...]] = [INITIAL]
    for k in range(round(HORIZON / segment)):
        start = round(k * segment, 12)
        end = round((k + 1) * segment, 12)

        def derivative(t, phase):
            rates = []
            for receiver, neighbors in enumerate(adjacency):
                interaction = 0.0
                for sender in neighbors:
                    lag = DELAYS.get((receiver, sender), 0.0)
                    if lag == 0.0:
                        delayed_sender = phase[sender]
                    else:
                        query_time = t - lag
                        if query_time <= 1e-14:
                            delayed_sender = INITIAL[sender]
                        else:
                            source_index = bisect.bisect_left(boundaries, query_time - 1e-12)
                            if source_index >= len(dense_segments):
                                raise ArithmeticError("reference queried unsolved future delay history")
                            delayed_sender = float(dense_segments[source_index](query_time)[sender])
                    interaction += math.sin(delayed_sender - phase[receiver])
                rates.append(FREQUENCIES[receiver] + COUPLING * interaction / len(neighbors))
            return rates

        result = solve_ivp(
            derivative,
            (start, end),
            states[-1],
            method="DOP853",
            dense_output=True,
            rtol=rtol,
            atol=atol,
            max_step=segment / 2,
        )
        if not result.success:
            raise ArithmeticError(f"SciPy reference integration failed: {result.message}")
        boundaries.append(end)
        dense_segments.append(result.sol)
        states.append(tuple(float(v) for v in result.y[:, -1]))
    return tuple(states)


def main() -> None:
    """Read-only, self-contained numerical verification receipt to stdout."""
    import scipy

    coarse_reference = reference_trajectory(segment=0.02, rtol=1e-11, atol=1e-13)
    fine_reference = reference_trajectory(segment=0.01, rtol=1e-12, atol=1e-14)
    refinement_difference = max(
        _max_phase_difference(phase, fine_reference[2 * i]) for i, phase in enumerate(coarse_reference)
    )

    comparisons: dict[str, dict[str, float | int]] = {}
    for step in (0.02, 0.01, 0.005, 0.0025):
        lag_steps = {edge: round(tau / step) for edge, tau in DELAYS.items()}
        if any(not math.isclose(lag_steps[key] * step, tau, abs_tol=1e-12) for key, tau in DELAYS.items()):
            raise ArithmeticError("delay cannot be represented on the solver step grid")
        actual = simulate_delayed_kuramoto(
            GRAPH,
            INITIAL,
            FREQUENCIES,
            delays=lag_steps,
            coupling=COUPLING,
            dt=step,
            steps=round(HORIZON / step),
        )
        ratio = round(GRID / step)
        worst = max(
            _max_phase_difference(phase, coarse_reference[i // ratio])
            for i, phase in enumerate(actual)
            if i % ratio == 0
        )
        comparisons[str(step)] = {
            "full_trace_max_phase_error_rad": worst,
            "terminal_max_phase_error_rad": _max_phase_difference(actual[-1], coarse_reference[-1]),
            "n_states": len(actual),
        }

    sandbox_path = Path(__file__).with_name("delay_sandbox.py")
    receipt = {
        "status": "LOCAL_NUMERICAL_PROBE_ONLY",
        "admission": "NON_ADMITTED_NOT_EXTERNAL_DDE_VALIDATION",
        "scipy_version": scipy.__version__,
        "python_version": sys.version.split()[0],
        "ode_core": "SciPy DOP853",
        "dde_history": "author-coded method of steps, fixed negative-time constant history",
        "model_fixture": "4-node directed heterogeneous delay; K=1.1; t_end=0.8s",
        "sandbox_source_sha256": hashlib.sha256(sandbox_path.read_bytes()).hexdigest(),
        "reference_tolerances": {"rtol": 1e-11, "atol": 1e-13},
        "reference_refinement_max_phase_error_rad": refinement_difference,
        "terminal_reference_phase_unwrapped_rad": coarse_reference[-1],
        "rk4_vs_scipy": comparisons,
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "pilot_authorization": "NOT_GRANTED",
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
