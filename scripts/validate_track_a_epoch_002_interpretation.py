#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 interpretation/adjudication.

Tooling mode is prospective only. Local interpretation preparation may read the
retained locked-analysis output outside the repository, but repository admission
stores only a content address of that local interpretation artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
INTERPRETATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json"
SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
PREREG_REL = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
RESULT_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_locked_analysis_result.py"

RESULT_RECORD_ID = "E002-ANALYSIS-RESULT-0001"
INTERPRETATION_RECORD_ID = "E002-INTERPRET-0001"
INTERPRETATION_SCOPE = "INTERPRETATION_CONTENT_ADDRESS_ONLY_SAME_SYSTEM_NONINDEPENDENT"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_INTERPRETATION_VALIDATOR"
LOCAL_INTERPRETATION_TYPE = "TRACK_A_EPOCH_002_LOCAL_INTERPRETATION"
EVIDENCE_CLASS = "SAME_SYSTEM_NONINDEPENDENT"
EXACT_CLAIM_SCOPE = (
    "TRACK_A_PDMAL_VS_RANDOM_REGULAR_TOPOLOGY_ROBUSTNESS_" "UNDER_EXACT_FROZEN_REFERENCE_ALGORITHM_AND_PROTOCOL"
)
SEPARATION_CONSTRAINTS = {
    "track_a_epoch_001_pooled": False,
    "epoch_003_pooled": False,
    "epoch_004_pooled": False,
    "structural_diagnostic_seeds_pooled": False,
    "other_topology_comparisons": "EXPLORATORY_ONLY",
    "failure_count_specific_effects": "EXPLORATORY_ONLY",
    "post_hoc_subgroups": "EXPLORATORY_ONLY",
    "confirmatory_relabeling_from_exploratory_results": False,
}

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]

SCOPE_LIMITATIONS = [
    "Primary comparison is PDMAL versus random_regular under the frozen Epoch 002 protocol only.",
    "The result does not establish canonical DGAF efficacy.",
    "The result does not establish independent validation because execution and interpretation are same-system.",
    "The result does not authorize or validate High-Assurance operation.",
    "Epoch 001 must not be pooled with Epoch 002.",
    "Epoch 004 or other exploratory evidence must not substitute for this confirmatory result.",
    "No topology-general, task-general, production, causal, or external-validity claim follows automatically.",
]

