#!/usr/bin/env python3
"""Validate AOSS v0.6 Stage-A pre-data readiness without generating outcomes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
READINESS_REL = "registry/aoss_v0_6_stage_a_predata_readiness_v1.json"
MEASUREMENT_REL = "registry/aoss_v0_6_acp_measurement_manifest_v1.json"
BOUNDARY_REL = "registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json"
RECEIPT_CONTRACT_REL = "registry/aoss_v0_6_stage_a_artifact_replay_receipt_contract_v1.json"
RECEIPT_SCHEMA_REL = "schemas/aoss_v0_6_stage_a_replay_receipt.schema.json"
FRESHNESS_REL = "registry/aoss_v0_6_stage_a_freshness_calibration_v1.json"
ELIGIBILITY_REL = "registry/aoss_v0_6_stage_a_episode_eligibility_repetition_v1.json"
GROUND_TRUTH_REL = "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json"

ALLOWED_STATUSES = {"BOUND", "PARTIAL", "OPEN", "BLOCKED"}
REQUIRED_PREDICATES = {
    "external_target_identity",
    "observer_boundary_and_trust_domains",
    "telemetry_schema",
    "extraction_functions_units_tolerances",
    "freshness_and_calibration",
    "comparator_policy",
    "aoss_decision_policy",
    "primary_endpoint",
    "secondary_and_safety_endpoints",
    "episode_eligibility_and_exclusion",
    "repetition_and_seed_plan",
    "failure_injection_ground_truth",
    "falsification_criteria",
    "practical_effect_or_adoption_rule",
    "analysis_and_multiplicity",
    "artifact_hash_and_replay_receipt",
    "authorization_and_nonauthority_boundary",
}

EXPECTED_APPARATUS_COMMIT = "69821cdcc1b9b9432b7001c6f52c867f9669f54d"
EXPECTED_SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
EXPECTED_SCHEMA = "agent-control-plane.provenance.v1"
EXPECTED_ADAPTER = "AOSS_V0_6_ACP_ADAPTER_V1"
EXPECTED_COMPARATOR = {
    "version": "AOSS_V0_5_OMR_FROZEN",
    "rule": {
        "missing_coarse_state": "HOLD",
        "o_eq_0_and_r_eq_0": "STOP",
        "otherwise": "CONTINUE",
    },
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"AOSS_V0_6_STAGE_A_PREDATA_FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON from {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def unresolved_predicates(readiness: dict[str, Any]) -> list[str]:
    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    if set(predicates) != REQUIRED_PREDICATES:
        fail("required predicate set drift")

    unresolved: list[str] = []
    for name in sorted(REQUIRED_PREDICATES):
        entry = predicates[name]
        if not isinstance(entry, dict):
            fail(f"predicate {name} must be an object")
        status = entry.get("status")
        if status not in ALLOWED_STATUSES:
            fail(f"predicate {name} has invalid status")
        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
            fail(f"predicate {name} evidence must be a list of non-empty strings")
        if status == "BOUND" and not evidence:
            fail(f"BOUND predicate {name} requires evidence")
        if status != "BOUND":
            missing = entry.get("missing")
            if not isinstance(missing, list) or not missing:
                fail(f"unresolved predicate {name} requires a non-empty missing list")
            if any(not isinstance(item, str) or not item for item in missing):
                fail(f"predicate {name} missing entries must be non-empty strings")
            unresolved.append(name)
    return unresolved


def validate_apparatus_binding(readiness: dict[str, Any]) -> None:
    apparatus = readiness.get("apparatus_acceptance")
    if not isinstance(apparatus, dict):
        fail("apparatus_acceptance must be an object")
    if apparatus.get("repository_commit") != EXPECTED_APPARATUS_COMMIT:
        fail("accepted apparatus commit drift")
    if apparatus.get("pull_request") != 859:
        fail("accepted apparatus PR drift")

    measurement = load_json(ROOT / MEASUREMENT_REL)
    source = measurement.get("source_system")
    if not isinstance(source, dict):
        fail("measurement source_system is malformed")
    if source.get("commit") != EXPECTED_SOURCE_COMMIT:
        fail("ACP source commit drift")
    if source.get("provenance_schema") != EXPECTED_SCHEMA:
        fail("ACP provenance schema drift")
    if measurement.get("observer_version") != EXPECTED_ADAPTER:
        fail("adapter version drift")
    if measurement.get("comparator") != EXPECTED_COMPARATOR:
        fail("frozen OMR comparator drift")

    classes = measurement.get("required_episode_classes")
    if not isinstance(classes, list) or len(classes) != 16 or len(set(classes)) != 16:
        fail("required Stage-A episode class contract drift")


def validate_observer_measurement_boundary(readiness: dict[str, Any]) -> None:
    boundary = load_json(ROOT / BOUNDARY_REL)
    if boundary.get("record_type") != "AOSS_V0_6_STAGE_A_OBSERVER_MEASUREMENT_BOUNDARY":
        fail("observer measurement boundary record_type drift")
    if boundary.get("schema_version") != 1 or boundary.get("controller_issue") != 810:
        fail("observer measurement boundary identity drift")
    if boundary.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
        fail("observer measurement boundary status drift")
    if boundary.get("outcome_collection_authorized") is not False:
        fail("observer measurement boundary cannot authorize outcome collection")
    if boundary.get("external_validation_established") is not False:
        fail("observer measurement boundary cannot establish external validation")
    if boundary.get("scientific_n_increment") != 0:
        fail("observer measurement boundary cannot increment scientific N")

    source = boundary.get("source_system")
    if not isinstance(source, dict):
        fail("observer measurement source_system is malformed")
    if source.get("commit") != EXPECTED_SOURCE_COMMIT or source.get("provenance_schema") != EXPECTED_SCHEMA:
        fail("observer measurement source identity drift")

    observer = boundary.get("observer")
    if not isinstance(observer, dict):
        fail("observer deployment contract is malformed")
    expected_observer = {
        "version": EXPECTED_ADAPTER,
        "deployment_mode": "EXTERNAL_POST_EXPORT_READ_ONLY",
        "input_surface": "EXPORTED_ACP_PROVENANCE_MANIFEST_ONLY",
        "source_process_mutation": False,
        "callbacks_into_source": False,
        "source_environment_or_config_injection": False,
        "source_scheduling_or_policy_control": False,
        "source_instrumentation_patch": False,
    }
    if observer != expected_observer:
        fail("observer deployment boundary drift")

    trust = boundary.get("trust_domain_contract")
    if not isinstance(trust, dict):
        fail("trust-domain contract is malformed")
    if trust.get("source_event_origin", {}).get("classification") != "SYSTEM":
        fail("source event origin classification drift")
    if trust.get("observer_metadata_origin", {}).get("classification") != "OBSERVER":
        fail("observer metadata classification drift")
    if trust.get("validator_domain") != {
        "classification": "UNMEASURED",
        "source_evidence": "ABSENT",
    }:
        fail("validator trust-domain boundary drift")
    if trust.get("authority_domain") != {
        "classification": "UNMEASURED",
        "source_evidence": "ABSENT",
    }:
        fail("authority trust-domain boundary drift")

    extraction = boundary.get("extraction_functions")
    if not isinstance(extraction, dict):
        fail("extraction function contract is malformed")
    expected_fields = {
        "trace_id",
        "observer_event_id",
        "source_event_id",
        "parent_event_id",
        "source_order_index",
        "component",
        "event_kind",
        "task_id",
        "capability",
        "state",
        "detail",
        "wall_time",
        "trust_domain",
        "validation_state",
        "authorization_state",
        "durable_attestation",
    }
    if set(extraction) != expected_fields:
        fail("extraction function field set drift")
    if extraction["wall_time"].get("freshness_threshold") != "SEPARATE_FROZEN_PREDICATE_CONTRACT":
        fail("timestamp extraction freshness-contract binding drift")
    if extraction["source_order_index"].get("tolerance") != "EXACT_INTEGER_ZERO_TOLERANCE":
        fail("source-order numeric tolerance drift")
    for field, entry in extraction.items():
        if not isinstance(entry, dict) or not entry.get("function_id"):
            fail(f"extraction function identity missing for {field}")

    tolerance = boundary.get("numeric_tolerance_policy")
    if tolerance != {
        "floating_numeric_measurements_present": False,
        "source_order_index_tolerance": 0,
        "timestamp_extraction_tolerance": "NONE_EXACT_PARSE_AND_PRESERVE",
        "freshness_threshold_is_not_an_extraction_tolerance": True,
    }:
        fail("numeric tolerance policy drift")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    observer_predicate = predicates.get("observer_boundary_and_trust_domains")
    extraction_predicate = predicates.get("extraction_functions_units_tolerances")
    if not isinstance(observer_predicate, dict) or observer_predicate.get("status") != "BOUND":
        fail("observer boundary predicate must be BOUND")
    if not isinstance(extraction_predicate, dict) or extraction_predicate.get("status") != "BOUND":
        fail("extraction predicate must be BOUND")


def validate_artifact_replay_receipt_contract(readiness: dict[str, Any]) -> None:
    contract = load_json(ROOT / RECEIPT_CONTRACT_REL)
    schema = load_json(ROOT / RECEIPT_SCHEMA_REL)

    if contract.get("record_type") != "AOSS_V0_6_STAGE_A_ARTIFACT_REPLAY_RECEIPT_CONTRACT":
        fail("artifact replay receipt contract record_type drift")
    if contract.get("schema_version") != 1 or contract.get("controller_issue") != 810:
        fail("artifact replay receipt contract identity drift")
    if contract.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
        fail("artifact replay receipt contract status drift")
    if contract.get("receipt_schema") != RECEIPT_SCHEMA_REL:
        fail("artifact replay receipt schema binding drift")
    if contract.get("digest_algorithm") != "SHA-256":
        fail("artifact replay digest algorithm drift")
    if contract.get("digest_encoding") != "lowercase_hex_without_prefix":
        fail("artifact replay digest encoding drift")
    if contract.get("pass_rule") != "PASS_IFF_ALL_REPLAY_VERIFICATION_BOOLEANS_TRUE":
        fail("artifact replay PASS rule drift")
    if contract.get("failure_rule") != "ANY_FALSE_OR_MISSING_REQUIRED_FIELD_YIELDS_FAIL_OR_SCHEMA_REJECTION":
        fail("artifact replay failure rule drift")
    if contract.get("outcome_collection_authorized") is not False:
        fail("artifact replay contract cannot authorize outcome collection")
    if contract.get("external_validation_established") is not False:
        fail("artifact replay contract cannot establish external validation")
    if contract.get("scientific_n_increment") != 0:
        fail("artifact replay contract cannot increment scientific N")

    content_boundary = contract.get("receipt_content_boundary")
    if content_boundary != {
        "outcome_payload_embedded": False,
        "episode_payload_embedded": False,
        "numerical_analysis_payload_embedded": False,
        "content_addresses_and_replay_status_only": True,
    }:
        fail("artifact replay receipt content boundary drift")

    expected_contract_roles = {
        "measurement_manifest_sha256",
        "observer_measurement_boundary_sha256",
        "decision_policy_sha256",
        "freshness_calibration_sha256",
        "eligibility_repetition_sha256",
        "failure_ground_truth_sha256",
        "analysis_multiplicity_sha256",
        "practical_effect_rule_sha256",
    }
    expected_artifact_roles = {
        "study_manifest_sha256",
        "source_episode_bundle_sha256",
        "normalized_bundle_sha256",
        "decision_bundle_sha256",
        "analysis_bundle_sha256",
    }
    if set(contract.get("required_contract_digest_roles", [])) != expected_contract_roles:
        fail("required contract digest roles drift")
    if set(contract.get("required_artifact_digest_roles", [])) != expected_artifact_roles:
        fail("required artifact digest roles drift")

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        fail(f"replay receipt JSON Schema is invalid: {exc}")

    sample_sha = "0" * 64
    sample = {
        "record_type": "AOSS_V0_6_STAGE_A_WHOLE_STUDY_REPLAY_RECEIPT",
        "schema_version": 1,
        "study_id": "synthetic-schema-check",
        "attempt_id": "attempt-0",
        "generated_at_utc": "2026-09-19T00:00:00Z",
        "source_system": {
            "repository": "ndrorchestration/agent-control-plane",
            "commit": EXPECTED_SOURCE_COMMIT,
            "provenance_schema": EXPECTED_SCHEMA,
        },
        "apparatus": {
            "accepted_commit": EXPECTED_APPARATUS_COMMIT,
            "adapter_version": EXPECTED_ADAPTER,
        },
        "contract_digests": {name: sample_sha for name in expected_contract_roles},
        "artifact_digests": {name: sample_sha for name in expected_artifact_roles},
        "replay_environment": {
            "python_version": "schema-check",
            "os": "schema-check",
            "architecture": "schema-check",
            "dependency_lock_sha256": sample_sha,
            "adapter_source_sha256": sample_sha,
        },
        "replay_verification": {
            "status": "FAIL",
            "source_identity_match": False,
            "contract_digest_match": False,
            "study_manifest_hash_match": False,
            "source_episode_bundle_hash_match": False,
            "normalized_replay_digest_match": False,
            "decision_replay_digest_match": False,
            "analysis_replay_digest_match": False,
        },
        "outcome_payload_embedded": False,
        "authorization_effect": "NONE",
        "external_validation_effect": "NONE",
        "scientific_n_increment": 0,
    }
    try:
        Draft202012Validator(schema).validate(sample)
    except ValidationError as exc:
        fail(f"replay receipt schema rejects its synthetic contract check: {exc.message}")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    receipt_predicate = predicates.get("artifact_hash_and_replay_receipt")
    if not isinstance(receipt_predicate, dict) or receipt_predicate.get("status") != "BOUND":
        fail("artifact hash/replay receipt predicate must be BOUND")


def validate_freshness_sampling_ground_truth(readiness: dict[str, Any]) -> None:
    freshness = load_json(ROOT / FRESHNESS_REL)
    eligibility = load_json(ROOT / ELIGIBILITY_REL)
    ground_truth = load_json(ROOT / GROUND_TRUTH_REL)
    measurement = load_json(ROOT / MEASUREMENT_REL)

    for record, expected_type in (
        (freshness, "AOSS_V0_6_STAGE_A_FRESHNESS_CALIBRATION_CONTRACT"),
        (eligibility, "AOSS_V0_6_STAGE_A_EPISODE_ELIGIBILITY_REPETITION_CONTRACT"),
        (ground_truth, "AOSS_V0_6_STAGE_A_FAILURE_INJECTION_GROUND_TRUTH"),
    ):
        if record.get("record_type") != expected_type:
            fail("Stage A study-design contract record_type drift")
        if record.get("schema_version") != 1 or record.get("controller_issue") != 810:
            fail("Stage A study-design contract identity drift")
        if record.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
            fail("Stage A study-design contract status drift")
        if record.get("outcome_collection_authorized") is not False:
            fail("Stage A study-design contract cannot authorize outcome collection")
        if record.get("external_validation_established") is not False:
            fail("Stage A study-design contract cannot establish external validation")
        if record.get("scientific_n_increment") != 0:
            fail("Stage A study-design contract cannot increment scientific N")

    if freshness.get("clock_domain") != {
        "source_and_observer_same_host_required": True,
        "source_timestamp_basis": "ACP timezone-aware UTC wall time",
        "observer_ingest_timestamp_basis": "same-host timezone-aware UTC wall time",
        "external_time_accuracy_claim": False,
        "cross_host_clock_comparison_allowed": False,
    }:
        fail("freshness clock-domain contract drift")
    if freshness.get("thresholds") != {
        "max_last_event_age_at_ingest_seconds": 30,
        "max_future_event_skew_seconds": 2,
        "non_injection_event_time_regression_seconds": 0,
    }:
        fail("freshness numeric threshold drift")
    calibration = freshness.get("calibration_semantics")
    if not isinstance(calibration, dict):
        fail("freshness calibration semantics are malformed")
    if calibration.get("absolute_clock_accuracy_established") is not False:
        fail("freshness contract cannot claim external clock accuracy")

    classes = measurement.get("required_episode_classes")
    if not isinstance(classes, list):
        fail("measurement required_episode_classes is malformed")
    if eligibility.get("required_episode_classes") != classes:
        fail("eligibility class set drift")
    primary = eligibility.get("primary_endpoint")
    if not isinstance(primary, dict):
        fail("primary endpoint eligibility contract is malformed")
    excluded = {"malformed_manifest", "mismatched_run_id"}
    if set(primary.get("structural_rejection_controls_excluded_from_denominator", [])) != excluded:
        fail("structural rejection exclusion set drift")
    if set(primary.get("eligible_classes", [])) != set(classes) - excluded:
        fail("primary endpoint eligible class set drift")
    if primary.get("no_posthoc_exclusion") is not True:
        fail("post-hoc exclusion must remain prohibited")

    repetition = eligibility.get("repetition_plan")
    if repetition != {
        "canonical_source_episodes_per_class": 1,
        "exact_byte_replay_passes_per_episode": 5,
        "replay_passes_count_as_independent_observations": False,
        "stochastic_sampling": False,
        "random_seed_policy": "NOT_APPLICABLE_NO_STOCHASTIC_SAMPLING",
        "independence_claim": False,
    }:
        fail("repetition/seed contract drift")

    labels = ground_truth.get("labels")
    if not isinstance(labels, dict) or set(labels) != set(classes):
        fail("failure-injection ground-truth class set drift")
    for name, entry in labels.items():
        if not isinstance(entry, dict):
            fail(f"ground-truth label {name} is malformed")
        if set(entry) != {
            "adapter_accept",
            "terminal_event",
            "condition",
            "primary_endpoint_eligible",
        }:
            fail(f"ground-truth label field drift for {name}")
        if not isinstance(entry.get("adapter_accept"), bool):
            fail(f"ground-truth adapter_accept must be boolean for {name}")
        if not isinstance(entry.get("condition"), str) or not entry["condition"]:
            fail(f"ground-truth condition is missing for {name}")
        if not isinstance(entry.get("primary_endpoint_eligible"), bool):
            fail(f"ground-truth eligibility must be boolean for {name}")

    for name in excluded:
        if labels[name]["adapter_accept"] is not False:
            fail("structural rejection control must fail adapter acceptance")
        if labels[name]["primary_endpoint_eligible"] is not False:
            fail("structural rejection control cannot enter primary denominator")
    for name in set(classes) - excluded:
        if labels[name]["adapter_accept"] is not True:
            fail("non-structural fixture must remain adapter-normalizable")
        if labels[name]["primary_endpoint_eligible"] is not True:
            fail("non-structural fixture must remain primary-endpoint eligible")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    for name in (
        "freshness_and_calibration",
        "episode_eligibility_and_exclusion",
        "repetition_and_seed_plan",
        "failure_injection_ground_truth",
    ):
        entry = predicates.get(name)
        if not isinstance(entry, dict) or entry.get("status") != "BOUND":
            fail(f"{name} predicate must be BOUND")


def validate_readiness(readiness: dict[str, Any]) -> list[str]:
    if readiness.get("record_type") != "AOSS_V0_6_STAGE_A_PREDATA_READINESS":
        fail("record_type drift")
    if readiness.get("schema_version") != 1:
        fail("schema_version drift")
    if readiness.get("controller_issue") != 810:
        fail("controller issue drift")
    if readiness.get("outcome_collection_authorized") is not False:
        fail("this readiness artifact cannot authorize outcome collection")
    if readiness.get("external_validation_established") is not False:
        fail("this readiness artifact cannot establish external validation")
    if readiness.get("scientific_n_increment") != 0:
        fail("this readiness artifact cannot increment scientific N")

    validate_apparatus_binding(readiness)
    validate_observer_measurement_boundary(readiness)
    validate_artifact_replay_receipt_contract(readiness)
    validate_freshness_sampling_ground_truth(readiness)
    unresolved = unresolved_predicates(readiness)
    expected_status = "READY_FOR_SEPARATE_AUTHORIZATION_REVIEW" if not unresolved else "NOT_READY_FAIL_CLOSED"
    if readiness.get("status") != expected_status:
        fail("top-level readiness status is inconsistent with predicate state")
    return unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assert-not-ready", action="store_true")
    parser.add_argument("--assert-ready", action="store_true")
    args = parser.parse_args()

    if args.assert_not_ready and args.assert_ready:
        fail("choose at most one readiness assertion")

    readiness = load_json(ROOT / READINESS_REL)
    unresolved = validate_readiness(readiness)

    if args.assert_ready and unresolved:
        fail("Stage A remains NOT READY: " + ",".join(unresolved))
    if args.assert_not_ready and not unresolved:
        fail("Stage A unexpectedly satisfies every pre-data predicate")

    print("AOSS_V0_6_STAGE_A_PREDATA_VALIDATION=PASS")
    print(f"READINESS_STATUS={readiness['status']}")
    print(f"UNRESOLVED_PREDICATE_COUNT={len(unresolved)}")
    for name in unresolved:
        print(f"UNRESOLVED={name}")
    print("OUTCOME_COLLECTION_AUTHORIZED=FALSE")
    print("EXTERNAL_VALIDATION_ESTABLISHED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
