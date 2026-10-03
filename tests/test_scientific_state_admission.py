from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

from components.scientific_state_admission import (
    ScientificStateAdmissionError,
    evaluate_scientific_state_transition,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "schemas" / "scientific_state_transition_record.schema.json").read_text(
        encoding="utf-8"
    )
)


def record(*, transition_class="INDEPENDENT_EMPIRICAL_REPLICATION", delta=1):
    return {
        "schema_version": "dgaf.scientific-state-transition.v1",
        "transition_id": "sst:2026-10-03:001",
        "controller_issue": "#1264",
        "created_at": "2026-10-03T15:30:00Z",
        "prior_state": {
            "current_state_ref": "docs/CURRENT_STATE.md@de8dec1",
            "current_state_digest": "sha256:" + "a" * 64,
            "canonical_scientific_n": 0,
            "independent_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
        },
        "candidate_transition": {
            "transition_class": transition_class,
            "proposed_scientific_n_delta": delta,
            "proposed_independent_validation_effect": "NONE",
            "proposed_efficacy_effect": "NONE",
            "proposed_authorization_effect": "NONE",
            "exact_claim_scope": "one independently generated empirical replicate",
        },
        "protocol": {
            "protocol_id": "protocol:replication-v1",
            "protocol_revision": "sha256:" + "b" * 64,
            "preregistration_or_freeze_ref": "freeze:replication-v1",
            "countable_unit_definition": "one independently generated frozen-protocol replicate",
            "protocol_explicitly_allows_requested_transition": True,
        },
        "evidence": {
            "raw_evidence_refs": ["evidence://raw/replicate-001"],
            "exact_source_identities": ["sha256:" + "c" * 64],
            "environment_identities": ["env:replicate-001"],
            "custody_refs": ["custody://replicate-001"],
            "outcome_generation_established": True,
            "raw_evidence_retained": True,
            "exact_identity_binding_passed": True,
            "custody_and_provenance_passed": True,
            "duplicate_check_passed": True,
            "duplicate_or_replay_of": None,
            "validity_state": "VALID",
            "lane_specific_admission": "ACCEPTED",
            "blocking_defeaters": [],
        },
        "independence": {
            "independence_required_for_transition": True,
            "attribution_verified": True,
            "relationship_disclosure_ref": "disclosure://replicate-001",
            "independence_adjudication_ref": "adjudication://independence-001",
            "independence_state": "ESTABLISHED",
        },
        "adjudication": {
            "adjudicator_authority_ref": "authority://scientific-state-adjudicator",
            "decision": "ADMIT",
            "rationale": "all positive-N predicates satisfied for the bounded candidate",
            "adjudicated_at": "2026-10-03T15:31:00Z",
        },
        "history": {
            "invalidation_of": None,
            "history_preserving": False,
            "reason": None,
        },
        "result": {
            "resulting_scientific_n": max(0, delta),
            "resulting_independent_validation": "NOT_ESTABLISHED",
            "resulting_canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "resulting_high_assurance": "NOT_AUTHORIZED",
        },
    }


def verified(record_value):
    return evaluate_scientific_state_transition(
        record_value,
        current_state_verifier=lambda _: True,
        evidence_bundle_verifier=lambda _: True,
        adjudicator_authority_verifier=lambda _: True,
    )


def test_schema_accepts_complete_transition_record():
    errors = list(jsonschema.Draft202012Validator(SCHEMA).iter_errors(record()))
    assert errors == []


def test_positive_n_requires_all_external_verifiers():
    decision = evaluate_scientific_state_transition(record())

    assert decision.admitted is False
    assert decision.scientific_n_delta == 0
    assert "CURRENT_STATE_VERIFIER_REQUIRED" in decision.reasons
    assert "EVIDENCE_BUNDLE_VERIFIER_REQUIRED" in decision.reasons
    assert "ADJUDICATOR_AUTHORITY_VERIFIER_REQUIRED" in decision.reasons
    assert decision.authoritative_state_mutation is False


