"""Isolated delayed Kuramoto sandbox for exploratory PDMAL graph comparisons.

NON-ADMITTED: Not imported by governed PDMAL pilot; no empirical collection,
authorization, or efficacy claim. delays[(i, j)] is sender j -> receiver i
latency in whole multiples of dt. Negative-time phase history is constant.
Delayed history is interpolated in unwrapped phases for RK4 stages.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence


def simulate_delayed_kuramoto(
    edges: Sequence[tuple[int, int]],
    initial_phases: Sequence[float],
    frequencies: Sequence[float],
    *,
    delays: Mapping[tuple[int, int], int] | None = None,
    coupling: float = 1.0,
    dt: float = 0.05,
    steps: int = 100,
) -> tuple[tuple[float, ...], ...]:
    """Degree-normalized delayed Kuramoto model with deterministic RK4.

    dθ_i/dt = ω_i + K/degree(i) * sum_j sin(θ_j(t - τ_ij) - θ_i(t)).
    Returns phase vectors at t=0,dt,...,steps*dt. This is not an independently
    validated delay differential equation (DDE) solver. Discrete, static delays
    only; no noise, packet loss, real traffic, or runtime agent coordination.
    """
    initial = tuple(float(x) for x in initial_phases)
    omega = tuple(float(x) for x in frequencies)
    n_nodes = len(initial)
    if n_nodes < 2 or len(omega) != n_nodes:
        raise ValueError("must supply matching phase/frequency arrays for >=2 nodes")
    if any(not math.isfinite(x) for x in (*initial, *omega)):
        raise ValueError("phase and frequency values must be finite")
    if not math.isfinite(coupling) or not math.isfinite(dt) or dt <= 0:
        raise ValueError("coupling must be finite and dt positive and finite")
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be a nonnegative integer")

    neighbor_sets: list[set[int]] = [set() for _ in range(n_nodes)]
    seen: set[tuple[int, int]] = set()
    for u, v in edges:
        if type(u) is not int or type(v) is not int or not (0 <= u < n_nodes and 0 <= v < n_nodes) or u == v:
            raise ValueError("edges require distinct integer node indices in range")
        edge = (min(u, v), max(u, v))
        if edge in seen:
            raise ValueError("duplicate undirected edge")
        seen.add(edge)
        neighbor_sets[u].add(v)
        neighbor_sets[v].add(u)
    if any(not neighbors for neighbors in neighbor_sets):
        raise ValueError("isolated vertices are outside this degree-normalized model")

    valid_directed = {(i, j) for i, neighbors in enumerate(neighbor_sets) for j in neighbors}
    lag = dict(delays or {})
    if any(k not in valid_directed or type(v) is not int or v < 0 for k, v in lag.items()):
        raise ValueError("each delay must be a nonnegative integer keyed by directed adjacency (receiver, sender)")
    adjacency = tuple(tuple(sorted(neighbors)) for neighbors in neighbor_sets)
    traces: list[tuple[float, ...]] = [initial]

    def derivative(stage: tuple[float, ...], index: int, stage_fraction: float) -> tuple[float, ...]:
        def history(j: int, lag_steps: int) -> float:
            if lag_steps == 0:
                return stage[j]
            left = index - lag_steps
            right = left + 1
            a = initial[j] if left < 0 else traces[left][j]
            b = initial[j] if right < 0 else traces[right][j]
            return (1.0 - stage_fraction) * a + stage_fraction * b

        return tuple(
            omega[i]
            + coupling / len(neighbors) * sum(math.sin(history(j, lag.get((i, j), 0)) - stage[i]) for j in neighbors)
            for i, neighbors in enumerate(adjacency)
        )

    def add(x: tuple[float, ...], k: tuple[float, ...], scale: float) -> tuple[float, ...]:
        return tuple(a + scale * b for a, b in zip(x, k))

    for index in range(steps):
        current = traces[-1]
        k1 = derivative(current, index, 0.0)
        k2 = derivative(add(current, k1, dt / 2.0), index, 0.5)
        k3 = derivative(add(current, k2, dt / 2.0), index, 0.5)
        k4 = derivative(add(current, k3, dt), index, 1.0)
        next_state = tuple(current[i] + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0 for i in range(n_nodes))
        if any(not math.isfinite(value) for value in next_state):
            raise ArithmeticError("non-finite numerical state")
        traces.append(next_state)
    return tuple(traces)


def circular_order_parameter(phases: Sequence[float]) -> float:
    """Kuramoto phase-coherence magnitude R in [0, 1], not a task utility score."""
    if not phases:
        raise ValueError("at least one phase required")
    if any(not math.isfinite(x) for x in phases):
        raise ValueError("phases must be finite")
    c = sum(math.cos(x) for x in phases) / len(phases)
    s = sum(math.sin(x) for x in phases) / len(phases)
    return math.hypot(c, s)
