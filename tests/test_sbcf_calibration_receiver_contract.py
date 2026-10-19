"""Closed-schema tests for the candidate calibration receiver contract."""

import json
from pathlib import Path

import pytest

from experiments.sbcf.calibration_receiver_contract import (
    calibration_receiver_contract_digest,
    evaluate_calibration_receiver_contract,
    validate_calibration_receiver_contract,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "calibration_receiver_contract_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_candidate_contract_is_not_ready():
    result = evaluate_calibration_receiver_contract(load())
    assert not result.ready
    assert result.blockers == (
        "calibration_receiver_contract_not_frozen",
        "receiver_build_unfrozen",
        "runtime_mapping_unfrozen:acs",
        "runtime_mapping_unfrozen:openshell",
        "runtime_mapping_unfrozen:sbcf",
    )


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("effect_contract_digest", "exact v1 effect contract"),
        ("receiver_custody_digest", "exact custody contract"),
        ("negative_observation_protocol_digest", "exact observation protocol"),
    ],
)
def test_contract_is_bound_to_exact_parent_bytes(field, message):
    contract = load()
    contract[field] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match=message):
        validate_calibration_receiver_contract(contract)


def test_unfrozen_build_cannot_smuggle_identity():
    contract = load()
    contract["receiver_build"]["build_id"] = "receiver:unexpected"
    with pytest.raises(ValueError, match="unfrozen receiver build"):
        validate_calibration_receiver_contract(contract)


def test_frozen_build_requires_source_hash():
    contract = load()
    contract["receiver_build"].update({"status": "FROZEN", "build_id": "receiver:v0"})
    with pytest.raises(ValueError, match="requires exact identity"):
        validate_calibration_receiver_contract(contract)


def test_unfrozen_mapping_cannot_smuggle_digest():
    contract = load()
    contract["system_runtime_mappings"]["sbcf"]["runtime_mapping_digest"] = "sha256:unexpected"
    with pytest.raises(ValueError, match="unfrozen runtime mapping"):
        validate_calibration_receiver_contract(contract)


def test_receipt_safeguards_cannot_be_weakened():
    for field in ("custody_envelope_required", "analysis_fields_prohibited", "trial_outcomes_prohibited"):
        contract = load()
        contract["receipt_contract"][field] = False
        with pytest.raises(ValueError, match="safeguard weakened"):
            validate_calibration_receiver_contract(contract)


def test_structural_ready_requires_frozen_build_and_all_mappings():
    contract = load()
    contract["status"] = "FROZEN"
    contract["receiver_build"] = {
        "status": "FROZEN",
        "build_id": "receiver:v0",
        "source_sha256": "a" * 64,
    }
    for system_id in ("sbcf", "acs", "openshell"):
        contract["system_runtime_mappings"][system_id] = {
            "status": "FROZEN",
            "runtime_mapping_digest": f"sha256:{system_id}-mapping-v0",
        }

    result = evaluate_calibration_receiver_contract(contract)
    assert result.ready
    assert result.blockers == ()
    assert calibration_receiver_contract_digest(contract).startswith("sha256:")


def test_candidate_digest_is_deterministic():
    first = calibration_receiver_contract_digest(load())
    second = calibration_receiver_contract_digest(load())
    assert first == second
    assert len(first) == len("sha256:") + 64
