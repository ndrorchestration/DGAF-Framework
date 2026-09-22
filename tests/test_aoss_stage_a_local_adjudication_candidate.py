from copy import deepcopy

import pytest

from scripts.aoss_stage_a.local_adjudication_candidate import (
    LocalAdjudicationCandidateError,
    prepare_local_adjudication_candidate,
    validate_local_adjudication_candidate,
)


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


def _trust_intake():
    return {
        "record_type": "AOSS_V0_6_STAGE_A_REVIEWER_TRUST_VERIFICATION_INTAKE",
        "status": "EXTERNAL_TRUST_FINDINGS_UNADJUDICATED",
        "controller_issue": 901,
        "bindings": {},
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


def _records():
    from scripts.aoss_stage_a.external_admission_decision_intake import record_sha256

    external_admission = _external_admission()
    reverification = _reverification()
    trust = _trust_intake()
    trust["bindings"] = {
        "external_admission_intake_sha256": record_sha256(external_admission),
        "reverification_packet_sha256": record_sha256(reverification),
    }
    return external_admission, reverification, trust


def _candidate():
    external_admission, reverification, trust = _records()
    candidate = prepare_local_adjudication_candidate(
        external_admission_intake=external_admission,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        adjudicator_identity="local-adjudicator:ci-fixture",
        adjudicated_at="2026-09-22T00:32:00Z",
        requested_disposition="ACCEPT",
    )
    return external_admission, reverification, trust, candidate


def test_external_verified_findings_still_block_local_acceptance():
    external_admission, reverification, trust, candidate = _candidate()
    report = validate_local_adjudication_candidate(
        candidate,
        external_admission_intake=external_admission,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
    )

    assert report["candidate_validation"] == "PASS_BLOCKED_LOCAL_ADJUDICATION_CANDIDATE"
    assert report["effective_disposition"] == "BLOCKED"
    assert report["blockers"] == [
        "LOCAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED",
        "LOCAL_INDEPENDENCE_NOT_VERIFIED",
    ]
    assert report["execution_allowed"] is False
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0


def test_candidate_binding_drift_fails_closed():
    external_admission, reverification, trust, candidate = _candidate()
    mutated = deepcopy(candidate)
    mutated["bindings"]["reviewer_trust_intake_sha256"] = "c" * 64

    with pytest.raises(
        LocalAdjudicationCandidateError,
        match="LOCAL_ADJUDICATION_BINDING_MISMATCH",
    ):
        validate_local_adjudication_candidate(
            mutated,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
        )


def test_effective_accept_cannot_be_declared():
    external_admission, reverification, trust, candidate = _candidate()
    candidate["local_adjudication"]["effective_disposition"] = "ACCEPT"

    with pytest.raises(
        LocalAdjudicationCandidateError,
        match="LOCAL_ADJUDICATION_EFFECTIVE_DISPOSITION_PROMOTED",
    ):
        validate_local_adjudication_candidate(
            candidate,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
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
def test_candidate_cannot_promote_execution_boundary(field, value):
    external_admission, reverification, trust, candidate = _candidate()
    mutated = deepcopy(candidate)
    mutated[field] = value

    with pytest.raises(
        LocalAdjudicationCandidateError,
        match=f"LOCAL_ADJUDICATION_BOUNDARY_DRIFT_{field.upper()}",
    ):
        validate_local_adjudication_candidate(
            mutated,
            external_admission_intake=external_admission,
            reverification_packet=reverification,
            reviewer_trust_intake=trust,
        )


def test_nonverified_external_findings_add_blockers():
    external_admission, reverification, trust = _records()
    trust["external_verification"]["findings"] = {
        "reviewer_attribution": "NOT_VERIFIED",
        "independence": "BLOCKED",
    }

    candidate = prepare_local_adjudication_candidate(
        external_admission_intake=external_admission,
        reverification_packet=reverification,
        reviewer_trust_intake=trust,
        adjudicator_identity="local-adjudicator:ci-fixture",
        adjudicated_at="2026-09-22T00:32:00Z",
        requested_disposition="ACCEPT",
    )

    assert candidate["local_adjudication"]["blockers"] == [
        "EXTERNAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED",
        "EXTERNAL_INDEPENDENCE_NOT_VERIFIED",
        "LOCAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED",
        "LOCAL_INDEPENDENCE_NOT_VERIFIED",
    ]
