"""Deterministic structural controls for proposed PDMAL-GR comparisons.

NON-ADMITTED: fixture geometry only, not an experimental runner or scientific
observations. Cubic random graphs use uniform stub matchings, conditioned
on obtaining a connected simple graph; seed PRNG is NOT cryptographic.
"""

from __future__ import annotations

import hashlib
import random
from collections import deque
from collections.abc import Sequence

from tools.pdmal.lattice_harness import DODECAHEDRAL_EDGES

N_NODES = 20
TARGET_DEGREE = 3


def validate_cubic_graph(edges: Sequence[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    """Normalize and validate a connected, labeled 20-node, 3-regular simple graph."""
    adjacency: list[set[int]] = [set() for _ in range(N_NODES)]
    normalized: set[tuple[int, int]] = set()
    for u, v in edges:
        if type(u) is not int or type(v) is not int or u == v or not (0 <= u < N_NODES and 0 <= v < N_NODES):
            raise ValueError("edges must connect two distinct integer vertices in range(20)")
        edge = (min(u, v), max(u, v))
        if edge in normalized:
            raise ValueError("duplicate undirected edge")
        normalized.add(edge)
        adjacency[u].add(v)
        adjacency[v].add(u)
    if len(normalized) != 30 or any(len(neighbors) != TARGET_DEGREE for neighbors in adjacency):
        raise ValueError("fixture must be a 20-node, 30-edge, degree-3 simple graph")
    visited = {0}
    frontier = deque([0])
    while frontier:
        for neighbor in adjacency[frontier.popleft()]:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
    if len(visited) != N_NODES:
        raise ValueError("graph must be connected")
    return tuple(sorted(normalized))


def circular_ladder_edges() -> tuple[tuple[int, int], ...]:
    """Two ten-vertex rings and ten rungs; 20 vertices, 30 edges, degree 3."""
    edges: list[tuple[int, int]] = []
    for i in range(10):
        edges.append((i, (i + 1) % 10))
        edges.append((10 + i, 10 + (i + 1) % 10))
        edges.append((i, 10 + i))
    return validate_cubic_graph(edges)


def random_connected_cubic_edges(*, seed: int, max_attempts: int = 10000) -> tuple[tuple[int, int], ...]:
    """Uniform labeled connected simple cubic graph by rejection of stub pairings.

    Every simple labeled cubic graph corresponds to (3!)**20 equally likely
    half-edge matchings. Conditioning on simple + connected yields uniform
    draws in that finite set. The random seed makes the result reproducible;
    it does not confer scientific independence, randomness certification,
    or permission to collect comparative experimental results.
    """
    if type(seed) is not int or type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("seed must be an integer and max_attempts a positive integer")
    rng = random.Random(seed)
    stubs = [node for node in range(N_NODES) for _ in range(TARGET_DEGREE)]
    for _ in range(max_attempts):
        rng.shuffle(stubs)
        paired = []
        seen: set[tuple[int, int]] = set()
        valid = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            edge = (min(u, v), max(u, v))
            if u == v or edge in seen:
                valid = False
                break
            seen.add(edge)
            paired.append(edge)
        if valid:
            try:
                return validate_cubic_graph(paired)
            except ValueError:
                # Rejection of disconnected cubic graphs preserves conditional uniformity.
                continue
    raise RuntimeError("exhausted requested stub-matching attempts without valid graph")


def fixture_fingerprint(edges: Sequence[tuple[int, int]]) -> str:
    """SHA-256 of canonical labeled graph identity, not an isomorphism signature."""
    canonical = validate_cubic_graph(edges)
    encoded = "pdmal-gr-graph-v1|20|" + ";".join(f"{u}-{v}" for u, v in canonical)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def derive_seed(master_seed: int, domain: str, index: int) -> int:
    """Domain-separated deterministic seed schedule; NOT cryptographic sampling."""
    if type(master_seed) is not int or type(index) is not int or index < 0:
        raise ValueError("master_seed and nonnegative index must be integers")
    if domain not in ("graph", "perturbation"):
        raise ValueError("domain must be 'graph' or 'perturbation'")
    payload = f"pdmal-gr-seed-v1|{master_seed}|{domain}|{index}".encode("ascii")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def named_comparator_edges(seed: int) -> dict[str, tuple[tuple[int, int], ...]]:
    """Topology-only fixtures. This function runs no oscillator or experiment."""
    return {
        "dodecahedral_proxy": validate_cubic_graph(DODECAHEDRAL_EDGES),
        "circular_ladder": circular_ladder_edges(),
        "random_connected_cubic": random_connected_cubic_edges(seed=seed),
    }
