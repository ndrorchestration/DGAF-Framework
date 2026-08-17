from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


def sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))


def load_masked(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def evaluate_pilot(rows: list[dict]) -> dict:
    by_topology = defaultdict(list)
    for row in rows:
        by_topology[row["topology"]].append(float(row["largest_component_fraction"]))

    sd_values = {label: sample_sd(values) for label, values in by_topology.items()}
    return {
        "topology_labels": sorted(by_topology),
        "sd_by_masked_topology": sd_values,
        "sd_pass_count": sum(sd <= 0.15 for sd in sd_values.values()),
        "sd_criterion_pass": sum(sd <= 0.15 for sd in sd_values.values()) >= 4,
        "results_are_masked": all(str(label).startswith("Topology_") for label in by_topology),
    }


def assert_pilot_success(summary: dict) -> None:
    if not summary["results_are_masked"]:
        raise AssertionError("pilot precision gate received unmasked topology labels")
    if not summary["sd_criterion_pass"]:
        raise AssertionError("pilot variance criterion failed; increase pilot seeds or amend protocol")
