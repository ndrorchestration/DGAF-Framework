import os

import pytest

from artifacts import blind_rows, write_csv


def test_topology_labels_are_masked_for_pilot_analysis(tmp_path):
    secret = "x" * 32
    rows = [
        {"seed": 0, "topology": "pdmal", "largest_component_fraction": 1.0},
        {"seed": 0, "topology": "ring", "largest_component_fraction": 0.5},
    ]
    masked = blind_rows(rows, secret)
    assert all(row["topology"].startswith("Topology_") for row in masked)
    assert all(row["topology"] not in {"pdmal", "ring"} for row in masked)


def test_missing_blinding_secret_fails_closed():
    with pytest.raises(ValueError):
        blind_rows([{"topology": "pdmal"}], "")


def test_csv_persistence_emits_sha256(tmp_path):
    path, digest = write_csv(
        [{"seed": 0, "topology": "Topology_A", "largest_component_fraction": 1.0}],
        "abc1234",
        tmp_path,
    )
    assert path.name.startswith("raw_pilot_abc1234_")
    assert len(digest) == 64
    assert path.with_suffix(path.suffix + ".sha256").exists()
