#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 locked-analysis result admission.

Tooling mode is prospective only. Event mode validates a one-file, creation-only
LOCKED_ANALYSIS_RESULT_RECORD that content-addresses the retained local analysis
output without importing numerical outcomes into the repository record.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
AUTH_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
RESULT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"
SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SEMANTICS.json"
AUTH_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"

AUTH_RECORD_ID = "E002-ANALYSIS-AUTH-0001"
RESULT_RECORD_ID = "E002-ANALYSIS-RESULT-0001"
RESULT_SCOPE = "LOCKED_PRIMARY_ANALYSIS_OUTPUT_CONTENT_ADDRESS_ONLY"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_VALIDATOR"
ANALYSIS_BLOB_SHA = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
ANALYSIS_CONFIG_SHA256 = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
EXPECTED_MATERIALIZED_INPUT_SHA256 = "b6bfe8e356084993f096398fd2a9ca3427fdaf15a5e55b70f764a688e407e937"
EXPECTED_PYTHON = "3.12.0"
EXPECTED_NUMPY = "2.5.1"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
CLASSIFICATIONS = {
    "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
    "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS",
    "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_RESULT_ADMISSION_FAIL: {message}")


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        fail(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_bytes(ref: str, relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{relpath}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"cannot read {ref}:{relpath}: {detail}")
    return completed.stdout


def git_object_exists(spec: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


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


def outside_repository(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return True
    return False


def require_external_regular_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not outside_repository(resolved):
        fail(f"{label} must remain outside the repository")
    if resolved.is_symlink() or not resolved.is_file():
        fail(f"{label} must be an external regular file")
    return resolved


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_schema(record: dict[str, Any]) -> None:
    schema = load_repo_json(SCHEMA_REL)
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"result record schema validation failed: {exc.message}")


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
    if records.get("LOCKED_ANALYSIS_RESULT_RECORD") != expected_entry:
        fail("locked-result semantic classification drift")
    expected_profile = {
        "authorization_effect": "NONE",
        "required_non_effects": FULL_NON_EFFECTS,
        "forbidden_non_effects": [],
    }
    if profiles.get("OBSERVATIONAL_PASS") != expected_profile:
        fail("observational PASS profile drift")
    if record.get("authorization_effect") != "NONE":
        fail("locked analysis result cannot carry authorization")
    if record.get("non_effects") != FULL_NON_EFFECTS:
        fail("locked analysis result must preserve the full non-effect ceiling")


def validate_authorization_history(ref: str = "HEAD") -> tuple[str, dict[str, Any]]:
    if not git_object_exists(f"{ref}:{AUTH_REL}"):
        fail("accepted primary-analysis authorization record is absent")
    history = [line for line in git("log", "--format=%H", ref, "--", AUTH_REL).splitlines() if line]
    if len(history) != 1:
        fail("primary-analysis authorization must have one immutable history event")
    event = history[0]
    lineage = git("rev-list", "--parents", "-n", "1", event).split()
    if len(lineage) != 2 or lineage[0] != event:
        fail("primary-analysis authorization event must have exactly one parent")
    parent = lineage[1]
    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", event).splitlines()
        if line
    ]
    if changed != [AUTH_REL]:
        fail("primary-analysis authorization event changed more than its canonical record")
    if git_object_exists(f"{parent}:{AUTH_REL}"):
        fail("primary-analysis authorization is not creation-only")

    auth_validator = load_module(
        ROOT / AUTH_VALIDATOR_REL,
        "track_a_epoch_002_auth_for_result_admission",
    )
    auth_validator.validate_authorization_event(event, accepted_parent_sha=parent)
    authorization = load_json_bytes(git_bytes(event, AUTH_REL), "primary-analysis authorization")
    return event, authorization


def expected_classification(estimate: float, low: float, high: float) -> str:
    if estimate > 0 and low > 0:
        return "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    if estimate < 0 and high < 0:
        return "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    return "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"


def validate_local_output_object(output: dict[str, Any], *, authorization_event_sha: str) -> None:
    expected_top_keys = {
        "record_type",
        "schema_version",
        "protocol_id",
        "authorization_event_commit_sha",
        "authorization_record_id",
        "materialized_input_sha256",
        "analysis_blob_sha",
        "analysis_config_sha256",
        "environment",
        "result",
        "scientific_n_increment",
        "canonical_dgaf_efficacy",
        "independent_validation",
        "high_assurance",
    }
    if set(output) != expected_top_keys:
        fail("local locked-analysis output field set drift")

    fixed = {
        "record_type": "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS_OUTPUT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "authorization_event_commit_sha": authorization_event_sha,
        "authorization_record_id": AUTH_RECORD_ID,
        "materialized_input_sha256": EXPECTED_MATERIALIZED_INPUT_SHA256,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }
    for key, expected in fixed.items():
        if output.get(key) != expected:
            fail(f"local locked-analysis output binding drift: {key}")

    if output.get("environment") != {"python": EXPECTED_PYTHON, "numpy": EXPECTED_NUMPY}:
        fail("local locked-analysis runtime identity drift")

    result = output.get("result")
    if not isinstance(result, dict):
        fail("locked primary result is malformed")
    expected_result_keys = {
        "protocol_id",
        "algorithm_id",
        "primary_topology",
        "primary_comparator",
        "paired_seed_count",
        "estimate_pdmal_minus_random_regular",
        "two_sided_95pct_percentile_ci",
        "classification",
        "bootstrap_resamples",
        "bootstrap_seed",
        "alpha",
        "canonical_dgaf_efficacy",
        "high_assurance",
    }
    if set(result) != expected_result_keys:
        fail("locked primary result field set drift")

    expected_result_fixed = {
        "protocol_id": PROTOCOL_ID,
        "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
        "primary_topology": "pdmal",
        "primary_comparator": "random_regular",
        "paired_seed_count": 50,
        "bootstrap_resamples": 10000,
        "bootstrap_seed": 20270251,
        "alpha": 0.05,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }
    for key, expected in expected_result_fixed.items():
        if result.get(key) != expected:
            fail(f"locked primary result contract drift: {key}")

    estimate = result.get("estimate_pdmal_minus_random_regular")
    ci = result.get("two_sided_95pct_percentile_ci")
    classification = result.get("classification")
    if not isinstance(estimate, (int, float)) or isinstance(estimate, bool) or not math.isfinite(float(estimate)):
        fail("locked primary estimate must be finite")
    if not isinstance(ci, list) or len(ci) != 2:
        fail("locked primary confidence interval is malformed")
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(float(x)) for x in ci):
        fail("locked primary confidence interval must be finite")
    estimate_f = float(estimate)
    low, high = float(ci[0]), float(ci[1])
    if not (-1.0 <= estimate_f <= 1.0 and -1.0 <= low <= high <= 1.0):
        fail("locked primary estimate or interval is outside the FFCR contrast range")
    if classification not in CLASSIFICATIONS:
        fail("locked primary classification is unknown")
    if classification != expected_classification(estimate_f, low, high):
        fail("locked primary classification is inconsistent with estimate and interval")


