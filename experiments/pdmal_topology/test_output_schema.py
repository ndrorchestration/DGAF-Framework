import csv

import pytest

from output_schema import validate_csv


def test_required_output_schema_passes(tmp_path):
    path = tmp_path / "dryrun.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "seed", "topology", "failure_count", "failure_nodes", "nodes_remaining",
            "largest_component_size", "largest_component_fraction", "connected",
            "connectivity_threshold_met", "component_count",
        ])
        writer.writeheader()
        for i, fraction in enumerate((1.0, 0.5)):
            writer.writerow({
                "seed": 0,
                "topology": f"Topology_{i}",
                "failure_count": i,
                "failure_nodes": "[]",
                "nodes_remaining": 20 - i,
                "largest_component_size": int(fraction * 20),
                "largest_component_fraction": fraction,
                "connected": True,
                "connectivity_threshold_met": True,
                "component_count": 1,
            })
    validate_csv(path)


def test_missing_column_is_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("seed,topology\n0,Topology_A\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        validate_csv(path)
