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


def test_current_stage_a_state_is_ready_for_separate_authorization_review() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    unresolved = validator.validate_readiness(readiness)
    assert readiness["status"] == "READY_FOR_SEPARATE_AUTHORIZATION_REVIEW"
    assert unresolved == []
    assert readiness["required_predicates"]["comparator_policy"]["status"] == "BOUND"
    assert readiness["required_predicates"]["primary_comparator_machine_derivation"]["status"] == "BOUND"
    assert readiness["required_predicates"]["aoss_decision_policy"]["status"] == "BOUND"
    assert readiness["outcome_collection_authorized"] is False
    assert readiness["external_validation_established"] is False
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
    broken = copy.deepcopy(readiness)
    entry = broken["required_predicates"]["primary_comparator_machine_derivation"]
    entry["status"] = "BLOCKED"
    entry["missing"] = ["synthetic test blocker"]
    with pytest.raises(SystemExit, match="readiness status is inconsistent"):
        validator.validate_readiness(broken)


def test_unresolved_predicate_requires_explicit_missing_reasons() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    broken = copy.deepcopy(readiness)
    entry = broken["required_predicates"]["primary_comparator_machine_derivation"]
    entry["status"] = "BLOCKED"
    entry["missing"] = []
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


def test_timestamp_extraction_stays_separate_from_bound_freshness_contract() -> None:
    validator = load_validator()
    boundary = validator.load_json(ROOT / validator.BOUNDARY_REL)
    wall_time = boundary["extraction_functions"]["wall_time"]
    assert wall_time["tolerance"] == "EXACT_PARSE_AND_PRESERVE"
    assert wall_time["freshness_threshold"] == "SEPARATE_FROZEN_PREDICATE_CONTRACT"
    readiness = current_readiness(validator)
    assert readiness["required_predicates"]["freshness_and_calibration"]["status"] == "BOUND"


def test_freshness_contract_has_numeric_fail_closed_thresholds() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    contract = validator.load_json(ROOT / validator.FRESHNESS_REL)
    assert contract["thresholds"] == {
        "max_last_event_age_at_ingest_seconds": 30,
        "max_future_event_skew_seconds": 2,
        "non_injection_event_time_regression_seconds": 0,
    }
    assert contract["clock_domain"]["source_and_observer_same_host_required"] is True
    assert contract["calibration_semantics"]["absolute_clock_accuracy_established"] is False


def test_sampling_contract_does_not_inflate_replays_into_independent_units() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    contract = validator.load_json(ROOT / validator.ELIGIBILITY_REL)
    assert contract["repetition_plan"]["canonical_source_episodes_per_class"] == 1
    assert contract["repetition_plan"]["exact_byte_replay_passes_per_episode"] == 5
    assert contract["repetition_plan"]["replay_passes_count_as_independent_observations"] is False
    assert contract["repetition_plan"]["stochastic_sampling"] is False


def test_ground_truth_preserves_structural_controls_outside_primary_denominator() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    truth = validator.load_json(ROOT / validator.GROUND_TRUTH_REL)
    for name in ("malformed_manifest", "mismatched_run_id"):
        assert truth["labels"][name]["adapter_accept"] is False
        assert truth["labels"][name]["primary_endpoint_eligible"] is False


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
        "primary_comparator_amendment_sha256",
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


def test_analysis_contract_is_finite_corpus_without_pseudo_inference() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    validator.validate_readiness(readiness)
    analysis = validator.load_json(ROOT / validator.ANALYSIS_CONTRACT_REL)
    assert analysis["analysis_population"]["random_sample"] is False
    assert analysis["analysis_population"]["population_generalization_authorized"] is False
    assert analysis["analysis_population"]["deterministic_replays_are_independent_units"] is False
    assert analysis["primary_analysis"]["estimator"] == "EXACT_FINITE_CORPUS_FRACTION"
    assert analysis["primary_analysis"]["endpoint"] == "AOSS_DECISION_DIFFERS_FROM_ACP_DIRECT_EVENT_BASELINE"
    assert analysis["primary_comparator_amendment"]["baseline_version"] == "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"
    assert analysis["primary_analysis"]["sampling_confidence_interval"] == "NONE"
    assert analysis["primary_analysis"]["p_value"] == "NONE"
    assert analysis["confirmatory_family"]["inferential_test_count"] == 0


def test_analysis_contract_preserves_typed_uncertainty_and_no_outcome_aware_exclusion() -> None:
    validator = load_validator()
    analysis = validator.load_json(ROOT / validator.ANALYSIS_CONTRACT_REL)
    assert analysis["uncertainty_policy"]["missing_value_imputation"] == "PROHIBITED"
    assert analysis["uncertainty_policy"]["forced_scoring_of_unmeasured_state"] == "PROHIBITED"
    assert analysis["exclusion_boundary"]["outcome_aware_exclusion"] is False
    assert analysis["multiplicity_policy"]["post_hoc_subgroups"] == "EXPLORATORY_ONLY"
    assert analysis["multiplicity_policy"]["confirmatory_relabeling_of_exploratory_results"] is False


