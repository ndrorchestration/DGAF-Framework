from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_aoss_v0_6_stage_a_predata_readiness.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("aoss_v06_predata_test", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def current_readiness(validator):
    return validator.load_json(ROOT / validator.READINESS_REL)


def test_current_stage_a_state_is_explicitly_not_ready() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    unresolved = validator.validate_readiness(readiness)
    assert readiness["status"] == "NOT_READY_FAIL_CLOSED"
    assert "aoss_decision_policy" in unresolved
    assert "freshness_and_calibration" in unresolved
    assert "analysis_and_multiplicity" in unresolved
    assert "observer_boundary_and_trust_domains" not in unresolved
    assert "extraction_functions_units_tolerances" not in unresolved
    assert "artifact_hash_and_replay_receipt" not in unresolved
    assert len(unresolved) == 7
    assert readiness["outcome_collection_authorized"] is False
    assert readiness["scientific_n_increment"] == 0


def test_bound_predicates_are_evidence_backed() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    for entry in readiness["required_predicates"].values():
        if entry["status"] == "BOUND":
            assert entry["evidence"]


def test_cannot_promote_collection_authorization() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    readiness["outcome_collection_authorized"] = True
    with pytest.raises(SystemExit, match="cannot authorize outcome collection"):
        validator.validate_readiness(readiness)


def test_cannot_claim_ready_while_any_predicate_is_unresolved() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    readiness["status"] = "READY_FOR_SEPARATE_AUTHORIZATION_REVIEW"
    with pytest.raises(SystemExit, match="readiness status is inconsistent"):
        validator.validate_readiness(readiness)


def test_unresolved_predicate_requires_explicit_missing_reasons() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    broken = copy.deepcopy(readiness)
    broken["required_predicates"]["aoss_decision_policy"]["missing"] = []
    with pytest.raises(SystemExit, match="requires a non-empty missing list"):
        validator.validate_readiness(broken)


def test_bound_predicate_cannot_have_empty_evidence() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    broken = copy.deepcopy(readiness)
    broken["required_predicates"]["comparator_policy"]["evidence"] = []
    with pytest.raises(SystemExit, match="requires evidence"):
        validator.validate_readiness(broken)


def test_apparatus_identity_is_exactly_bound() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    broken = copy.deepcopy(readiness)
    broken["apparatus_acceptance"]["repository_commit"] = "0" * 40
    with pytest.raises(SystemExit, match="accepted apparatus commit drift"):
        validator.validate_readiness(broken)


def test_observer_boundary_is_external_read_only_and_nonauthoritative() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    boundary = validator.load_json(ROOT / validator.BOUNDARY_REL)
    assert boundary["observer"]["deployment_mode"] == "EXTERNAL_POST_EXPORT_READ_ONLY"
    assert boundary["observer"]["source_process_mutation"] is False
    assert boundary["observer"]["callbacks_into_source"] is False
    assert boundary["trust_domain_contract"]["validator_domain"]["classification"] == "UNMEASURED"
    assert boundary["trust_domain_contract"]["authority_domain"]["classification"] == "UNMEASURED"


def test_timestamp_extraction_does_not_bind_freshness() -> None:
    validator = load_validator()
    boundary = validator.load_json(ROOT / validator.BOUNDARY_REL)
    wall_time = boundary["extraction_functions"]["wall_time"]
    assert wall_time["tolerance"] == "EXACT_PARSE_AND_PRESERVE"
    assert wall_time["freshness_threshold"] == "SEPARATE_UNRESOLVED_PREDICATE"
    readiness = current_readiness(validator)
    assert readiness["required_predicates"]["freshness_and_calibration"]["status"] == "OPEN"


def test_observer_boundary_rejects_source_mutation() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    boundary = validator.load_json(ROOT / validator.BOUNDARY_REL)
    broken = copy.deepcopy(boundary)
    broken["observer"]["source_process_mutation"] = True
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.BOUNDARY_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="observer deployment boundary drift"):
        validator.validate_readiness(readiness)


def test_extraction_contract_requires_every_field_function_identity() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    boundary = validator.load_json(ROOT / validator.BOUNDARY_REL)
    broken = copy.deepcopy(boundary)
    broken["extraction_functions"]["task_id"]["function_id"] = ""
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.BOUNDARY_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="extraction function identity missing"):
        validator.validate_readiness(readiness)


def test_replay_receipt_contract_is_content_address_only() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    contract = validator.load_json(ROOT / validator.RECEIPT_CONTRACT_REL)
    assert contract["receipt_content_boundary"] == {
        "outcome_payload_embedded": False,
        "episode_payload_embedded": False,
        "numerical_analysis_payload_embedded": False,
        "content_addresses_and_replay_status_only": True,
    }
    assert contract["pass_rule"] == "PASS_IFF_ALL_REPLAY_VERIFICATION_BOOLEANS_TRUE"


def test_replay_receipt_contract_requires_future_frozen_contract_digests() -> None:
    validator = load_validator()
    contract = validator.load_json(ROOT / validator.RECEIPT_CONTRACT_REL)
    roles = set(contract["required_contract_digest_roles"])
    assert {
        "decision_policy_sha256",
        "freshness_calibration_sha256",
        "eligibility_repetition_sha256",
        "failure_ground_truth_sha256",
        "analysis_multiplicity_sha256",
        "practical_effect_rule_sha256",
    }.issubset(roles)


def test_replay_receipt_schema_rejects_embedded_outcome_payload() -> None:
    validator = load_validator()
    schema = validator.load_json(ROOT / validator.RECEIPT_SCHEMA_REL)
    sample_sha = "0" * 64
    contract = validator.load_json(ROOT / validator.RECEIPT_CONTRACT_REL)
    receipt = {
        "record_type": "AOSS_V0_6_STAGE_A_WHOLE_STUDY_REPLAY_RECEIPT",
        "schema_version": 1,
        "study_id": "synthetic-test",
        "attempt_id": "attempt-0",
        "generated_at_utc": "2026-09-19T00:00:00Z",
        "source_system": {
            "repository": "ndrorchestration/agent-control-plane",
            "commit": validator.EXPECTED_SOURCE_COMMIT,
            "provenance_schema": validator.EXPECTED_SCHEMA,
        },
        "apparatus": {
            "accepted_commit": validator.EXPECTED_APPARATUS_COMMIT,
            "adapter_version": validator.EXPECTED_ADAPTER,
        },
        "contract_digests": {name: sample_sha for name in contract["required_contract_digest_roles"]},
        "artifact_digests": {name: sample_sha for name in contract["required_artifact_digest_roles"]},
        "replay_environment": {
            "python_version": "test",
            "os": "test",
            "architecture": "test",
            "dependency_lock_sha256": sample_sha,
            "adapter_source_sha256": sample_sha,
        },
        "replay_verification": {
            "status": "PASS",
            "source_identity_match": True,
            "contract_digest_match": True,
            "study_manifest_hash_match": True,
            "source_episode_bundle_hash_match": True,
            "normalized_replay_digest_match": True,
            "decision_replay_digest_match": True,
            "analysis_replay_digest_match": True,
        },
        "outcome_payload_embedded": False,
        "authorization_effect": "NONE",
        "external_validation_effect": "NONE",
        "scientific_n_increment": 0,
        "numerical_result": {"estimate": 0.5},
    }
    with pytest.raises(validator.ValidationError):
        validator.Draft202012Validator(schema).validate(receipt)
