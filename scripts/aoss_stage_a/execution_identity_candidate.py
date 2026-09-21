"""Prospective non-fixture execution identity candidate for AOSS Stage A.

This module represents exact executable, destination, and attempt identities for
external review. It does not accept them and cannot enable collection.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping, NoReturn, Sequence

EXPECTED_CONTROLLER_ISSUE = 901
EXPECTED_SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
EXPECTED_SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
EXPECTED_SOURCE_MODULE = "src/agent_control_plane/core.py"
EXPECTED_SOURCE_MODULE_BLOB = "1341df7296a426b336b76ac6b1e4df67611ec931"
EXPECTED_RECIPE_CATALOG = "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXECUTION_IDENTITY_CANDIDATE"
STATUS = "PROSPECTIVE_NON_FIXTURE_CANDIDATE_NOT_ACCEPTED"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


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
    environment_digest = _validate_sha256(
        environment_candidate_record_sha256,
        "EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID",
    )

    if not argv or any(not isinstance(item, str) or not item for item in argv):
        _fail("EXECUTION_IDENTITY_ARGV_INVALID")
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
        "executable_identity": {
            "kind": "EXACT_PYTHON_PROCESS_CANDIDATE",
            "interpreter_path": interpreter,
            "interpreter_sha256": interpreter_digest,
            "argv": list(argv),
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
) -> dict[str, object]:
    """Validate exact candidate structure while forbidding self-admission."""

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

    environment_digest = candidate.get("environment_candidate_record_sha256")
    if not isinstance(environment_digest, str):
        _fail("EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID")
    _validate_sha256(
        environment_digest,
        "EXECUTION_IDENTITY_ENVIRONMENT_CANDIDATE_SHA_INVALID",
    )

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
    argv = executable.get("argv")
    if not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
        _fail("EXECUTION_IDENTITY_ARGV_INVALID")
    workdir = executable.get("working_directory")
    if not isinstance(workdir, str):
        _fail("EXECUTION_IDENTITY_WORKDIR_MISSING")
    _nonempty(workdir, "EXECUTION_IDENTITY_WORKDIR_MISSING")

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
