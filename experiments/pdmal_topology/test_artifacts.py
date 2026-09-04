import os

import pytest

from artifacts import blind_rows, environment_commit_short, write_csv


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


def test_candidate_sha_takes_precedence_over_pull_request_merge_sha(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "d8986ca59f6b3bf59ce2de944dbbf1cdb549b0c2")
    monkeypatch.setenv("CANDIDATE_SHA", "1ebd12f8c975fd9074060293732699035fa45c87")
    assert environment_commit_short() == "1ebd12f"


def test_candidate_sha_falls_back_to_github_sha(monkeypatch):
    monkeypatch.delenv("CANDIDATE_SHA", raising=False)
    monkeypatch.setenv("GITHUB_SHA", "1234567890abcdef")
    assert environment_commit_short() == "1234567"
