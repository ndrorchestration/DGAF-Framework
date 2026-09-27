from __future__ import annotations

import pytest

from scripts.dgaf_capability_state_machine import (
    TransactionSnapshot,
    TransactionState,
    TransitionFacts,
    TransitionRefusal,
    allowed_targets,
    transition,
    validate_trace,
)


def facts(**changes):
    base = dict(
        action_canonicalized=True,
        evidence_complete=True,
        required_verification_passed=True,
        verification_inconclusive=False,
        approval_required=True,
        approval_present=True,
        requester_approver_separated=True,
        authorization_active=True,
        authorization_scoped=True,
        delegation_non_widening=True,
        action_digest_matches=True,
        commit_guards_passed=True,
        authorization_consumed=False,
        idempotency_safe=True,
        execution_receipt_present=True,
        execution_outcome_unknown=False,
        postcondition_verified=True,
        postcondition_failed=False,
        postcondition_inconclusive=False,
        recovery_required=False,
        recovery_mode=None,
        audit_recorded=True,
    )
    base.update(changes)
    return TransitionFacts(**base)


def snap(state, **changes):
    return TransactionSnapshot(state=state, facts=facts(**changes))


def test_nominal_state_graph_reaches_closed():
    sequence = [
        TransactionState.PROPOSED,
        TransactionState.CANONICALIZED,
        TransactionState.EVIDENCE_GATHERING,
        TransactionState.VERIFICATION_PENDING,
        TransactionState.VERIFIED,
        TransactionState.APPROVAL_PENDING,
        TransactionState.AUTHORIZED,
        TransactionState.PREPARED,
        TransactionState.COMMIT_REVALIDATION,
        TransactionState.COMMIT_REVALIDATED,
        TransactionState.EXECUTING,
        TransactionState.EXECUTED,
        TransactionState.POSTCONDITION_PENDING,
        TransactionState.VERIFIED_POSTCONDITION,
        TransactionState.CLOSED,
    ]
    result = validate_trace(sequence, {state: facts() for state in sequence[1:]})
    assert result.state == TransactionState.CLOSED


def test_execution_cannot_skip_commit_revalidation():
    assert TransactionState.EXECUTING not in allowed_targets(TransactionState.AUTHORIZED)
    with pytest.raises(TransitionRefusal, match="illegal transition"):
        transition(snap(TransactionState.AUTHORIZED), TransactionState.EXECUTING)


def test_failed_verification_cannot_become_verified():
    with pytest.raises(TransitionRefusal, match="verification did not pass"):
        transition(
            snap(TransactionState.VERIFICATION_PENDING, required_verification_passed=False),
            TransactionState.VERIFIED,
        )


def test_inconclusive_verification_cannot_become_verified():
    with pytest.raises(TransitionRefusal, match="inconclusive"):
        transition(
            snap(TransactionState.VERIFICATION_PENDING, verification_inconclusive=True),
            TransactionState.VERIFIED,
        )


@pytest.mark.parametrize(
    "change, message",
    [
        ({"authorization_active": False}, "inactive"),
        ({"authorization_scoped": False}, "scope"),
        ({"delegation_non_widening": False}, "widens"),
        ({"approval_present": False}, "approval is absent"),
        ({"requester_approver_separated": False}, "separation"),
        ({"action_digest_matches": False}, "digest"),
    ],
)
def test_authorization_guards_fail_closed(change, message):
    with pytest.raises(TransitionRefusal, match=message):
        transition(
            snap(TransactionState.APPROVAL_PENDING, **change),
            TransactionState.AUTHORIZED,
        )


@pytest.mark.parametrize(
    "change, message",
    [
        ({"authorization_active": False}, "inactive at commit"),
        ({"authorization_consumed": True}, "already consumed"),
        ({"action_digest_matches": False}, "digest changed"),
        ({"commit_guards_passed": False}, "guards failed"),
        ({"idempotency_safe": False}, "idempotency"),
    ],
)
def test_commit_revalidation_guards_fail_closed(change, message):
    with pytest.raises(TransitionRefusal, match=message):
        transition(
            snap(TransactionState.COMMIT_REVALIDATION, **change),
            TransactionState.COMMIT_REVALIDATED,
        )


def test_execution_requires_receipt():
    with pytest.raises(TransitionRefusal, match="receipt"):
        transition(
            snap(TransactionState.EXECUTING, execution_receipt_present=False),
            TransactionState.EXECUTED,
        )


def test_unknown_execution_outcome_is_explicit():
    result = transition(
        snap(TransactionState.EXECUTING, execution_outcome_unknown=True),
        TransactionState.EXECUTION_OUTCOME_UNKNOWN,
    )
    assert result.state == TransactionState.EXECUTION_OUTCOME_UNKNOWN
    assert TransactionState.EXECUTING not in allowed_targets(result.state)


def test_postcondition_failure_preserves_executed_history():
    current = transition(snap(TransactionState.EXECUTED), TransactionState.POSTCONDITION_PENDING)
    current = TransactionSnapshot(
        current.state,
        facts(postcondition_verified=False, postcondition_failed=True),
    )
    current = transition(current, TransactionState.POSTCONDITION_FAILED)
    assert current.state == TransactionState.POSTCONDITION_FAILED


def test_failed_postcondition_can_enter_compensation():
    current = transition(
        snap(TransactionState.POSTCONDITION_FAILED, recovery_required=True, recovery_mode="COMPENSATE"),
        TransactionState.CONTAINMENT,
    )
    current = transition(
        TransactionSnapshot(
            current.state,
            facts(recovery_required=True, recovery_mode="COMPENSATE"),
        ),
        TransactionState.COMPENSATION_PENDING,
    )
    assert current.state == TransactionState.COMPENSATION_PENDING


def test_closure_requires_audit_record():
    with pytest.raises(TransitionRefusal, match="audit"):
        transition(
            snap(TransactionState.VERIFIED_POSTCONDITION, audit_recorded=False),
            TransactionState.CLOSED,
        )


def test_rejected_transaction_can_close_only_with_audit():
    result = transition(
        snap(TransactionState.REJECTED, audit_recorded=True),
        TransactionState.CLOSED,
    )
    assert result.state == TransactionState.CLOSED


def test_trace_must_start_proposed():
    with pytest.raises(TransitionRefusal, match="start at PROPOSED"):
        validate_trace(
            [TransactionState.AUTHORIZED, TransactionState.PREPARED],
            {},
        )


def test_unknown_outcome_routes_to_containment_not_direct_execute():
    targets = allowed_targets(TransactionState.EXECUTION_OUTCOME_UNKNOWN)
    assert TransactionState.CONTAINMENT in targets
    assert TransactionState.ESCALATED in targets
    assert TransactionState.EXECUTING not in targets
    assert TransactionState.EXECUTED not in targets


def test_consumed_authorization_blocks_execution_even_after_prior_commit():
    with pytest.raises(TransitionRefusal, match="already consumed"):
        transition(
            snap(TransactionState.COMMIT_REVALIDATED, authorization_consumed=True),
            TransactionState.EXECUTING,
        )
