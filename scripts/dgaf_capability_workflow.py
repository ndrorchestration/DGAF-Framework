from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class RecoveryClass(str, Enum):
    REVERSIBLE = "REVERSIBLE"
    COMPENSATABLE = "COMPENSATABLE"
    IRREVERSIBLE = "IRREVERSIBLE"


class ExecutionState(str, Enum):
    NEW = "NEW"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    EXECUTION_OUTCOME_UNKNOWN = "EXECUTION_OUTCOME_UNKNOWN"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"


class PostconditionState(str, Enum):
    NOT_CHECKED = "NOT_CHECKED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class WorkflowStep:
    node_id: str
    capability_id: str
    access: str
    sensitivity_in: frozenset[str]
    externality: str
    destination_class: str | None = None
    recovery: RecoveryClass = RecoveryClass.REVERSIBLE


@dataclass(frozen=True)
class WorkflowOutcome:
    execution_state: ExecutionState
    postcondition_state: PostconditionState
    recovery_required: bool
    recovery_mode: str | None


def prohibited_sensitive_egress(
    steps: Iterable[WorkflowStep],
    *,
    protected_labels: frozenset[str],
    allowed_destinations: frozenset[str],
) -> bool:
    accumulated: set[str] = set()
    for step in steps:
        accumulated.update(step.sensitivity_in)
        if step.access in {"write", "delete", "privilege_change"} and step.externality == "external":
            if accumulated.intersection(protected_labels):
                if step.destination_class not in allowed_destinations:
                    return True
    return False


def composed_workflow_permitted(
    steps: Iterable[WorkflowStep],
    *,
    individually_authorized: bool,
    composition_authorized: bool,
    protected_labels: frozenset[str] = frozenset(),
    allowed_destinations: frozenset[str] = frozenset(),
) -> bool:
    if not individually_authorized:
        return False
    if not composition_authorized:
        return False
    return not prohibited_sensitive_egress(
        steps,
        protected_labels=protected_labels,
        allowed_destinations=allowed_destinations,
    )


def execution_established(
    *,
    execution_state: ExecutionState,
    provider_receipt_present: bool,
) -> bool:
    return (
        execution_state == ExecutionState.EXECUTED
        and provider_receipt_present
    )


def classify_outcome(
    *,
    completed_steps: int,
    total_steps: int,
    provider_outcome_known: bool,
    postcondition_state: PostconditionState,
    recovery_classes: Iterable[RecoveryClass],
) -> WorkflowOutcome:
    recovery_classes = tuple(recovery_classes)

    if not provider_outcome_known:
        return WorkflowOutcome(
            execution_state=ExecutionState.EXECUTION_OUTCOME_UNKNOWN,
            postcondition_state=postcondition_state,
            recovery_required=False,
            recovery_mode="RECONCILE",
        )

    if completed_steps == 0:
        return WorkflowOutcome(
            execution_state=ExecutionState.FAILED,
            postcondition_state=postcondition_state,
            recovery_required=False,
            recovery_mode=None,
        )

    if completed_steps < total_steps:
        if RecoveryClass.IRREVERSIBLE in recovery_classes[:completed_steps]:
            mode = "CONTAIN_OR_ESCALATE"
        elif RecoveryClass.COMPENSATABLE in recovery_classes[:completed_steps]:
            mode = "COMPENSATE"
        else:
            mode = "ROLLBACK"
        return WorkflowOutcome(
            execution_state=ExecutionState.PARTIALLY_EXECUTED,
            postcondition_state=postcondition_state,
            recovery_required=True,
            recovery_mode=mode,
        )

    if postcondition_state in {PostconditionState.FAILED, PostconditionState.INCONCLUSIVE}:
        if RecoveryClass.IRREVERSIBLE in recovery_classes:
            mode = "CONTAIN_OR_ESCALATE"
        elif RecoveryClass.COMPENSATABLE in recovery_classes:
            mode = "COMPENSATE"
        else:
            mode = "ROLLBACK"
        return WorkflowOutcome(
            execution_state=ExecutionState.EXECUTED,
            postcondition_state=postcondition_state,
            recovery_required=True,
            recovery_mode=mode,
        )

    return WorkflowOutcome(
        execution_state=ExecutionState.EXECUTED,
        postcondition_state=postcondition_state,
        recovery_required=False,
        recovery_mode=None,
    )
