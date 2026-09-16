import pytest

from dgaf_discovery.validity import (
    DependencyEdge,
    DependencyRelation,
    ImpactDisposition,
    ValidityEvent,
    ValidityState,
    compute_validity_impact,
    validate_validity_event,
)


def invalidation_event(subject_ref="validator:v1"):
    return ValidityEvent(
        event_id="event:validator-v1-invalid",
        subject_ref=subject_ref,
        prior_state=ValidityState.ACTIVE,
        new_state=ValidityState.INVALIDATED,
        cause_code="VALIDATOR_DEFECT",
        evidence_refs=("test://validator-defect",),
        authority_scope="synthetic-assurance-fixture",
        decision_ref="decision://synthetic-owner",
    )


def test_required_dependency_propagates_to_reverification_then_suspension():
    edges = (
        DependencyEdge("validator:v1", "receipt:r1", DependencyRelation.REQUIRES_VALIDITY, "policy://required"),
        DependencyEdge("receipt:r1", "claim:c1", DependencyRelation.SUPPORTS_REQUIRED, "policy://support"),
    )
    result = compute_validity_impact(invalidation_event(), edges)
    assert result.disposition_for("receipt:r1") is ImpactDisposition.REVERIFY
    assert result.disposition_for("claim:c1") is ImpactDisposition.SUSPEND
    assert result.unresolved_paths == ()


def test_reference_and_lineage_edges_preserve_history_and_stop_propagation():
    edges = (
        DependencyEdge("validator:v1", "historical:h1", DependencyRelation.REFERENCES, "policy://reference"),
        DependencyEdge("validator:v1", "lineage:l1", DependencyRelation.LINEAGE, "policy://lineage"),
        DependencyEdge("historical:h1", "claim:unreached", DependencyRelation.SUPPORTS_REQUIRED, "policy://downstream"),
    )
    result = compute_validity_impact(invalidation_event(), edges)
    assert result.disposition_for("historical:h1") is ImpactDisposition.NO_EFFECT
    assert result.disposition_for("lineage:l1") is ImpactDisposition.NO_EFFECT
    assert result.disposition_for("claim:unreached") is None


def test_projection_dependency_becomes_stale_without_back_propagation():
    edges = (
        DependencyEdge("claim:c1", "projection:p1", DependencyRelation.PRESENTS, "policy://projection"),
        DependencyEdge("source:authority", "claim:c1", DependencyRelation.SUPPORTS_REQUIRED, "policy://source"),
    )
    result = compute_validity_impact(invalidation_event("claim:c1"), edges)
    assert result.disposition_for("projection:p1") is ImpactDisposition.STALE_PROJECTION
    assert result.disposition_for("source:authority") is None


def test_contributory_support_requires_reverification_not_auto_invalidation():
    edges = (
        DependencyEdge("evidence:e1", "claim:c1", DependencyRelation.SUPPORTS_CONTRIBUTORY, "policy://contributory"),
    )
    result = compute_validity_impact(invalidation_event("evidence:e1"), edges)
    assert result.disposition_for("claim:c1") is ImpactDisposition.REVERIFY
    assert result.disposition_for("claim:c1") is not ImpactDisposition.INVALIDATE


def test_ambiguous_relations_fail_closed_as_unresolved():
    edges = (
        DependencyEdge("claim:c1", "claim:c2", DependencyRelation.DEFEATS, "policy://defeater"),
    )
    result = compute_validity_impact(invalidation_event("claim:c1"), edges)
    assert result.disposition_for("claim:c2") is None
    assert len(result.unresolved_paths) == 1
    assert "DEFEATS" in result.unresolved_paths[0]
    assert result.authoritative_effect == "NONE"
    assert result.scientific_state_effect == "NONE"
    assert result.scientific_n_increment == 0


def test_validity_event_requires_evidence_and_decision_identity():
    with pytest.raises(ValueError, match="evidence_refs"):
        validate_validity_event(
            ValidityEvent(
                event_id="event:bad",
                subject_ref="validator:v1",
                prior_state=ValidityState.ACTIVE,
                new_state=ValidityState.INVALIDATED,
                cause_code="VALIDATOR_DEFECT",
                evidence_refs=(),
                authority_scope="synthetic-assurance-fixture",
                decision_ref="decision://synthetic-owner",
            )
        )
    with pytest.raises(ValueError, match="decision_ref"):
        validate_validity_event(
            ValidityEvent(
                event_id="event:bad-2",
                subject_ref="validator:v1",
                prior_state=ValidityState.ACTIVE,
                new_state=ValidityState.INVALIDATED,
                cause_code="VALIDATOR_DEFECT",
                evidence_refs=("test://validator-defect",),
                authority_scope="synthetic-assurance-fixture",
                decision_ref="",
            )
        )


def test_runtime_enum_strings_are_rejected_fail_closed():
    with pytest.raises(ValueError, match="new_state"):
        validate_validity_event(
            ValidityEvent(
                event_id="event:bad-state",
                subject_ref="validator:v1",
                prior_state=ValidityState.ACTIVE,
                new_state="INVALIDATED",  # type: ignore[arg-type]
                cause_code="VALIDATOR_DEFECT",
                evidence_refs=("test://validator-defect",),
                authority_scope="synthetic-assurance-fixture",
                decision_ref="decision://synthetic-owner",
            )
        )


def test_active_events_do_not_trigger_invalidation_traversal():
    event = ValidityEvent(
        event_id="event:active",
        subject_ref="validator:v1",
        prior_state=ValidityState.INVALIDATED,
        new_state=ValidityState.ACTIVE,
        cause_code="REVALIDATED_BY_OWNER",
        evidence_refs=("test://fresh-revalidation",),
        authority_scope="synthetic-assurance-fixture",
        decision_ref="decision://synthetic-owner",
    )
    with pytest.raises(ValueError, match="INVALIDATED or SUPERSEDED"):
        compute_validity_impact(event, ())
