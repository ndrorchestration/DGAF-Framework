import pytest

from artifacts import blind_label, blind_rows, write_csv


def test_topology_labels_are_masked_with_external_secret():
    rows = [
        {"seed": 0, "topology": "pdmal", "largest_component_fraction": 1.0},
        {"seed": 0, "topology": "ring", "largest_component_fraction": 1.0},
    ]
    masked = blind_rows(rows, "test-secret")
    assert all(row["topology"].startswith("Topology_") for row in masked)
    assert len({row["topology"] for row in masked}) == 2
    assert all(len(row["topology"].split("_")[-1]) == 12 for row in masked)


def test_blinding_mapping_changes_with_secret():
    assert blind_label("pdmal", "secret-a") != blind_label("pdmal", "secret-b")


def test_missing_blinding_secret_is_rejected():
    with pytest.raises(ValueError):
        blind_label("pdmal", "")


def test_csv_persistence_emits_sha256(tmp_path):
    path, digest = write_csv(
        [{"seed": 0, "topology": "Topology_A", "largest_component_fraction": 1.0}],
        "abc1234",
        tmp_path,
    )
    assert path.name.startswith("raw_pilot_abc1234_")
    assert len(digest) == 64
    assert path.with_suffix(path.suffix + ".sha256").exists()
