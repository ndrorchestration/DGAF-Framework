from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Mapping

from scripts.dgaf_capability_idempotency import (
    IdempotencyConflict,
    IdempotencyInFlight,
    IdempotencyOutcomeUnknown,
    InMemoryIdempotencyLedger,
)
from scripts.dgaf_capability_state_machine import (
    _ALLOWED,
    TransactionSnapshot,
    TransactionState,
    TransitionFacts,
    TransitionRefusal,
    transition,
)
from scripts.dgaf_capability_workflow import (
    ExecutionState,
    PostconditionState,
    RecoveryClass,
    WorkflowOutcome,
    WorkflowStep,
    classify_outcome,
    composed_workflow_permitted,
)


@dataclass(frozen=True)
class ModelFinding:
    invariant: str
    detail: str


Graph = Mapping[TransactionState, frozenset[TransactionState]]


def simple_paths(
    start: TransactionState,
    target: TransactionState,
    *,
    graph: Graph = _ALLOWED,
) -> tuple[tuple[TransactionState, ...], ...]:
    found: list[tuple[TransactionState, ...]] = []
    stack: list[tuple[TransactionState, tuple[TransactionState, ...]]] = [(start, (start,))]
    while stack:
        node, path = stack.pop()
        if node == target:
            found.append(path)
            continue
        for nxt in graph.get(node, frozenset()):
            if nxt not in path:
                stack.append((nxt, path + (nxt,)))
    return tuple(found)


def all_paths_include(
    target: TransactionState,
    required: tuple[TransactionState, ...],
    *,
    graph: Graph = _ALLOWED,
) -> bool:
    paths = simple_paths(TransactionState.PROPOSED, target, graph=graph)
    if not paths:
        return False
    return all(all(state in path for state in required) for path in paths)


def graph_safety_findings(*, graph: Graph = _ALLOWED) -> tuple[ModelFinding, ...]:
    findings: list[ModelFinding] = []
    required_before_execute = (
        TransactionState.AUTHORIZED,
        TransactionState.COMMIT_REVALIDATION,
        TransactionState.COMMIT_REVALIDATED,
    )
    if not all_paths_include(
        TransactionState.EXECUTING,
        required_before_execute,
        graph=graph,
    ):
        findings.append(
            ModelFinding(
                "G1_G2_G13",
                "an execution path bypasses authorization or commit revalidation",
            )
        )

    if not all_paths_include(
        TransactionState.EXECUTED,
        (TransactionState.EXECUTING,),
        graph=graph,
    ):
        findings.append(ModelFinding("G6", "an executed path bypasses the executing state"))

    unknown_targets = graph.get(
        TransactionState.EXECUTION_OUTCOME_UNKNOWN,
        frozenset(),
    )
    if TransactionState.EXECUTING in unknown_targets or TransactionState.EXECUTED in unknown_targets:
        findings.append(
            ModelFinding(
                "REPLAY_UNKNOWN",
                "unknown execution outcome permits direct re-execution/completion",
            )
        )
    for post_state in (
        TransactionState.POSTCONDITION_FAILED,
        TransactionState.POSTCONDITION_INCONCLUSIVE,
    ):
        if TransactionState.CLOSED in graph.get(post_state, frozenset()):
            findings.append(
                ModelFinding(
                    "G15",
                    f"{post_state.value} can close without recovery/escalation",
                )
            )

    if TransactionState.EXECUTING in graph.get(TransactionState.AUTHORIZED, frozenset()):
        findings.append(ModelFinding("G13", "AUTHORIZED can execute without commit revalidation"))

    return tuple(findings)


def _facts(
    *,
    required_verification_passed: bool = True,
    approval_present: bool = True,
    requester_approver_separated: bool = True,
    authorization_active: bool = True,
    authorization_scoped: bool = True,
    delegation_non_widening: bool = True,
    action_digest_matches: bool = True,
    commit_guards_passed: bool = True,
    authorization_consumed: bool = False,
    idempotency_safe: bool = True,
    execution_receipt_present: bool = True,
    execution_outcome_unknown: bool = False,
    audit_recorded: bool = True,
) -> TransitionFacts:
    return TransitionFacts(
        action_canonicalized=True,
        evidence_complete=True,
        required_verification_passed=required_verification_passed,
        verification_inconclusive=False,
        approval_required=True,
        approval_present=approval_present,
        requester_approver_separated=requester_approver_separated,
        authorization_active=authorization_active,
        authorization_scoped=authorization_scoped,
        delegation_non_widening=delegation_non_widening,
        action_digest_matches=action_digest_matches,
        commit_guards_passed=commit_guards_passed,
        authorization_consumed=authorization_consumed,
        idempotency_safe=idempotency_safe,
        execution_receipt_present=execution_receipt_present,
        execution_outcome_unknown=execution_outcome_unknown,
        postcondition_verified=True,
        postcondition_failed=False,
        postcondition_inconclusive=False,
        recovery_required=False,
        recovery_mode=None,
        audit_recorded=audit_recorded,
    )


