from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from graph_harness import apply_node_failures, build_topologies, random_node_failures, structural_metrics


def single_case(seed: int, topology: str, failures: int) -> dict:
    graph = build_topologies(seed)[topology]
    selected = random_node_failures(seed, failures)
    post = apply_node_failures(graph, selected)
    return {
        "seed": seed,
        "topology": topology,
        "failure_count": failures,
        "failure_nodes": list(selected),
        **structural_metrics(post),
    }


def canonical_bytes(case: dict) -> bytes:
    return (json.dumps(case, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest_case(case: dict) -> str:
    return hashlib.sha256(canonical_bytes(case)).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--topology", required=True, choices=["ring", "pdmal", "random_regular", "small_world", "complete"])
    parser.add_argument("--failures", type=int, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    case = single_case(args.seed, args.topology, args.failures)
    encoded = canonical_bytes(case)
    digest = hashlib.sha256(encoded).hexdigest()
    if args.output:
        args.output.write_bytes(encoded)
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
