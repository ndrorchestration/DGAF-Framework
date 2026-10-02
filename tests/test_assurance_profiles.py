import json

import pytest

from components.assurance_profiles import (
    AssuranceProfile,
    DerivationClass,
    ExternalReviewDisclosure,
    ExternalReviewReceipt,
    MeasurementContract,
    MeasurementField,
    PredicateStatus,
    ReadinessPredicate,
    ReplayContract,
    ReplayReceipt,
    ReviewFinding,
    SourceBinding,
    evaluate_external_review,
    evaluate_readiness,
    evaluate_replay,
)


def _source():
    return SourceBinding(
        repository="example/system",
        revision="a" * 40,
        source_schema="example.events.v1",
    )


def _replay_contract():
    return ReplayContract(
        required_digest_roles=("source_sha256", "normalized_sha256"),
        required_verification_fields=("source_identity_match", "normalized_digest_match"),
    )


def test_measurement_contract_preserves_direct_derived_and_unmeasured_states():
    contract = MeasurementContract(
        source=_source(),
        fields=(
            MeasurementField(
                name="event_kind",
                derivation=DerivationClass.DIRECT,
                value="completed",
                source_field="event",
                unit="enum",
            ),
            MeasurementField(
                name="observer_id",
                derivation=DerivationClass.DERIVED,
                value="b" * 64,
                unit="sha256",
            ),
            MeasurementField(
                name="authorization_state",
                derivation=DerivationClass.UNMEASURED,
            ),
        ),
        non_inference_rules=("completion does not imply authorization",),
    )
    profile = AssuranceProfile(
        profile_id="example.assurance.v0",
        measurement=contract,
        replay=_replay_contract(),
        readiness=(ReadinessPredicate("source_identity", PredicateStatus.BOUND, ("source",)),),
    )

    assert profile.measurement.fields[2].value is None
    assert profile.non_effects == (
        "NO_EXECUTION_AUTHORITY",
        "NO_SCIENTIFIC_N_INCREMENT",
        "NO_EFFICACY_EFFECT",
    )


def test_unmeasured_field_cannot_carry_inferred_value():
    with pytest.raises(ValueError, match="cannot carry"):
        MeasurementField(
            name="authorization_state",
            derivation=DerivationClass.UNMEASURED,
            value="AUTHORIZED",
        )


def test_replay_fails_closed_on_missing_or_false_evidence():
    receipt = ReplayReceipt(
        source=_source(),
        digests={"source_sha256": "c" * 64},
        verifications={
            "source_identity_match": True,
            "normalized_digest_match": False,
        },
        replay_environment={"python_version": "3.12"},
    )

    decision = evaluate_replay(_replay_contract(), receipt)

    assert decision.status == "BLOCKED"
    assert "MISSING_DIGEST:normalized_sha256" in decision.reasons
    assert "VERIFICATION_NOT_TRUE:normalized_digest_match" in decision.reasons
    assert decision.authorization_effect == "NONE"
    assert decision.execution_effect == "NONE"
    assert decision.scientific_n_increment == 0
    assert decision.efficacy_effect == "NONE"


def test_readiness_is_non_authorizing_and_blocks_unknown_predicate():
    decision = evaluate_readiness(
        (
            ReadinessPredicate("source_identity", PredicateStatus.BOUND, ("source",)),
            ReadinessPredicate("runtime_identity", PredicateStatus.NOT_ESTABLISHED),
        )
    )

    assert decision.status == "BLOCKED"
    assert decision.reasons == ("READINESS_NOT_ESTABLISHED:runtime_identity",)
    assert decision.authorization_effect == "NONE"
    assert decision.execution_effect == "NONE"


def test_positive_external_review_does_not_execute_local_acceptance():
    receipt = ExternalReviewReceipt(
        disclosure=ExternalReviewDisclosure(
            reviewer_identity="reviewer-1",
            relationship_disclosure="no implementation role",
            independence_finding=ReviewFinding.VERIFIED,
        ),
        source=_source(),
        finding=ReviewFinding.VERIFIED,
        retained_evidence_refs=("sha256:abc",),
    )

    decision = evaluate_external_review(receipt)

    assert decision.pass_
    assert receipt.local_acceptance_executed is False
    assert decision.authorization_effect == "NONE"
    assert decision.execution_effect == "NONE"


def test_external_review_cannot_smuggle_authorization():
    receipt = ExternalReviewReceipt(
        disclosure=ExternalReviewDisclosure(
            reviewer_identity="reviewer-1",
            relationship_disclosure="no implementation role",
            independence_finding=ReviewFinding.VERIFIED,
        ),
        source=_source(),
        finding=ReviewFinding.VERIFIED,
        authorization_effect="GRANTED",
    )

    decision = evaluate_external_review(receipt)

    assert decision.status == "BLOCKED"
    assert "EXTERNAL_REVIEW_CANNOT_GRANT_AUTHORIZATION" in decision.reasons


def test_decision_is_json_serializable():
    decision = evaluate_readiness((ReadinessPredicate("source_identity", PredicateStatus.PASS),))

    encoded = json.dumps(decision.to_dict(), sort_keys=True)
    assert '"authorization_effect": "NONE"' in encoded
    assert '"scientific_n_increment": 0' in encoded
