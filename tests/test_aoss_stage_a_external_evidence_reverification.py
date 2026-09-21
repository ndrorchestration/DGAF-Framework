import hashlib
from copy import deepcopy

import pytest

from scripts.aoss_stage_a.execution_identity_candidate import (
    prepare_execution_identity_candidate,
)
from scripts.aoss_stage_a.external_admission_decision_intake import (
    prepare_external_admission_decision_intake,
    record_sha256,
)
from scripts.aoss_stage_a.external_evidence_reverification import (
    ExternalEvidenceReverificationError,
    prepare_external_evidence_reverification_packet,
    validate_external_evidence_reverification_packet,
)
from scripts.aoss_stage_a.installed_environment_evidence import (
    capture_installed_environment_evidence_candidate,
)
from scripts.aoss_stage_a.runtime_binding import RuntimeFacts

SHA_A = "a" * 64
SHA_B = "b" * 64
EXTERNAL_BYTES = b'{"decision":"ACCEPT","scope":"stage-a-admission"}\n'
ATTRIBUTION_BYTES = b'{"reviewer":"external-reviewer:example","role":"reviewer"}\n'


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _environment_candidate():
    return capture_installed_environment_evidence_candidate(
        observed_at="2026-09-21T22:00:00Z",
        facts=RuntimeFacts(
            implementation="cpython",
            version="3.12.3",
            platform_system="Linux",
            platform_machine="x86_64",
            executable="/opt/python/3.12.3/bin/python",
            prefix="/opt/python/3.12.3",
            base_prefix="/opt/python/3.12.3",
        ),
    )


def _fixtures():
    environment = _environment_candidate()
    identity = prepare_execution_identity_candidate(
        interpreter_path="/opt/python/3.12.3/bin/python",
        interpreter_sha256=SHA_A,
        argv=["-m", "aoss_stage_a_driver", "--plan", "stage-a"],
        working_directory="/srv/aoss-stage-a",
        destination_uri="file:///srv/aoss-stage-a/retained/attempt-0001",
        attempt_id="aoss-stage-a-attempt-0001",
        recipe_catalog_sha256=SHA_B,
        environment_candidate_record_sha256=record_sha256(environment),
    )
    intake = prepare_external_admission_decision_intake(
        environment_candidate=environment,
        execution_identity_candidate=identity,
        reviewer_identity="external-reviewer:example",
        reviewed_at="2026-09-21T23:30:00Z",
        external_record_uri="https://example.invalid/aoss-stage-a/decision.json",
        external_record_sha256=_sha(EXTERNAL_BYTES),
        independence_claimed=True,
        independence_basis="organizationally separate review function",
        installed_environment_decision="ACCEPT",
        source_driver_executable_decision="ACCEPT",
        destination_attempt_decision="ACCEPT",
    )
    artifacts = [
        (
            "reviewer-attribution",
            "https://example.invalid/aoss-stage-a/reviewer.json",
            _sha(ATTRIBUTION_BYTES),
            ATTRIBUTION_BYTES,
        )
    ]
    packet = prepare_external_evidence_reverification_packet(
        intake=intake,
        environment_candidate=environment,
        execution_identity_candidate=identity,
        retrieval_source_uri="https://example.invalid/aoss-stage-a/decision.json",
        retrieved_at="2026-09-21T23:45:00Z",
        external_record_bytes=EXTERNAL_BYTES,
        attribution_artifacts=artifacts,
    )
    return environment, identity, intake, artifacts, packet


def test_reverification_matches_bytes_without_promoting_trust():
    environment, identity, intake, artifacts, packet = _fixtures()
    report = validate_external_evidence_reverification_packet(
        packet,
        intake=intake,
        environment_candidate=environment,
        execution_identity_candidate=identity,
        external_record_bytes=EXTERNAL_BYTES,
        attribution_artifacts=artifacts,
    )

    assert report["reverification"] == "PASS_DECLARED_BYTES_MATCH_SHA256"
    assert report["external_record_retrieved"] is True
    assert report["attribution_evidence_retrieved"] is True
    assert report["reviewer_attribution_verified"] is False
    assert report["independence_verified"] is False
    assert report["local_adjudication"] == "NOT_EXECUTED"
    assert report["installed_environment_acceptance"] == "NOT_ESTABLISHED"
    assert report["source_driver_binding"] == "NOT_ESTABLISHED"
    assert report["executable_acceptance"] == "NOT_ESTABLISHED"
    assert report["destination_acceptance"] == "NOT_ESTABLISHED"
    assert report["execution_allowed"] is False
    assert report["scientific_n_increment"] == 0


def test_external_record_hash_mismatch_fails_closed():
    environment, identity, intake, artifacts, packet = _fixtures()

    with pytest.raises(
        ExternalEvidenceReverificationError,
        match="REVERIFICATION_EXTERNAL_RECORD_SHA_MISMATCH",
    ):
        validate_external_evidence_reverification_packet(
            packet,
            intake=intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
            external_record_bytes=b"tampered",
            attribution_artifacts=artifacts,
        )


def test_attribution_artifact_hash_mismatch_fails_closed():
    environment, identity, intake, artifacts, packet = _fixtures()
    tampered = [
        (
            artifacts[0][0],
            artifacts[0][1],
            artifacts[0][2],
            b"tampered",
        )
    ]

    with pytest.raises(
        ExternalEvidenceReverificationError,
        match="REVERIFICATION_ATTRIBUTION_SHA_MISMATCH",
    ):
        validate_external_evidence_reverification_packet(
            packet,
            intake=intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
            external_record_bytes=EXTERNAL_BYTES,
            attribution_artifacts=tampered,
        )


def test_retrieval_uri_must_match_intake_uri():
    environment, identity, intake, artifacts, _ = _fixtures()

    with pytest.raises(
        ExternalEvidenceReverificationError,
        match="REVERIFICATION_RETRIEVAL_SOURCE_URI_MISMATCH",
    ):
        prepare_external_evidence_reverification_packet(
            intake=intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
            retrieval_source_uri="https://example.invalid/wrong.json",
            retrieved_at="2026-09-21T23:45:00Z",
            external_record_bytes=EXTERNAL_BYTES,
            attribution_artifacts=artifacts,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reviewer_attribution_verified", True),
        ("independence_verified", True),
        ("local_adjudication", "ACCEPTED"),
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
def test_reverification_packet_cannot_promote_boundary(field, value):
    environment, identity, intake, artifacts, packet = _fixtures()
    mutated = deepcopy(packet)
    mutated[field] = value

    with pytest.raises(
        ExternalEvidenceReverificationError,
        match=f"REVERIFICATION_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_external_evidence_reverification_packet(
            mutated,
            intake=intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
            external_record_bytes=EXTERNAL_BYTES,
            attribution_artifacts=artifacts,
        )


def test_attribution_binding_cannot_claim_trust_anchor():
    environment, identity, intake, artifacts, packet = _fixtures()
    packet["attribution_binding"] = "VERIFIED_IDENTITY"

    with pytest.raises(
        ExternalEvidenceReverificationError,
        match="REVERIFICATION_ATTRIBUTION_BINDING_OVERCLAIM",
    ):
        validate_external_evidence_reverification_packet(
            packet,
            intake=intake,
            environment_candidate=environment,
            execution_identity_candidate=identity,
            external_record_bytes=EXTERNAL_BYTES,
            attribution_artifacts=artifacts,
        )
