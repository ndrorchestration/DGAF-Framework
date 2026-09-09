from __future__ import annotations

import json
from pathlib import Path

import pytest

from run_canonical_epoch_004 import (
    ANALYSIS_BLOB_SHA,
    ANALYSIS_CONFIG_SHA256,
    COLLECTION_CONTRACT_MERGE_SHA,
    EPOCH_ID,
    OBSERVATIONS,
    PREFLIGHT_MERGE_SHA,
    PREREG_MERGE_SHA,
    SEEDS,
    SEED_START,
    RUN_REQUEST_PATH,
    _load_request,
    validate_run_request,
)


def _request(parent_sha: str) -> dict:
    return {
        "record_type": "DGAF_CANONICAL_SOLO_EMPIRICAL_RUN_REQUEST",
        "schema_version": 1,
        "epoch_id": EPOCH_ID,
        "authorized_runner_parent_sha": parent_sha,
        "preregistration_merge_sha": PREREG_MERGE_SHA,
        "treatment_input_preflight_merge_sha": PREFLIGHT_MERGE_SHA,
        "collection_contract_merge_sha": COLLECTION_CONTRACT_MERGE_SHA,
        "seed_start": SEED_START,
        "seeds": SEEDS,
        "expected_observations": OBSERVATIONS,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "validation_track": "SOLO_DEVELOPER",
        "limitations_acknowledged": True,
        "authorize_empirical_collection": True,
        "authorize_unblinding": False,
        "historical_pooling_allowed": False,
    }


def test_repository_contains_no_epoch004_run_request_yet():
    assert not RUN_REQUEST_PATH.exists()


def test_load_request_fails_closed_when_absent(tmp_path: Path):
    with pytest.raises(SystemExit, match="valid run request absent"):
        _load_request(tmp_path / "absent.json")


def test_exact_request_accepts_known_parent_and_distinct_run_sha():
    parent = "1" * 40
    run_sha = "2" * 40
    validate_run_request(_request(parent), frozen_sha=run_sha, parent_sha=parent)


def test_request_rejects_self_referential_parent_binding():
    sha = "3" * 40
    with pytest.raises(SystemExit, match="authorization commit must be distinct"):
        validate_run_request(_request(sha), frozen_sha=sha, parent_sha=sha)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("authorize_unblinding", True),
        ("historical_pooling_allowed", True),
        ("seeds", 49),
        ("expected_observations", 8999),
        ("validation_track", "HIGH_ASSURANCE"),
        ("analysis_blob_sha", "0" * 40),
    ],
)
def test_request_rejects_material_boundary_changes(field: str, value):
    parent = "4" * 40
    request = _request(parent)
    request[field] = value
    with pytest.raises(SystemExit, match="run request mismatch"):
        validate_run_request(request, frozen_sha="5" * 40, parent_sha=parent)


def test_request_rejects_extra_fields():
    parent = "6" * 40
    request = _request(parent)
    request["post_hoc_override"] = True
    with pytest.raises(SystemExit, match="run request mismatch"):
        validate_run_request(request, frozen_sha="7" * 40, parent_sha=parent)
