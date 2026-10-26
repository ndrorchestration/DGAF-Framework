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
    if domain not in ("graph", "perturbation", "label", "placement"):
        raise ValueError("domain must be 'graph', 'perturbation', 'label' or 'placement'")
    payload = f"pdmal-gr-seed-v1|{master_seed}|{domain}|{index}".encode("ascii")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def label_permutation(master_seed: int, arm: str, replicate: int) -> tuple[int, ...]:
    """Generate a reproducible old-to-new vertex map per arm and replicate.

    Separate deterministic PRNG seed namespaces generate distinct indexing
    streams; collisions are still possible and no statistical independence
    is proved. Relabeling physical nodes and all their attributes together
    does NOT randomize their structural positions or disturbance exposure.
    No oscillator simulation, perturbation or experimental result is created.
    """
    valid_arms = ("dodecahedral_proxy", "circular_ladder", "random_connected_cubic")
    if type(master_seed) is not int or type(replicate) is not int or replicate < 0:
        raise ValueError("master_seed and nonnegative replicate must be integers")
    if arm not in valid_arms:
        raise ValueError("arm must be a known structural comparator")
    arm_id = valid_arms.index(arm)
    rng = random.Random(derive_seed(master_seed, "label", replicate * len(valid_arms) + arm_id))
    mapping = list(range(N_NODES))
    rng.shuffle(mapping)
    return tuple(mapping)



def prospective_perturbation_vertex(master_seed: int, arm: str, replicate: int) -> int:
    """Return a distinct, prospectively sampled *source-label* disturbance site.

    This selection uses a separate 'placement' PRNG seed stream, NOT the
    vertex label-permutation stream. The site is uniform over twenty labeled
    vertices, but structural exposures across graph families are not
    guaranteed equivalent. Calling this helper constructs only a fixture:
    it does not run, authorize or record a dynamical experiment.
    """
    valid_arms = ("dodecahedral_proxy", "circular_ladder", "random_connected_cubic")
    if type(master_seed) is not int or type(replicate) is not int or replicate < 0:
        raise ValueError("master_seed and nonnegative replicate must be integers")
    if arm not in valid_arms:
        raise ValueError("arm must be a known structural comparator")
    stream_index = replicate * len(valid_arms) + valid_arms.index(arm)
    return random.Random(derive_seed(master_seed, "placement", stream_index)).randrange(N_NODES)


def relabel_cubic_graph(edges: Sequence[tuple[int, int]], old_to_new: Sequence[int]) -> tuple[tuple[int, int], ...]:
    """Apply a bijective old-to-new map and revalidate the labeled graph.

    The output can be mapped back exactly; this never changes graph
    isomorphism class, structural costs, or the original edge fixture.
    """
    canonical = validate_cubic_graph(edges)
    if len(old_to_new) != N_NODES or any(type(v) is not int for v in old_to_new):
        raise ValueError("old_to_new must contain twenty integer vertex identifiers")
    if set(old_to_new) != set(range(N_NODES)):
        raise ValueError("old_to_new must be a permutation of range(20)")
    return validate_cubic_graph(tuple((old_to_new[u], old_to_new[v]) for u, v in canonical))


def relabel_vertex_values(values: Sequence[float], old_to_new: Sequence[int]) -> tuple[float, ...]:
    """Keep node-attached attributes consistent with an old-to-new vertex map."""
    if len(values) != N_NODES or len(old_to_new) != N_NODES:
        raise ValueError("expected twenty vertex values and twenty mapped identifiers")
    if any(type(v) is not int for v in old_to_new) or set(old_to_new) != set(range(N_NODES)):
        raise ValueError("old_to_new must be a permutation of range(20)")
    remapped = [0.0] * N_NODES
    for old, new in enumerate(old_to_new):
        remapped[new] = float(values[old])
    return tuple(remapped)


def relabel_directed_delays(lags: dict[tuple[int, int], int], old_to_new: Sequence[int]) -> dict[tuple[int, int], int]:
    """Carry directed receiver/sender delay orientation through relabeling."""
    if len(old_to_new) != N_NODES or any(type(v) is not int for v in old_to_new):
        raise ValueError("old_to_new must contain twenty integer vertex identifiers")
    if set(old_to_new) != set(range(N_NODES)):
        raise ValueError("old_to_new must be a permutation of range(20)")
    remapped: dict[tuple[int, int], int] = {}
    for (receiver, sender), delay in lags.items():
        if (
            type(receiver) is not int
            or type(sender) is not int
            or not (0 <= receiver < N_NODES and 0 <= sender < N_NODES)
        ):
            raise ValueError("delay key must use two valid directed vertex indices")
        if type(delay) is not int or delay < 0:
            raise ValueError("delay values must be nonnegative integer step counts")
        remapped[(old_to_new[receiver], old_to_new[sender])] = delay
    return remapped


def named_comparator_edges(seed: int) -> dict[str, tuple[tuple[int, int], ...]]:
    """Topology-only fixtures. This function runs no oscillator or experiment."""
    return {
        "dodecahedral_proxy": validate_cubic_graph(DODECAHEDRAL_EDGES),
        "circular_ladder": circular_ladder_edges(),
        "random_connected_cubic": random_connected_cubic_edges(seed=seed),
    }
