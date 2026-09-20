#!/usr/bin/env python3
"""Fail-closed AOSS v0.6 Stage-A collection authorization tooling.

This module validates a creation-only bounded authorization event and the subsequent
creation-only pre-collection receipt. It never generates or inspects Stage-A outcomes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

SOURCE_BASIS = "807216df1bd5b28c677b8c42822975b2941c1211"
ACP_REPOSITORY = "ndrorchestration/agent-control-plane"
ACP_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
ACP_SCHEMA = "agent-control-plane.provenance.v1"
APPARATUS_COMMIT = "69821cdcc1b9b9432b7001c6f52c867f9669f54d"
ADAPTER_VERSION = "AOSS_V0_6_ACP_ADAPTER_V1"
POLICY_VERSION = "AOSS_V0_6_STAGE_A_POLICY_V1"
COMPARATOR_VERSION = "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"

AUTH_REL = "registry/aoss_v0_6_stage_a_collection_authorization_v1.json"
RECEIPT_REL = "registry/aoss_v0_6_stage_a_precollection_receipt_v1.json"
AUTH_SCHEMA_REL = "schemas/aoss_v0_6_stage_a_collection_authorization.schema.json"
RECEIPT_SCHEMA_REL = "schemas/aoss_v0_6_stage_a_precollection_receipt.schema.json"
READINESS_REL = "registry/aoss_v0_6_stage_a_predata_readiness_v1.json"

CONTRACT_PATHS = [
    "registry/aoss_v0_6_acp_measurement_manifest_v1.json",
    "registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json",
    "registry/aoss_v0_6_stage_a_primary_comparator_amendment_v1.json",
    "registry/aoss_v0_6_stage_a_decision_policy_v1.json",
    "registry/aoss_v0_6_stage_a_freshness_calibration_v1.json",
    "registry/aoss_v0_6_stage_a_episode_eligibility_repetition_v1.json",
    "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json",
    "registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json",
    "registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json",
]

NON_EFFECTS = [
    "DOES_NOT_ESTABLISH_EXTERNAL_VALIDATION",
    "DOES_NOT_ESTABLISH_AOSS_SUPERIORITY",
    "DOES_NOT_ESTABLISH_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_PRODUCTION_ASSURANCE",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
    "DOES_NOT_REOPEN_OR_POOL_TRACK_A_EPOCH_002",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N_BEFORE_GOVERNED_ANALYSIS_AND_DISPOSITION",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"AOSS_V0_6_STAGE_A_COLLECTION_AUTH_FAIL: {message}")


def git(*args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_object_exists(spec: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).returncode == 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load JSON from {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {path.relative_to(ROOT)}")
    return value


def load_json_at_ref(ref: str, relpath: str) -> dict[str, Any]:
    try:
        value = json.loads(git("show", f"{ref}:{relpath}"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at {ref}:{relpath}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object at {ref}:{relpath}")
    return value


def validate_schema(record: dict[str, Any], schema_rel: str) -> None:
    schema = load_json(ROOT / schema_rel)
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"{schema_rel} validation failed: {exc.message}")


def assert_frozen_predata_basis() -> None:
    readiness = load_json_at_ref(SOURCE_BASIS, READINESS_REL)
    if readiness.get("status") != "READY_FOR_SEPARATE_AUTHORIZATION_REVIEW":
        fail("source basis is not ready for separate authorization review")
    if readiness.get("outcome_collection_authorized") is not False:
        fail("pre-data readiness artifact must remain non-authorizing")
    if readiness.get("external_validation_established") is not False:
        fail("pre-data readiness artifact cannot establish external validation")
    if readiness.get("scientific_n_increment") != 0:
        fail("pre-data readiness artifact cannot increment scientific N")
    predicates = readiness.get("required_predicates")
    if not isinstance(predicates, dict) or not predicates:
        fail("pre-data readiness predicates are missing")
    unresolved = [name for name, entry in predicates.items() if entry.get("status") != "BOUND"]
    if unresolved:
        fail(f"pre-data source basis has unresolved predicates: {unresolved}")


def expected_authorization() -> dict[str, Any]:
    return {
        "record_type": "AOSS_V0_6_STAGE_A_COLLECTION_AUTHORIZATION",
        "schema_version": 1,
        "controller_issue": 890,
        "status": "AUTHORIZED_BOUNDED_STAGE_A_COLLECTION",
        "authority": {
            "class": "PROJECT_OWNER_EXPLICIT_AUTHORIZATION",
            "actor": "ndrorchestration",
            "decision": "AUTHORIZE_EXACT_FROZEN_STAGE_A_COLLECTION_ONLY",
        },
        "authorization_basis": {
            "issue": 890,
            "comment_id": 5744865345,
            "comment_url": "https://github.com/ndrorchestration/DGAF-Framework/issues/890#issuecomment-5744865345",
        },
        "protected_source_basis": SOURCE_BASIS,
        "source_system": {
            "repository": ACP_REPOSITORY,
            "commit": ACP_COMMIT,
            "provenance_schema": ACP_SCHEMA,
        },
        "apparatus": {
            "accepted_commit": APPARATUS_COMMIT,
            "adapter_version": ADAPTER_VERSION,
            "decision_policy": POLICY_VERSION,
            "primary_comparator": COMPARATOR_VERSION,
        },
        "scope": {
            "episode_classes": 16,
            "canonical_source_episodes_per_class": 1,
            "exact_byte_replay_passes_per_episode": 5,
            "frozen_eligibility_only": True,
            "frozen_failure_ground_truth_only": True,
            "frozen_analysis_only": True,
        },
        "non_effects": list(NON_EFFECTS),
        "outcome_collection_authorized": True,
        "external_validation_established": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def validate_authorization(record: dict[str, Any]) -> None:
    assert_frozen_predata_basis()
    validate_schema(record, AUTH_SCHEMA_REL)
    if record != expected_authorization():
        fail("authorization record does not match the exact bounded authorization contract")


def expected_precollection_receipt(authorization_ref: str) -> dict[str, Any]:
    authorization_ref = git("rev-parse", authorization_ref)
    authorization = load_json_at_ref(authorization_ref, AUTH_REL)
    validate_authorization(authorization)
    contract_blobs = {
        path: git("rev-parse", f"{SOURCE_BASIS}:{path}")
        for path in CONTRACT_PATHS
    }
    return {
        "record_type": "AOSS_V0_6_STAGE_A_PRECOLLECTION_RECEIPT",
        "schema_version": 1,
        "status": "PASS",
        "authorization_binding": {
            "commit_sha": authorization_ref,
            "blob_sha": git("rev-parse", f"{authorization_ref}:{AUTH_REL}"),
            "path": AUTH_REL,
        },
        "protected_source_basis": SOURCE_BASIS,
        "source_system": {
            "repository": ACP_REPOSITORY,
            "commit": ACP_COMMIT,
            "provenance_schema": ACP_SCHEMA,
        },
        "apparatus": {
            "accepted_commit": APPARATUS_COMMIT,
            "adapter_version": ADAPTER_VERSION,
            "decision_policy": POLICY_VERSION,
            "primary_comparator": COMPARATOR_VERSION,
        },
        "frozen_contract_blobs": contract_blobs,
        "predata_readiness": {
            "path": READINESS_REL,
            "blob_sha": git("rev-parse", f"{SOURCE_BASIS}:{READINESS_REL}"),
            "status": "READY_FOR_SEPARATE_AUTHORIZATION_REVIEW",
        },
        "outcomes_generated_before_receipt": False,
        "outcome_collection_authorized": True,
        "external_validation_established": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def validate_precollection_receipt(record: dict[str, Any], authorization_ref: str) -> None:
    validate_schema(record, RECEIPT_SCHEMA_REL)
    if record != expected_precollection_receipt(authorization_ref):
        fail("pre-collection receipt does not match exact frozen identities")


def creation_only_parent(head: str, path: str) -> str:
    head = git("rev-parse", head)
    lineage = git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("creation event must have exactly one parent")
    parent = lineage[1]
    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines()
        if line
    ]
    if changed != [path]:
        fail(f"creation event must change exactly {path}")
    if git_object_exists(f"{parent}:{path}"):
        fail(f"{path} must be creation-only")
    history = [line for line in git("log", "--format=%H", head, "--", path).splitlines() if line]
    if history != [head]:
        fail(f"{path} must have first-and-only history at the event commit")
    return parent


def validate_authorization_event(head: str, accepted_parent_sha: str) -> None:
    parent = creation_only_parent(head, AUTH_REL)
    if parent != git("rev-parse", accepted_parent_sha):
        fail("authorization event parent is not the accepted tooling commit")
    record = load_json_at_ref(head, AUTH_REL)
    validate_authorization(record)
    if git_object_exists(f"{head}:{RECEIPT_REL}"):
        fail("authorization event must not create the pre-collection receipt")


def validate_receipt_event(head: str, authorization_ref: str) -> None:
    parent = creation_only_parent(head, RECEIPT_REL)
    authorization_ref = git("rev-parse", authorization_ref)
    if parent != authorization_ref:
        fail("pre-collection receipt must be the direct child of the authorization event")
    record = load_json_at_ref(head, RECEIPT_REL)
    validate_precollection_receipt(record, authorization_ref)


def validate_tooling_only() -> None:
    assert_frozen_predata_basis()
    if (ROOT / AUTH_REL).exists() or git_object_exists(f"HEAD:{AUTH_REL}"):
        fail("tooling-only validation requires authorization record to be absent")
    if (ROOT / RECEIPT_REL).exists() or git_object_exists(f"HEAD:{RECEIPT_REL}"):
        fail("tooling-only validation requires pre-collection receipt to be absent")


def validate_repository_state(ref: str = "HEAD") -> None:
    ref = git("rev-parse", ref)
    has_auth = git_object_exists(f"{ref}:{AUTH_REL}")
    has_receipt = git_object_exists(f"{ref}:{RECEIPT_REL}")
    if not has_auth:
        if has_receipt:
            fail("pre-collection receipt cannot exist without authorization")
        assert_frozen_predata_basis()
        return

    auth_ref = git("log", "-1", "--format=%H", ref, "--", AUTH_REL)
    authorization = load_json_at_ref(ref, AUTH_REL)
    validate_authorization(authorization)

    if not has_receipt:
        return

    receipt_ref = git("log", "-1", "--format=%H", ref, "--", RECEIPT_REL)
    lineage = git("rev-list", "--parents", "-n", "1", receipt_ref).split()
    if len(lineage) != 2 or lineage[1] != auth_ref:
        fail("accepted pre-collection receipt is not the direct child of the authorization event")
    receipt = load_json_at_ref(ref, RECEIPT_REL)
    validate_precollection_receipt(receipt, auth_ref)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tooling-only", action="store_true")
    group.add_argument("--validate-state", action="store_true")
    group.add_argument("--print-authorization", action="store_true")
    group.add_argument("--validate-authorization-event")
    group.add_argument("--print-precollection-receipt")
    group.add_argument("--validate-precollection-event")
    parser.add_argument("--accepted-parent")
    parser.add_argument("--authorization-ref")
    args = parser.parse_args()

    if args.tooling_only:
        validate_tooling_only()
    elif args.validate_state:
        validate_repository_state()
    elif args.print_authorization:
        assert_frozen_predata_basis()
        print(json.dumps(expected_authorization(), indent=2, sort_keys=True))
    elif args.validate_authorization_event:
        if not args.accepted_parent:
            fail("--accepted-parent is required")
        validate_authorization_event(args.validate_authorization_event, args.accepted_parent)
    elif args.print_precollection_receipt:
        print(json.dumps(expected_precollection_receipt(args.print_precollection_receipt), indent=2, sort_keys=True))
    elif args.validate_precollection_event:
        if not args.authorization_ref:
            fail("--authorization-ref is required")
        validate_receipt_event(args.validate_precollection_event, args.authorization_ref)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
