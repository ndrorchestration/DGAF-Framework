#!/usr/bin/env python3
"""Fail-closed Track A Epoch 002 locked-result admission validator.

This module validates prospective tooling, local non-secret locked-analysis output,
one-file output admission, and a later one-file result receipt. It never executes
the empirical analysis and never promotes scientific N, efficacy, independence,
or High-Assurance state.
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
AUTH_REL = (
    "docs/experiment/track_a_runs/"
    "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
)
OUTPUT_REL = (
    "docs/experiment/track_a_runs/"
    "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_OUTPUT.json"
)
RESULT_REL = (
    "docs/experiment/track_a_runs/"
    "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
)
OUTPUT_SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_OUTPUT_SCHEMA.json"
SHARED_SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
SEMANTICS_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_result_record_semantics.py"
AUTH_VALIDATOR_REL = "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"

AUTH_RECORD_ID = "E002-ANALYSIS-AUTH-0001"
RESULT_RECORD_ID = "E002-ANALYSIS-RESULT-0001"
RESULT_SCOPE = "LOCKED_PRIMARY_ANALYSIS_RESULT_BYTES"
RESULT_PRODUCER = "DGAF_TRACK_A_EPOCH_002_LOCKED_RESULT_VALIDATOR"

EXPECTED_AUTH_EVENT = "e87917e644d71de7351c5983fa7ed89d9231962f"
EXPECTED_INPUT_SHA256 = "b6bfe8e356084993f096398fd2a9ca3427fdaf15a5e55b70f764a688e407e937"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_LOCKED_RESULT_FAIL: {message}")


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


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load module {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_object_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"{label} is invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        return load_object_bytes(path.read_bytes(), label)
    except OSError as exc:
        fail(f"cannot read {label}: {exc}")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def validate_schema(record: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_object(schema_path, f"{label} schema")
    try:
        Draft202012Validator(schema).validate(record)
    except ValidationError as exc:
        fail(f"{label} schema validation failed: {exc.message}")


def validate_accepted_authorization(ref: str = "HEAD") -> str:
    history = [
        line
        for line in git("log", "--format=%H", ref, "--", AUTH_REL).splitlines()
        if line
    ]
    if history != [EXPECTED_AUTH_EVENT]:
        fail(
            "accepted primary-analysis authorization history drift: "
            f"expected {[EXPECTED_AUTH_EVENT]!r}, got {history!r}"
        )

    git("merge-base", "--is-ancestor", EXPECTED_AUTH_EVENT, ref)
    lineage = git("rev-list", "--parents", "-n", "1", EXPECTED_AUTH_EVENT).split()
    if len(lineage) != 2 or lineage[0] != EXPECTED_AUTH_EVENT:
        fail("accepted authorization event is not a one-parent commit")
    auth_parent = lineage[1]

    validator = load_module(
        ROOT / AUTH_VALIDATOR_REL,
        "track_a_epoch_002_authorization_for_locked_result",
    )
    validator.validate_authorization_event(
        EXPECTED_AUTH_EVENT,
        accepted_parent_sha=auth_parent,
    )
    return EXPECTED_AUTH_EVENT


def expected_classification(estimate: float, low: float, high: float) -> str:
    if estimate > 0 and low > 0:
        return "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    if estimate < 0 and high < 0:
        return "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    return "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"


def validate_output_object(output: dict[str, Any]) -> None:
    validate_schema(
        output,
        ROOT / OUTPUT_SCHEMA_REL,
        "locked primary-analysis output",
    )

    if output.get("authorization_event_commit_sha") != EXPECTED_AUTH_EVENT:
        fail("locked output authorization-event binding drift")
    if output.get("materialized_input_sha256") != EXPECTED_INPUT_SHA256:
        fail("locked output materialized-input binding drift")

    result = output.get("result")
    if not isinstance(result, dict):
        fail("locked output result must be an object")

    estimate = result.get("estimate_pdmal_minus_random_regular")
    interval = result.get("two_sided_95pct_percentile_ci")
    if not isinstance(estimate, (int, float)) or isinstance(estimate, bool):
        fail("locked estimate must be numeric")
    if not math.isfinite(float(estimate)):
        fail("locked estimate must be finite")
    if not isinstance(interval, list) or len(interval) != 2:
        fail("locked confidence interval must have two bounds")

    low, high = interval
    for value in (low, high):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            fail("locked confidence interval bounds must be numeric")
        if not math.isfinite(float(value)):
            fail("locked confidence interval bounds must be finite")
    if float(low) > float(high):
        fail("locked confidence interval bounds are reversed")

    expected = expected_classification(float(estimate), float(low), float(high))
    if result.get("classification") != expected:
        fail(
            "locked result classification contradicts the preregistered "
            f"decision rule: expected {expected}"
        )


def validate_output_bytes(payload: bytes) -> dict[str, Any]:
    output = load_object_bytes(payload, "locked primary-analysis output")
    validate_output_object(output)
    validate_accepted_authorization("HEAD")
    return output


def validate_output_file(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        pass
    else:
        fail("local locked-analysis output must remain outside the repository before admission")
    if resolved.is_symlink() or not resolved.is_file():
        fail("local locked-analysis output must be an external regular file")
    return validate_output_bytes(resolved.read_bytes())


def event_parent(head: str, required_path: str, *, creation_only: bool) -> tuple[str, str]:
    resolved = git("rev-parse", head)
    lineage = git("rev-list", "--parents", "-n", "1", resolved).split()
    if len(lineage) != 2 or lineage[0] != resolved:
        fail("admission event must have exactly one parent")
    parent = lineage[1]

    changed = [
        line
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            resolved,
        ).splitlines()
        if line
    ]
    if changed != [required_path]:
        fail(f"admission event must change exactly {required_path}")

    if creation_only and git_object_exists(f"{parent}:{required_path}"):
        fail(f"{required_path} must be creation-only")

    history = [
        line
        for line in git("log", "--format=%H", resolved, "--", required_path).splitlines()
        if line
    ]
    if creation_only and history != [resolved]:
        fail(f"{required_path} must have first-and-only history at the event commit")
    return resolved, parent


def validate_output_admission_event(head: str, *, accepted_parent_sha: str) -> str:
    resolved, parent = event_parent(head, OUTPUT_REL, creation_only=True)
    if parent != accepted_parent_sha:
        fail("output-admission parent is not the accepted protected-main parent")

    validate_accepted_authorization(parent)
    if git_object_exists(f"{parent}:{RESULT_REL}") or git_object_exists(f"{resolved}:{RESULT_REL}"):
        fail("locked result receipt must remain absent during output admission")
    if not git_object_exists(f"{resolved}:{OUTPUT_REL}"):
        fail("canonical locked-analysis output is absent at admission head")

    output = load_object_bytes(
        git_bytes(resolved, OUTPUT_REL),
        "canonical locked primary-analysis output",
    )
    validate_output_object(output)
    return parent


def expected_result_record(
    *,
    output_event_sha: str,
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
            "system": RESULT_PRODUCER,
            "version_or_commit": result_parent_sha,
        },
        "immutable_subject": {
            "commit_sha": output_event_sha,
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
    output_event_sha: str,
    output_sha256: str,
    result_parent_sha: str,
) -> None:
    validate_schema(
        record,
        ROOT / SHARED_SCHEMA_REL,
        "locked analysis result record",
    )
    semantics = load_module(
        ROOT / SEMANTICS_VALIDATOR_REL,
        "track_a_epoch_002_result_semantics_for_locked_result",
    )
    policy = semantics.validate_policy()
    semantics.validate_record_semantics(record, policy)

    expected = expected_result_record(
        output_event_sha=output_event_sha,
        output_sha256=output_sha256,
        result_parent_sha=result_parent_sha,
        generated_at_utc=str(record.get("generated_at_utc", "")),
    )
    if record != expected:
        fail("locked analysis result record does not match the exact non-authorizing contract")


def accepted_output_identity(ref: str) -> tuple[str, bytes]:
    history = [
        line
        for line in git("log", "--format=%H", ref, "--", OUTPUT_REL).splitlines()
        if line
    ]
    if len(history) != 1:
        fail("canonical locked-analysis output must have one immutable history event")
    output_event = history[0]
    git("merge-base", "--is-ancestor", output_event, ref)

    lineage = git("rev-list", "--parents", "-n", "1", output_event).split()
    if len(lineage) != 2 or lineage[0] != output_event:
        fail("canonical locked-analysis output event must have exactly one parent")
    output_parent = lineage[1]
    changed = [
        line
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            output_event,
        ).splitlines()
        if line
    ]
    if changed != [OUTPUT_REL]:
        fail("canonical locked-analysis output event changed more than the output path")
    if git_object_exists(f"{output_parent}:{OUTPUT_REL}"):
        fail("canonical locked-analysis output event is not creation-only")

    payload = git_bytes(ref, OUTPUT_REL)
    output = load_object_bytes(payload, "accepted locked primary-analysis output")
    validate_output_object(output)
    validate_accepted_authorization(ref)
    return output_event, payload


def validate_result_event(head: str, *, accepted_parent_sha: str) -> str:
    resolved, parent = event_parent(head, RESULT_REL, creation_only=True)
    if parent != accepted_parent_sha:
        fail("result-receipt parent is not the accepted protected-main parent")
    if not git_object_exists(f"{parent}:{OUTPUT_REL}"):
        fail("result receipt requires an accepted canonical locked-analysis output")

    output_event, parent_output = accepted_output_identity(parent)
    head_output = git_bytes(resolved, OUTPUT_REL)
    if parent_output != head_output:
        fail("canonical locked-analysis output bytes changed during result receipt")

    record = load_object_bytes(
        git_bytes(resolved, RESULT_REL),
        "locked analysis result record",
    )
    validate_result_record(
        record,
        output_event_sha=output_event,
        output_sha256=sha256_bytes(parent_output),
        result_parent_sha=parent,
    )
    return parent


def validate_tooling_only() -> None:
    validate_accepted_authorization("HEAD")
    if git_object_exists(f"HEAD:{OUTPUT_REL}") or (ROOT / OUTPUT_REL).exists():
        fail("tooling-only state requires canonical locked-analysis output to remain absent")
    if git_object_exists(f"HEAD:{RESULT_REL}") or (ROOT / RESULT_REL).exists():
        fail("tooling-only state requires locked analysis result receipt to remain absent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling", action="store_true")
    mode.add_argument("--validate-output", type=Path)
    mode.add_argument("--validate-output-event", metavar="SHA")
    mode.add_argument("--validate-result-event", metavar="SHA")
    parser.add_argument("--accepted-parent", metavar="SHA")
    args = parser.parse_args()

    if args.tooling:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_LOCKED_RESULT_TOOLING=PASS_NONEXECUTING")
        print("PRIMARY_ANALYSIS_EXECUTION=NOT_PERFORMED")
    elif args.validate_output is not None:
        validate_output_file(args.validate_output)
        print("TRACK_A_EPOCH_002_LOCKED_ANALYSIS_OUTPUT=PASS_LOCAL_VALIDATION")
    elif args.validate_output_event is not None:
        if not args.accepted_parent:
            fail("--accepted-parent is required for output-admission event validation")
        validate_output_admission_event(
            args.validate_output_event,
            accepted_parent_sha=args.accepted_parent,
        )
        print("TRACK_A_EPOCH_002_LOCKED_ANALYSIS_OUTPUT_ADMISSION=PASS")
    else:
        if not args.accepted_parent:
            fail("--accepted-parent is required for result-event validation")
        validate_result_event(
            args.validate_result_event,
            accepted_parent_sha=args.accepted_parent,
        )
        print("TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECEIPT=PASS")

    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