def validate_local_output_bytes(payload: bytes, *, authorization_event_sha: str) -> str:
    output = load_json_bytes(payload, "local locked-analysis output")
    validate_local_output_object(output, authorization_event_sha=authorization_event_sha)
    return hashlib.sha256(payload).hexdigest()


def expected_result_record(
    *,
    authorization_event_sha: str,
    output_sha256: str,
    result_parent_sha: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    return {
        "record_type": "LOCKED_ANALYSIS_RESULT_RECORD",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": RESULT_RECORD_ID,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": result_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": authorization_event_sha,
            "sha256": output_sha256,
        },
        "evidence_scope": RESULT_SCOPE,
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [AUTH_RECORD_ID],
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def validate_result_record(
    record: dict[str, Any],
    *,
    authorization_event_sha: str,
    result_parent_sha: str,
) -> None:
    validate_schema(record)
    validate_semantics(record)
    subject = record.get("immutable_subject")
    if not isinstance(subject, dict):
        fail("locked analysis result immutable subject is malformed")
    output_sha256 = subject.get("sha256")
    if not isinstance(output_sha256, str):
        fail("locked analysis result output digest is absent")
    expected = expected_result_record(
        authorization_event_sha=authorization_event_sha,
        output_sha256=output_sha256,
        result_parent_sha=result_parent_sha,
        generated_at_utc=str(record.get("generated_at_utc", "")),
    )
    if record != expected:
        fail("locked analysis result record does not match the exact admission contract")


def validate_tooling_only() -> None:
    validate_semantics(
        expected_result_record(
            authorization_event_sha="0" * 40,
            output_sha256="0" * 64,
            result_parent_sha="0" * 40,
            generated_at_utc="2026-01-01T00:00:00Z",
        )
    )
    if (ROOT / RESULT_REL).exists() or git_object_exists(f"HEAD:{RESULT_REL}"):
        fail("tooling mode requires the canonical locked analysis result record to remain absent")


def validate_result_event(head: str, *, accepted_parent_sha: str) -> str:
    head = git("rev-parse", head)
    lineage = git("rev-list", "--parents", "-n", "1", head).split()
    if len(lineage) != 2 or lineage[0] != head:
        fail("locked analysis result event must have exactly one parent")
    parent = lineage[1]
    if parent != accepted_parent_sha:
        fail("locked analysis result parent is not the accepted protected-main parent")

    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", head).splitlines()
        if line
    ]
    if changed != [RESULT_REL]:
        fail("locked analysis result event must create exactly the canonical result record")
    if git_object_exists(f"{parent}:{RESULT_REL}"):
        fail("locked analysis result record must be creation-only")
    history = [line for line in git("log", "--format=%H", head, "--", RESULT_REL).splitlines() if line]
    if history != [head]:
        fail("locked analysis result record must have first-and-only immutable history")

    authorization_event, _ = validate_authorization_history(parent)
    if git_bytes(parent, AUTH_REL) != git_bytes(head, AUTH_REL):
        fail("primary-analysis authorization bytes changed during result admission")

    record = load_json_bytes(git_bytes(head, RESULT_REL), "locked analysis result record")
    validate_result_record(
        record,
        authorization_event_sha=authorization_event,
        result_parent_sha=parent,
    )
    return parent


