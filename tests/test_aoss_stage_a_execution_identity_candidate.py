from copy import deepcopy
from pathlib import Path

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    ExecutionIdentityCandidateError,
    prepare_execution_identity_candidate,
    validate_execution_identity_candidate,
)

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64


def _candidate(tmp_path: Path | None = None):
    root = tmp_path or Path(__file__).resolve().parent
    driver = root / "source_driver_candidate.py"
    if not driver.exists():
        driver.write_bytes(b"# source-driver candidate\n")
    return prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=["-m", "aoss_stage_a_driver", "--plan", "stage-a"],
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=SHA_B,
        environment_candidate_record_sha256=SHA_C,
        source_driver_path="scripts/aoss_stage_a/source_driver.py",
        source_driver_file=driver,
    )


def test_non_fixture_candidate_validates_without_acceptance(tmp_path):
    candidate = _candidate(tmp_path)
    report = validate_execution_identity_candidate(candidate)

    assert report["candidate_validation"] == "PASS_NON_FIXTURE_IDENTITY_CANDIDATE"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["external_adjudication"] == "NOT_EXECUTED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


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
def test_candidate_rejects_fixture_identity_substitution(tmp_path, field, value, error):
    candidate = _candidate(tmp_path)
    candidate[field] = value

    with pytest.raises(ExecutionIdentityCandidateError, match=error):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_post_inspection_attempt(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["attempt_identity"]["outcome_inspected"] = True

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_OUTCOME_ALREADY_INSPECTED",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_source_commit_drift(tmp_path):
    candidate = _candidate(tmp_path)
    candidate["source"]["commit"] = "0" * 40

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_COMMIT_MISMATCH",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_rejects_adjudication_prepopulation(tmp_path):
    candidate = _candidate(tmp_path)
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
def test_candidate_cannot_promote_readiness(tmp_path, field, value):
    candidate = _candidate(tmp_path)
    candidate[field] = value

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match=f"EXECUTION_IDENTITY_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_execution_identity_candidate(candidate)


def test_candidate_detects_executable_identity_mutation(tmp_path):
    candidate = _candidate(tmp_path)
    mutated = deepcopy(candidate)
    mutated["executable_identity"]["interpreter_sha256"] = "not-a-sha"

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_INTERPRETER_SHA_INVALID",
    ):
        validate_execution_identity_candidate(mutated)


def test_prepare_rejects_missing_source_driver_file(tmp_path):
    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_FILE_MISSING",
    ):
        prepare_execution_identity_candidate(
            interpreter_path="/opt/python/3.12.3/bin/python",
            interpreter_sha256=SHA_A,
            argv=["-m", "definitely_missing_aoss_driver_901"],
            working_directory="/srv/aoss-stage-a",
            destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
            attempt_id="aoss-stage-a-attempt-0001",
            recipe_catalog_sha256=SHA_B,
            environment_candidate_record_sha256=SHA_C,
            source_driver_path="scripts/aoss_stage_a/source_driver.py",
            source_driver_file=tmp_path / "missing.py",
        )


def test_source_driver_digest_is_derived_from_real_file(tmp_path):
    driver = tmp_path / "driver.py"
    driver.write_bytes(b"print('candidate')\n")
    candidate = prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=["-m", "aoss_stage_a_driver"],
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=SHA_B,
        environment_candidate_record_sha256=SHA_C,
        source_driver_path="scripts/aoss_stage_a/source_driver.py",
        source_driver_file=driver,
    )
    assert candidate["source_driver_identity"]["path"] == "scripts/aoss_stage_a/source_driver.py"
    assert candidate["source_driver_identity"]["sha256"] == __import__("hashlib").sha256(
        driver.read_bytes()
    ).hexdigest()
    report = validate_execution_identity_candidate(candidate)
    assert report["source_driver_candidate_identity"] == candidate["source_driver_identity"]


def test_structural_validation_rejects_removed_source_driver_identity(tmp_path):
    candidate = _candidate(tmp_path)
    del candidate["source_driver_identity"]

    with pytest.raises(
        ExecutionIdentityCandidateError,
        match="EXECUTION_IDENTITY_SOURCE_DRIVER_MISSING",
    ):
        validate_execution_identity_candidate(candidate)
