from copy import deepcopy

import pytest

from scripts.aoss_stage_a.installed_environment_evidence import (
    InstalledEnvironmentEvidenceError,
    capture_installed_environment_evidence_candidate,
    validate_installed_environment_evidence_candidate,
)
from scripts.aoss_stage_a.runtime_binding import RuntimeFacts


_FACTS = RuntimeFacts(
    implementation="cpython",
    version="3.12.3",
    platform_system="Linux",
    platform_machine="x86_64",
    executable="/opt/python/3.12.3/bin/python",
    prefix="/opt/python/3.12.3",
    base_prefix="/opt/python/3.12.3",
)


def _candidate():
    return capture_installed_environment_evidence_candidate(
        observed_at="2026-09-21T21:00:00+00:00",
        facts=_FACTS,
    )


def test_candidate_environment_evidence_is_digest_bound_and_non_accepting():
    candidate = _candidate()
    report = validate_installed_environment_evidence_candidate(candidate)

    assert candidate["evidence_sha256"] == report["evidence_sha256"]
    assert report["candidate_validation"] == "PASS_OBSERVED_CANDIDATE_NOT_ACCEPTED"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("interpreter_implementation", "pypy", "ENVIRONMENT_INTERPRETER_IMPLEMENTATION_MISMATCH"),
        ("interpreter_version", "3.12.2", "ENVIRONMENT_INTERPRETER_VERSION_MISMATCH"),
        ("dependency_lock_sha256", "0" * 64, "ENVIRONMENT_DEPENDENCY_LOCK_MISMATCH"),
        ("platform_system", "", "ENVIRONMENT_PLATFORM_SYSTEM_MISSING"),
        ("executable", "", "ENVIRONMENT_EXECUTABLE_MISSING"),
        ("environment_observed_at", "not-a-time", "ENVIRONMENT_OBSERVED_AT_INVALID"),
    ],
)
def test_candidate_environment_evidence_fails_closed_on_runtime_drift(field, value, error):
    candidate = _candidate()
    candidate["evidence"][field] = value

    with pytest.raises(InstalledEnvironmentEvidenceError, match=error):
        validate_installed_environment_evidence_candidate(candidate)


def test_candidate_environment_evidence_rejects_digest_tamper():
    candidate = _candidate()
    candidate["evidence"]["platform_machine"] = "arm64"

    with pytest.raises(
        InstalledEnvironmentEvidenceError,
        match="ENVIRONMENT_EVIDENCE_DIGEST_MISMATCH",
    ):
        validate_installed_environment_evidence_candidate(candidate)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("installed_environment_acceptance", "ACCEPTED", "ENVIRONMENT_ACCEPTANCE_PREMATURE"),
        ("source_driver_binding", "ESTABLISHED", "SOURCE_DRIVER_BINDING_PREMATURE"),
        ("execution_allowed", True, "EXECUTION_PREMATURE"),
        ("collection_execution_readiness", "ESTABLISHED", "COLLECTION_READINESS_PREMATURE"),
        ("outcomes_generated", True, "OUTCOME_GENERATION_PREMATURE"),
        ("scientific_n_increment", 1, "SCIENTIFIC_N_INCREMENT_INVALID"),
    ],
)
def test_candidate_environment_evidence_cannot_promote_state(field, value, error):
    candidate = deepcopy(_candidate())
    candidate[field] = value

    with pytest.raises(InstalledEnvironmentEvidenceError, match=error):
        validate_installed_environment_evidence_candidate(candidate)
