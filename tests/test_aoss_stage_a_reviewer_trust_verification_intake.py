from copy import deepcopy

import pytest

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256
from scripts.aoss_stage_a.reviewer_trust_verification_intake import (
    ReviewerTrustVerificationIntakeError,
    prepare_reviewer_trust_verification_intake,
    validate_reviewer_trust_verification_intake,
)

SHA = "a" * 64


def _external_admission():
    return {
        "record_type": "AOSS_V0_6_STAGE_A_EXTERNAL_ADMISSION_DECISION_INTAKE",
        "status": "EXTERNAL_DECISION_UNVERIFIED_NOT_ADJUDICATED",
        "controller_issue": 901,
        "fixture": "structural-only",
    }


def _reverification():
    return {
        "record_type": "AOSS_V0_6_STAGE_A_EXTERNAL_EVIDENCE_REVERIFICATION_PACKET",
        "status": "CRYPTOGRAPHIC_BYTES_MATCHED_NO_TRUST_PROMOTION",
        "controller_issue": 901,
        "cryptographic_reverification": "PASS_DECLARED_BYTES_MATCH_SHA256",
        "reviewer_attribution_evidence": [
            {
                "artifact_id": "reviewer-attribution",
                "declared_sha256": "b" * 64,
                "observed_sha256": "b" * 64,
                "digest_match": True,
            }
        ],
        "reviewer_attribution_verified": False,
        "independence_verified": False,
        "local_adjudication": "NOT_EXECUTED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
    }


def _packet():
    external_admission = _external_admission()
    reverification = _reverification()
    packet = prepare_reviewer_trust_verification_intake(
        external_admission_intake=external_admission,
        reverification_packet=reverification,
        verifier_identity="external-trust-verifier:fixture",
        verified_at="2026-09-21T23:50:00Z",
        verification_record_uri="https://example.invalid/aoss/trust-verification.json",
        verification_record_sha256=SHA,
        verification_method_summary="Fixture-only structural verification method.",
        reviewer_attribution_finding="VERIFIED",
        independence_finding="VERIFIED",
    )
    return external_admission, reverification, packet


def test_external_verified_findings_do_not_promote_local_trust():
    external_admission, reverification, packet = _packet()
    report = validate_reviewer_trust_verification_intake(
        packet,
        external_admission_intake=external_admission,
        reverification_packet=reverification,
    )

    assert report["intake_validation"] == "PASS_EXTERNAL_TRUST_FINDINGS_STRUCTURAL_ONLY"
    assert report["external_findings"] == {
        "reviewer_attribution": "VERIFIED",
        "independence": "VERIFIED",
    }
    assert report["reviewer_attribution_verified"] is False
    assert report["independence_verified"] is False
    assert report["local_adjudication"] == "NOT_EXECUTED"
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0


def test_reverification_binding_drift_fails_closed():
    external_admission, reverification, packet = _packet()
    mutated = deepcopy(packet)
    mutated["bindings"]["reverification_packet_sha256"] = "c" * 64

    with pytest.raises(
        ReviewerTrustVerificationIntakeError,
        match="TRUST_INTAKE_REVERIFICATION_BINDING_MISMATCH",
    ):
        validate_reviewer_trust_verification_intake(
            mutated,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
        )


def test_nonpassing_reverification_cannot_feed_trust_intake():
    external_admission, reverification, _ = _packet()
    reverification["cryptographic_reverification"] = "NOT_EXECUTED"

    with pytest.raises(
        ReviewerTrustVerificationIntakeError,
        match="TRUST_INTAKE_REVERIFICATION_NOT_PASS",
    ):
        prepare_reviewer_trust_verification_intake(
            external_admission_intake=external_admission,
            reverification_packet=reverification,
            verifier_identity="external-trust-verifier:fixture",
            verified_at="2026-09-21T23:50:00Z",
            verification_record_uri="https://example.invalid/aoss/trust-verification.json",
            verification_record_sha256=SHA,
            verification_method_summary="Fixture-only structural verification method.",
            reviewer_attribution_finding="VERIFIED",
            independence_finding="VERIFIED",
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
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
def test_external_trust_intake_cannot_promote_execution_boundary(field, value):
    external_admission, reverification, packet = _packet()
    mutated = deepcopy(packet)
    mutated[field] = value

    with pytest.raises(
        ReviewerTrustVerificationIntakeError,
        match=f"TRUST_INTAKE_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_reviewer_trust_verification_intake(
            mutated,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
        )


def test_external_findings_cannot_self_promote_local_trust_state():
    external_admission, reverification, packet = _packet()
    packet["local_trust_state"] = {
        "reviewer_attribution_verified": True,
        "independence_verified": True,
    }

    with pytest.raises(
        ReviewerTrustVerificationIntakeError,
        match="TRUST_INTAKE_LOCAL_TRUST_PROMOTION",
    ):
        validate_reviewer_trust_verification_intake(
            packet,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
        )


def test_binding_is_exact_record_hash():
    external_admission, reverification, packet = _packet()
    assert packet["bindings"]["external_admission_intake_sha256"] == record_sha256(
        external_admission
    )
    assert packet["bindings"]["reverification_packet_sha256"] == record_sha256(
        reverification
    )
