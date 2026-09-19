#!/usr/bin/env python3
"""Validate AOSS v0.6 Stage-A pre-data readiness without generating outcomes."""

from __future__ import annotations

import argparse
import hashlib
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
ANALYSIS_CONTRACT_REL = "registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json"
ADOPTION_RULE_REL = "registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json"
COMPARATOR_INPUT_GAP_REL = "registry/aoss_v0_6_stage_a_comparator_input_derivation_gap_v1.json"
PRIMARY_COMPARATOR_REL = "registry/aoss_v0_6_stage_a_primary_comparator_amendment_v1.json"
PRIMARY_COMPARATOR_SOURCE_REL = "scripts/aoss_v0_6_stage_a_acp_direct_baseline.py"
DECISION_POLICY_REL = "registry/aoss_v0_6_stage_a_decision_policy_v1.json"
DECISION_POLICY_SOURCE_REL = "scripts/aoss_v0_6_stage_a_decision_policy.py"

ALLOWED_STATUSES = {"BOUND", "PARTIAL", "OPEN", "BLOCKED"}
REQUIRED_PREDICATES = {
    "external_target_identity",
    "observer_boundary_and_trust_domains",
    "telemetry_schema",
    "extraction_functions_units_tolerances",
    "freshness_and_calibration",
    "comparator_policy",
    "primary_comparator_machine_derivation",
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
EXPECTED_DECISION_POLICY = "AOSS_V0_6_STAGE_A_POLICY_V1"
EXPECTED_DECISION_POLICY_SOURCE_BLOB = "dd03a34fe17579c57dcf386abac9f1f5e7eb23de"
EXPECTED_PRIMARY_COMPARATOR = "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"
EXPECTED_PRIMARY_COMPARATOR_SOURCE_BLOB = "f1846d00084b9e0a1b1ddbd21999f1ce9627c4f5"
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
        "primary_comparator_amendment_sha256",
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


def validate_analysis_and_adoption_contracts(readiness: dict[str, Any]) -> None:
    analysis = load_json(ROOT / ANALYSIS_CONTRACT_REL)
    adoption = load_json(ROOT / ADOPTION_RULE_REL)

    if analysis.get("record_type") != "AOSS_V0_6_STAGE_A_ANALYSIS_MULTIPLICITY_CONTRACT":
        fail("analysis contract record_type drift")
    if analysis.get("schema_version") != 1 or analysis.get("controller_issue") != 810:
        fail("analysis contract identity drift")
    if analysis.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
        fail("analysis contract status drift")
    if analysis.get("outcome_collection_authorized") is not False:
        fail("analysis contract cannot authorize outcome collection")
    if analysis.get("external_validation_established") is not False:
        fail("analysis contract cannot establish external validation")
    if analysis.get("scientific_n_increment") != 0:
        fail("analysis contract cannot increment scientific N")

    population = analysis.get("analysis_population")
    if population != {
        "type": "FINITE_PREREGISTERED_PURPOSIVE_CONFORMANCE_CORPUS",
        "random_sample": False,
        "population_generalization_authorized": False,
        "unit_of_analysis": "UNIQUE_ELIGIBLE_EPISODE",
        "deterministic_replays_are_independent_units": False,
    }:
        fail("analysis population contract drift")

    if analysis.get("primary_comparator_amendment") != {
        "version": "AOSS_V0_6_STAGE_A_PRIMARY_COMPARATOR_AMENDMENT_V1",
        "contract": PRIMARY_COMPARATOR_REL,
        "baseline_version": EXPECTED_PRIMARY_COMPARATOR,
        "executable": PRIMARY_COMPARATOR_SOURCE_REL,
    }:
        fail("analysis primary comparator amendment binding drift")

    primary = analysis.get("primary_analysis")
    if not isinstance(primary, dict):
        fail("primary analysis contract is malformed")
    expected_primary = {
        "endpoint": "AOSS_DECISION_DIFFERS_FROM_ACP_DIRECT_EVENT_BASELINE",
        "estimator": "EXACT_FINITE_CORPUS_FRACTION",
        "sampling_confidence_interval": "NONE",
        "p_value": "NONE",
        "null_hypothesis_test": "NONE",
        "bootstrap": "NONE",
        "population_effect_claim": "PROHIBITED",
    }
    for key, expected in expected_primary.items():
        if primary.get(key) != expected:
            fail(f"primary analysis contract drift: {key}")
    if primary.get("numerator") != (
        "count of unique eligible episodes with AOSS decision != prospective ACP direct-event baseline decision"
    ):
        fail("primary numerator drift")
    if primary.get("denominator") != (
        "count of unique eligible episodes satisfying the separately frozen eligibility contract"
    ):
        fail("primary denominator drift")

    uncertainty = analysis.get("uncertainty_policy")
    if uncertainty != {
        "sampling_uncertainty": "NOT_MODELED_BECAUSE_CORPUS_IS_PURPOSIVE_AND_FINITE",
        "epistemic_uncertainty": "RETAIN_TYPED_UNMEASURED_INCONCLUSIVE_STALE_CONFLICTING_STATES",
        "missing_value_imputation": "PROHIBITED",
        "forced_scoring_of_unmeasured_state": "PROHIBITED",
        "denominator_must_be_explicit": True,
    }:
        fail("analysis uncertainty policy drift")

    confirmatory = analysis.get("confirmatory_family")
    if confirmatory != {
        "primary_endpoint_count": 1,
        "inferential_test_count": 0,
        "classification": "PREREGISTERED_DESCRIPTIVE_PRIMARY_ENDPOINT",
    }:
        fail("analysis confirmatory-family drift")

    multiplicity = analysis.get("multiplicity_policy")
    if multiplicity != {
        "inferential_multiplicity_adjustment": "NOT_APPLICABLE_NO_INFERENTIAL_TESTS",
        "secondary_endpoints": "DESCRIPTIVE_ONLY",
        "failure_class_specific_results": "DESCRIPTIVE_ONLY",
        "post_hoc_subgroups": "EXPLORATORY_ONLY",
        "confirmatory_relabeling_of_exploratory_results": False,
        "new_inferential_hypothesis_requires_new_preregistration": True,
    }:
        fail("analysis multiplicity policy drift")

    exclusion = analysis.get("exclusion_boundary")
    if exclusion != {
        "eligibility_source": "SEPARATELY_FROZEN_ELIGIBILITY_CONTRACT",
        "outcome_aware_exclusion": False,
        "infrastructure_or_protocol_failure": ("INVALIDATES_OR_MARKS_ATTEMPT_INCONCLUSIVE_NOT_SILENTLY_EXCLUDED"),
    }:
        fail("analysis exclusion boundary drift")

    limits = analysis.get("interpretation_limits")
    expected_limits = {
        "Decision divergence is not decision correctness.",
        "Decision divergence is not AOSS superiority.",
        "Decision divergence is not causal value of added observables.",
        "Finite-corpus fractions do not generalize to other frameworks, workloads, or populations.",
        "Deterministic replays do not increase effective sample size.",
        "The ACP direct-event baseline is a pre-data source-native comparator, not ground truth.",
    }
    if not isinstance(limits, list) or set(limits) != expected_limits:
        fail("analysis interpretation limits drift")

    if adoption.get("record_type") != "AOSS_V0_6_STAGE_A_PRACTICAL_EFFECT_ADOPTION_RULE":
        fail("adoption rule record_type drift")
    if adoption.get("schema_version") != 1 or adoption.get("controller_issue") != 810:
        fail("adoption rule identity drift")
    if adoption.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
        fail("adoption rule status drift")
    if adoption.get("decision_divergence_threshold_for_portability") != "NONE":
        fail("portability cannot depend on a decision-divergence threshold")
    if adoption.get("minimum_effect_size_for_portability") != "NONE":
        fail("portability cannot depend on a minimum effect size")
    if adoption.get("zero_divergence_interpretation") != (
        "DOES_NOT_FAIL_PORTABILITY_IF_STRUCTURAL_AND_SAFETY_CRITERIA_PASS"
    ):
        fail("zero-divergence portability interpretation drift")

    positive = adoption.get("positive_portability_classification")
    if not isinstance(positive, dict) or positive.get("label") != "BOUNDED_ACP_PORTABILITY_SUPPORTED":
        fail("positive portability classification drift")
    required = positive.get("requires_all")
    expected_required = {
        "all required Stage-A episode classes represented according to the frozen corpus contract",
        "unchanged observer consumes eligible adapter output deterministically",
        "identical manifests replay to identical reconstructed state and AOSS decision",
        "missing source observables are never fabricated or promoted to measured",
        "runtime-monitor safety violations equal zero",
        "EXECUTE with authorization not TRUE equals zero",
        "EXECUTE with validation not TRUE equals zero",
        "EXECUTE with provenance not TRUE equals zero",
        "corrupted lineage or stale telemetry never produces an unsafe stronger decision",
        "source identity is reconstructable from the retained evidence bundle",
        "whole-study replay receipt validates PASS",
    }
    if not isinstance(required, list) or set(required) != expected_required:
        fail("positive portability requirements drift")

    negative = adoption.get("negative_portability_classification")
    if negative != {
        "label": "BOUNDED_ACP_PORTABILITY_NOT_SUPPORTED",
        "trigger": "ANY_FROZEN_FALSIFICATION_OR_SAFETY_CRITERION_FAILS",
    }:
        fail("negative portability classification drift")
    inconclusive = adoption.get("inconclusive_classification")
    if inconclusive != {
        "label": "INCONCLUSIVE",
        "trigger": (
            "REQUIRED_EVIDENCE_OR_EXECUTION_IS_MISSING_OR_PROTOCOL_INVALID_WITHOUT_A_FROZEN_FAILURE_CLASSIFICATION"
        ),
    }:
        fail("inconclusive portability classification drift")
    if adoption.get("promotion_ceiling_if_supported") != (
        "BOUNDED_CROSS_REPOSITORY_OBSERVER_PORTABILITY_AGAINST_EXACT_ACP_COMMIT_ONLY"
    ):
        fail("portability promotion ceiling drift")
    expected_prohibited = {
        "AOSS superiority",
        "production-like external validation",
        "production safety or readiness",
        "universal framework compatibility",
        "causal necessity of richer observables",
        "DGAF efficacy",
        "PDMAL efficacy",
        "independent external validation",
        "High-Assurance authorization",
    }
    prohibited = adoption.get("prohibited_promotions")
    if not isinstance(prohibited, list) or set(prohibited) != expected_prohibited:
        fail("prohibited portability promotions drift")
    if adoption.get("stage_b_rule") != (
        "STAGE_B_REQUIRES_SEPARATE_PRODUCTION_LIKE_OR_THIRD_PARTY_RUNTIME_IDENTITY_AND_PREREGISTRATION"
    ):
        fail("Stage-B boundary drift")
    if adoption.get("outcome_collection_authorized") is not False:
        fail("adoption rule cannot authorize outcome collection")
    if adoption.get("external_validation_established") is not False:
        fail("adoption rule cannot establish external validation")
    if adoption.get("scientific_n_increment") != 0:
        fail("adoption rule cannot increment scientific N")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    analysis_predicate = predicates.get("analysis_and_multiplicity")
    adoption_predicate = predicates.get("practical_effect_or_adoption_rule")
    if not isinstance(analysis_predicate, dict) or analysis_predicate.get("status") != "BOUND":
        fail("analysis/multiplicity predicate must be BOUND")
    if not isinstance(adoption_predicate, dict) or adoption_predicate.get("status") != "BOUND":
        fail("practical-effect/adoption predicate must be BOUND")


def validate_decision_policy(readiness: dict[str, Any]) -> None:
    policy = load_json(ROOT / DECISION_POLICY_REL)
    if policy.get("record_type") != "AOSS_V0_6_STAGE_A_DECISION_POLICY":
        fail("decision policy record_type drift")
    if policy.get("schema_version") != 1 or policy.get("controller_issue") != 810:
        fail("decision policy identity drift")
    if policy.get("status") != "FROZEN_PREDATA_CONTRACT_NO_OUTCOMES":
        fail("decision policy status drift")
    if policy.get("policy_version") != EXPECTED_DECISION_POLICY:
        fail("decision policy version drift")

    provenance = policy.get("provenance")
    if not isinstance(provenance, dict):
        fail("decision policy provenance malformed")
    if provenance.get("classification") != "NEW_PROSPECTIVE_V0_6_POLICY_FREEZE":
        fail("decision policy provenance classification drift")
    if provenance.get("historical_v0_5_executable_source_located") is not False:
        fail("decision policy cannot claim a located historical v0.5 executable source")
    if provenance.get("historical_v0_5_equivalence_claimed") is not False:
        fail("decision policy cannot claim historical v0.5 equivalence")

    executable = policy.get("executable_binding")
    if not isinstance(executable, dict):
        fail("decision policy executable binding malformed")
    if executable.get("path") != DECISION_POLICY_SOURCE_REL:
        fail("decision policy executable path drift")
    if executable.get("git_blob_sha") != EXPECTED_DECISION_POLICY_SOURCE_BLOB:
        fail("decision policy executable blob binding drift")
    source_bytes = (ROOT / DECISION_POLICY_SOURCE_REL).read_bytes()
    source_header = f"blob {len(source_bytes)}\0".encode("utf-8")
    actual_source_blob = hashlib.sha1(source_header + source_bytes, usedforsecurity=False).hexdigest()
    if actual_source_blob != EXPECTED_DECISION_POLICY_SOURCE_BLOB:
        fail("decision policy executable source bytes drift")
    if executable.get("entrypoint") != "evaluate_policy":
        fail("decision policy entrypoint drift")
    if executable.get("input_type") != "PolicyInput" or executable.get("result_type") != "PolicyResult":
        fail("decision policy executable type binding drift")

    expected_rules = [
        (1, "terminal == true", "RECORD_OUTCOME", "TERMINAL"),
        (2, "blocked == true", "ESCALATE_BLOCK", "BLOCKED"),
        (3, "deadlock_candidate == true", "PERTURB", "DEADLOCK_CANDIDATE"),
        (4, "conflicted == true", "ESCALATE_CONFLICT", "CONFLICTED"),
        (5, "uncertain == true", "REQUEST_EVIDENCE", "UNCERTAIN"),
        (
            6,
            "authorization == TRUE and validation == TRUE and provenance_valid == TRUE "
            "and no required predicate is INCONCLUSIVE",
            "EXECUTE",
            "AUTHORIZED_AND_VALIDATED_AND_PROVENANCE_VALID",
        ),
        (
            7,
            "validation == TRUE and authorization == FALSE",
            "REQUEST_AUTHORIZATION",
            "VALIDATED_AND_NOT_AUTHORIZED",
        ),
        (
            8,
            "required_predicate_inconclusive == true or authorization/validation/provenance_valid "
            "contains INCONCLUSIVE",
            "HOLD",
            "REQUIRED_PREDICATE_INCONCLUSIVE",
        ),
        (9, "otherwise", "HOLD", "DEFAULT_FAIL_CLOSED"),
    ]
    rules = policy.get("ordered_rules")
    if not isinstance(rules, list) or len(rules) != len(expected_rules):
        fail("decision policy ordered rule set drift")
    actual_rules = [
        (entry.get("priority"), entry.get("when"), entry.get("decision"), entry.get("rule_id"))
        for entry in rules
        if isinstance(entry, dict)
    ]
    if actual_rules != expected_rules:
        fail("decision policy ordered rule semantics drift")

    execution = policy.get("execution_boundary")
    expected_execution = {
        "execution_bearing_decision": "EXECUTE",
        "non_execute_outputs_are_control_or_advisory": True,
        "execute_requires_authorization_true": True,
        "execute_requires_validation_true": True,
        "execute_requires_provenance_true": True,
        "execute_forbidden_when_required_predicate_inconclusive": True,
    }
    if execution != expected_execution:
        fail("decision policy execution boundary drift")

    scope = policy.get("stage_a_scope")
    if not isinstance(scope, dict):
        fail("decision policy Stage-A scope malformed")
    if scope.get("external_target_repository") != "ndrorchestration/agent-control-plane":
        fail("decision policy target repository drift")
    if scope.get("external_target_commit") != EXPECTED_SOURCE_COMMIT:
        fail("decision policy target commit drift")
    if scope.get("observer_version") != EXPECTED_ADAPTER:
        fail("decision policy observer binding drift")
    if scope.get("policy_is_not_dgaf_authorization_mapping") is not True:
        fail("decision policy must remain outside DGAF authorization mapping")
    if scope.get("policy_is_not_production_authority") is not True:
        fail("decision policy must remain non-production authority")

    if policy.get("outcome_collection_authorized") is not False:
        fail("decision policy cannot authorize outcome collection")
    if policy.get("external_validation_established") is not False:
        fail("decision policy cannot establish external validation")
    if policy.get("scientific_n_increment") != 0:
        fail("decision policy cannot increment scientific N")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    entry = predicates.get("aoss_decision_policy")
    if not isinstance(entry, dict) or entry.get("status") != "BOUND":
        fail("AOSS decision policy predicate must be BOUND")


def validate_primary_comparator_amendment(readiness: dict[str, Any]) -> None:
    gap = load_json(ROOT / COMPARATOR_INPUT_GAP_REL)
    amendment = load_json(ROOT / PRIMARY_COMPARATOR_REL)

    if gap.get("record_type") != "AOSS_V0_6_STAGE_A_COMPARATOR_INPUT_DERIVATION_GAP":
        fail("historical comparator gap record_type drift")
    if gap.get("status") != "BLOCKED_NO_MACHINE_BOUND_DERIVATION":
        fail("historical OMR gap must remain explicit rather than being rewritten as recovered")
    if gap.get("not_established") != {
        "authoritative_semantic_definition_for_each_coarse_dimension": True,
        "machine_bound_acp_to_omr_extraction": True,
        "unit_and_tolerance_contract_for_each_coarse_dimension": True,
    }:
        fail("historical OMR missing-state evidence drift")
    prohibited = gap.get("prohibited")
    if not isinstance(prohibited, dict) or not all(
        prohibited.get(k) is True
        for k in (
            "infer_omr_dimensions_from_names",
            "reconstruct_mapping_from_outcomes",
            "treat_historical_reference_projection_as_derivation",
            "collect_stage_a_outcomes_before_resolution",
        )
    ):
        fail("historical OMR gap prohibition drift")

    if amendment.get("record_type") != "AOSS_V0_6_STAGE_A_PRIMARY_COMPARATOR_AMENDMENT":
        fail("primary comparator amendment record_type drift")
    if amendment.get("schema_version") != 1 or amendment.get("controller_issue") != 810:
        fail("primary comparator amendment identity drift")
    if amendment.get("status") != "FROZEN_PREDATA_PROTOCOL_AMENDMENT_NO_OUTCOMES":
        fail("primary comparator amendment status drift")
    if amendment.get("amendment_version") != "AOSS_V0_6_STAGE_A_PRIMARY_COMPARATOR_AMENDMENT_V1":
        fail("primary comparator amendment version drift")

    timing = amendment.get("timing")
    if timing != {
        "stage_a_outcome_collection_started": False,
        "stage_a_outcomes_inspected": False,
        "existing_apparatus_fixtures_available_before_amendment": True,
        "amendment_is_predata": True,
    }:
        fail("primary comparator amendment timing boundary drift")

    superseded = amendment.get("superseded_confirmatory_comparator")
    if not isinstance(superseded, dict):
        fail("superseded comparator record malformed")
    if superseded.get("version") != EXPECTED_COMPARATOR["version"]:
        fail("superseded historical comparator identity drift")
    if superseded.get("status") != "NOT_MACHINE_USABLE_FOR_STAGE_A":
        fail("historical OMR comparator usability classification drift")
    if superseded.get("historical_gap_record") != COMPARATOR_INPUT_GAP_REL:
        fail("historical OMR gap binding drift")
    if superseded.get("historical_reference_projection_is_not_derivation") is not True:
        fail("historical reference projection must not become a derivation")
    if superseded.get("omr_semantics_inferred_or_reconstructed") is not False:
        fail("OMR semantics must not be inferred or reconstructed")

    primary = amendment.get("primary_comparator")
    if not isinstance(primary, dict):
        fail("primary comparator contract malformed")
    if primary.get("version") != EXPECTED_PRIMARY_COMPARATOR:
        fail("primary comparator version drift")
    if primary.get("classification") != "PROSPECTIVE_MACHINE_DERIVABLE_SOURCE_EVENT_BASELINE":
        fail("primary comparator classification drift")

    executable = primary.get("executable_binding")
    if not isinstance(executable, dict):
        fail("primary comparator executable binding malformed")
    if executable.get("path") != PRIMARY_COMPARATOR_SOURCE_REL:
        fail("primary comparator executable path drift")
    if executable.get("git_blob_sha") != EXPECTED_PRIMARY_COMPARATOR_SOURCE_BLOB:
        fail("primary comparator executable blob binding drift")
    if executable.get("entrypoint") != "evaluate_baseline":
        fail("primary comparator entrypoint drift")
    source_bytes = (ROOT / PRIMARY_COMPARATOR_SOURCE_REL).read_bytes()
    source_header = f"blob {len(source_bytes)}\0".encode("utf-8")
    actual_source_blob = hashlib.sha1(source_header + source_bytes, usedforsecurity=False).hexdigest()
    if actual_source_blob != EXPECTED_PRIMARY_COMPARATOR_SOURCE_BLOB:
        fail("primary comparator executable source bytes drift")

    if primary.get("source_identity") != {
        "repository": "ndrorchestration/agent-control-plane",
        "commit": EXPECTED_SOURCE_COMMIT,
        "provenance_schema": EXPECTED_SCHEMA,
    }:
        fail("primary comparator source identity drift")
    if set(primary.get("source_fields_used", [])) != {
        "manifest.schema",
        "manifest.run_id",
        "manifest.event_count",
        "events[].run_id",
        "events[].event",
    }:
        fail("primary comparator source-field set drift")
    ignored = set(primary.get("explicitly_ignored_for_baseline", []))
    if "historical O/M/R variables" not in ignored:
        fail("primary comparator must explicitly exclude historical OMR variables")
    if "AOSS authorization state" not in ignored or "AOSS provenance-valid state" not in ignored:
        fail("primary comparator must remain independent of richer AOSS governance state")

    if primary.get("units_and_tolerances") != {
        "schema": "exact string identity; zero tolerance",
        "run_id": "exact opaque identifier equality; zero tolerance",
        "event_count": "exact integer equality to events[] length; zero tolerance",
        "event_kind": "exact categorical string membership; zero tolerance",
        "terminal_event_cardinality": "exact integer count; zero tolerance",
    }:
        fail("primary comparator unit/tolerance contract drift")

    expected_rules = [
        (1, "structural manifest identity invalid", "HOLD", False),
        (2, "no recognized terminal event", "HOLD", True),
        (3, "more than one recognized terminal event", "HOLD", True),
        (4, "exactly one terminal event == task.completed", "RECORD_OUTCOME", True),
        (
            5,
            "exactly one terminal event in {task.denied, task.rejected, task.failed, "
            "task.cancelled, task.budget_exhausted}",
            "ESCALATE_BLOCK",
            True,
        ),
    ]
    rules = primary.get("decision_rules")
    if not isinstance(rules, list):
        fail("primary comparator decision rules malformed")
    actual_rules = [
        (entry.get("priority"), entry.get("when"), entry.get("decision"), entry.get("input_valid"))
        for entry in rules
        if isinstance(entry, dict)
    ]
    if actual_rules != expected_rules:
        fail("primary comparator decision-rule drift")
    if primary.get("fail_closed_default") != "HOLD":
        fail("primary comparator fail-closed default drift")

    endpoint = amendment.get("primary_endpoint_amendment")
    if endpoint != {
        "previous_endpoint": "AOSS_DECISION_DIFFERS_FROM_FROZEN_OMR",
        "replacement_endpoint": "AOSS_DECISION_DIFFERS_FROM_ACP_DIRECT_EVENT_BASELINE",
        "estimator": "EXACT_FINITE_CORPUS_FRACTION",
        "comparison": "exact AOSS policy action string != exact ACP direct-event baseline action string",
        "interpretation": "DESCRIPTIVE_DECISION_DIVERGENCE_NOT_CORRECTNESS_OR_SUPERIORITY",
    }:
        fail("primary endpoint amendment drift")

    integrity = amendment.get("integrity_boundary")
    if not isinstance(integrity, list):
        fail("primary comparator amendment integrity boundary malformed")
    if "Injected ground-truth condition labels are not inputs to the baseline." not in integrity:
        fail("primary comparator cannot use injected ground-truth labels")
    if "A null divergence result remains admissible evidence." not in integrity:
        fail("primary comparator amendment must preserve null-result admissibility")

    if amendment.get("authorization_effect") != "NONE":
        fail("primary comparator amendment cannot create authorization")
    if amendment.get("outcome_collection_authorized") is not False:
        fail("primary comparator amendment cannot authorize outcome collection")
    if amendment.get("external_validation_established") is not False:
        fail("primary comparator amendment cannot establish external validation")
    if amendment.get("scientific_n_increment") != 0:
        fail("primary comparator amendment cannot increment scientific N")

    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict):
        fail("required_predicates must be an object")
    comparator_policy = predicates.get("comparator_policy")
    machine_derivation = predicates.get("primary_comparator_machine_derivation")
    if not isinstance(comparator_policy, dict) or comparator_policy.get("status") != "BOUND":
        fail("primary comparator policy predicate must be BOUND")
    if not isinstance(machine_derivation, dict) or machine_derivation.get("status") != "BOUND":
        fail("primary comparator machine derivation predicate must be BOUND")


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
    validate_analysis_and_adoption_contracts(readiness)
    validate_decision_policy(readiness)
    validate_primary_comparator_amendment(readiness)
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
