"""Prospective non-fixture execution identity candidate for AOSS Stage A.

This module represents exact executable, destination, and attempt identities for
external review. It does not accept them and cannot enable collection.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, NoReturn, Sequence

EXPECTED_CONTROLLER_ISSUE = 901
EXPECTED_SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
EXPECTED_SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
EXPECTED_SOURCE_MODULE = "src/agent_control_plane/core.py"
EXPECTED_SOURCE_MODULE_BLOB = "1341df7296a426b336b76ac6b1e4df67611ec931"
EXPECTED_RECIPE_CATALOG = "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
EXPECTED_SOURCE_DRIVER_PATH = "scripts/aoss_stage_a/source_driver.py"
RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXECUTION_IDENTITY_CANDIDATE"
STATUS = "PROSPECTIVE_NON_FIXTURE_CANDIDATE_NOT_ACCEPTED"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_EXPECTED_DRIVER_FLAGS = ("--acp-root", "--recipe-class", "--run-id", "--output")
_EXPECTED_RECIPE_CLASSES = {
    "normal_completion",
    "policy_denial",
    "unknown_capability_rejection",
    "handler_failure",
    "cancellation",
    "exact_budget_success",
    "budget_exhaustion",
    "suppressed_budget_exception_fail_closed",
    "missing_event",
    "reordered_exported_events",
    "duplicate_replayed_event",
    "stale_timestamp",
    "malformed_manifest",
    "mismatched_run_id",
    "source_order_ambiguity",
    "missing_authority_evidence",
}


class ExecutionIdentityCandidateError(ValueError):
    """Raised when a prospective identity candidate fails closed."""


def _fail(code: str) -> NoReturn:
    raise ExecutionIdentityCandidateError(code)


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            dict(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("utf-8")


def record_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _nonempty(value: str, code: str) -> str:
    stripped = value.strip()
    if not stripped:
        _fail(code)
    return stripped


def _validate_sha256(value: str, code: str) -> str:
    if _SHA256_RE.fullmatch(value) is None:
        _fail(code)
    return value


def _validate_driver_argv(
    argv: Sequence[str],
    driver_path: str,
    working_directory: str,
    driver_file: Path,
) -> list[str]:
    if not argv or any(not isinstance(item, str) or not item for item in argv):
        _fail("EXECUTION_IDENTITY_ARGV_INVALID")
    values = list(argv)
    if values[0] != driver_path:
        _fail("EXECUTION_IDENTITY_ARGV_DRIVER_MISMATCH")
    if len(values) != 9 or tuple(values[1::2]) != _EXPECTED_DRIVER_FLAGS:
        _fail("EXECUTION_IDENTITY_ARGV_SHAPE_MISMATCH")
    option_values = dict(zip(values[1::2], values[2::2], strict=True))
    if any(not value.strip() for value in option_values.values()):
        _fail("EXECUTION_IDENTITY_ARGV_INVALID")
    if option_values["--recipe-class"] not in _EXPECTED_RECIPE_CLASSES:
        _fail("EXECUTION_IDENTITY_ARGV_RECIPE_NOT_FROZEN")
    workdir = Path(working_directory)
    if not workdir.is_dir():
        _fail("EXECUTION_IDENTITY_WORKDIR_NOT_DIRECTORY")
    if (workdir / values[0]).resolve() != Path(driver_file).resolve():
        _fail("EXECUTION_IDENTITY_ARGV_DRIVER_RESOLUTION_MISMATCH")
    return values


def _reject_fixture_uri(uri: str) -> None:
    lowered = uri.lower()
    if lowered.startswith("fixture://") or "synthetic-fixture" in lowered:
        _fail("EXECUTION_IDENTITY_DESTINATION_FIXTURE_FORBIDDEN")


def _reject_fixture_attempt(attempt_id: str) -> None:
    lowered = attempt_id.lower()
    if "fixture" in lowered or "synthetic" in lowered:
        _fail("EXECUTION_IDENTITY_ATTEMPT_FIXTURE_FORBIDDEN")


def prepare_execution_identity_candidate(
    *,
    interpreter_path: str,
    interpreter_sha256: str,
    argv: Sequence[str],
    working_directory: str,
    destination_uri: str,
    attempt_id: str,
    recipe_catalog_sha256: str,
    environment_candidate_record_sha256: str,
    source_driver_path: str = EXPECTED_SOURCE_DRIVER_PATH,
    source_driver_file: Path | None = None,
    recipe_catalog_file: Path | None = None,
) -> dict[str, object]:
    """Prepare a review candidate without accepting any identity."""

    interpreter = _nonempty(interpreter_path, "EXECUTION_IDENTITY_INTERPRETER_PATH_MISSING")
    interpreter_digest = _validate_sha256(
        interpreter_sha256,
        "EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID",
    )
    workdir = _nonempty(working_directory, "EXECUTION_IDENTITY_WORKDIR_MISSING")
    destination = _nonempty(destination_uri, "EXECUTION_IDENTITY_DESTINATION_MISSING")
    attempt = _nonempty(attempt_id, "EXECUTION_IDENTITY_ATTEMPT_MISSING")
    recipe_digest = _validate_sha256(
        recipe_catalog_sha256,
        "EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_INVALID",
    )
    catalog_file = (
        Path(recipe_catalog_file)
        if recipe_catalog_file is not None
        else Path(__file__).resolve().parents[2] / EXPECTED_RECIPE_CATALOG
    )
    if not catalog_file.is_file():
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_FILE_MISSING")
    observed_recipe_digest = hashlib.sha256(catalog_file.read_bytes()).hexdigest()
    if observed_recipe_digest != recipe_digest:
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_MISMATCH")
    environment_digest = _validate_sha256(
        environment_candidate_record_sha256,
        "EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID",
    )
    driver_path = _nonempty(source_driver_path, "EXECUTION_IDENTITY_SOURCE_DRIVER_PATH_MISSING")
    if driver_path != EXPECTED_SOURCE_DRIVER_PATH:
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_PATH_MISMATCH")
    driver_file = (
        Path(source_driver_file)
        if source_driver_file is not None
        else Path(__file__).resolve().parents[2] / EXPECTED_SOURCE_DRIVER_PATH
    )
    if not driver_file.is_file():
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_FILE_MISSING")
    driver_sha256 = hashlib.sha256(driver_file.read_bytes()).hexdigest()

    argv_values = _validate_driver_argv(argv, driver_path, workdir, driver_file)
    _reject_fixture_uri(destination)
    _reject_fixture_attempt(attempt)

    return {
        "record_type": RECORD_TYPE,
        "status": STATUS,
        "controller_issue": EXPECTED_CONTROLLER_ISSUE,
        "source": {
            "repository": EXPECTED_SOURCE_REPOSITORY,
            "commit": EXPECTED_SOURCE_COMMIT,
            "module_path": EXPECTED_SOURCE_MODULE,
            "module_blob": EXPECTED_SOURCE_MODULE_BLOB,
            "recipe_catalog_path": EXPECTED_RECIPE_CATALOG,
            "recipe_catalog_sha256": recipe_digest,
        },
        "environment_candidate_record_sha256": environment_digest,
        "source_driver_identity": {
            "kind": "EXACT_SOURCE_DRIVER_FILE_CANDIDATE",
            "path": driver_path,
            "sha256": driver_sha256,
        },
        "executable_identity": {
            "kind": "EXACT_PYTHON_PROCESS_CANDIDATE",
            "interpreter_path": interpreter,
            "interpreter_sha256": interpreter_digest,
            "argv": argv_values,
            "working_directory": workdir,
        },
        "destination_identity": {
            "kind": "NON_FIXTURE_DESTINATION_CANDIDATE",
            "uri": destination,
        },
        "attempt_identity": {
            "kind": "PROSPECTIVE_ATTEMPT_CANDIDATE",
            "attempt_id": attempt,
            "created_before_execution": True,
            "outcome_inspected": False,
        },
        "adjudication": {
            "status": "NOT_EXECUTED",
            "reviewer_identity": None,
            "reviewed_at": None,
            "decision_record_sha256": None,
        },
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_execution_identity_candidate(
    candidate: Mapping[str, Any],
    *,
    source_driver_file: Path | None = None,
    recipe_catalog_file: Path | None = None,
) -> dict[str, object]:
    """Validate candidate structure and reverify the canonical source-driver file bytes."""

    if candidate.get("record_type") != RECORD_TYPE:
        _fail("EXECUTION_IDENTITY_CANDIDATE_TYPE_MISMATCH")
    if candidate.get("status") != STATUS:
        _fail("EXECUTION_IDENTITY_CANDIDATE_STATUS_MISMATCH")
    if candidate.get("controller_issue") != EXPECTED_CONTROLLER_ISSUE:
        _fail("EXECUTION_IDENTITY_CANDIDATE_CONTROLLER_MISMATCH")

    source = candidate.get("source")
    if not isinstance(source, Mapping):
        _fail("EXECUTION_IDENTITY_SOURCE_MISSING")
    if source.get("repository") != EXPECTED_SOURCE_REPOSITORY:
        _fail("EXECUTION_IDENTITY_SOURCE_REPOSITORY_MISMATCH")
    if source.get("commit") != EXPECTED_SOURCE_COMMIT:
        _fail("EXECUTION_IDENTITY_SOURCE_COMMIT_MISMATCH")
    if source.get("module_path") != EXPECTED_SOURCE_MODULE:
        _fail("EXECUTION_IDENTITY_SOURCE_MODULE_MISMATCH")
    if source.get("module_blob") != EXPECTED_SOURCE_MODULE_BLOB:
        _fail("EXECUTION_IDENTITY_SOURCE_BLOB_MISMATCH")
    if source.get("recipe_catalog_path") != EXPECTED_RECIPE_CATALOG:
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_PATH_MISMATCH")
    recipe_digest = source.get("recipe_catalog_sha256")
    if not isinstance(recipe_digest, str):
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_INVALID")
    _validate_sha256(recipe_digest, "EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_INVALID")
    resolved_catalog = (
        Path(recipe_catalog_file)
        if recipe_catalog_file is not None
        else Path(__file__).resolve().parents[2] / EXPECTED_RECIPE_CATALOG
    )
    if not resolved_catalog.is_file():
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_FILE_MISSING")
    observed_recipe_digest = hashlib.sha256(resolved_catalog.read_bytes()).hexdigest()
    if observed_recipe_digest != recipe_digest:
        _fail("EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_MISMATCH")

    environment_digest = candidate.get("environment_candidate_record_sha256")
    if not isinstance(environment_digest, str):
        _fail("EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID")
    _validate_sha256(
        environment_digest,
        "EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID",
    )

    driver = candidate.get("source_driver_identity")
    if not isinstance(driver, Mapping):
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_MISSING")
    if driver.get("kind") != "EXACT_SOURCE_DRIVER_FILE_CANDIDATE":
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_KIND_MISMATCH")
    driver_path = driver.get("path")
    if not isinstance(driver_path, str):
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_PATH_MISSING")
    _nonempty(driver_path, "EXECUTION_IDENTITY_SOURCE_DRIVER_PATH_MISSING")
    if driver_path != EXPECTED_SOURCE_DRIVER_PATH:
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_PATH_MISMATCH")
    driver_sha = driver.get("sha256")
    if not isinstance(driver_sha, str):
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_SHA_INVALID")
    _validate_sha256(driver_sha, "EXECUTION_IDENTITY_SOURCE_DRIVER_SHA_INVALID")
    resolved_driver = (
        Path(source_driver_file)
        if source_driver_file is not None
        else Path(__file__).resolve().parents[2] / EXPECTED_SOURCE_DRIVER_PATH
    )
    if not resolved_driver.is_file():
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_FILE_MISSING")
    observed_driver_sha = hashlib.sha256(resolved_driver.read_bytes()).hexdigest()
    if observed_driver_sha != driver_sha:
        _fail("EXECUTION_IDENTITY_SOURCE_DRIVER_SHA_MISMATCH")

    executable = candidate.get("executable_identity")
    if not isinstance(executable, Mapping):
        _fail("EXECUTION_IDENTITY_EXECUTABLE_MISSING")
    if executable.get("kind") != "EXACT_PYTHON_PROCESS_CANDIDATE":
        _fail("EXECUTION_IDENTITY_EXECUTABLE_KIND_MISMATCH")
    interpreter = executable.get("interpreter_path")
    if not isinstance(interpreter, str):
        _fail("EXECUTION_IDENTITY_INTERPRETER_PATH_MISSING")
    _nonempty(interpreter, "EXECUTION_IDENTITY_INTERPRETER_PATH_MISSING")
    interpreter_sha = executable.get("interpreter_sha256")
    if not isinstance(interpreter_sha, str):
        _fail("EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID")
    _validate_sha256(interpreter_sha, "EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID")
    workdir = executable.get("working_directory")
    if not isinstance(workdir, str):
        _fail("EXECUTION_IDENTITY_WORKDIR_MISSING")
    workdir = _nonempty(workdir, "EXECUTION_IDENTITY_WORKDIR_MISSING")
    argv = executable.get("argv")
    if not isinstance(argv, list):
        _fail("EXECUTION_IDENTITY_ARGV_INVALID")
    _validate_driver_argv(argv, driver_path, workdir, resolved_driver)

    destination = candidate.get("destination_identity")
    if not isinstance(destination, Mapping):
        _fail("EXECUTION_IDENTITY_DESTINATION_MISSING")
    if destination.get("kind") != "NON_FIXTURE_DESTINATION_CANDIDATE":
        _fail("EXECUTION_IDENTITY_DESTINATION_KIND_MISMATCH")
    destination_uri = destination.get("uri")
    if not isinstance(destination_uri, str):
        _fail("EXECUTION_IDENTITY_DESTINATION_MISSING")
    _reject_fixture_uri(_nonempty(destination_uri, "EXECUTION_IDENTITY_DESTINATION_MISSING"))

    attempt = candidate.get("attempt_identity")
    if not isinstance(attempt, Mapping):
        _fail("EXECUTION_IDENTITY_ATTEMPT_MISSING")
    if attempt.get("kind") != "PROSPECTIVE_ATTEMPT_CANDIDATE":
        _fail("EXECUTION_IDENTITY_ATTEMPT_KIND_MISMATCH")
    attempt_id = attempt.get("attempt_id")
    if not isinstance(attempt_id, str):
        _fail("EXECUTION_IDENTITY_ATTEMPT_MISSING")
    _reject_fixture_attempt(_nonempty(attempt_id, "EXECUTION_IDENTITY_ATTEMPT_MISSING"))
    if attempt.get("created_before_execution") is not True:
        _fail("EXECUTION_IDENTITY_ATTEMPT_NOT_PROSPECTIVE")
    if attempt.get("outcome_inspected") is not False:
        _fail("EXECUTION_IDENTITY_OUTCOME_ALREADY_INSPECTED")

    if candidate.get("adjudication") != {
        "status": "NOT_EXECUTED",
        "reviewer_identity": None,
        "reviewed_at": None,
        "decision_record_sha256": None,
    }:
        _fail("EXECUTION_IDENTITY_ADJUDICATION_PREMATURE")

    boundary = {
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
    for field, expected in boundary.items():
        if candidate.get(field) != expected:
            _fail(f"EXECUTION_IDENTITY_BOUNDARY_DRIFT_{field.upper()}")

    return {
        "record_type": "AOSS_STAGE_A_EXECUTION_IDENTITY_CANDIDATE_REPORT",
        "candidate_validation": "PASS_NON_FIXTURE_IDENTITY_CANDIDATE",
        "candidate_record_sha256": record_sha256(candidate),
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_candidate_identity": {
            "path": driver_path,
            "sha256": driver_sha,
        },
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "external_adjudication": "NOT_EXECUTED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
