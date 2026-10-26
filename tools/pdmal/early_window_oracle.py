"""Analytic right derivatives and a no-delay-history first-window ODE check.

Only t in [0, min positive delay] is modeled; positive directed delays see
the constant prescribed past, while zero-lag neighbors see current states.
NON-ADMITTED, SAME-AUTHOR numerical/analytic software evidence only.
This does not supply a full DDE solver or an independent validation.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from tools.pdmal.scipy_reference_probe import (
    COUPLING,
    DELAYS,
    FREQUENCIES,
    GRAPH,
    INITIAL,
)

EARLIEST_POSITIVE_DELAY = min(DELAYS.values())


def initial_window_rhs(phases: Sequence[float]) -> tuple[float, ...]:
    """True right-side ODE while t is no later than minimum positive lag."""
    if len(phases) != len(INITIAL) or any(not math.isfinite(v) for v in phases):
        raise ValueError("phases must be a finite four-node vector")
    neighbors: list[list[int]] = [[] for _ in INITIAL]
    for u, v in GRAPH:
        neighbors[u].append(v)
        neighbors[v].append(u)
    return tuple(
        FREQUENCIES[i]
        + COUPLING
        / len(neighbors[i])
        * sum(math.sin((INITIAL[j] if (i, j) in DELAYS else phases[j]) - phases[i]) for j in neighbors[i])
        for i in range(len(INITIAL))
    )


def analytic_initial_derivatives() -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Right-side first and second phase derivatives at t=0 (rad/s, rad/s²).

    The specified history has zero derivative before zero. For positive
    delays, their source slope at the right-hand boundary remains zero.
    For zero delay links, the current source slope enters the acceleration.
    """
    slope = initial_window_rhs(INITIAL)
    neighbors: list[list[int]] = [[] for _ in INITIAL]
    for u, v in GRAPH:
        neighbors[u].append(v)
        neighbors[v].append(u)
    acceleration = tuple(
        COUPLING
        / len(neighbors[i])
        * sum(
            math.cos(INITIAL[j] - INITIAL[i]) * ((0.0 if (i, j) in DELAYS else slope[j]) - slope[i])
            for j in neighbors[i]
        )
        for i in range(len(INITIAL))
    )
    return slope, acceleration


def initial_window_trajectory(dt: float) -> tuple[tuple[float, ...], ...]:
    """Independent short-window RK4 ODE path, without delay buffers or SciPy.

    Returns states at 0, dt, ..., minimum positive lag. Divisibility is
    required so no timestamp is silently rounded or skipped.
    """
    if type(dt) not in (int, float) or not math.isfinite(dt) or dt <= 0:
        raise ValueError("dt must be finite and positive")
    n = EARLIEST_POSITIVE_DELAY / dt
    if dt > EARLIEST_POSITIVE_DELAY or not math.isclose(n, round(n), abs_tol=1e-10, rel_tol=0):
        raise ValueError("dt must evenly divide the first positive directed delay")
    steps = round(n)
    states: list[tuple[float, ...]] = [INITIAL]
    for _ in range(steps):
        current = states[-1]
        k1 = initial_window_rhs(current)
        k2 = initial_window_rhs(tuple(v + 0.5 * dt * s for v, s in zip(current, k1)))
        k3 = initial_window_rhs(tuple(v + 0.5 * dt * s for v, s in zip(current, k2)))
        k4 = initial_window_rhs(tuple(v + dt * s for v, s in zip(current, k3)))
        next_state = tuple(v + dt * (a + 2 * b + 2 * c + d) / 6 for v, a, b, c, d in zip(current, k1, k2, k3, k4))
        if any(not math.isfinite(v) for v in next_state):
            raise ArithmeticError("nonfinite initial-window phase state")
        states.append(next_state)
    return tuple(states)
