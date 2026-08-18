"""Deterministic topology provenance helpers for the PDMAL pre-freeze harness."""
from __future__ import annotations

import hashlib

import networkx as nx


def graph_fingerprint(graph: nx.Graph) -> str:
    """Return a deterministic SHA-256 fingerprint of an undirected graph.

    Nodes and endpoints are normalized before hashing so the fingerprint is
    stable for the same labeled graph regardless of NetworkX edge iteration
    order or edge orientation.
    """
    normalized_edges = sorted(
        (min(u, v), max(u, v)) for u, v in graph.edges()
    )
    edge_text = "|".join(f"{u},{v}" for u, v in normalized_edges)
    return hashlib.sha256(edge_text.encode("utf-8")).hexdigest()
