from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_COLUMNS = {
    "seed",
    "topology",
    "failure_count",
    "failure_nodes",
    "nodes_remaining",
    "largest_component_fraction",
    "connected",
    "connectivity_threshold_met",
    "component_count",
}


def validate_csv(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("output CSV contains no observations")
    for column in REQUIRED_COLUMNS:
        values = [row[column] for row in rows]
        if not all(value not in ("", "NA", "NaN", "nan", "None") for value in values):
            raise ValueError(f"column contains missing values: {column}")
    if len({row["largest_component_fraction"] for row in rows}) == 1:
        raise ValueError("largest_component_fraction is constant in the dry-run output")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    validate_csv(args.path)
    print("output schema: PASS")
