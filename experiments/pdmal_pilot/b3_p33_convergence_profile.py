"""B3 non-empirical persistent P-33 graph-convergence profile.

Uses the live PDMALConvergenceMonitor with one persistent monitor per graph
sequence. It does not map monitor status to consensus updates and has no
empirical efficacy endpoint.
"""
from __future__ import annotations

import math
from typing import Mapping, Sequence

from components.ensemble_v17 import PDMALConvergenceMonitor, PDMALGraph

PROFILE_ID = "DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1"
EDGE_KEYS = (("a", "b"), ("a", "c"))


def _validate_snapshot(snapshot: Mapping[tuple[str, str], float]) -> None:
    if set(snapshot) != set(EDGE_KEYS):
        raise ValueError("graph snapshot must contain the exact registered edge set")
    values = []
    for edge in EDGE_KEYS:
        value = snapshot[edge]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("edge weights must be numeric")
        value = float(value)
        if not math.isfinite(value) or value < 0.0 or value > 1.0:
            raise ValueError("edge weights must be finite and within [0,1]")
        values.append(value)
    if not math.isclose(sum(values), 1.0, abs_tol=1e-12):
        raise ValueError("registered source row must remain normalized")


class PersistentP33Sequence:
    def __init__(self, sequence_id: str, first_snapshot: Mapping[tuple[str, str], float]):
        if not sequence_id:
            raise ValueError("sequence_id is required")
        _validate_snapshot(first_snapshot)
        self.sequence_id = sequence_id
        self.graph = PDMALGraph()
        self.graph.add_node("a")
        self.graph.add_node("b")
        self.graph.add_node("c")
        for (src, dst), weight in first_snapshot.items():
            self.graph.add_edge(src, dst, float(weight))
        self.monitor = PDMALConvergenceMonitor(self.graph)
        self.turns = 0
        self.events = []

    def apply(self, turn_id: str, snapshot: Mapping[tuple[str, str], float]) -> dict:
        if not turn_id:
            raise ValueError("turn_id is required")
        _validate_snapshot(snapshot)
        for (src, dst), weight in snapshot.items():
            self.graph.edges[src][dst].weight = float(weight)
        evt = self.monitor.check(turn_id=turn_id)
        self.turns += 1
        record = {
            "sequence_id": self.sequence_id,
            "turn_id": turn_id,
            "turn_number": evt.turn_number,
            "status": evt.status,
            "severity": evt.severity,
            "routing_action": evt.routing_action,
            "graph_norm_delta": evt.graph_norm_delta,
            "max_edge_delta": evt.max_edge_delta,
            "consecutive_divergent": evt.consecutive_divergent,
        }
        self.events.append(record)
        return record

    def summary(self) -> dict:
        return {
            "profile_id": PROFILE_ID,
            "sequence_id": self.sequence_id,
            "turns": self.turns,
            "monitor_summary": self.monitor.summary(),
            "events": list(self.events),
            "scientific_n_increment": 0,
            "empirical_execution_authorized": False,
            "consensus_alpha_mapping": "PROHIBITED",
        }


def run_registered_sequence() -> dict:
    snapshots: Sequence[Mapping[tuple[str, str], float]] = (
        {("a", "b"): 0.50, ("a", "c"): 0.50},
        {("a", "b"): 0.60, ("a", "c"): 0.40},
        {("a", "b"): 0.70, ("a", "c"): 0.30},
        {("a", "b"): 0.80, ("a", "c"): 0.20},
        {("a", "b"): 0.80, ("a", "c"): 0.20},
        {("a", "b"): 0.80, ("a", "c"): 0.20},
        {("a", "b"): 0.80, ("a", "c"): 0.20},
    )
    seq = PersistentP33Sequence("B3-REGISTERED-SEQUENCE-001", snapshots[0])
    for idx, snapshot in enumerate(snapshots, start=1):
        seq.apply(f"turn-{idx}", snapshot)
    return seq.summary()
