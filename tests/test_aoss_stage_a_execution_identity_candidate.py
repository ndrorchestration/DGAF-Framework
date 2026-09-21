from copy import deepcopy

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    ExecutionIdentityCandidateError,
    prepare_execution_identity_candidate,
    validate_execution_identity_candidate,
)

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64


def _candidate():
    return prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=["-m", "aoss_stage_a_driver", "--plan", "stage-a"],
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=SHA_B,
        environment_candidate_record_sha256=SHA_C,
    )


def test_non_fixture_candidate_validates_without_acceptance():
    candidate = _candidate()
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
