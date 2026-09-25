from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable


class TransactionState(str, Enum):
    PROPOSED = "PROPOSED"
    CANONICALIZED = "CANONICALIZED"
    EVIDENCE_GATHERING = "EVIDENCE_GATHERING"
    VERIFICATION_PENDING = "VERIFICATION_PENDING"
    VERIFIED = "VERIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    AUTHORIZED = "AUTHORIZED"
    PREPARED = "PREPARED"
    COMMIT_REVALIDATION = "COMMIT_REVALIDATION"
    COMMIT_REVALIDATED = "COMMIT_REVALIDATED"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    EXECUTION_OUTCOME_UNKNOWN = "EXECUTION_OUTCOME_UNKNOWN"
    POSTCONDITION_PENDING = "POSTCONDITION_PENDING"
    VERIFIED_POSTCONDITION = "VERIFIED_POSTCONDITION"
    POSTCONDITION_FAILED = "POSTCONDITION_FAILED"
    POSTCONDITION_INCONCLUSIVE = "POSTCONDITION_INCONCLUSIVE"
    CONTAINMENT = "CONTAINMENT"
    ROLLBACK_PENDING = "ROLLBACK_PENDING"
    COMPENSATION_PENDING = "COMPENSATION_PENDING"
    ROLLED_BACK = "ROLLED_BACK"
    COMPENSATED = "COMPENSATED"
    RECOVERY_FAILED = "RECOVERY_FAILED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"
    CLOSED = "CLOSED"


class TransitionRefusal(RuntimeError):
    pass


@dataclass(frozen=True)
class TransitionFacts:
    action_canonicalized: bool = False
    evidence_complete: bool = False
    required_verification_passed: bool = False
    verification_inconclusive: bool = False
    approval_required: bool = True
    approval_present: bool = False
    requester_approver_separated: bool = False
    authorization_active: bool = False
    authorization_scoped: bool = False
    delegation_non_widening: bool = False
    action_digest_matches: bool = False
    commit_guards_passed: bool = False
    authorization_consumed: bool = False
    idempotency_safe: bool = True
    execution_receipt_present: bool = False
    execution_outcome_unknown: bool = False
    postcondition_verified: bool = False
    postcondition_failed: bool = False
    postcondition_inconclusive: bool = False
    recovery_required: bool = False
    recovery_mode: str | None = None
    audit_recorded: bool = False


@dataclass(frozen=True)
class TransactionSnapshot:
    state: TransactionState
    facts: TransitionFacts


_TERMINAL = {
    TransactionState.REJECTED,
    TransactionState.FAILED,
    TransactionState.ESCALATED,
    TransactionState.CLOSED,
}
_ALLOWED: dict[TransactionState, frozenset[TransactionState]] = {
    TransactionState.PROPOSED: frozenset({TransactionState.CANONICALIZED, TransactionState.REJECTED}),
    TransactionState.CANONICALIZED: frozenset({TransactionState.EVIDENCE_GATHERING, TransactionState.REJECTED}),
    TransactionState.EVIDENCE_GATHERING: frozenset({TransactionState.VERIFICATION_PENDING, TransactionState.REJECTED}),
    TransactionState.VERIFICATION_PENDING: frozenset(
        {
            TransactionState.VERIFIED,
            TransactionState.INCONCLUSIVE,
            TransactionState.REJECTED,
        }
    ),
    TransactionState.VERIFIED: frozenset({TransactionState.APPROVAL_PENDING, TransactionState.AUTHORIZED}),
    TransactionState.INCONCLUSIVE: frozenset({TransactionState.ESCALATED, TransactionState.REJECTED}),
    TransactionState.APPROVAL_PENDING: frozenset({TransactionState.AUTHORIZED, TransactionState.REJECTED}),
    TransactionState.AUTHORIZED: frozenset({TransactionState.PREPARED, TransactionState.REJECTED}),
    TransactionState.PREPARED: frozenset({TransactionState.COMMIT_REVALIDATION, TransactionState.REJECTED}),
    TransactionState.COMMIT_REVALIDATION: frozenset(
        {
            TransactionState.COMMIT_REVALIDATED,
            TransactionState.REJECTED,
        }
    ),
    TransactionState.COMMIT_REVALIDATED: frozenset({TransactionState.EXECUTING, TransactionState.REJECTED}),
    TransactionState.EXECUTING: frozenset(
        {
            TransactionState.EXECUTED,
            TransactionState.EXECUTION_OUTCOME_UNKNOWN,
            TransactionState.FAILED,
        }
    ),
    TransactionState.EXECUTED: frozenset({TransactionState.POSTCONDITION_PENDING, TransactionState.CONTAINMENT}),
    TransactionState.EXECUTION_OUTCOME_UNKNOWN: frozenset({TransactionState.CONTAINMENT, TransactionState.ESCALATED}),
    TransactionState.POSTCONDITION_PENDING: frozenset(
        {
            TransactionState.VERIFIED_POSTCONDITION,
            TransactionState.POSTCONDITION_FAILED,
            TransactionState.POSTCONDITION_INCONCLUSIVE,
        }
    ),
    TransactionState.VERIFIED_POSTCONDITION: frozenset({TransactionState.CLOSED}),
    TransactionState.POSTCONDITION_FAILED: frozenset({TransactionState.CONTAINMENT, TransactionState.ESCALATED}),
    TransactionState.POSTCONDITION_INCONCLUSIVE: frozenset({TransactionState.CONTAINMENT, TransactionState.ESCALATED}),
    TransactionState.CONTAINMENT: frozenset(
        {
            TransactionState.ROLLBACK_PENDING,
            TransactionState.COMPENSATION_PENDING,
            TransactionState.ESCALATED,
        }
    ),
    TransactionState.ROLLBACK_PENDING: frozenset({TransactionState.ROLLED_BACK, TransactionState.RECOVERY_FAILED}),
    TransactionState.COMPENSATION_PENDING: frozenset({TransactionState.COMPENSATED, TransactionState.RECOVERY_FAILED}),
    TransactionState.ROLLED_BACK: frozenset({TransactionState.CLOSED}),
    TransactionState.COMPENSATED: frozenset({TransactionState.CLOSED}),
    TransactionState.RECOVERY_FAILED: frozenset({TransactionState.ESCALATED}),
    TransactionState.REJECTED: frozenset({TransactionState.CLOSED}),
    TransactionState.FAILED: frozenset({TransactionState.CLOSED, TransactionState.CONTAINMENT}),
    TransactionState.ESCALATED: frozenset({TransactionState.CLOSED}),
    TransactionState.CLOSED: frozenset(),
}


