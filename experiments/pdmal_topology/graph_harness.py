from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import networkx as nx


@dataclass(frozen=True)
class TopologySpec:
    name: str
    generator: Callable[[int], nx.Graph]


def build_topologies(seed: int) -> dict[str, nx.Graph]:
    """Build the preregistered topology family deterministically for a seed."""
    return {
        "ring": nx.cycle_graph(20),
        "pdmal": nx.dodecahedral_graph(),
        "random_regular": nx.random_regular_graph(3, 20, seed=seed),
        "small_world": nx.watts_strogatz_graph(20, 4, 0.3, seed=seed),
        "complete": nx.complete_graph(20),
    }


def random_node_failures(seed: int, count: int, n: int = 20) -> tuple[int, ...]:
    """Select a reproducible uniform node-failure set without replacement."""
    if not 0 <= count <= n:
        raise ValueError("failure count must be between 0 and n")
    import random

    rng = random.Random(seed)
    return tuple(sorted(rng.sample(range(n), count)))


def apply_node_failures(graph: nx.Graph, failures: tuple[int, ...]) -> nx.Graph:
    """Return a copy after removing the specified node IDs."""
    result = graph.copy()
    result.remove_nodes_from(failures)
    return result


def structural_metrics(
    graph: nx.Graph, *, original_nodes: int = 20
) -> dict[str, float | int | bool]:
    """Compute preregistered structural outcomes for a post-failure graph.

    Largest-component fraction uses the original population N, and the
    connectivity threshold is the preregistered >= N/2 threshold.
    """
    if original_nodes <= 0:
        raise ValueError("original_nodes must be positive")
    remaining = graph.number_of_nodes()
    largest = max((len(c) for c in nx.connected_components(graph)), default=0)
    return {
        "nodes_remaining": remaining,
        "largest_component_size": largest,
        "largest_component_fraction": largest / original_nodes,
        "connected": nx.is_connected(graph) if remaining else False,
        "connectivity_threshold_met": largest >= original_nodes / 2,
        "component_count": nx.number_connected_components(graph) if remaining else 0,
    }