def _permitted(source: TransactionState, target: TransactionState, facts: TransitionFacts) -> bool:
    try:
        transition(TransactionSnapshot(source, facts), target)
    except TransitionRefusal:
        return False
    return True


def exhaustive_guard_findings() -> tuple[ModelFinding, ...]:
    findings: list[ModelFinding] = []

    auth_names = (
        "required_verification_passed",
        "authorization_active",
        "authorization_scoped",
        "delegation_non_widening",
        "approval_present",
        "requester_approver_separated",
        "action_digest_matches",
    )
    for bits in product((False, True), repeat=len(auth_names)):
        values = dict(zip(auth_names, bits))
        expected = all(bits)
        actual = _permitted(
            TransactionState.APPROVAL_PENDING,
            TransactionState.AUTHORIZED,
            _facts(**values),
        )
        if actual != expected:
            findings.append(
                ModelFinding(
                    "AUTHORIZATION_GUARDS",
                    f"authorization guard mismatch for {values}",
                )
            )
            break

    commit_names = (
        "authorization_active",
        "action_digest_matches",
        "commit_guards_passed",
        "idempotency_safe",
    )
    for bits in product((False, True), repeat=len(commit_names)):
        for consumed in (False, True):
            values = dict(zip(commit_names, bits))
            values["authorization_consumed"] = consumed
            expected = all(bits) and not consumed
            actual = _permitted(
                TransactionState.COMMIT_REVALIDATION,
                TransactionState.COMMIT_REVALIDATED,
                _facts(**values),
            )
            if actual != expected:
                findings.append(
                    ModelFinding(
                        "COMMIT_GUARDS",
                        f"commit guard mismatch for {values}",
                    )
                )
                return tuple(findings)

    for receipt, unknown in product((False, True), repeat=2):
        expected = receipt and not unknown
        actual = _permitted(
            TransactionState.EXECUTING,
            TransactionState.EXECUTED,
            _facts(
                execution_receipt_present=receipt,
                execution_outcome_unknown=unknown,
            ),
        )
        if actual != expected:
            findings.append(
                ModelFinding(
                    "EXECUTION_RECEIPT",
                    f"execution evidence mismatch receipt={receipt} unknown={unknown}",
                )
            )

    for audit in (False, True):
        actual = _permitted(
            TransactionState.VERIFIED_POSTCONDITION,
            TransactionState.CLOSED,
            _facts(audit_recorded=audit),
        )
        if actual != audit:
            findings.append(
                ModelFinding(
                    "AUDIT_BEFORE_CLOSURE",
                    f"closure audit mismatch audit={audit}",
                )
            )

    return tuple(findings)


def composition_findings(
    evaluator=composed_workflow_permitted,
) -> tuple[ModelFinding, ...]:
    findings: list[ModelFinding] = []
    for individually_authorized, composition_authorized, sensitive, external, destination_allowed in product(
        (False, True), repeat=5
    ):
        steps = (
            WorkflowStep(
                node_id="read",
                capability_id="drive.file.read",
                access="read",
                sensitivity_in=frozenset({"confidential"} if sensitive else set()),
                externality="none",
            ),
            WorkflowStep(
                node_id="write",
                capability_id="slack.message.send",
                access="write",
                sensitivity_in=frozenset(),
                externality="external" if external else "internal",
                destination_class="approved" if destination_allowed else "unapproved",
            ),
        )
        expected = (
            individually_authorized
            and composition_authorized
            and not (sensitive and external and not destination_allowed)
        )
        actual = evaluator(
            steps,
            individually_authorized=individually_authorized,
            composition_authorized=composition_authorized,
            protected_labels=frozenset({"confidential"}),
            allowed_destinations=frozenset({"approved"}),
        )
        if actual != expected:
            findings.append(
                ModelFinding(
                    "G14_COMPOSITION",
                    "composition mismatch "
                    f"individual={individually_authorized} "
                    f"composition={composition_authorized} "
                    f"sensitive={sensitive} external={external} "
                    f"destination_allowed={destination_allowed}",
                )
            )
            break
    return tuple(findings)


