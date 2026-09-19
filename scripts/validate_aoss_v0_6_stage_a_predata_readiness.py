#!/usr/bin/env python3
"""Validate AOSS v0.6 Stage-A pre-data readiness without generating outcomes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
READINESS_REL = "registry/aoss_v0_6_stage_a_predata_readiness_v1.json"
MEASUREMENT_REL = "registry/aoss_v0_6_acp_measurement_manifest_v1.json"

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
