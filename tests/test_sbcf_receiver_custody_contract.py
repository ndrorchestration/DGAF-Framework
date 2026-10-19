"""Closed-schema tests for candidate receiver custody contract."""

import copy
import json
from pathlib import Path

import pytest

from experiments.sbcf.receiver_custody_contract import (
    evaluate_receiver_custody_contract,
    receiver_custody_contract_digest,
    validate_receiver_custody_contract,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "receiver_custody_contract_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_receiver_custody_is_not_ready():
    result = evaluate_receiver_custody_contract(load())
    assert not result.ready
    assert result.blockers == (
        "custody_contract_not_frozen",
        "durable_retention_unfrozen",
        "receiver_operator_unassigned",
    )


def test_receiver_custody_digest_is_deterministic():
    contract = load()
    assert receiver_custody_contract_digest(contract) == receiver_custody_contract_digest(copy.deepcopy(contract))


def test_candidate_is_bound_to_exact_v1_effect_contract():
    contract = load()
    contract["effect_contract_digest"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="exact v1 effect contract"):
        validate_receiver_custody_contract(contract)


@pytest.mark.parametrize(
    "field",
    [
        "outside_implementation_required",
        "uncoached_required",
        "same_owner_automation_disallowed",
    ],
)
def test_receiver_operator_independence_requirements_cannot_be_weakened(field):
    contract = load()
    contract["receiver_operator"][field] = False
    with pytest.raises(ValueError, match="requirement weakened"):
        validate_receiver_custody_contract(contract)


def test_unassigned_operator_cannot_have_identity():
    contract = load()
    contract["receiver_operator"]["operator_id"] = "someone"
    with pytest.raises(ValueError, match="unassigned receiver operator"):
        validate_receiver_custody_contract(contract)


def test_assigned_operator_requires_identity():
    contract = load()
    contract["receiver_operator"]["status"] = "ASSIGNED"
    with pytest.raises(ValueError, match="requires id"):
        validate_receiver_custody_contract(contract)


def test_raw_receipt_cannot_include_analysis_fields_by_policy_relaxation():
    contract = load()
    contract["raw_receipt"]["analysis_fields_prohibited"] = False
    with pytest.raises(ValueError, match="safeguard weakened"):
        validate_receiver_custody_contract(contract)


def test_private_keys_remain_prohibited_from_raw_receipt():
    contract = load()
    contract["raw_receipt"]["private_keys_prohibited"] = False
    with pytest.raises(ValueError, match="safeguard weakened"):
        validate_receiver_custody_contract(contract)


def test_frozen_retention_requires_complete_identity():
    contract = load()
    contract["durable_retention"]["status"] = "FROZEN"
    with pytest.raises(ValueError, match="complete identity"):
        validate_receiver_custody_contract(contract)


def test_structural_ready_requires_operator_and_retention_freeze():
    contract = load()
    contract["status"] = "FROZEN"
    contract["receiver_operator"]["status"] = "ASSIGNED"
    contract["receiver_operator"]["operator_id"] = "EXTERNAL_RECEIVER_OPERATOR_001"
    contract["durable_retention"].update(
        {
            "status": "FROZEN",
            "archive_location": "approved://receiver-evidence",
            "archive_identifier": "receipt-set-001",
            "retention_period": "P1Y",
            "access_control_owner": "EXTERNAL_RECEIVER_OPERATOR_001",
        }
    )

    result = evaluate_receiver_custody_contract(contract)

    assert result.ready
    assert result.blockers == ()


def test_structural_ready_does_not_imply_independent_validation():
    contract = load()
    contract["status"] = "FROZEN"
    contract["receiver_operator"]["status"] = "ASSIGNED"
    contract["receiver_operator"]["operator_id"] = "EXTERNAL_RECEIVER_OPERATOR_001"
    contract["durable_retention"].update(
        {
            "status": "FROZEN",
            "archive_location": "approved://receiver-evidence",
            "archive_identifier": "receipt-set-001",
            "retention_period": "P1Y",
            "access_control_owner": "EXTERNAL_RECEIVER_OPERATOR_001",
        }
    )

    result = evaluate_receiver_custody_contract(copy.deepcopy(contract))

    assert result.ready
    assert contract["separation"]["independent_validation_not_implied"] is True


def test_unknown_top_level_field_is_rejected():
    contract = load()
    contract["scientific_n_increment"] = 1
    with pytest.raises(ValueError):
        validate_receiver_custody_contract(contract)
