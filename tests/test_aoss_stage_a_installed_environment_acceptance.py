from copy import deepcopy

import pytest

from scripts.aoss_stage_a.installed_environment_acceptance import (
    InstalledEnvironmentAcceptancePacketError,
    candidate_record_sha256,
    prepare_installed_environment_acceptance_packet,
    validate_installed_environment_acceptance_packet,
)
from scripts.aoss_stage_a.installed_environment_evidence import (
    InstalledEnvironmentEvidenceError,
    capture_installed_environment_evidence_candidate,
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
        observed_at="2026-09-21T22:00:00+00:00",
        facts=_FACTS,
    )


def _packet():
    candidate = _candidate()
    return candidate, prepare_installed_environment_acceptance_packet(
        candidate=candidate,
        candidate_source_ref="synthetic://aoss-stage-a/environment-candidate",
    )


def test_acceptance_packet_binds_complete_candidate_without_accepting_it():
    candidate, packet = _packet()
    report = validate_installed_environment_acceptance_packet(
        packet,
        candidate=candidate,
    )

    assert packet["candidate_record_sha256"] == candidate_record_sha256(candidate)
    assert report["packet_validation"] == "PASS_STRUCTURAL_BINDING_ONLY"
    assert report["external_adjudication"] == "NOT_EXECUTED"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0


def test_acceptance_packet_rejects_candidate_record_digest_drift():
    candidate, packet = _packet()
    packet["candidate_record_sha256"] = "0" * 64

    with pytest.raises(
        InstalledEnvironmentAcceptancePacketError,
        match="ENVIRONMENT_ACCEPTANCE_CANDIDATE_RECORD_SHA_MISMATCH",
    ):
        validate_installed_environment_acceptance_packet(packet, candidate=candidate)


def test_acceptance_packet_rejects_evidence_digest_drift():
    candidate, packet = _packet()
    packet["candidate_evidence_sha256"] = "0" * 64

    with pytest.raises(
        InstalledEnvironmentAcceptancePacketError,
        match="ENVIRONMENT_ACCEPTANCE_EVIDENCE_SHA_MISMATCH",
    ):
        validate_installed_environment_acceptance_packet(packet, candidate=candidate)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("status", "ACCEPTED", "ENVIRONMENT_ACCEPTANCE_ADJUDICATION_MUST_REMAIN_EXTERNAL"),
        ("reviewer_identity", "self", "ENVIRONMENT_ACCEPTANCE_REVIEWER_PREPOPULATED"),
        ("reviewed_at", "2026-09-21T22:00:00Z", "ENVIRONMENT_ACCEPTANCE_REVIEW_TIME_PREPOPULATED"),
        ("decision_record_sha256", "1" * 64, "ENVIRONMENT_ACCEPTANCE_DECISION_DIGEST_PREPOPULATED"),
        (
            "installed_environment_acceptance",
            "ACCEPTED",
            "ENVIRONMENT_ACCEPTANCE_PREMATURE",
        ),
    ],
)
def test_acceptance_packet_cannot_self_adjudicate(field, value, error):
    candidate, packet = _packet()
    packet["adjudication"][field] = value

    with pytest.raises(InstalledEnvironmentAcceptancePacketError, match=error):
        validate_installed_environment_acceptance_packet(packet, candidate=candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_driver_binding", "ESTABLISHED"),
        ("executable_acceptance", "ACCEPTED"),
        ("destination_acceptance", "ACCEPTED"),
        ("execution_allowed", True),
        ("collection_execution_readiness", "ESTABLISHED"),
        ("outcomes_generated", True),
        ("scientific_n_increment", 1),
    ],
)
def test_acceptance_packet_cannot_promote_other_readiness_state(field, value):
    candidate, packet = _packet()
    packet[field] = value

    with pytest.raises(
        InstalledEnvironmentAcceptancePacketError,
        match=f"ENVIRONMENT_ACCEPTANCE_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_installed_environment_acceptance_packet(packet, candidate=candidate)


def test_acceptance_packet_detects_candidate_mutation_after_packet_preparation():
    candidate, packet = _packet()
    mutated = deepcopy(candidate)
    mutated["evidence"]["platform_machine"] = "arm64"

    with pytest.raises(
        InstalledEnvironmentEvidenceError,
        match="ENVIRONMENT_EVIDENCE_DIGEST_MISMATCH",
    ):
        validate_installed_environment_acceptance_packet(packet, candidate=mutated)