def allowed_targets(state: TransactionState) -> frozenset[TransactionState]:
    return _ALLOWED[state]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TransitionRefusal(message)


def validate_transition(snapshot: TransactionSnapshot, target: TransactionState) -> None:
    source = snapshot.state
    facts = snapshot.facts
    _require(target in _ALLOWED[source], f"illegal transition: {source.value} -> {target.value}")

    if target == TransactionState.CANONICALIZED:
        _require(facts.action_canonicalized, "canonical action is not established")
    elif target == TransactionState.VERIFICATION_PENDING:
        _require(facts.evidence_complete, "required evidence is incomplete")
    elif target == TransactionState.VERIFIED:
        _require(facts.required_verification_passed, "required verification did not pass")
        _require(not facts.verification_inconclusive, "verification remains inconclusive")
    elif target == TransactionState.INCONCLUSIVE:
        _require(facts.verification_inconclusive, "verification is not inconclusive")
    elif target == TransactionState.AUTHORIZED:
        _require(facts.required_verification_passed, "verification cannot be replaced by authorization")
        _require(facts.authorization_active, "authorization is inactive")
        _require(facts.authorization_scoped, "authorization scope is invalid")
        _require(facts.delegation_non_widening, "delegation widens authority")
        if facts.approval_required:
            _require(facts.approval_present, "required approval is absent")
            _require(facts.requester_approver_separated, "requester/approver separation failed")
            _require(facts.action_digest_matches, "approval digest does not match action")
    elif target == TransactionState.COMMIT_REVALIDATED:
        _require(facts.authorization_active, "authorization is inactive at commit")
        _require(not facts.authorization_consumed, "authorization is already consumed")
        _require(facts.action_digest_matches, "action digest changed before commit")
        _require(facts.commit_guards_passed, "commit-time guards failed")
        _require(facts.idempotency_safe, "idempotency state does not permit execution")
    elif target == TransactionState.EXECUTING:
        _require(source == TransactionState.COMMIT_REVALIDATED, "execution requires commit revalidation")
        _require(facts.authorization_active, "authorization is inactive at execution")
        _require(not facts.authorization_consumed, "authorization is already consumed")
        _require(facts.idempotency_safe, "replay/idempotency state blocks execution")
    elif target == TransactionState.EXECUTED:
        _require(facts.execution_receipt_present, "execution receipt is absent")
        _require(not facts.execution_outcome_unknown, "execution outcome remains unknown")
    elif target == TransactionState.EXECUTION_OUTCOME_UNKNOWN:
        _require(facts.execution_outcome_unknown, "execution outcome is not unknown")
    elif target == TransactionState.VERIFIED_POSTCONDITION:
        _require(facts.postcondition_verified, "postcondition is not verified")
    elif target == TransactionState.POSTCONDITION_FAILED:
        _require(facts.postcondition_failed, "postcondition failure is not established")
    elif target == TransactionState.POSTCONDITION_INCONCLUSIVE:
        _require(facts.postcondition_inconclusive, "postcondition is not inconclusive")
    elif target == TransactionState.ROLLBACK_PENDING:
        _require(facts.recovery_required, "recovery is not required")
        _require(facts.recovery_mode == "ROLLBACK", "rollback is not the selected recovery mode")
    elif target == TransactionState.COMPENSATION_PENDING:
        _require(facts.recovery_required, "recovery is not required")
        _require(facts.recovery_mode == "COMPENSATE", "compensation is not the selected recovery mode")
    elif target == TransactionState.CLOSED:
        _require(
            source in _TERMINAL
            or source
            in {
                TransactionState.VERIFIED_POSTCONDITION,
                TransactionState.ROLLED_BACK,
                TransactionState.COMPENSATED,
            },
            "closure source is not terminal",
        )
        _require(facts.audit_recorded, "audit record is required before closure")


def transition(snapshot: TransactionSnapshot, target: TransactionState) -> TransactionSnapshot:
    validate_transition(snapshot, target)
    return replace(snapshot, state=target)


def validate_trace(
    states: Iterable[TransactionState],
    facts_by_target: dict[TransactionState, TransitionFacts],
) -> TransactionSnapshot:
    sequence = tuple(states)
    if not sequence:
        raise ValueError("trace must contain at least one state")
    if sequence[0] != TransactionState.PROPOSED:
        raise TransitionRefusal("trace must start at PROPOSED")

    snapshot = TransactionSnapshot(TransactionState.PROPOSED, TransitionFacts())
    for target in sequence[1:]:
        snapshot = TransactionSnapshot(snapshot.state, facts_by_target.get(target, snapshot.facts))
        snapshot = transition(snapshot, target)
    return snapshot
