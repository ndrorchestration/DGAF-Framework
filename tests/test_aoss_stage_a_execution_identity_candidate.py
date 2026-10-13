import ast
import hashlib
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    EXPECTED_DRIVER_BLOB,
    EXPECTED_DRIVER_ENTRYPOINT,
    EXPECTED_DRIVER_INTRODUCTION_COMMIT,
    EXPECTED_DRIVER_PATH,
    EXPECTED_DRIVER_SHA256,
    EXPECTED_RECIPE_CATALOG_SHA256,
    ExecutionIdentityCandidateError,
    prepare_execution_identity_candidate,
    validate_execution_identity_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
SHA_A = "a" * 64
SHA_C = "c" * 64


def _candidate():
    return prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=EXPECTED_RECIPE_CATALOG_SHA256,
        environment_candidate_record_sha256=SHA_C,
    )


def test_exact_driver_candidate_validates_without_acceptance():
    candidate = _candidate()
    report = validate_execution_identity_candidate(candidate)

    assert report["candidate_validation"] == "PASS_EXACT_DRIVER_IDENTITY_CANDIDATE"
    assert report["driver_git_blob"] == EXPECTED_DRIVER_BLOB
    assert report["driver_sha256"] == EXPECTED_DRIVER_SHA256
    assert report["driver_entrypoint"] == EXPECTED_DRIVER_ENTRYPOINT
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["external_adjudication"] == "NOT_EXECUTED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


def test_driver_identity_constants_match_actual_tracked_source_without_importing_driver():
    driver = ROOT / EXPECTED_DRIVER_PATH
    assert driver.is_file()
    assert hashlib.sha256(driver.read_bytes()).hexdigest() == EXPECTED_DRIVER_SHA256

    blob = subprocess.check_output(
        ["git", "-C", str(ROOT), "hash-object", "--", EXPECTED_DRIVER_PATH],
        text=True,
    ).strip()
    assert blob == EXPECTED_DRIVER_BLOB

    introduction_blob = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "rev-parse",
            f"{EXPECTED_DRIVER_INTRODUCTION_COMMIT}:{EXPECTED_DRIVER_PATH}",
        ],
        text=True,
    ).strip()
    assert introduction_blob == EXPECTED_DRIVER_BLOB

    blob_bytes = subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", EXPECTED_DRIVER_BLOB])
    assert hashlib.sha256(blob_bytes).hexdigest() == EXPECTED_DRIVER_SHA256

    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert f"{EXPECTED_DRIVER_PATH} text eol=lf" in attributes.splitlines()

    tree = ast.parse(driver.read_text(encoding="utf-8"), filename=str(driver))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert EXPECTED_DRIVER_ENTRYPOINT.rsplit(":", 1)[1] in functions


@pytest.mark.parametrize(
    ("mutation", "error"),
    [
        (
            lambda c: c["driver_identity"].__setitem__(
                "introduced_at_commit",
                "0" * 40,
            ),
            "EXECUTION_IDENTITY_DRIVER_COMMIT_MISMATCH",
        ),
        (
            lambda c: c["driver_identity"].__setitem__(
                "path",
                "scripts/aoss_stage_a/definitely_missing_driver.py",
            ),
            "EXECUTION_IDENTITY_DRIVER_PATH_MISMATCH",
        ),
        (
            lambda c: c["driver_identity"].__setitem__("git_blob", "0" * 40),
            "EXECUTION_IDENTITY_DRIVER_BLOB_MISMATCH",
        ),
        (
            lambda c: c["driver_identity"].__setitem__("sha256", "0" * 64),
            "EXECUTION_IDENTITY_DRIVER_SHA_MISMATCH",
        ),
        (
            lambda c: c["driver_identity"].__setitem__(
                "entrypoint",
                "scripts.aoss_stage_a.source_driver:missing",
            ),
            "EXECUTION_IDENTITY_DRIVER_ENTRYPOINT_MISMATCH",
        ),
        (
            lambda c: c["executable_identity"].__setitem__(
                "driver_entrypoint",
                "scripts.aoss_stage_a.source_driver:missing",
            ),
            "EXECUTION_IDENTITY_EXECUTABLE_ENTRYPOINT_MISMATCH",
        ),
    ],
)
def test_candidate_rejects_fictional_or_substituted_driver_identity(mutation, error):
    candidate = _candidate()
    mutation(candidate)
    with pytest.raises(ExecutionIdentityCandidateError, match=error):
        validate_execution_identity_candidate(candidate)


def test_prepare_rejects_stale_recipe_catalog_identity():
    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_RECIPE_CATALOG_SHA_MISMATCH",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            working_directory="/srv/aoss-stage-a",
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256="b" * 64,
            environment_candidate_record_sha256=SHA_C,
        )


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        (
            "destination_identity",
            {"kind": "NON_FIXTURE_DESTINATION_CANDIDATE", "uri": "fixture://bad"},
            "EXECUTION_IDENTITY_DESTINATION_FIXTURE_FORBIDDEN",
        ),
        (
            "attempt_identity",
            {
                "kind": "PROSPECTIVE_ATTEMPT_CANDIDATE",
                "attempt_id": "synthetic-fixture-attempt",
                "created_before_execution": True,
                "outcome_inspected": False,
            },
            "EXECUTION_IDENTITY_ATTEMPT_FIXTURE_FORBIDDEN",
        ),
    ],
)
def test_candidate_rejects_fixture_identity_substitution(field, value, error):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(ExecutionIdentityCandidateError, match=error):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_post_inspection_attempt():
    candidate = _candidate()
    candidate["attempt_identity"]["outcome_inspected"] = True

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_OUTCOME_ALREADY_INSPECTED",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_source_commit_drift():
    candidate = _candidate()
    candidate["source"]["commit"] = "0" * 40

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_COMMIT_MISMATCH",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_adjudication_prepopulation():
    candidate = _candidate()
    candidate["adjudication"]["reviewer_identity"] = "self"

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_ADJUDICATION_PREMATURE",
    ):
        validate_execution_identity_candidate(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("installed_environment_acceptance", "ACCEPTED"),
        ("source_driver_binding", "ESTABLISHED"),
        ("executable_acceptance", "ACCEPTED"),
        ("destination_acceptance", "ACCEPTED"),
        ("execution_allowed", True),
        ("collection_execution_readiness", "ESTABLISHED"),
        ("outcomes_generated", True),
        ("scientific_n_increment", 1),
    ],
)
def test_candidate_cannot_promote_readiness(field, value):
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match=f"EXECUTION_IDENTITY_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_detects_executable_identity_mutation():
    candidate = _candidate()
    mutated = deepcopy(candidate)
    mutated["executable_identity"]["interpreter_sha256"] = "not-a-sha"

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID",
    ):
        validate_execution_identity_candidate(mutated)