def test_independent_empirical_replication_can_be_record_admissible():
    decision = verified(record())

    assert decision.admitted is True
    assert decision.scientific_n_delta == 1
    assert decision.resulting_scientific_n == 1
    assert decision.independent_validation_effect == "NONE"
    assert decision.efficacy_effect == "NONE"
    assert decision.authorization_effect == "NONE"
    assert decision.authoritative_state_mutation is False


def test_same_system_evidence_cannot_increment_canonical_n():
    candidate = record(transition_class="SAME_SYSTEM_NONINDEPENDENT")
    decision = verified(candidate)

    assert decision.admitted is False
    assert decision.scientific_n_delta == 0
    assert "TRANSITION_CLASS_CANNOT_INCREMENT_CANONICAL_N" in decision.reasons
    assert "POSITIVE_N_REQUIRES_INDEPENDENT_EMPIRICAL_REPLICATION" in decision.reasons


def test_outside_operator_usability_does_not_become_scientific_n():
    candidate = record(transition_class="OUTSIDE_OPERATOR_USABILITY")
    decision = verified(candidate)

    assert decision.admitted is False
    assert "TRANSITION_CLASS_CANNOT_INCREMENT_CANONICAL_N" in decision.reasons


def test_unfamiliar_user_hci_does_not_become_scientific_n():
    candidate = record(transition_class="UNFAMILIAR_USER_HCI")
    decision = verified(candidate)

    assert decision.admitted is False
    assert "TRANSITION_CLASS_CANNOT_INCREMENT_CANONICAL_N" in decision.reasons


def test_duplicate_or_replay_cannot_increment_n():
    candidate = record()
    candidate["evidence"]["duplicate_or_replay_of"] = "sst:historical:001"
    decision = verified(candidate)

    assert decision.admitted is False
    assert "DUPLICATE_OR_REPLAY_CHECK_FAILED" in decision.reasons


def test_missing_independence_adjudication_fails_closed():
    candidate = record()
    candidate["independence"]["independence_state"] = "NOT_ESTABLISHED"
    candidate["independence"]["independence_adjudication_ref"] = None
    decision = verified(candidate)

    assert decision.admitted is False
    assert "REQUIRED_INDEPENDENCE_NOT_ESTABLISHED" in decision.reasons


def test_blocking_defeater_fails_closed():
    candidate = record()
    candidate["evidence"]["blocking_defeaters"] = ["custody ambiguity"]
    decision = verified(candidate)

    assert decision.admitted is False
    assert "BLOCKING_DEFEATER_ACTIVE" in decision.reasons


def test_rejected_adjudication_never_returns_state_effect():
    candidate = record()
    candidate["adjudication"]["decision"] = "REJECT"
    decision = verified(candidate)

    assert decision.admitted is False
    assert decision.scientific_n_delta == 0
    assert decision.resulting_scientific_n == 0
    assert "PROJECT_LEVEL_EFFECT_REQUIRES_ADMIT_DECISION" in decision.reasons
    assert "ADJUDICATION_REJECT" in decision.reasons


def test_resulting_n_must_equal_prior_plus_delta():
    candidate = record()
    candidate["result"]["resulting_scientific_n"] = 3
    decision = verified(candidate)

    assert decision.admitted is False
    assert "RESULTING_SCIENTIFIC_N_MISMATCH" in decision.reasons


def test_independent_validation_effect_is_separate_and_not_implemented_in_v1():
    candidate = record(transition_class="INDEPENDENT_REVIEW", delta=0)
    candidate["candidate_transition"]["proposed_independent_validation_effect"] = (
        "ESTABLISH_BOUNDED_REVIEW"
    )
    candidate["result"]["resulting_independent_validation"] = "BOUNDED_ESTABLISHED"
    decision = verified(candidate)

    assert decision.admitted is False
    assert "INDEPENDENT_VALIDATION_EFFECT_NOT_IMPLEMENTED_IN_V1" in decision.reasons
    assert "INDEPENDENT_VALIDATION_RESULT_CHANGED_WITHOUT_IMPLEMENTED_EFFECT" in decision.reasons