COMPETING_INTERPRETATIONS = {
    "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS": [
        "The frozen primary contrast is directionally positive under the preregistered decision rule.",
        (
            "A same-system implementation, measurement, or execution artifact could still contribute "
            "to the observed contrast."
        ),
        (
            "The result may be specific to the frozen topology, failure regime, runner, or estimator "
            "rather than DGAF generally."
        ),
    ],
    "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS": [
        "The frozen primary contrast is directionally negative under the preregistered decision rule.",
        (
            "A same-system implementation, measurement, or execution artifact could still contribute "
            "to the observed contrast."
        ),
        (
            "The result may be specific to the frozen topology, failure regime, runner, or estimator "
            "rather than DGAF generally."
        ),
    ],
    "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED": [
        "The frozen primary contrast does not satisfy the preregistered directional-support rule.",
        (
            "The data may be compatible with a smaller effect, no practically useful effect, or uncertainty "
            "at the planned sample size."
        ),
        (
            "The result may be specific to the frozen topology, failure regime, runner, or estimator "
            "rather than DGAF generally."
        ),
    ],
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_INTERPRETATION_FAIL: {message}")


def load_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"{label} is invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def load_repo_json(relpath: str) -> dict[str, Any]:
    try:
        return load_json_bytes((ROOT / relpath).read_bytes(), relpath)
    except OSError as exc:
        fail(f"cannot read {relpath}: {exc}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def result_validator() -> Any:
    return load_module(ROOT / RESULT_VALIDATOR_REL, "track_a_epoch_002_result_for_interpretation")


def validate_preregistered_contract() -> dict[str, Any]:
    prereg = load_repo_json(PREREG_REL)
    if prereg.get("protocol_id") != PROTOCOL_ID:
        fail("preregistration protocol drift")

    expected_question = (
        "Under the fixed reference neighbor-mean alpha-0.5 consensus algorithm, "
        "does the PDMAL topology yield higher failure-and-recovery success than "
        "the matched random-regular topology across the preregistered failure-count panel?"
    )
    if prereg.get("research_question") != expected_question:
        fail("preregistered research question drift")
    if prereg.get("directional_hypothesis") != "PDMAL_TOPOLOGY_FFCR_GREATER_THAN_RANDOM_REGULAR":
        fail("preregistered directional hypothesis drift")

    algorithm = prereg.get("algorithm")
    endpoint = prereg.get("endpoint")
    analysis = prereg.get("primary_analysis")
    multiplicity = prereg.get("multiplicity_policy")
    historical = prereg.get("historical_evidence_policy")
    ceiling = prereg.get("claim_ceiling")
    rationale = prereg.get("sample_size_rationale")
    if not isinstance(algorithm, dict):
        fail("preregistration algorithm section is malformed")
    if not isinstance(endpoint, dict):
        fail("preregistration endpoint section is malformed")
    if not isinstance(analysis, dict):
        fail("preregistration primary-analysis section is malformed")
    if not isinstance(multiplicity, dict):
        fail("preregistration multiplicity section is malformed")
    if not isinstance(historical, dict):
        fail("preregistration historical-evidence section is malformed")
    if not isinstance(ceiling, dict):
        fail("preregistration claim-ceiling section is malformed")
    if not isinstance(rationale, dict):
        fail("preregistration sample-size rationale is malformed")

    expected_analysis = {
        "primary_comparator": "random_regular",
        "primary_topology": "pdmal",
        "estimand": "mean of 50 paired_seed_effect values",
        "bootstrap": "paired_seed_effects_percentile",
        "bootstrap_resamples": 10000,
        "bootstrap_seed": 20270251,
        "confidence_interval": "two_sided_95_percentile",
        "alpha": 0.05,
        "directional_support_rule": "estimate_gt_0_and_two_sided_95pct_ci_lower_gt_0",
        "directional_negative_rule": "estimate_lt_0_and_two_sided_95pct_ci_upper_lt_0",
        "otherwise_rule": "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
    }
    for key, expected in expected_analysis.items():
        if analysis.get(key) != expected:
            fail(f"preregistered primary-analysis contract drift: {key}")

    if algorithm.get("public_id") != "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1":
        fail("preregistered algorithm identity drift")
    if endpoint.get("field") != "ffcr_success" or endpoint.get("type") != "boolean":
        fail("preregistered endpoint drift")
    if rationale.get("paired_seed_units") != 50 or rationale.get("power_claim") != "NONE":
        fail("preregistered sample-size rationale drift")

    if multiplicity.get("confirmatory_family") != ["pdmal_vs_random_regular"]:
        fail("confirmatory family drift")
    if multiplicity.get("confirmatory_test_count") != 1:
        fail("confirmatory test-count drift")
    for key in (
        "other_topology_comparisons",
        "failure_count_specific_effects",
        "post_hoc_subgroups",
    ):
        if multiplicity.get(key) != "EXPLORATORY_ONLY":
            fail(f"exploratory-separation policy drift: {key}")
    if multiplicity.get("confirmatory_relabeling_from_exploratory_results") is not False:
        fail("confirmatory relabeling prohibition drift")

    for key in (
        "pool_experiment_001",
        "pool_epoch_003",
        "pool_epoch_004",
        "pool_structural_diagnostic_seeds",
        "pool_track_a_epoch_001",
    ):
        if historical.get(key) is not False:
            fail(f"historical pooling prohibition drift: {key}")

    if ceiling.get("allowed_if_executed") != EXACT_CLAIM_SCOPE:
        fail("exact Track A claim ceiling drift")
    expected_ceiling = {
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "integrated_track_c": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
        "production_readiness": "NOT_ESTABLISHED",
    }
    for key, expected in expected_ceiling.items():
        if ceiling.get(key) != expected:
            fail(f"claim ceiling drift: {key}")
    return prereg


def validate_schema(record: dict[str, Any]) -> None:
    schema = load_repo_json(SCHEMA_REL)
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"interpretation-note schema validation failed: {exc.message}")


def validate_semantics(record: dict[str, Any]) -> None:
    semantics = load_repo_json(SEMANTICS_REL)
    records = semantics.get("records")
    profiles = semantics.get("profiles")
    if not isinstance(records, dict) or not isinstance(profiles, dict):
        fail("result-record semantic policy is malformed")
    expected_entry = {
        "authority_class": "NONAUTHORIZING_OBSERVATION",
        "pass_profile": "OBSERVATIONAL_PASS",
    }
    if records.get("INTERPRETATION_NOTE") != expected_entry:
        fail("interpretation-note semantic classification drift")
    expected_profile = {
        "authorization_effect": "NONE",
        "required_non_effects": FULL_NON_EFFECTS,
        "forbidden_non_effects": [],
    }
    if profiles.get("OBSERVATIONAL_PASS") != expected_profile:
        fail("observational PASS profile drift")
    if record.get("authorization_effect") != "NONE":
        fail("interpretation note cannot carry authorization")
    if record.get("non_effects") != FULL_NON_EFFECTS:
        fail("interpretation note must preserve the full non-effect ceiling")


def accepted_result_binding(ref: str = "HEAD") -> tuple[str, str]:
    validator = result_validator()
    result_event = validator.validate_accepted_result(ref)
    record = load_json_bytes(
        validator.git_bytes(result_event, validator.RESULT_REL),
        "accepted locked analysis result record",
    )
    subject = record.get("immutable_subject")
    if not isinstance(subject, dict):
        fail("accepted result immutable subject is malformed")
    output_sha256 = subject.get("sha256")
    if not isinstance(output_sha256, str) or len(output_sha256) != 64:
        fail("accepted result output digest is malformed")
    return result_event, output_sha256


def interpretation_statement(classification: str) -> str:
    statements = {
        "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS": (
            "The preregistered Track A Epoch 002 primary comparison satisfies the frozen directional-support rule."
        ),
        "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS": (
            "The preregistered Track A Epoch 002 primary comparison is directionally negative under the frozen rule."
        ),
        "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED": (
            "The preregistered Track A Epoch 002 primary comparison does not satisfy the frozen "
            "directional-support rule."
        ),
    }
    if classification not in statements:
        fail("unknown result classification")
    return statements[classification]


def expected_local_interpretation(
    *,
    result_event_sha: str,
    locked_output_sha256: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    validate_preregistered_contract()
    classification = result["classification"]
    return {
        "record_type": LOCAL_INTERPRETATION_TYPE,
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "result_record_event_commit_sha": result_event_sha,
        "locked_analysis_output_sha256": locked_output_sha256,
        "evidence_class": EVIDENCE_CLASS,
        "separation_constraints": dict(SEPARATION_CONSTRAINTS),
        "confirmatory_contract": {
            "research_question": (
                "Under the fixed reference neighbor-mean alpha-0.5 consensus algorithm, "
                "does the PDMAL topology yield higher failure-and-recovery success than "
                "the matched random-regular topology across the preregistered failure-count panel?"
            ),
            "directional_hypothesis": "PDMAL_TOPOLOGY_FFCR_GREATER_THAN_RANDOM_REGULAR",
            "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
            "endpoint_field": "ffcr_success",
            "primary_topology": "pdmal",
            "primary_comparator": "random_regular",
            "paired_seed_count": 50,
            "estimand_definition": "mean of 50 paired_seed_effect values",
            "estimate_result_field": "estimate_pdmal_minus_random_regular",
            "interval_definition": "two_sided_95_percentile",
            "interval_result_field": "two_sided_95pct_percentile_ci",
            "alpha": 0.05,
            "bootstrap": "paired_seed_effects_percentile",
            "bootstrap_resamples": 10000,
            "bootstrap_seed": 20270251,
            "confirmatory_test_count": 1,
            "directional_support_rule": "estimate_gt_0_and_two_sided_95pct_ci_lower_gt_0",
            "directional_negative_rule": "estimate_lt_0_and_two_sided_95pct_ci_upper_lt_0",
            "otherwise_rule": "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
        },
        "result": {
            "estimate_pdmal_minus_random_regular": result["estimate_pdmal_minus_random_regular"],
            "two_sided_95pct_percentile_ci": result["two_sided_95pct_percentile_ci"],
            "classification": classification,
        },
        "interpretation": {
            "confirmatory_statement": interpretation_statement(classification),
            "competing_interpretations": COMPETING_INTERPRETATIONS[classification],
            "scope_limitations": SCOPE_LIMITATIONS,
            "claim_scope": EXACT_CLAIM_SCOPE,
            "exploratory_claims": [],
        },
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "integrated_track_c": "NOT_ESTABLISHED",
            "independent_validation": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED_N0",
            "production_readiness": "NOT_ESTABLISHED",
        },
    }


def validate_local_interpretation(
    artifact: dict[str, Any],
    *,
    result_event_sha: str,
    locked_output_sha256: str,
    result: dict[str, Any],
) -> None:
    expected = expected_local_interpretation(
        result_event_sha=result_event_sha,
        locked_output_sha256=locked_output_sha256,
        result=result,
    )
    if artifact != expected:
        fail("local interpretation artifact does not match the frozen interpretation contract")


def expected_repository_note(
    *,
    result_event_sha: str,
    interpretation_sha256: str,
    parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    return {
        "record_type": "INTERPRETATION_NOTE",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": INTERPRETATION_RECORD_ID,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": parent_sha,
        },
        "immutable_subject": {
            "commit_sha": result_event_sha,
            "sha256": interpretation_sha256,
        },
        "evidence_scope": INTERPRETATION_SCOPE,
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [RESULT_RECORD_ID],
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def validate_repository_note(
    record: dict[str, Any],
    *,
    result_event_sha: str,
    parent_sha: str,
) -> None:
    validate_schema(record)
    validate_semantics(record)
    subject = record.get("immutable_subject")
    if not isinstance(subject, dict):
        fail("interpretation immutable subject is malformed")
    interpretation_sha256 = subject.get("sha256")
    if not isinstance(interpretation_sha256, str):
        fail("interpretation artifact digest is absent")
    expected = expected_repository_note(
        result_event_sha=result_event_sha,
        interpretation_sha256=interpretation_sha256,
        parent_sha=parent_sha,
        generated_at_utc=str(record.get("generated_at_utc", "")),
    )
    if record != expected:
        fail("interpretation note does not match the exact admission contract")


def validate_external_interpretation_bytes(
    payload: bytes,
    *,
    result_event_sha: str,
    locked_output_sha256: str,
    result: dict[str, Any],
) -> str:
    artifact = load_json_bytes(payload, "local interpretation artifact")
    validate_local_interpretation(
        artifact,
        result_event_sha=result_event_sha,
        locked_output_sha256=locked_output_sha256,
        result=result,
    )
    return hashlib.sha256(payload).hexdigest()


def validate_tooling_only() -> None:
    validator = result_validator()
    validate_preregistered_contract()
    result_event, _ = accepted_result_binding("HEAD")
    if (ROOT / INTERPRETATION_REL).exists() or validator.git_object_exists(f"HEAD:{INTERPRETATION_REL}"):
        fail("tooling mode requires the canonical interpretation note to remain absent")
    validate_semantics(
        expected_repository_note(
            result_event_sha=result_event,
            interpretation_sha256="0" * 64,
            parent_sha=validator.git("rev-parse", "HEAD"),
            generated_at_utc="2026-01-01T00:00:00Z",
        )
    )


def validate_interpretation_event(head: str, *, accepted_parent_sha: str) -> str:
    validator = result_validator()
    head = validator.git("rev-parse", head)
    lineage = validator.git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("interpretation event must have exactly one parent")
    parent = lineage[1]
    if parent != accepted_parent_sha:
        fail("interpretation parent is not the accepted protected-main parent")

    changed = [
        line for line in validator.git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines() if line
    ]
    if changed != [INTERPRETATION_REL]:
        fail("interpretation event must create exactly the canonical interpretation note")
    if validator.git_object_exists(f"{parent}:{INTERPRETATION_REL}"):
        fail("interpretation note must be creation-only")
    history = [
        line for line in validator.git("log", "--format=%H", head, "--", INTERPRETATION_REL).splitlines() if line
    ]
    if history != [head]:
        fail("interpretation note must have first-and-only immutable history")

    result_event, _ = accepted_result_binding(parent)
    if validator.git_bytes(parent, RESULT_REL) != validator.git_bytes(head, RESULT_REL):
        fail("locked analysis result bytes changed during interpretation admission")

    record = load_json_bytes(validator.git_bytes(head, INTERPRETATION_REL), "interpretation note")
    validate_repository_note(record, result_event_sha=result_event, parent_sha=parent)
    return parent


def validate_accepted_interpretation(ref: str = "HEAD") -> str:
    validator = result_validator()
    if not validator.git_object_exists(f"{ref}:{INTERPRETATION_REL}"):
        fail("accepted-state validation requires the interpretation note")
    history = [line for line in validator.git("log", "--format=%H", ref, "--", INTERPRETATION_REL).splitlines() if line]
    if len(history) != 1:
        fail("interpretation note must have one immutable history event")
    event = history[0]
    lineage = validator.git("rev-list", "--parents", "-n", "1", event).split()
    if len(lineage) != 2 or lineage[0] != event:
        fail("accepted interpretation event must have exactly one parent")
    parent = lineage[1]
    changed = [
        line for line in validator.git("diff-tree", "--no-commit-id", "--name-only", "-r", event).splitlines() if line
    ]
    if changed != [INTERPRETATION_REL]:
        fail("accepted interpretation event changed more than its canonical note")
    if validator.git_object_exists(f"{parent}:{INTERPRETATION_REL}"):
        fail("accepted interpretation note is not creation-only")
    result_event, _ = accepted_result_binding(parent)
    if validator.git_bytes(parent, RESULT_REL) != validator.git_bytes(event, RESULT_REL):
        fail("locked analysis result bytes changed during accepted interpretation event")
    record = load_json_bytes(validator.git_bytes(event, INTERPRETATION_REL), "accepted interpretation note")
    validate_repository_note(record, result_event_sha=result_event, parent_sha=parent)
    return event


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling", action="store_true")
    mode.add_argument("--event-commit")
    mode.add_argument("--accepted-state", action="store_true")
    parser.add_argument("--accepted-parent")
    args = parser.parse_args()

    if args.tooling:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_INTERPRETATION_TOOLING=PASS_NONEXECUTING")
        print("INTERPRETATION_NOTE=ABSENT")
    elif args.accepted_state:
        validate_accepted_interpretation("HEAD")
        print("TRACK_A_EPOCH_002_INTERPRETATION_NOTE=ESTABLISHED_PRESERVED")
    else:
        if not args.accepted_parent:
            fail("--accepted-parent is required for event validation")
        validate_interpretation_event(args.event_commit, accepted_parent_sha=args.accepted_parent)
        print("TRACK_A_EPOCH_002_INTERPRETATION_EVENT=VALIDATED_PENDING_ACCEPTANCE")

    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
