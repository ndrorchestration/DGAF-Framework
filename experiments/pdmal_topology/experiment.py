from __future__ import annotations

import json
import os
from pathlib import Path

from artifacts import blind_rows, environment_commit_short, write_csv
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
                metrics = structural_metrics(post, original_nodes=20)
                rows.append({
                    "seed": seed,
                    "topology": topology,
                    "failure_count": failure_count,
                    "failure_nodes": json.dumps(list(failures), separators=(",", ":")),
                    **metrics,
                })
    return rows


def persist_masked_pilot(seed_count: int = 50, output_dir: str | Path = "artifacts/pilot") -> tuple[Path, str]:
    """Persist a topology-masked CSV and SHA-256 digest before any analysis."""
    secret = os.environ.get("PDMAL_BLINDING_KEY")
    if not secret:
        raise RuntimeError("PDMAL_BLINDING_KEY must be supplied externally for pilot execution")
    rows = blind_rows(run_structural_pilot(seed_count), secret)
    return write_csv(rows, environment_commit_short(), output_dir)


def write_raw_jsonl(rows: list[dict], path: str | Path) -> None:
    """Legacy/raw debugging output; not the confirmatory artifact format."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


if __name__ == "__main__":
    destination, digest = persist_masked_pilot(50)
    print(f"wrote masked pilot artifact: {destination}")
    print(f"sha256: {digest}")