def test_portability_rule_has_no_divergence_or_effect_threshold() -> None:
    validator = load_validator()
    adoption = validator.load_json(ROOT / validator.ADOPTION_RULE_REL)
    assert adoption["decision_divergence_threshold_for_portability"] == "NONE"
    assert adoption["minimum_effect_size_for_portability"] == "NONE"
    assert adoption["zero_divergence_interpretation"] == (
        "DOES_NOT_FAIL_PORTABILITY_IF_STRUCTURAL_AND_SAFETY_CRITERIA_PASS"
    )
    assert adoption["promotion_ceiling_if_supported"] == (
        "BOUNDED_CROSS_REPOSITORY_OBSERVER_PORTABILITY_AGAINST_EXACT_ACP_COMMIT_ONLY"
    )


def test_analysis_contract_rejects_sampling_ci_in_purposive_corpus() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    analysis = validator.load_json(ROOT / validator.ANALYSIS_CONTRACT_REL)
    broken = copy.deepcopy(analysis)
    broken["primary_analysis"]["sampling_confidence_interval"] = "two_sided_95_percent"
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.ANALYSIS_CONTRACT_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="primary analysis contract drift"):
        validator.validate_readiness(readiness)


def test_adoption_rule_rejects_post_hoc_effect_threshold() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    adoption = validator.load_json(ROOT / validator.ADOPTION_RULE_REL)
    broken = copy.deepcopy(adoption)
    broken["minimum_effect_size_for_portability"] = 0.2
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.ADOPTION_RULE_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="minimum effect size"):
        validator.validate_readiness(readiness)


def test_primary_comparator_amendment_is_predata_and_machine_bound() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    assert validator.validate_readiness(readiness) == []
    amendment = validator.load_json(ROOT / validator.PRIMARY_COMPARATOR_REL)
    assert amendment["timing"]["stage_a_outcome_collection_started"] is False
    assert amendment["timing"]["stage_a_outcomes_inspected"] is False
    assert amendment["primary_comparator"]["version"] == "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"
    assert amendment["superseded_confirmatory_comparator"]["omr_semantics_inferred_or_reconstructed"] is False
    gap = validator.load_json(ROOT / validator.COMPARATOR_INPUT_GAP_REL)
    assert gap["status"] == "BLOCKED_NO_MACHINE_BOUND_DERIVATION"


def test_historical_omr_gap_cannot_be_rewritten_as_recovered() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    gap = validator.load_json(ROOT / validator.COMPARATOR_INPUT_GAP_REL)
    broken = copy.deepcopy(gap)
    broken["status"] = "BOUND"
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.COMPARATOR_INPUT_GAP_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="historical OMR gap must remain explicit"):
        validator.validate_readiness(readiness)


def test_primary_comparator_amendment_cannot_self_authorize_collection() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    amendment = validator.load_json(ROOT / validator.PRIMARY_COMPARATOR_REL)
    broken = copy.deepcopy(amendment)
    broken["outcome_collection_authorized"] = True
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.PRIMARY_COMPARATOR_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="cannot authorize outcome collection"):
        validator.validate_readiness(readiness)


def test_primary_comparator_amendment_rejects_result_conditioning() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    amendment = validator.load_json(ROOT / validator.PRIMARY_COMPARATOR_REL)
    broken = copy.deepcopy(amendment)
    broken["timing"]["stage_a_outcomes_inspected"] = True
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.PRIMARY_COMPARATOR_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="timing boundary drift"):
        validator.validate_readiness(readiness)


def test_prospective_decision_policy_is_bound_without_claiming_v05_recovery() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    unresolved = validator.validate_readiness(readiness)
    assert unresolved == []
    policy = validator.load_json(ROOT / validator.DECISION_POLICY_REL)
    assert policy["policy_version"] == "AOSS_V0_6_STAGE_A_POLICY_V1"
    assert policy["provenance"]["classification"] == "NEW_PROSPECTIVE_V0_6_POLICY_FREEZE"
    assert policy["provenance"]["historical_v0_5_executable_source_located"] is False
    assert policy["provenance"]["historical_v0_5_equivalence_claimed"] is False
    assert policy["outcome_collection_authorized"] is False


def test_decision_policy_contract_cannot_self_authorize_collection() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    policy = validator.load_json(ROOT / validator.DECISION_POLICY_REL)
    broken = copy.deepcopy(policy)
    broken["outcome_collection_authorized"] = True
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.DECISION_POLICY_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="decision policy cannot authorize outcome collection"):
        validator.validate_readiness(readiness)


def test_decision_policy_contract_rejects_historical_equivalence_promotion() -> None:
    validator = load_validator()
    readiness = current_readiness(validator)
    policy = validator.load_json(ROOT / validator.DECISION_POLICY_REL)
    broken = copy.deepcopy(policy)
    broken["provenance"]["historical_v0_5_equivalence_claimed"] = True
    original_load = validator.load_json

    def fake_load(path):
        if path == ROOT / validator.DECISION_POLICY_REL:
            return broken
        return original_load(path)

    validator.load_json = fake_load
    with pytest.raises(SystemExit, match="cannot claim historical v0.5 equivalence"):
        validator.validate_readiness(readiness)
