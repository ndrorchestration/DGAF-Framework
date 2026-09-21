from copy import deepcopy

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    prepare_execution_identity_candidate,
)
from scripts.aoss_stage_a.external_admission_decision_intake import (
    ExternalAdmissionDecisionIntakeError,
    prepare_external_admission_decision_intake,
    validate_external_admission_decision_intake,
)
from scripts.aoss_stage_a.installed_environment_evidence import (
    capture_installed_environment_evidence_candidate,
)
from scripts.aoss_stage_a.runtime_binding import RuntimeFacts

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64


def _environment_candidate():
    facts = RuntimeFacts(
        implementation="CPython",
        version="3.12.3",
        platform_system="Linux",
        platform_machine="x86_64",
        executable="/opt/python/3.12.3/bin/python",
        prefix="/opt/python/3.12.3",
        base_prefix="/opt/python/3.12.3",
    )
    return capture_installed_environment_evidence_candidate(
        observed_at="2026-09-21T22:00:00Z",
        facts=facts,
    )


def _identity_candidate(environment_candidate):
    from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256

    return prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=["-m", "aoss_stage_a_driver", "--plan", "stage-a"],
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=SHA_B,
        environment_candidate_record_sha256=record_sha256(environment_candidate),
    )


def _intake():
    environment = _environment_candidate()
    identity = _identity_candidate(environment)
    intake = prepare_external_admission_decision_intake(
        environment_candidate=environment,
        execution_identity_candidate=identity,
        reviewer_identity="external-reviewer:example",
        reviewed_at="2026-09-21T23:30:00Z",
        external_record_uri="https://example.invalid/aoss-stage-a/decision.json",
        external_record_sha256=SHA_D,
        independence_claimed=True,
        independence_basis="organizationally separate review function",
        installed_environment_decision="ACCEPT",
        source_driver_executable_decision="ACCEPT",
        destination_attempt_decision="ACCEPT",
    )
    return environment, identity, intake


def test_external_accept_reports_do_not_promote_local_readiness():
    environment, identity, intake = _intake()
    report = validate_external_admission_decision_intake(
        intake,
        environment_candidate=environment,
        execution_identity_candidate=identity,
    )

    assert report["intake_validation"] == "PASS_EXTERNAL_DECISION_STRUCTURAL_ONLY"
    assert report["external_decisions"] == {
        "installed_environment": "ACCEPT",
        "source_driver_executable": "ACCEPT",
        "destination_attempt": "ACCEPT",
    }
    assert report["reviewer_attribution_verified"] is False
    assert report["independence_verified"] is False
    assert report["cryptographic_reverification"] == "NOT_EXECUTED"
    assert report["local_adjudication"] == "NOT_EXECUTED"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


def test_candidate_binding_drift_fails_closed():
    environment, identity, intake = _intake()
    intake["candidate_bindings"]["execution_identity_candidate_record_sha256"] = SHA_C

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match="EXTERNAL_DECISION_EXECUTION_IDENTITY_SHA_MISMATCH",
    ):
        validate_external_admission_decision_intake(
            intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
        )


def test_missing_independence_basis_fails_when_independence_claimed():
    environment, identity, intake = _intake()
    intake["external_review"]["independence_basis"] = None

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match="EXTERNAL_DECISION_INDEPENDENCE_BASIS_MISSING",
    ):
        validate_external_admission_decision_intake(
            intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
        )


def test_invalid_external_disposition_fails_closed():
    environment, identity, intake = _intake()
    intake["external_decisions"]["destination_attempt"] = "PASS"

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match="EXTERNAL_DECISION_DISPOSITION_INVALID",
    ):
        validate_external_admission_decision_intake(
            intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
        )


def test_local_adjudication_cannot_be_prepopulated():
    environment, identity, intake = _intake()
    intake["local_adjudication"]["status"] = "ACCEPTED"

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match="EXTERNAL_DECISION_LOCAL_ADJUDICATION_PREMATURE",
    ):
        validate_external_admission_decision_intake(
            intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
        )


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
def test_external_decision_intake_cannot_promote_boundary(field, value):
    environment, identity, intake = _intake()
    mutated = deepcopy(intake)
    mutated[field] = value

    with pytest.raises(
        ExternalAdmissionDecisionIntakeError,
        match=f"EXTERNAL_DECISION_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_external_admission_decision_intake(
            mutated,
            environment_candidate=environment,
            execution_identity_candidate=identity,
        )
