#!/usr/bin/env python3
"""Validate Track A Epoch 002 result-record semantics without creating authority.

The existing JSON Schema and ledger validator remain responsible for structural
envelope/order checks. This layer binds each record type to a fail-closed semantic
profile so a structurally valid ledger cannot silently overstate authorization.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
LEDGER_VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_result_ledger.py"

EXPECTED_POLICY_EFFECT = {
    "creates_result_records": False,
    "authorizes_collection": False,
    "authorizes_unblinding": False,
    "authorizes_primary_analysis": False,
    "executes_empirical_work": False,
    "increments_scientific_n": False,
    "establishes_canonical_dgaf_efficacy": False,
    "establishes_independent_validation": False,
    "authorizes_high_assurance": False,
}
EXPECTED_AUTHORITY_CLASSES = {
    "NONAUTHORIZING_OBSERVATION",
    "NONAUTHORIZING_STATE_TRANSITION",
    "HUMAN_CONTROLLED_AUTHORIZATION",
}
EXPECTED_PROFILE_NAMES = {
    "OBSERVATIONAL_PASS",
    "DATASET_LOCK_PASS",
    "UNBLINDING_AUTHORIZATION_PASS",
    "MATERIALIZATION_PASS",
    "PRIMARY_ANALYSIS_AUTHORIZATION_PASS",
    "NON_PASS_FAIL_CLOSED",
}
EXPECTED_RECORD_CLASS = {
    "PRECOLLECTION_GATE_CHECKLIST": "NONAUTHORIZING_OBSERVATION",
    "COLLECTION_START_RECEIPT": "NONAUTHORIZING_OBSERVATION",
    "PER_SEED_EXECUTION_RECORD": "NONAUTHORIZING_OBSERVATION",
    "QC_LEDGER": "NONAUTHORIZING_OBSERVATION",
    "DATASET_LOCK_RECEIPT": "NONAUTHORIZING_STATE_TRANSITION",
    "UNBLINDING_DECISION_RECORD": "HUMAN_CONTROLLED_AUTHORIZATION",
    "MATERIALIZATION_RECEIPT": "NONAUTHORIZING_STATE_TRANSITION",
    "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD": "HUMAN_CONTROLLED_AUTHORIZATION",
    "LOCKED_ANALYSIS_RESULT_RECORD": "NONAUTHORIZING_OBSERVATION",
    "INTERPRETATION_NOTE": "NONAUTHORIZING_OBSERVATION",
}
EXPECTED_PASS_PROFILE = {
    "PRECOLLECTION_GATE_CHECKLIST": "OBSERVATIONAL_PASS",
    "COLLECTION_START_RECEIPT": "OBSERVATIONAL_PASS",
    "PER_SEED_EXECUTION_RECORD": "OBSERVATIONAL_PASS",
    "QC_LEDGER": "OBSERVATIONAL_PASS",
    "DATASET_LOCK_RECEIPT": "DATASET_LOCK_PASS",
    "UNBLINDING_DECISION_RECORD": "UNBLINDING_AUTHORIZATION_PASS",
    "MATERIALIZATION_RECEIPT": "MATERIALIZATION_PASS",
    "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD": "PRIMARY_ANALYSIS_AUTHORIZATION_PASS",
    "LOCKED_ANALYSIS_RESULT_RECORD": "OBSERVATIONAL_PASS",
    "INTERPRETATION_NOTE": "OBSERVATIONAL_PASS",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_RESULT_SEMANTICS_FAIL: {message}")


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def load_structural_validator() -> Any:
    spec = importlib.util.spec_from_file_location("epoch_002_result_ledger", LEDGER_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        fail("structural ledger validator cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def string_set(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"{label} must be a string array")
    if len(value) != len(set(value)):
        fail(f"{label} must not contain duplicates")
    return set(value)


def validate_profile(
    name: str,
    profile: dict[str, Any],
    *,
    allowed_effects: set[str],
    allowed_non_effects: set[str],
) -> None:
    effect = profile.get("authorization_effect")
    if effect not in allowed_effects:
        fail(f"profile {name} has invalid authorization_effect {effect!r}")
    required = string_set(profile.get("required_non_effects"), f"profile {name} required_non_effects")
    forbidden = string_set(profile.get("forbidden_non_effects"), f"profile {name} forbidden_non_effects")
    if not required <= allowed_non_effects or not forbidden <= allowed_non_effects:
        fail(f"profile {name} references an unknown non-effect")
    if required & forbidden:
        fail(f"profile {name} requires and forbids the same non-effect")


def validate_policy() -> dict[str, Any]:
    policy = load_object(POLICY_PATH, "semantic policy")
    schema = load_object(SCHEMA_PATH, "structural result-record schema")
    structural = load_structural_validator()

    if policy.get("record_type") != "TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS":
        fail("semantic policy record_type drift")
    if policy.get("schema_version") != 1:
        fail("semantic policy schema_version drift")
    if policy.get("protocol_id") != "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002":
        fail("semantic policy protocol drift")
    if policy.get("status") != "PROSPECTIVE_SEMANTIC_POLICY_NONAUTHORIZING":
        fail("semantic policy status drift")
    if policy.get("policy_effect") != EXPECTED_POLICY_EFFECT:
        fail("semantic policy unexpectedly changes authority or scientific state")
    if string_set(policy.get("authority_classes"), "authority_classes") != EXPECTED_AUTHORITY_CLASSES:
        fail("authority class set drift")

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        fail("structural schema properties missing")
    record_type_schema = properties.get("record_type")
    effect_schema = properties.get("authorization_effect")
    non_effects_schema = properties.get("non_effects")
    if not all(isinstance(value, dict) for value in (record_type_schema, effect_schema, non_effects_schema)):
        fail("structural schema semantic enums missing")

    structural_types = string_set(record_type_schema.get("enum"), "schema record_type enum")
    ledger_types = set(structural.ORDER)
    if structural_types != ledger_types:
        fail("structural schema and ledger order disagree on record types")

    records = policy.get("records")
    profiles = policy.get("profiles")
    if not isinstance(records, dict) or set(records) != structural_types:
        fail("semantic policy must cover every structural record type exactly once")
    if not isinstance(profiles, dict) or set(profiles) != EXPECTED_PROFILE_NAMES:
        fail("semantic profile set drift")

    allowed_effects = string_set(effect_schema.get("enum"), "schema authorization_effect enum")
    items = non_effects_schema.get("items")
    if not isinstance(items, dict):
        fail("structural schema non_effect items missing")
    allowed_non_effects = string_set(items.get("enum"), "schema non_effect enum")
    all_non_effects = string_set(policy.get("all_non_effects"), "all_non_effects")
    if all_non_effects != allowed_non_effects:
        fail("semantic policy must bind the full structural non-effect vocabulary")

    for name, value in profiles.items():
        if not isinstance(value, dict):
            fail(f"profile {name} must be an object")
        validate_profile(
            name,
            value,
            allowed_effects=allowed_effects,
            allowed_non_effects=allowed_non_effects,
        )

    full_non_effect_profiles = {
        "OBSERVATIONAL_PASS",
        "DATASET_LOCK_PASS",
        "MATERIALIZATION_PASS",
        "NON_PASS_FAIL_CLOSED",
    }
    for name in full_non_effect_profiles:
        profile = profiles[name]
        if string_set(profile["required_non_effects"], f"profile {name}") != all_non_effects:
            fail(f"profile {name} must retain the full non-authorization ceiling")
        if profile["forbidden_non_effects"] != []:
            fail(f"profile {name} must not forbid a non-effect")

    if profiles["OBSERVATIONAL_PASS"]["authorization_effect"] != "NONE":
        fail("observational PASS records cannot carry authorization")
    if profiles["NON_PASS_FAIL_CLOSED"]["authorization_effect"] != "NONE":
        fail("non-PASS records must fail closed to authorization_effect=NONE")
    for name in ("DATASET_LOCK_PASS", "MATERIALIZATION_PASS"):
        if profiles[name]["authorization_effect"] != "REQUIRES_SEPARATE_EXACT_COMMIT":
            fail(f"{name} must require a separate exact authorization commit")

    unblind = profiles["UNBLINDING_AUTHORIZATION_PASS"]
    if unblind["authorization_effect"] != "BOUNDED_RECORD_ONLY":
        fail("unblinding PASS must be bounded-record-only authority")
    if string_set(unblind["forbidden_non_effects"], "unblinding forbidden") != {
        "DOES_NOT_AUTHORIZE_UNBLINDING"
    }:
        fail("unblinding PASS contradiction guard drift")
    if string_set(unblind["required_non_effects"], "unblinding required") != all_non_effects - {
        "DOES_NOT_AUTHORIZE_UNBLINDING"
    }:
        fail("unblinding PASS authority ceiling drift")

    analysis = profiles["PRIMARY_ANALYSIS_AUTHORIZATION_PASS"]
    if analysis["authorization_effect"] != "BOUNDED_RECORD_ONLY":
        fail("primary-analysis PASS must be bounded-record-only authority")
    if string_set(analysis["forbidden_non_effects"], "analysis forbidden") != {
        "DOES_NOT_AUTHORIZE_ANALYSIS"
    }:
        fail("primary-analysis PASS contradiction guard drift")
    if string_set(analysis["required_non_effects"], "analysis required") != all_non_effects - {
        "DOES_NOT_AUTHORIZE_ANALYSIS"
    }:
        fail("primary-analysis PASS authority ceiling drift")

    for record_type, expected_class in EXPECTED_RECORD_CLASS.items():
        entry = records[record_type]
        if not isinstance(entry, dict):
            fail(f"record policy {record_type} must be an object")
        if entry.get("authority_class") != expected_class:
            fail(f"record {record_type} authority_class drift")
        if entry.get("pass_profile") != EXPECTED_PASS_PROFILE[record_type]:
            fail(f"record {record_type} pass_profile drift")

    if (
        records["DATASET_LOCK_RECEIPT"].get("requires_separate_exact_commit_for")
        != "UNBLINDING_DECISION_RECORD"
    ):
        fail("dataset lock must require separate unblinding decision commit")
    if (
        records["MATERIALIZATION_RECEIPT"].get("requires_separate_exact_commit_for")
        != "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"
    ):
        fail("materialization must require separate primary-analysis authorization commit")
    if (
        records["UNBLINDING_DECISION_RECORD"].get("bounded_scope")
        != "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY"
    ):
        fail("unblinding bounded scope drift")
    if records["PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"].get("bounded_scope") != "LOCKED_PRIMARY_ANALYSIS_ONLY":
        fail("primary-analysis bounded scope drift")
    if policy.get("non_pass_profile") != "NON_PASS_FAIL_CLOSED":
        fail("non-PASS profile drift")

    return policy


def validate_record_semantics(record: dict[str, Any], policy: dict[str, Any]) -> None:
    record_type = record.get("record_type")
    records = policy["records"]
    profiles = policy["profiles"]
    if not isinstance(record_type, str) or record_type not in records:
        fail(f"unknown record_type {record_type!r}")

    entry = records[record_type]
    profile_name = entry["pass_profile"] if record.get("status") == "PASS" else policy["non_pass_profile"]
    profile = profiles[profile_name]

    if record.get("authorization_effect") != profile["authorization_effect"]:
        fail(
            f"{record_type} status={record.get('status')} authorization_effect mismatch: "
            f"{record.get('authorization_effect')!r} != {profile['authorization_effect']!r}"
        )

    actual_non_effects = string_set(record.get("non_effects"), f"{record_type} non_effects")
    required_non_effects = string_set(profile["required_non_effects"], f"profile {profile_name} required")
    forbidden_non_effects = string_set(profile["forbidden_non_effects"], f"profile {profile_name} forbidden")
    if actual_non_effects != required_non_effects:
        fail(
            f"{record_type} status={record.get('status')} non_effects mismatch: "
            f"actual={sorted(actual_non_effects)} expected={sorted(required_non_effects)}"
        )
    if actual_non_effects & forbidden_non_effects:
        fail(f"{record_type} carries a non-effect that contradicts its bounded authority")

    expected_scientific_effect = {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    if record.get("scientific_state_effect") != expected_scientific_effect:
        fail(f"{record_type} attempts scientific-state promotion")


def validate_ledger(path: Path) -> None:
    policy = validate_policy()
    structural = load_structural_validator()
    try:
        structural.validate_ledger(path)
        records = structural.load_records(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"structural ledger validation failed: {exc}")
    for record in records:
        validate_record_semantics(record, policy)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--policy-only", action="store_true", help="validate semantic policy coherence only")
    group.add_argument("--ledger", type=Path, help="validate one structural ledger plus semantic profiles")
    args = parser.parse_args()

    if args.policy_only:
        validate_policy()
        print("TRACK_A_EPOCH_002_RESULT_SEMANTIC_POLICY=PASS_NONAUTHORIZING")
    else:
        validate_ledger(args.ledger)
        print("TRACK_A_EPOCH_002_RESULT_LEDGER=PASS_STRUCTURAL_AND_SEMANTIC")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
