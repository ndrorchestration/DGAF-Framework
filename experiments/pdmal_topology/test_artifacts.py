from artifacts import blind_rows, write_csv


def test_topology_labels_are_masked_for_pilot_analysis(tmp_path):
    rows = [
        {"seed": 0, "topology": "pdmal", "largest_component_fraction": 1.0},
        {"seed": 0, "topology": "ring", "largest_component_fraction": 1.0},
    ]
    masked = blind_rows(rows)
    assert all(row["topology"].startswith("Topology_") for row in masked)
    assert {row["topology"] for row in masked} == {"Topology_A", "Topology_B"}


def test_csv_persistence_emits_sha256(tmp_path):
    path, digest = write_csv(
        [{"seed": 0, "topology": "Topology_A", "largest_component_fraction": 1.0}],
        "abc1234",
        tmp_path,
    )
    assert path.name.startswith("raw_pilot_abc1234_")
    assert len(digest) == 64
    assert path.with_suffix(path.suffix + ".sha256").exists()
