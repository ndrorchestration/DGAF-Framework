"""Fail-closed scientific-state transition admission.

This module validates a caller-supplied Scientific State Transition Record.
It never discovers evidence, edits CURRENT_STATE.md, executes experiments, or
mutates canonical scientific state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SCIENTIFIC_STATE_TRANSITION_SCHEMA_VERSION = "dgaf.scientific-state-transition.v1"

TRANSITION_CLASSES = frozenset(
    {
        "ENGINEERING_ASSURANCE",
        "SAME_SYSTEM_NONINDEPENDENT",
        "OUTSIDE_OPERATOR_USABILITY",
        "UNFAMILIAR_USER_HCI",
        "INDEPENDENT_REVIEW",
        "INDEPENDENT_EMPIRICAL_REPLICATION",
        "INVALIDATION_RETRACTION",
    }
)

NON_N_PROMOTING_CLASSES = frozenset(
    {
        "ENGINEERING_ASSURANCE",
        "SAME_SYSTEM_NONINDEPENDENT",
        "OUTSIDE_OPERATOR_USABILITY",
        "UNFAMILIAR_USER_HCI",
        "INDEPENDENT_REVIEW",
    }
)


@dataclass(frozen=True)
class ScientificStateAdmissionDecision:
    transition_id: str
    admitted: bool
    scientific_n_delta: int
    independent_validation_effect: str
    efficacy_effect: str
    authorization_effect: str
    resulting_scientific_n: int
    reasons: tuple[str, ...]
    authoritative_state_mutation: bool = False

    def __post_init__(self) -> None:
        if self.authoritative_state_mutation is not False:
            raise ValueError("scientific-state admission decision cannot mutate canonical state")


class ScientificStateAdmissionError(ValueError):
    pass


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ScientificStateAdmissionError(f"{field} must be a mapping")
    return value


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ScientificStateAdmissionError(f"{field} must not be blank")
    return value.strip()


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ScientificStateAdmissionError(f"{field} must be boolean")
    return value


def _int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ScientificStateAdmissionError(f"{field} must be integer")
    return value


def _string_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ScientificStateAdmissionError(f"{field} must be a list")
    items = tuple(_required_text(item, f"{field}[]") for item in value)
    return items


def _effect_is_none(value: str) -> bool:
    return value == "NONE"


def evaluate_scientific_state_transition(
    record: Mapping[str, Any],
) -> ScientificStateAdmissionDecision:
    """Evaluate one transition record without mutating project state."""

    root = _mapping(record, "record")
    schema_version = _required_text(root.get("schema_version"), "schema_version")
    if schema_version != SCIENTIFIC_STATE_TRANSITION_SCHEMA_VERSION:
        raise ScientificStateAdmissionError("unsupported schema_version")

    transition_id = _required_text(root.get("transition_id"), "transition_id")
    _required_text(root.get("controller_issue"), "controller_issue")
    _required_text(root.get("created_at"), "created_at")

    prior = _mapping(root.get("prior_state"), "prior_state")
    candidate = _mapping(root.get("candidate_transition"), "candidate_transition")
    protocol = _mapping(root.get("protocol"), "protocol")
    evidence = _mapping(root.get("evidence"), "evidence")
    independence = _mapping(root.get("independence"), "independence")
    adjudication = _mapping(root.get("adjudication"), "adjudication")
    history = _mapping(root.get("history"), "history")
    result = _mapping(root.get("result"), "result")

    _required_text(prior.get("current_state_ref"), "prior_state.current_state_ref")
    _required_text(prior.get("current_state_digest"), "prior_state.current_state_digest")
    prior_n = _int(prior.get("canonical_scientific_n"), "prior_state.canonical_scientific_n")
    if prior_n < 0:
        raise ScientificStateAdmissionError("prior scientific N must be non-negative")
    prior_independent = _required_text(
        prior.get("independent_validation"), "prior_state.independent_validation"
    )
    prior_efficacy = _required_text(
        prior.get("canonical_dgaf_efficacy"), "prior_state.canonical_dgaf_efficacy"
    )
    prior_high_assurance = _required_text(
        prior.get("high_assurance"), "prior_state.high_assurance"
    )

    transition_class = _required_text(
        candidate.get("transition_class"), "candidate_transition.transition_class"
    )
    if transition_class not in TRANSITION_CLASSES:
        raise ScientificStateAdmissionError("unsupported transition_class")

    proposed_delta = _int(
        candidate.get("proposed_scientific_n_delta"),
        "candidate_transition.proposed_scientific_n_delta",
    )
    independent_effect = _required_text(
        candidate.get("proposed_independent_validation_effect"),
        "candidate_transition.proposed_independent_validation_effect",
    )
    efficacy_effect = _required_text(
        candidate.get("proposed_efficacy_effect"),
        "candidate_transition.proposed_efficacy_effect",
    )
    authorization_effect = _required_text(
        candidate.get("proposed_authorization_effect"),
        "candidate_transition.proposed_authorization_effect",
    )
    _required_text(candidate.get("exact_claim_scope"), "candidate_transition.exact_claim_scope")

    _required_text(protocol.get("protocol_id"), "protocol.protocol_id")
    _required_text(protocol.get("protocol_revision"), "protocol.protocol_revision")
    _required_text(
        protocol.get("preregistration_or_freeze_ref"),
        "protocol.preregistration_or_freeze_ref",
    )
    countable_unit = _required_text(
        protocol.get("countable_unit_definition"),
        "protocol.countable_unit_definition",
    )
    protocol_allows = _bool(
        protocol.get("protocol_explicitly_allows_requested_transition"),
        "protocol.protocol_explicitly_allows_requested_transition",
    )

    raw_refs = _string_list(evidence.get("raw_evidence_refs"), "evidence.raw_evidence_refs")
    source_ids = _string_list(
        evidence.get("exact_source_identities"), "evidence.exact_source_identities"
    )
    environment_ids = _string_list(
        evidence.get("environment_identities"), "evidence.environment_identities"
    )
    custody_refs = _string_list(evidence.get("custody_refs"), "evidence.custody_refs")
    outcome_generated = _bool(
        evidence.get("outcome_generation_established"),
        "evidence.outcome_generation_established",
    )
    raw_retained = _bool(
        evidence.get("raw_evidence_retained"), "evidence.raw_evidence_retained"
    )
    identity_passed = _bool(
        evidence.get("exact_identity_binding_passed"),
        "evidence.exact_identity_binding_passed",
    )
    custody_passed = _bool(
        evidence.get("custody_and_provenance_passed"),
        "evidence.custody_and_provenance_passed",
    )
    duplicate_passed = _bool(
        evidence.get("duplicate_check_passed"), "evidence.duplicate_check_passed"
    )
    duplicate_of = evidence.get("duplicate_or_replay_of")
    if duplicate_of is not None:
        _required_text(duplicate_of, "evidence.duplicate_or_replay_of")
    validity_state = _required_text(evidence.get("validity_state"), "evidence.validity_state")
    if validity_state not in {"VALID", "INVALID", "INCONCLUSIVE"}:
        raise ScientificStateAdmissionError("unsupported evidence validity_state")
    lane_admission = _required_text(
        evidence.get("lane_specific_admission"), "evidence.lane_specific_admission"
    )
    if lane_admission not in {"ACCEPTED", "REJECTED", "NOT_APPLICABLE", "INCONCLUSIVE"}:
        raise ScientificStateAdmissionError("unsupported lane_specific_admission")
    blockers = _string_list(evidence.get("blocking_defeaters"), "evidence.blocking_defeaters")

    independence_required = _bool(
        independence.get("independence_required_for_transition"),
        "independence.independence_required_for_transition",
    )
    attribution_verified = _bool(
        independence.get("attribution_verified"), "independence.attribution_verified"
    )
    relationship_ref = independence.get("relationship_disclosure_ref")
    if relationship_ref is not None:
        _required_text(relationship_ref, "independence.relationship_disclosure_ref")
    independence_ref = independence.get("independence_adjudication_ref")
    if independence_ref is not None:
        _required_text(independence_ref, "independence.independence_adjudication_ref")
    independence_state = _required_text(
        independence.get("independence_state"), "independence.independence_state"
    )
    if independence_state not in {
        "ESTABLISHED",
        "NOT_ESTABLISHED",
        "NOT_APPLICABLE",
        "INCONCLUSIVE",
    }:
        raise ScientificStateAdmissionError("unsupported independence_state")

    _required_text(
        adjudication.get("adjudicator_authority_ref"),
        "adjudication.adjudicator_authority_ref",
    )
    adjudication_decision = _required_text(adjudication.get("decision"), "adjudication.decision")
    if adjudication_decision not in {"ADMIT", "REJECT", "INCONCLUSIVE"}:
        raise ScientificStateAdmissionError("unsupported adjudication decision")
    _required_text(adjudication.get("rationale"), "adjudication.rationale")
    _required_text(adjudication.get("adjudicated_at"), "adjudication.adjudicated_at")

    invalidation_of = history.get("invalidation_of")
    if invalidation_of is not None:
        _required_text(invalidation_of, "history.invalidation_of")
    history_preserving = _bool(history.get("history_preserving"), "history.history_preserving")
    history_reason = history.get("reason")
    if history_reason is not None:
        _required_text(history_reason, "history.reason")

    resulting_n = _int(result.get("resulting_scientific_n"), "result.resulting_scientific_n")
    if resulting_n < 0:
        raise ScientificStateAdmissionError("resulting scientific N must be non-negative")
    resulting_independent = _required_text(
        result.get("resulting_independent_validation"),
        "result.resulting_independent_validation",
    )
    resulting_efficacy = _required_text(
        result.get("resulting_canonical_dgaf_efficacy"),
        "result.resulting_canonical_dgaf_efficacy",
    )
    resulting_high_assurance = _required_text(
        result.get("resulting_high_assurance"), "result.resulting_high_assurance"
    )

    reasons: list[str] = []

    # v1 machine semantics implement N-only transitions. Other project-level
    # effects remain separate and fail closed until independently specified.
    if not _effect_is_none(independent_effect):
        reasons.append("INDEPENDENT_VALIDATION_EFFECT_NOT_IMPLEMENTED_IN_V1")
    if not _effect_is_none(efficacy_effect):
        reasons.append("EFFICACY_EFFECT_NOT_IMPLEMENTED_IN_V1")
    if not _effect_is_none(authorization_effect):
        reasons.append("AUTHORIZATION_EFFECT_NOT_IMPLEMENTED_IN_V1")
    if resulting_independent != prior_independent:
        reasons.append("INDEPENDENT_VALIDATION_RESULT_CHANGED_WITHOUT_IMPLEMENTED_EFFECT")
    if resulting_efficacy != prior_efficacy:
        reasons.append("EFFICACY_RESULT_CHANGED_WITHOUT_IMPLEMENTED_EFFECT")
    if resulting_high_assurance != prior_high_assurance:
        reasons.append("HIGH_ASSURANCE_RESULT_CHANGED_WITHOUT_IMPLEMENTED_EFFECT")

    if transition_class in NON_N_PROMOTING_CLASSES and proposed_delta != 0:
        reasons.append("TRANSITION_CLASS_CANNOT_INCREMENT_CANONICAL_N")

    if proposed_delta > 0:
        if transition_class != "INDEPENDENT_EMPIRICAL_REPLICATION":
            reasons.append("POSITIVE_N_REQUIRES_INDEPENDENT_EMPIRICAL_REPLICATION")
        if not protocol_allows:
            reasons.append("PROTOCOL_DOES_NOT_ALLOW_REQUESTED_TRANSITION")
        if countable_unit == "NOT_APPLICABLE":
            reasons.append("COUNTABLE_UNIT_NOT_DEFINED")
        if not outcome_generated:
            reasons.append("EMPIRICAL_OUTCOME_GENERATION_NOT_ESTABLISHED")
        if not raw_refs or not raw_retained:
            reasons.append("RAW_EVIDENCE_NOT_RETAINED")
        if not source_ids or not environment_ids or not identity_passed:
            reasons.append("EXACT_IDENTITY_BINDING_NOT_ESTABLISHED")
        if not custody_refs or not custody_passed:
            reasons.append("CUSTODY_OR_PROVENANCE_NOT_ESTABLISHED")
        if not duplicate_passed or duplicate_of is not None:
            reasons.append("DUPLICATE_OR_REPLAY_CHECK_FAILED")
        if validity_state != "VALID":
            reasons.append("PROTOCOL_VALIDITY_NOT_VALID")
        if lane_admission != "ACCEPTED":
            reasons.append("LANE_SPECIFIC_ADMISSION_NOT_ACCEPTED")
        if blockers:
            reasons.append("BLOCKING_DEFEATER_ACTIVE")
        if not independence_required:
            reasons.append("POSITIVE_N_REQUIRES_EXPLICIT_INDEPENDENCE_REQUIREMENT")
        if (
            not attribution_verified
            or relationship_ref is None
            or independence_ref is None
            or independence_state != "ESTABLISHED"
        ):
            reasons.append("REQUIRED_INDEPENDENCE_NOT_ESTABLISHED")

    if proposed_delta < 0:
        if transition_class != "INVALIDATION_RETRACTION":
            reasons.append("NEGATIVE_N_REQUIRES_INVALIDATION_RETRACTION_CLASS")
        if not protocol_allows:
            reasons.append("PROTOCOL_DOES_NOT_ALLOW_REQUESTED_TRANSITION")
        if invalidation_of is None or not history_preserving or history_reason is None:
            reasons.append("HISTORY_PRESERVING_INVALIDATION_RECORD_REQUIRED")
        if validity_state != "VALID":
            reasons.append("INVALIDATION_EVIDENCE_NOT_VALID")
        if lane_admission != "ACCEPTED":
            reasons.append("INVALIDATION_NOT_ACCEPTED_BY_GOVERNING_LANE")
        if not raw_refs or not raw_retained or not identity_passed or not custody_passed:
            reasons.append("INVALIDATION_EVIDENCE_CHAIN_INCOMPLETE")
        if blockers:
            reasons.append("BLOCKING_DEFEATER_ACTIVE")

    if proposed_delta == 0 and transition_class == "INVALIDATION_RETRACTION":
        if invalidation_of is None or not history_preserving or history_reason is None:
            reasons.append("HISTORY_PRESERVING_INVALIDATION_RECORD_REQUIRED")

    requested_effect = (
        proposed_delta != 0
        or not _effect_is_none(independent_effect)
        or not _effect_is_none(efficacy_effect)
        or not _effect_is_none(authorization_effect)
    )
    if requested_effect and adjudication_decision != "ADMIT":
        reasons.append("PROJECT_LEVEL_EFFECT_REQUIRES_ADMIT_DECISION")

    expected_n = prior_n + proposed_delta
    if expected_n < 0:
        reasons.append("SCIENTIFIC_N_CANNOT_BECOME_NEGATIVE")
    elif resulting_n != expected_n:
        reasons.append("RESULTING_SCIENTIFIC_N_MISMATCH")

    if reasons:
        admitted = False
    else:
        admitted = adjudication_decision == "ADMIT"

    return ScientificStateAdmissionDecision(
        transition_id=transition_id,
        admitted=admitted,
        scientific_n_delta=proposed_delta if admitted else 0,
        independent_validation_effect=independent_effect if admitted else "NONE",
        efficacy_effect=efficacy_effect if admitted else "NONE",
        authorization_effect=authorization_effect if admitted else "NONE",
        resulting_scientific_n=resulting_n if admitted else prior_n,
        reasons=tuple(reasons),
    )
