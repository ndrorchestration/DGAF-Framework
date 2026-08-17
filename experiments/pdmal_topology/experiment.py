from __future__ import annotations

import json
from pathlib import Path

from graph_harness import apply_node_failures, build_topologies, random_node_failures, structural_metrics

FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)


def run_structural_pilot(seed_count: int = 50) -> list[dict]:
    """Generate raw structural observations only; no inferential analysis occurs here."""
    rows: list[dict] = []
    for seed in range(seed_count):
        graphs = build_topologies(seed)
        for failure_count in FAILURE_COUNTS:
            failures = random_node_failures(seed, failure_count)
            for topology, graph in graphs.items():
                post = apply_node_failures(graph, failures)
                metrics = structural_metrics(post)
                rows.append({
                    "seed": seed,
                    "topology": topology,
                    "failure_count": failure_count,
                    "failure_nodes": list(failures),
                    **metrics,
                })
    return rows


def write_raw_jsonl(rows: list[dict], path: str | Path) -> None:
    """Persist immutable-style raw observations as JSON Lines."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


if __name__ == "__main__":
    rows = run_structural_pilot(50)
    write_raw_jsonl(rows, "artifacts/pilot/raw_structural.jsonl")
    print(f"wrote {len(rows)} raw observations")
