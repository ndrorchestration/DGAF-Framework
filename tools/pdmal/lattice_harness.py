"""Repository-owned derivative of the supplied PDMAL lattice audit helper.

Provenance
----------
This module is derived from the external ``lattice_harness.py`` artifact
identified in repository evidence as SHA-256
``f8382b68bbf155fe574bd76118db6fc2142c558c21d0f109e3b92103a1611216``.
The external artifact itself is not rewritten or reidentified by this file.

Issue #117 correction
---------------------
On the unweighted 3-regular dodecahedral graph, Forman-Ricci curvature is
exactly -2 on every edge. A threshold comparison therefore has zero
within-graph discriminating signal and must not report all 30 edges as
"anomalies". This derivative reports ``NO_DISCRIMINATING_SIGNAL`` and
suppresses anomaly flags whenever the unweighted curvature is constant.

This module intentionally uses only the Python standard library so that the
semantic regression can run in the repository's base quality environment.
It does not establish usefulness of weighted Forman-Ricci, anomaly-detection
efficacy, PDMAL freeze readiness, pilot authorization, or empirical evidence.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import fmean, pvariance
from typing import Iterable

SOURCE_ARTIFACT_SHA256 = (
    "f8382b68bbf155fe574bd76118db6fc2142c558c21d0f109e3b92103a1611216"
)
NO_DISCRIMINATING_SIGNAL = "NO_DISCRIMINATING_SIGNAL"
THRESHOLD_APPLIED = "THRESHOLD_APPLIED"

# Exact edge set for NetworkX's canonical 20-node dodecahedral graph.
DODECAHEDRAL_EDGES = (
    (0, 1), (0, 19), (0, 10), (1, 2), (1, 8), (2, 3), (2, 6),
    (3, 4), (3, 19), (4, 5), (4, 17), (5, 6), (5, 15), (6, 7),
    (7, 8), (7, 14), (8, 9), (9, 10), (9, 13), (10, 11),
    (11, 12), (11, 18), (12, 13), (12, 16), (13, 14), (14, 15),
    (15, 16), (16, 17), (17, 18), (18, 19),
)


class SimpleGraph:
    """Minimal undirected graph interface required by the audit helper."""

    def __init__(self, edges: Iterable[tuple[int, int]]):
        self._edges = tuple(edges)
        adjacency: dict[int, set[int]] = defaultdict(set)
        for u, v in self._edges:
            if u == v:
                raise ValueError("self-loops are not supported")
            adjacency[u].add(v)
            adjacency[v].add(u)
        self._adjacency = dict(adjacency)

    def edges(self) -> tuple[tuple[int, int], ...]:
        return self._edges

    def degree(self, node: int) -> int:
        return len(self._adjacency[node])

    def number_of_edges(self) -> int:
        return len(self._edges)

    def number_of_nodes(self) -> int:
        return len(self._adjacency)


def build_pdmal_lattice() -> SimpleGraph:
    """Return the canonical 20-node, 30-edge dodecahedral base graph."""
    return SimpleGraph(DODECAHEDRAL_EDGES)


def forman_ricci_unweighted(graph) -> dict[tuple[int, int], float]:
    """Compute unweighted Forman-Ricci curvature for each simple-graph edge."""
    return {
        (u, v): float(4 - graph.degree(u) - graph.degree(v))
        for u, v in graph.edges()
    }


def lattice_audit(graph, ricci_floor: float = -2.0) -> dict:
    """Audit unweighted curvature without mislabeling a constant metric.

    If all edge curvatures are identical, no edge can be distinguished from
    any other by this metric. Threshold-based anomaly flagging is therefore
    disabled and ``NO_DISCRIMINATING_SIGNAL`` is returned.

    If curvature varies across edges, the supplied threshold is applied and
    the result is labeled ``THRESHOLD_APPLIED``. That label means only that a
    threshold comparison was mechanically possible; it does not validate the
    threshold as an anomaly detector.
    """
    ricci = forman_ricci_unweighted(graph)
    if not ricci:
        raise ValueError("lattice audit requires at least one edge")

    values = list(ricci.values())
    variance = float(pvariance(values))
    constant = all(value == values[0] for value in values)

    if constant:
        flagged_edges: list[tuple[int, int]] = []
        state = NO_DISCRIMINATING_SIGNAL
        threshold_available = False
    else:
        flagged_edges = [
            edge for edge, value in ricci.items() if value <= ricci_floor
        ]
        state = THRESHOLD_APPLIED
        threshold_available = True

    return {
        "n_edges": len(ricci),
        "ricci_min": float(min(values)),
        "ricci_mean": float(fmean(values)),
        "ricci_variance": variance,
        "signal_state": state,
        "threshold_flagging_available": threshold_available,
        "ricci_floor": float(ricci_floor),
        "flagged_edges": flagged_edges,
    }
