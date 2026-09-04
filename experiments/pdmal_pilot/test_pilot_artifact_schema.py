from __future__ import annotations

import hashlib

import pytest

from pilot_artifact_schema import canonical_json_bytes, validate_artifact

TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURES = (0, 1, 2, 3, 4, 5, 6, 8, 10)
CONDITIONS = ("blind_a", "blind_b", "blind_c", "blind_d")


def _record(condition: str, trial_id: int, topology: str, failure_count: int) -> dict:
    record = {
        "experiment_id": "PDMAL-PILOT-V1",
        "protocol_version": "0.7.5",
        "experiment_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "blinded_condition_id": condition,
        "trial_id": trial_id,
        "topology": topology,
        "failure_count": failure_count,
        "primary_outcome": 0.1,
        "secondary_outcomes": {"final_mean": 0.0},
        "failure": failure_count > 0,
        "recovery": failure_count > 0,
        "ffcr_success": True,
        "runtime_ms": 1,
        "status": "RECOVERED" if failure_count > 0 else "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env",
    }
    record["artifact_sha256"] = hashlib.sha256(canonical_json_bytes(record)).hexdigest()
    return record


def _document() -> dict:
    records = []
    trial_id = 0
    for condition in CONDITIONS:
        for topology in TOPOLOGIES:
            for failure_count in FAILURES:
                records.append(_record(condition, trial_id, topology, failure_count))
                trial_id += 1
    return {
        "schema_version": "1.0",
        "artifact_version": "seed-20260819",
        "protocol_status": "FROZEN",
        "empirical_data_collection": True,
        "frozen_commit_sha": "a" * 40,
        "seed_id": 20260819,
        "runtime_seconds": 1.0,
        "records": records,
    }


def test_valid_complete_artifact_passes() -> None:
    validate_artifact(_document(), expected_seed=20260819)


def test_recovered_success_is_valid_ffcr_outcome() -> None:
    document = _document()
    recovered = document["records"][1]
    assert recovered["status"] == "RECOVERED"
    assert recovered["recovery"] is True
    assert recovered["ffcr_success"] is True
    validate_artifact(document, expected_seed=20260819)


def test_duplicate_matrix_cell_is_rejected() -> None:
    document = _document()
    duplicate = dict(document["records"][0])
    duplicate["trial_id"] = document["records"][-1]["trial_id"]
    duplicate["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in duplicate.items() if k != "artifact_sha256"})
    ).hexdigest()
    document["records"][-1] = duplicate
    with pytest.raises(AssertionError, match="duplicate pilot matrix cell"):
        validate_artifact(document, expected_seed=20260819)


def test_condition_distribution_must_be_balanced() -> None:
    document = _document()
    for record in document["records"][45:90]:
        record["blinded_condition_id"] = "blind_a"
        record["artifact_sha256"] = hashlib.sha256(
            canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})
        ).hexdigest()
    with pytest.raises(AssertionError):
        validate_artifact(document, expected_seed=20260819)


def test_each_condition_must_have_identical_matrix_cells() -> None:
    document = _document()
    first = document["records"][0]       # blind_a / ring / 0
    second = document["records"][46]     # blind_b / ring / 1
    first["topology"], second["topology"] = second["topology"], first["topology"]
    first["failure_count"], second["failure_count"] = second["failure_count"], first["failure_count"]
    first["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in first.items() if k != "artifact_sha256"})
    ).hexdigest()
    second["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in second.items() if k != "artifact_sha256"})
    ).hexdigest()
    with pytest.raises(AssertionError, match="complete canonical pilot matrix"):
        validate_artifact(document, expected_seed=20260819)


def test_record_commit_must_match_document_commit() -> None:
    document = _document()
    document["records"][0]["experiment_commit_sha"] = "b" * 40
    document["records"][0]["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in document["records"][0].items() if k != "artifact_sha256"})
    ).hexdigest()
    with pytest.raises(AssertionError, match="experiment_commit_sha"):
        validate_artifact(document, expected_seed=20260819)


def test_recovered_record_requires_recovery_flag() -> None:
    document = _document()
    record = document["records"][1]
    record["recovery"] = False
    record["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in record.items() if k != "artifact_sha256"})
    ).hexdigest()
    with pytest.raises(AssertionError, match="RECOVERED records require recovery=true"):
        validate_artifact(document, expected_seed=20260819)
