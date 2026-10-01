from components.assurance_profile_v0 import (
    AUTHORIZATION_EFFECT_NONE,
    CERTIFICATION_EFFECT_NONE,
    AssuranceProfileInput,
    DimensionAssessment,
    DimensionStatus,
    IndependenceClass,
    evaluate_assurance_profile,
)


def _dimension(
    status: DimensionStatus = DimensionStatus.PASS,
    *,
    required: bool = True,
    evidence_ref: str = "evidence://example",
) -> DimensionAssessment:
    return DimensionAssessment(
        status=status,
        required=required,
        evidence_refs=(evidence_ref,),
    )


def _profile(
    *,
    readiness: DimensionStatus = DimensionStatus.PASS,
    independence_class: IndependenceClass = IndependenceClass.SAME_SYSTEM,
) -> AssuranceProfileInput:
    return AssuranceProfileInput(
        profile_id="ASSURANCE-PROFILE-V0-TEST",
        profile_version="v0-candidate",
        target_system="agent-control-plane",
        source_identity="source-1",
        runtime_identity="runtime-1",
        environment_identity="environment-1",
        material_source_manifest_ref="manifest://example",
        measurement_apparatus=_dimension(evidence_ref="evidence://measurement"),
        runtime_source_environment_binding=_dimension(evidence_ref="evidence://binding"),
        authorization_decision_separation=_dimension(evidence_ref="evidence://separation"),
        custody_replay_integrity=_dimension(evidence_ref="evidence://custody"),
        readiness_preflight=_dimension(
            readiness,
            evidence_ref="evidence://readiness",
        ),
        trust_independence_review=_dimension(evidence_ref="evidence://trust"),
        independence_class=independence_class,
        claim_ceiling=(
            "no production-executor claim",
            "no High-Assurance claim",
            "no independent-validation claim",
        ),
    )


def test_same_system_profile_can_pass_without_becoming_independent() -> None:
    receipt = evaluate_assurance_profile(_profile())

    assert receipt.passed is True
    assert receipt.independence_class is IndependenceClass.SAME_SYSTEM
    assert receipt.authorization_effect == AUTHORIZATION_EFFECT_NONE
    assert receipt.certification_effect == CERTIFICATION_EFFECT_NONE
    assert receipt.unresolved_blockers == ()


def test_required_unknown_dimension_fails_closed() -> None:
    receipt = evaluate_assurance_profile(
        _profile(readiness=DimensionStatus.UNKNOWN)
    )

    assert receipt.passed is False
    assert "readiness/preflight:UNKNOWN" in receipt.unresolved_blockers
    assert receipt.authorization_effect == AUTHORIZATION_EFFECT_NONE


def test_unverified_independence_is_blocking_when_review_required() -> None:
    receipt = evaluate_assurance_profile(
        _profile(
            independence_class=IndependenceClass.INDEPENDENT_UNVERIFIED,
        )
    )

    assert receipt.passed is False
    assert "independence:INDEPENDENT_UNVERIFIED" in receipt.unresolved_blockers


def test_evidence_refs_are_deduplicated() -> None:
    shared = _dimension(evidence_ref="evidence://shared")
    profile = AssuranceProfileInput(
        profile_id="ASSURANCE-PROFILE-V0-DEDUPE",
        profile_version="v0-candidate",
        target_system="example",
        source_identity="source",
        runtime_identity="runtime",
        environment_identity="environment",
        material_source_manifest_ref=None,
        measurement_apparatus=shared,
        runtime_source_environment_binding=shared,
        authorization_decision_separation=shared,
        custody_replay_integrity=shared,
        readiness_preflight=shared,
        trust_independence_review=shared,
        independence_class=IndependenceClass.SAME_SYSTEM,
        claim_ceiling=("bounded",),
    )

    receipt = evaluate_assurance_profile(profile)

    assert receipt.evidence_refs == ("evidence://shared",)
