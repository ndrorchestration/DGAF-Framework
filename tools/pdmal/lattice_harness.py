"""Repository-owned derivative of the supplied PDMAL lattice harness.

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

This is structural/audit semantics only. It does not establish usefulness of
weighted Forman-Ricci, anomaly-detection efficacy, PDMAL freeze readiness,
pilot authorization, or empirical evidence.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Callable

import networkx as nx
import numpy as np

SOURCE_ARTIFACT_SHA256 = (
    "f8382b68bbf155fe574bd76118db6fc2142c558c21d0f109e3b92103a1611216"
)
NO_DISCRIMINATING_SIGNAL = "NO_DISCRIMINATING_SIGNAL"
THRESHOLD_APPLIED = "THRESHOLD_APPLIED"

PHI = (1 + 5**0.5) / 2


def plastic_constant() -> float:
    """Return the real root of x^3 = x + 1."""
    roots = np.roots([1, 0, -1, -1])
    real = [root.real for root in roots if abs(root.imag) < 1e-9]
    if len(real) != 1:
        raise RuntimeError("plastic constant root resolution was not unique")
    return float(real[0])


RHO_P = plastic_constant()


@dataclass
class ContractionMonitor:
    """Finite-difference contraction monitor; an empirical proxy, not proof."""

    F: Callable
    metric: Callable = lambda a, b: np.linalg.norm(a - b)
    eta: float = 1e-8
    history: list[float] = field(default_factory=list)

    def step_pair(self, x, x_perturbed):
        d_in = self.metric(x, x_perturbed) + self.eta
        d_out = self.metric(self.F(x), self.F(x_perturbed)) + self.eta
        estimate = float(d_out / d_in)
        self.history.append(estimate)
        return estimate

    def sample(self, x0, n_samples=1000, perturb_scale=1e-3, rng=None):
        rng = rng or np.random.default_rng()
        for _ in range(n_samples):
            x = x0 + rng.normal(scale=1.0, size=x0.shape)
            dx = rng.normal(scale=perturb_scale, size=x0.shape)
            self.step_pair(x, x + dx)
        return np.asarray(self.history)

    def report(self):
        history = np.asarray(self.history)
        if history.size == 0:
            raise ValueError("no contraction samples recorded")
        non_contracting_rate = float((history >= 1.0).mean())
        return {
            "n": int(history.size),
            "mean_L": float(history.mean()),
            "p95_L": float(np.percentile(history, 95)),
            "P(L>=1)": non_contracting_rate,
            "verdict": (
                "CONTRACTING (proxy only, not proven)"
                if non_contracting_rate < 0.01
                else "DIVERGENT-RISK: >1% of samples show L>=1"
            ),
        }


def admission_distance(E: np.ndarray) -> float:
    """Return normalized admission distance for a triad evidence matrix."""
    col_mean = E.mean(axis=1, keepdims=True)
    numerator = np.linalg.norm(E - col_mean, ord="fro")
    denominator = np.linalg.norm(col_mean) + 1e-12
    return float(numerator / denominator)


def calibrate_tau(samples: list[float], k_sigma: float = 3.0) -> float:
    """Calibrate a threshold from observed healthy-run distances."""
    arr = np.asarray(samples, dtype=float)
    if arr.size == 0:
        raise ValueError("at least one calibration sample is required")
    return float(arr.mean() + k_sigma * arr.std())


def build_pdmal_lattice() -> nx.Graph:
    """Return the 20-vertex dodecahedral base graph."""
    return nx.dodecahedral_graph()


def forman_ricci_unweighted(G: nx.Graph) -> dict[tuple[int, int], float]:
    """Compute unweighted Forman-Ricci curvature for each simple-graph edge."""
    return {
        (u, v): float(4 - G.degree(u) - G.degree(v))
        for u, v in G.edges()
    }


def exact_cheeger_constant(G: nx.Graph) -> tuple[float, set]:
    """Compute exact h(G) by brute force; intended only for small graphs."""
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    edges = list(G.edges())
    best_h = None
    best_set = None
    for k in range(1, n // 2 + 1):
        for subset in itertools.combinations(nodes, k):
            subset_set = set(subset)
            boundary = sum(
                1 for u, v in edges if (u in subset_set) != (v in subset_set)
            )
            h_value = boundary / k
            if best_h is None or h_value < best_h:
                best_h = h_value
                best_set = subset_set
    if best_h is None or best_set is None:
        raise ValueError("Cheeger constant requires a non-empty graph")
    return float(best_h), best_set


def lattice_audit(G: nx.Graph, ricci_floor: float = -2.0) -> dict:
    """Audit unweighted curvature without mislabeling a constant metric.

    If all edge curvatures are identical, no edge can be distinguished from
    any other by this metric. In that case threshold-based anomaly flagging is
    disabled and the explicit state ``NO_DISCRIMINATING_SIGNAL`` is returned.

    For a graph whose unweighted curvature varies across edges, the supplied
    threshold is applied and the result is labeled ``THRESHOLD_APPLIED``.
    This does not calibrate or validate the threshold as an anomaly detector.
    """
    ricci = forman_ricci_unweighted(G)
    if not ricci:
        raise ValueError("lattice audit requires at least one edge")

    values = np.asarray(list(ricci.values()), dtype=float)
    variance = float(values.var())
    constant = bool(np.all(values == values[0]))

    if constant:
        flagged_edges: list[tuple[int, int]] = []
        state = NO_DISCRIMINATING_SIGNAL
        threshold_available = False
    else:
        flagged_edges = [edge for edge, value in ricci.items() if value <= ricci_floor]
        state = THRESHOLD_APPLIED
        threshold_available = True

    return {
        "n_edges": len(ricci),
        "ricci_min": float(values.min()),
        "ricci_mean": float(values.mean()),
        "ricci_variance": variance,
        "signal_state": state,
        "threshold_flagging_available": threshold_available,
        "ricci_floor": float(ricci_floor),
        "flagged_edges": flagged_edges,
    }
