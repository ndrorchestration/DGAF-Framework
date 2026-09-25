from __future__ import annotations

from scripts.dgaf_capability_workflow import (
    ExecutionState,
    PostconditionState,
    RecoveryClass,
    WorkflowStep,
    classify_outcome,
    composed_workflow_permitted,
)


def test_g14_individual_authorization_does_not_authorize_composition():
    steps = [
        WorkflowStep(
            node_id="read",
            capability_id="drive.file.read",
            access="read",
            sensitivity_in=frozenset({"confidential"}),
            externality="none",
        ),
        WorkflowStep(
            node_id="send",
            capability_id="slack.message.send",
            access="write",
            sensitivity_in=frozenset(),
            externality="external",
            destination_class="public-channel",
        ),
    ]
    assert composed_workflow_permitted(
        steps,
        individually_authorized=True,
        composition_authorized=False,
        protected_labels=frozenset({"confidential"}),
        allowed_destinations=frozenset(),
    ) is False


def test_g14_sensitive_read_to_unapproved_external_write_is_blocked():
    steps = [
        WorkflowStep(
            node_id="read",
            capability_id="drive.file.read",
            access="read",
            sensitivity_in=frozenset({"PII"}),
            externality="none",
        ),
        WorkflowStep(
            node_id="send",
            capability_id="gmail.message.send",
            access="write",
            sensitivity_in=frozenset(),
            externality="external",
            destination_class="external-recipient",
        ),
    ]
    assert composed_workflow_permitted(
        steps,
        individually_authorized=True,
        composition_authorized=True,
        protected_labels=frozenset({"PII"}),
        allowed_destinations=frozenset({"internal-recipient"}),
    ) is False


def test_g14_approved_destination_allows_governed_egress():
    steps = [
        WorkflowStep(
            node_id="read",
            capability_id="drive.file.read",
            access="read",
            sensitivity_in=frozenset({"confidential"}),
            externality="none",
        ),
        WorkflowStep(
            node_id="send",
            capability_id="slack.message.send",
            access="write",
            sensitivity_in=frozenset(),
            externality="external",
            destination_class="approved-secure-channel",
        ),
    ]
    assert composed_workflow_permitted(
        steps,
        individually_authorized=True,
        composition_authorized=True,
        protected_labels=frozenset({"confidential"}),
        allowed_destinations=frozenset({"approved-secure-channel"}),
    ) is True


def test_g15_partial_execution_preserves_partial_state_and_compensates():
    outcome = classify_outcome(
        completed_steps=2,
        total_steps=3,
        provider_outcome_known=True,
        postcondition_state=PostconditionState.NOT_CHECKED,
        recovery_classes=[
            RecoveryClass.REVERSIBLE,
            RecoveryClass.COMPENSATABLE,
            RecoveryClass.REVERSIBLE,
        ],
    )
    assert outcome.execution_state == ExecutionState.PARTIALLY_EXECUTED
    assert outcome.recovery_required is True
    assert outcome.recovery_mode == "COMPENSATE"


def test_g15_irreversible_partial_execution_escalates():
    outcome = classify_outcome(
        completed_steps=1,
        total_steps=2,
        provider_outcome_known=True,
        postcondition_state=PostconditionState.NOT_CHECKED,
        recovery_classes=[
            RecoveryClass.IRREVERSIBLE,
            RecoveryClass.REVERSIBLE,
        ],
    )
    assert outcome.execution_state == ExecutionState.PARTIALLY_EXECUTED
    assert outcome.recovery_mode == "CONTAIN_OR_ESCALATE"


def test_g15_postcondition_failure_does_not_erase_execution():
    outcome = classify_outcome(
        completed_steps=1,
        total_steps=1,
        provider_outcome_known=True,
        postcondition_state=PostconditionState.FAILED,
        recovery_classes=[RecoveryClass.COMPENSATABLE],
    )
    assert outcome.execution_state == ExecutionState.EXECUTED
    assert outcome.postcondition_state == PostconditionState.FAILED
    assert outcome.recovery_required is True
    assert outcome.recovery_mode == "COMPENSATE"
def test_unknown_provider_outcome_requires_reconciliation():
    outcome = classify_outcome(
        completed_steps=0,
        total_steps=1,
        provider_outcome_known=False,
        postcondition_state=PostconditionState.INCONCLUSIVE,
        recovery_classes=[RecoveryClass.IRREVERSIBLE],
    )
    assert outcome.execution_state == ExecutionState.EXECUTION_OUTCOME_UNKNOWN
    assert outcome.recovery_mode == "RECONCILE"
