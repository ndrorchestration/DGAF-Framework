from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.validate_track_a_epoch_002_preregistration import (
    EXPECTED_PREDECESSOR_BLOB,
    validate_records,
)

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
SUCCESSOR = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"


def records() -> tuple[dict[str, object], dict[str, object]]:
    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    successor = json.loads(SUCCESSOR.read_text(encoding="utf-8"))
    return successor, predecessor


def test_successor_preregistration_is_valid_proposal() -> None:
    successor, predecessor = records()
    validate_records(successor, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_protocol_identity_cannot_reuse_epoch_001() -> None:
    successor, predecessor = records()
    successor["protocol_id"] = predecessor["protocol_id"]
    with pytest.raises(AssertionError):
        validate_records(successor, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_successor_seed_collision_fails_closed() -> None:
    successor, predecessor = records()
    mutated = copy.deepcopy(successor)
    mutated["matrix"]["seeds"][0] = predecessor["matrix"]["seeds"][0]
    with pytest.raises(AssertionError):
        validate_records(mutated, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_endpoint_drift_fails_closed() -> None:
    successor, predecessor = records()
    mutated = copy.deepcopy(successor)
    mutated["endpoint"]["field"] = "different_endpoint"
    with pytest.raises(AssertionError):
        validate_records(mutated, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_estimand_drift_fails_closed() -> None:
    successor, predecessor = records()
    mutated = copy.deepcopy(successor)
    mutated["primary_analysis"]["estimand"] = "post_hoc_changed_estimand"
    with pytest.raises(AssertionError):
        validate_records(mutated, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_preregistration_cannot_authorize_collection() -> None:
    successor, predecessor = records()
    mutated = copy.deepcopy(successor)
    mutated["empirical_execution_authorized"] = True
    with pytest.raises(AssertionError):
        validate_records(mutated, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_solo_custody_cannot_be_labeled_independent() -> None:
    successor, predecessor = records()
    mutated = copy.deepcopy(successor)
    mutated["blinding_and_custody"]["same_developer_custody_is_independent"] = True
    with pytest.raises(AssertionError):
        validate_records(mutated, predecessor, EXPECTED_PREDECESSOR_BLOB)


def test_predecessor_blob_drift_fails_closed() -> None:
    successor, predecessor = records()
    with pytest.raises(AssertionError):
        validate_records(successor, predecessor, "0" * 40)
