"""Pre-freeze PDMAL harness contract primitives.

This module validates the implementation controls without executing empirical
workloads. It deliberately keeps experimental conditions separate from the
topology-comparison set.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any

import networkx as nx
import numpy as np
from numpy.random import Generator, PCG64, SeedSequence

from topology_utils import graph_fingerprint

EXPERIMENT_CONDITIONS = (
    "null",
    "simple",
    "static",
    "dgaf",
    "dgaf_pdmal",
)

TOPOLOGY_SPECS = {
    "ring": {"nodes": 20, "edges": 20, "regular_degree": 2, "connected": True},
    "pdmal": {"nodes": 20, "edges": 30, "regular_degree": 3, "connected": True},
    "random_regular": {"nodes": 20, "edges": 30, "regular_degree": 3, "connected": True},
    "small_world": {"nodes": 20, "edges": 40, "regular_degree": None, "connected": True},
    "complete": {"nodes": 20, "edges": 190, "regular_degree": 19, "connected": True},
}

# The first four child streams are already part of the verified contract.
# task_initialization is appended so their identities and spawn keys remain stable.
STREAM_IDS = (
    "trial_order",
    "failure_injection",
    "topology_construction",
    "analysis_resampling",
    "task_initialization",
)


def make_streams(root_seed: int) -> dict[str, Generator]:
    """Create deterministic child streams using NumPy SeedSequence.spawn."""
    root = SeedSequence(root_seed)
    children = root.spawn(len(STREAM_IDS))
    return {
        stream_id: Generator(PCG64(child))
        for stream_id, child in zip(STREAM_IDS, children, strict=True)
    }


def stream_fingerprint(root_seed: int) -> dict[str, Any]:
    """Return auditable metadata for the deterministic stream tree."""
    root = SeedSequence(root_seed)
    children = root.spawn(len(STREAM_IDS))
    return {
        "root_entropy": int(root.entropy),
        "pool_size": int(root.pool_size),
        "stream_ids": list(STREAM_IDS),
        "spawn_keys": {
            stream_id: list(child.spawn_key)
            for stream_id, child in zip(STREAM_IDS, children, strict=True)
        },
    }


def generate_topology(name: str, rng: Generator) -> nx.Graph:
    if name == "ring":
        return nx.cycle_graph(20)
    if name == "pdmal":
        return nx.dodecahedral_graph()
    if name == "random_regular":
        return nx.random_regular_graph(3, 20, seed=rng)
    if name == "small_world":
        return nx.watts_strogatz_graph(20, 4, 0.3, seed=rng)
    if name == "complete":
        return nx.complete_graph(20)
    raise ValueError(f"Unknown topology: {name}")


def validate_topology(graph: nx.Graph, name: str) -> None:
    """Fail closed if a generated graph violates its frozen invariants."""
    spec = TOPOLOGY_SPECS[name]
    if graph.number_of_nodes() != spec["nodes"]:
        raise AssertionError(f"{name}: node count mismatch")
    if graph.number_of_edges() != spec["edges"]:
        raise AssertionError(f"{name}: edge count mismatch")
    if spec["connected"] and not nx.is_connected(graph):
        raise AssertionError(f"{name}: graph is disconnected")
    degree_set = {degree for _, degree in graph.degree()}
    if spec["regular_degree"] is not None and degree_set != {spec["regular_degree"]}:
        raise AssertionError(f"{name}: degree regularity mismatch")
    if name == "pdmal" and nx.node_connectivity(graph) < 3:
        raise AssertionError("pdmal: node connectivity < 3")


def blind_condition(condition: str, key: bytes) -> str:
    """Return a deterministic blinded identifier; never expose the key."""
    digest = hmac.new(key, condition.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"blind_{digest[:16]}"


def validate_artifact_contract(artifact: dict[str, Any]) -> None:
    """Validate required fields without requiring an external schema package."""
    required = {
        "experiment_id",
        "protocol_commit",
        "runner_commit",
        "seed_id",
        "root_seed",
        "results",
        "runtime_seconds",
        "environment_fingerprint",
        "protocol_status",
        "empirical_data_collection",
    }
    missing = required - set(artifact)
    if missing:
        raise AssertionError(f"artifact missing fields: {sorted(missing)}")
    if artifact["protocol_status"] != "PRE-FREEZE":
        raise AssertionError("pre-freeze validation artifact must declare PRE-FREEZE")
    if artifact["empirical_data_collection"] is not False:
        raise AssertionError("harness validation must not authorize empirical collection")
    if not isinstance(artifact["results"], list):
        raise AssertionError("results must be a list")


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


@dataclass(frozen=True)
class HarnessResult:
    condition: str
    blinded_condition_id: str
    topology: str
    topology_valid: bool
    topology_fingerprint: str
    status: str


def deterministic_contract_run(root_seed: int, key: bytes) -> list[HarnessResult]:
    """Validate all topology contracts once; this is not an efficacy run."""
    streams = make_streams(root_seed)
    order = streams["trial_order"].permutation(list(EXPERIMENT_CONDITIONS)).tolist()
    outputs: list[HarnessResult] = []
    for topology in TOPOLOGY_SPECS:
        graph = generate_topology(topology, streams["topology_construction"])
        validate_topology(graph, topology)
        outputs.append(
            HarnessResult(
                condition=order[0],
                blinded_condition_id=blind_condition(order[0], key),
                topology=topology,
                topology_valid=True,
                topology_fingerprint=graph_fingerprint(graph),
                status="CONTRACT_VALIDATED_ONLY",
            )
        )
    return outputs
