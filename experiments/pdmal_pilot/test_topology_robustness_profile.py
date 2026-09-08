from __future__ import annotations

import json

from topology_robustness_profile import (
    ALGORITHM_ID,
    DIAGNOSTIC_SEEDS,
    PROFILE_ID,
    run_probe,
)


def test_track_a_probe_is_structural_only_and_complete(tmp_path):
    out = tmp_path / "probe.json"
    document = run_probe(out)

    assert document["profile_id"] == PROFILE_ID
    assert document["algorithm_id"] == ALGORITHM_ID
    assert document["scientific_n_increment"] == 0
    assert document["empirical_authorization"] is False
    assert document["completed_cells"] == document["expected_cells"] == 90
    assert document["seeds"] == list(DIAGNOSTIC_SEEDS)
    assert len(document["records"]) == 90

    raw = out.read_text(encoding="utf-8").lower()
    for forbidden in (
        "ffcr",
        "final_std",
        "consensus_success",
        "treatment_effect",
        "confidence_interval",
        "p_value",
        "governance_trace",
        "condition",
        "dgaf",
    ):
        assert forbidden not in raw


def test_track_a_probe_has_unique_matrix_and_recovery_identity(tmp_path):
    document = run_probe(tmp_path / "probe.json")
    identities = {
        (r["seed"], r["topology"], r["failure_count"])
        for r in document["records"]
    }
    assert len(identities) == 90
    assert all(
        r["phase_update_hashes"]["pre_failure"]
        == r["phase_update_hashes"]["recovered"]
        for r in document["records"]
    )


def test_track_a_probe_is_byte_deterministic(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    run_probe(first)
    run_probe(second)
    assert first.read_bytes() == second.read_bytes()

    parsed = json.loads(first.read_text(encoding="utf-8"))
    assert parsed["classification"] == "STRUCTURAL_HASH_ONLY_NONEMPIRICAL"
