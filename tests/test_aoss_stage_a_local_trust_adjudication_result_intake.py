from copy import deepcopy

import pytest

from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256
from scripts.aoss_stage_a.local_adjudication_candidate import (
    prepare_local_adjudication_candidate,
)
from scripts.aoss_stage_a.local_trust_adjudication_result_intake import (
    LocalTrustAdjudicationResultIntakeError,
    prepare_local_trust_adjudication_result_intake,
    validate_local_trust_adjudication_result_intake,
)
from scripts.aoss_stage_a.local_trust_review_packet import (
    prepare_local_trust_review_packet,
)


def _records():
    external = {
        "record_type": "AOSS_V0_6_STAGE_A_EXTERNAL_ADMISSION_DECISION_INTAKE",
        "status": "EXTERNAL_DECISION_UNVERIFIED_NOT_ADJUDICATED",
        "controller_issue": 901,
        "fixture": "structural-only",
    }
    reverification = {
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
    trust = {
        "record_type": "AOSS_V0_6_STAGE_A_REVIEWER_TRUST_VERIFICATION_INTAKE",
        "status": "EXTERNAL_TRUST_FINDINGS_UNADJUDICATED",
        "controller_issue": 901,
        "bindings": {
            "external_admission_intake_sha256": record_sha256(external),
            "reverification_packet_sha256": record_sha256(reverification),
        },
        "external_verification": {
            "verifier_identity": "external-trust-verifier:fixture",
            "verified_at": "2026-09-22T00:31:00Z",
            "verification_record_uri": "https://example.invalid/aoss/trust-verification.json",
            "verification_record_sha256": "a" * 64,
            "verification_method_summary": "Fixture-only structural verification method.",
            "findings": {
                "reviewer_attribution": "VERIFIED",
                "independence": "VERIFIED",
            },
        },
        "attribution_evidence_count": 1,
        "local_trust_state": {
            "reviewer_attribution_verified": False,
            "independence_verified": False,
        },
        "local_adjudication": "NOT_EXECUTED",
        "installed_environment_acceptance": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
    candidate = prepare_local_adjudication_candidate(
        external_admission_intake=external,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        adjudicator_identity="local-adjudicator:fixture",
        adjudicated_at="2026-09-22T00:32:00Z",
        requested_disposition="ACCEPT",
    )
    evidence = [
        (
            "reviewer_attribution",
            "evidence://aoss/local-review/reviewer-attribution",
            "c" * 64,
        ),
        (
            "independence",
            "evidence://aoss/local-review/independence",
            "d" * 64,
        ),
    ]
    packet = prepare_local_trust_review_packet(
        external_admission_intake=external,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        local_adjudication_candidate=candidate,
        retained_evidence=evidence,
    )
    return external, reverification, trust, candidate, evidence, packet


def _positive_intake():
    external, reverification, trust, candidate, evidence, packet = _records()
    intake = prepare_local_trust_adjudication_result_intake(
        review_packet=packet,
        external_admission_intake=external,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        local_adjudication_candidate=candidate,
        retained_evidence=evidence,
        reviewer_identity="local-reviewer:fixture",
        reviewed_at="2026-09-22T00:59:00Z",
        decision_record_uri="evidence://aoss/local-review/decision",
        decision_record_sha256="e" * 64,
        fresh_cryptographic_verification_reported=True,
        reviewer_attribution_finding="VERIFIED",
        independence_finding="VERIFIED",
    )
    return external, reverification, trust, candidate, evidence, packet, intake


def test_positive_reported_findings_do_not_promote_local_trust():
    external, reverification, trust, candidate, evidence, packet, intake = _positive_intake()
    report = validate_local_trust_adjudication_result_intake(
        intake,
        review_packet=packet,
        external_admission_intake=external,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        local_adjudication_candidate=candidate,
        retained_evidence=evidence,
    )

    assert report["intake_validation"] == "PASS_RECORDED_NO_TRUST_PROMOTION"
    assert report["reported_outcome"] == "POSITIVE_REVIEW_REPORTED"
    assert report["trust_promotion"] == "NOT_EXECUTED"
    assert report["reviewer_attribution_verified"] is False
    assert report["independence_verified"] is False
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0


def test_non_positive_findings_are_retained_without_promotion():
    external, reverification, trust, candidate, evidence, packet = _records()
    intake = prepare_local_trust_adjudication_result_intake(
        review_packet=packet,
        external_admission_intake=external,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        local_adjudication_candidate=candidate,
        retained_evidence=evidence,
        reviewer_identity="local-reviewer:fixture",
        reviewed_at="2026-09-22T00:59:00Z",
        decision_record_uri="evidence://aoss/local-review/decision",
        decision_record_sha256="e" * 64,
        fresh_cryptographic_verification_reported=False,
        reviewer_attribution_finding="NOT_VERIFIED",
        independence_finding="BLOCKED",
    )

    assert intake["reported_review"]["reported_outcome"] == ("NON_POSITIVE_REVIEW_REPORTED")
    assert intake["reviewer_attribution_verified"] is False
    assert intake["independence_verified"] is False


def test_binding_drift_fails_closed():
    external, reverification, trust, candidate, evidence, packet, intake = (
        _positive_intake()
    )
    mutated = deepcopy(intake)
    mutated["bindings"]["local_trust_review_packet_sha256"] = "f" * 64

    with pytest.raises(
        LocalTrustAdjudicationResultIntakeError,
        match="LOCAL_TRUST_ADJUDICATION_RESULT_BINDING_MISMATCH",
    ):
        validate_local_trust_adjudication_result_intake(
            mutated,
            review_packet=packet,
            external_admission_intake=external,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
            local_adjudication_candidate=candidate,
            retained_evidence=evidence,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("trust_promotion", "EXECUTED"),
        ("reviewer_attribution_verified", True),
        ("independence_verified", True),
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
def test_intake_cannot_promote_trust_or_execution_boundary(field, value):
    external, reverification, trust, candidate, evidence, packet, intake = (
        _positive_intake()
    )
    mutated = deepcopy(intake)
    mutated[field] = value

    with pytest.raises(
        LocalTrustAdjudicationResultIntakeError,
        match=f"LOCAL_TRUST_ADJUDICATION_RESULT_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_local_trust_adjudication_result_intake(
            mutated,
            review_packet=packet,
            external_admission_intake=external,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
            local_adjudication_candidate=candidate,
            retained_evidence=evidence,
        )


def test_invalid_finding_fails_closed():
    external, reverification, trust, candidate, evidence, packet = _records()

    with pytest.raises(
        LocalTrustAdjudicationResultIntakeError,
        match="LOCAL_TRUST_ADJUDICATION_RESULT_INDEPENDENCE_INVALID",
    ):
        prepare_local_trust_adjudication_result_intake(
            review_packet=packet,
            external_admission_intake=external,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
            local_adjudication_candidate=candidate,
            retained_evidence=evidence,
            reviewer_identity="local-reviewer:fixture",
            reviewed_at="2026-09-22T00:59:00Z",
            decision_record_uri="evidence://aoss/local-review/decision",
            decision_record_sha256="e" * 64,
            fresh_cryptographic_verification_reported=True,
            reviewer_attribution_finding="VERIFIED",
            independence_finding="ACCEPT",
        )