def test_zero_effect_engineering_record_can_be_admitted_without_n_change():
    candidate = record(transition_class="ENGINEERING_ASSURANCE", delta=0)
    candidate["protocol"]["protocol_explicitly_allows_requested_transition"] = False
    candidate["protocol"]["countable_unit_definition"] = "NOT_APPLICABLE"
    candidate["evidence"] = {
        "raw_evidence_refs": [],
        "exact_source_identities": [],
        "environment_identities": [],
        "custody_refs": [],
        "outcome_generation_established": False,
        "raw_evidence_retained": False,
        "exact_identity_binding_passed": False,
        "custody_and_provenance_passed": False,
        "duplicate_check_passed": False,
        "duplicate_or_replay_of": None,
        "validity_state": "INCONCLUSIVE",
        "lane_specific_admission": "NOT_APPLICABLE",
        "blocking_defeaters": [],
    }
    candidate["independence"] = {
        "independence_required_for_transition": False,
        "attribution_verified": False,
        "relationship_disclosure_ref": None,
        "independence_adjudication_ref": None,
        "independence_state": "NOT_APPLICABLE",
    }
    candidate["result"]["resulting_scientific_n"] = 0

    decision = evaluate_scientific_state_transition(candidate)

    assert decision.admitted is True
    assert decision.scientific_n_delta == 0
    assert decision.resulting_scientific_n == 0


def test_history_preserving_invalidation_can_decrement_only_explicitly():
    candidate = record(transition_class="INVALIDATION_RETRACTION", delta=-1)
    candidate["prior_state"]["canonical_scientific_n"] = 1
    candidate["result"]["resulting_scientific_n"] = 0
    candidate["history"] = {
        "invalidation_of": "sst:historical:counted-unit-001",
        "history_preserving": True,
        "reason": "later-discovered protocol defect invalidates current admissibility",
    }
    decision = verified(candidate)

    assert decision.admitted is True
    assert decision.scientific_n_delta == -1
    assert decision.resulting_scientific_n == 0


def test_silent_negative_delta_is_rejected():
    candidate = record(transition_class="ENGINEERING_ASSURANCE", delta=-1)
    candidate["prior_state"]["canonical_scientific_n"] = 1
    candidate["result"]["resulting_scientific_n"] = 0
    decision = verified(candidate)

    assert decision.admitted is False
    assert "NEGATIVE_N_REQUIRES_INVALIDATION_RETRACTION_CLASS" in decision.reasons


def test_invalidation_requires_history_preservation():
    candidate = record(transition_class="INVALIDATION_RETRACTION", delta=-1)
    candidate["prior_state"]["canonical_scientific_n"] = 1
    candidate["result"]["resulting_scientific_n"] = 0
    decision = verified(candidate)

    assert decision.admitted is False
    assert "HISTORY_PRESERVING_INVALIDATION_RECORD_REQUIRED" in decision.reasons


def test_external_verifier_failure_is_fail_closed():
    decision = evaluate_scientific_state_transition(
        record(),
        current_state_verifier=lambda _: True,
        evidence_bundle_verifier=lambda _: False,
        adjudicator_authority_verifier=lambda _: True,
    )

    assert decision.admitted is False
    assert "EVIDENCE_BUNDLE_VERIFICATION_FAILED" in decision.reasons


def test_bad_shape_raises_before_any_admission_decision():
    candidate = copy.deepcopy(record())
    candidate["prior_state"]["canonical_scientific_n"] = "0"

    try:
        evaluate_scientific_state_transition(candidate)
    except ScientificStateAdmissionError as exc:
        assert "must be integer" in str(exc)
    else:
        raise AssertionError("invalid shape must fail closed")