def validate_accepted_result(ref: str = "HEAD") -> str:
    if not git_object_exists(f"{ref}:{RESULT_REL}"):
        fail("accepted-state validation requires the locked analysis result record")
    history = [line for line in git("log", "--format=%H", ref, "--", RESULT_REL).splitlines() if line]
    if len(history) != 1:
        fail("locked analysis result must have one immutable history event")
    event = history[0]
    lineage = git("rev-list", "--parents", "-n", "1", event).split()
    if len(lineage) != 2 or lineage[0] != event:
        fail("accepted locked analysis result event must have exactly one parent")
    parent = lineage[1]
    changed = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", event).splitlines()
        if line
    ]
    if changed != [RESULT_REL]:
        fail("accepted locked analysis result event changed more than its canonical record")
    if git_object_exists(f"{parent}:{RESULT_REL}"):
        fail("accepted locked analysis result is not creation-only")
    authorization_event, _ = validate_authorization_history(parent)
    if git_bytes(parent, AUTH_REL) != git_bytes(event, AUTH_REL):
        fail("primary-analysis authorization bytes changed during accepted result event")
    record = load_json_bytes(git_bytes(event, RESULT_REL), "accepted locked analysis result record")
    validate_result_record(
        record,
        authorization_event_sha=authorization_event,
        result_parent_sha=parent,
    )
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
        print("TRACK_A_EPOCH_002_RESULT_ADMISSION_TOOLING=PASS_NONEXECUTING")
        print("LOCKED_ANALYSIS_RESULT_RECORD=ABSENT")
    elif args.accepted_state:
        validate_accepted_result("HEAD")
        print("TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT=ESTABLISHED_PRESERVED")
    else:
        if not args.accepted_parent:
            fail("--accepted-parent is required for event validation")
        validate_result_event(args.event_commit, accepted_parent_sha=args.accepted_parent)
        print("TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_EVENT=VALIDATED_PENDING_ACCEPTANCE")

    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