def _expected_recovery_mode(
    recovery_classes: tuple[RecoveryClass, ...],
) -> str:
    if RecoveryClass.IRREVERSIBLE in recovery_classes:
        return "CONTAIN_OR_ESCALATE"
    if RecoveryClass.COMPENSATABLE in recovery_classes:
        return "COMPENSATE"
    return "ROLLBACK"


def recovery_findings(
    classifier=classify_outcome,
) -> tuple[ModelFinding, ...]:
    findings: list[ModelFinding] = []
    recovery_values = tuple(RecoveryClass)
    post_states = tuple(PostconditionState)
    for total_steps in (1, 2, 3):
        for classes in product(recovery_values, repeat=total_steps):
            for completed_steps in range(total_steps + 1):
                for provider_known in (False, True):
                    for post_state in post_states:
                        actual = classifier(
                            completed_steps=completed_steps,
                            total_steps=total_steps,
                            provider_outcome_known=provider_known,
                            postcondition_state=post_state,
                            recovery_classes=classes,
                        )
                        if not provider_known:
                            expected = WorkflowOutcome(
                                execution_state=ExecutionState.EXECUTION_OUTCOME_UNKNOWN,
                                postcondition_state=post_state,
                                recovery_required=False,
                                recovery_mode="RECONCILE",
                            )
                        elif completed_steps == 0:
                            expected = WorkflowOutcome(
                                execution_state=ExecutionState.FAILED,
                                postcondition_state=post_state,
                                recovery_required=False,
                                recovery_mode=None,
                            )
                        elif completed_steps < total_steps:
                            expected = WorkflowOutcome(
                                execution_state=ExecutionState.PARTIALLY_EXECUTED,
                                postcondition_state=post_state,
                                recovery_required=True,
                                recovery_mode=_expected_recovery_mode(classes[:completed_steps]),
                            )
                        elif post_state in {
                            PostconditionState.FAILED,
                            PostconditionState.INCONCLUSIVE,
                        }:
                            expected = WorkflowOutcome(
                                execution_state=ExecutionState.EXECUTED,
                                postcondition_state=post_state,
                                recovery_required=True,
                                recovery_mode=_expected_recovery_mode(classes),
                            )
                        else:
                            expected = WorkflowOutcome(
                                execution_state=ExecutionState.EXECUTED,
                                postcondition_state=post_state,
                                recovery_required=False,
                                recovery_mode=None,
                            )
                        if actual != expected:
                            findings.append(
                                ModelFinding(
                                    "G15_RECOVERY",
                                    "recovery mismatch "
                                    f"total={total_steps} completed={completed_steps} "
                                    f"known={provider_known} post={post_state.value} "
                                    f"classes={[item.value for item in classes]}",
                                )
                            )
                            return tuple(findings)
    return tuple(findings)


def idempotency_interleaving_findings(
    ledger_factory=InMemoryIdempotencyLedger,
) -> tuple[ModelFinding, ...]:
    findings: list[ModelFinding] = []
    digest_a = "sha256:" + "a" * 64
    digest_b = "sha256:" + "b" * 64

    for first, second in (("A", "B"), ("B", "A")):
        ledger = ledger_factory()
        winners = 0
        for worker in (first, second):
            try:
                result = ledger.claim("idem:shared", digest_a)
                if result is None:
                    winners += 1
            except IdempotencyInFlight:
                pass
        if winners != 1:
            findings.append(
                ModelFinding(
                    "IDEMPOTENCY_CONCURRENCY",
                    f"same-digest competing claims produced {winners} reservation winners",
                )
            )
            break

    ledger = ledger_factory()
    try:
        ledger.claim("idem:conflict", digest_a)
        ledger.claim("idem:conflict", digest_b)
    except IdempotencyConflict:
        pass
    else:
        findings.append(
            ModelFinding(
                "IDEMPOTENCY_DIGEST_BINDING",
                "same idempotency key accepted two different action digests",
            )
        )

    ledger = ledger_factory()
    ledger.claim("idem:unknown", digest_a)
    ledger.mark_unknown("idem:unknown", digest_a)
    try:
        ledger.claim("idem:unknown", digest_a)
    except IdempotencyOutcomeUnknown:
        pass
    else:
        findings.append(
            ModelFinding(
                "IDEMPOTENCY_UNKNOWN",
                "unknown execution outcome allowed retry before reconciliation",
            )
        )
    return tuple(findings)


def small_state_findings() -> tuple[ModelFinding, ...]:
    return composition_findings() + recovery_findings() + idempotency_interleaving_findings()


def model_check() -> tuple[ModelFinding, ...]:
    return graph_safety_findings() + exhaustive_guard_findings() + small_state_findings()
