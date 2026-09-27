from __future__ import annotations

from scripts.dgaf_capability_idempotency import InMemoryIdempotencyLedger
from scripts.dgaf_capability_model_check import (
    all_paths_include,
    composition_findings,
    exhaustive_guard_findings,
    graph_safety_findings,
    idempotency_interleaving_findings,
    model_check,
    recovery_findings,
    simple_paths,
    small_state_findings,
)
from scripts.dgaf_capability_state_machine import (
    _ALLOWED,
    TransactionState,
)
from scripts.dgaf_capability_workflow import (
    ExecutionState,
    WorkflowOutcome,
)


def test_reference_model_has_no_bounded_findings():
    assert model_check() == ()


def test_execute_is_reachable_in_reference_graph():
    paths = simple_paths(TransactionState.PROPOSED, TransactionState.EXECUTING)
    assert paths


def test_every_execution_path_contains_authorization_and_commit_revalidation():
    assert all_paths_include(
        TransactionState.EXECUTING,
        (
            TransactionState.AUTHORIZED,
            TransactionState.COMMIT_REVALIDATION,
            TransactionState.COMMIT_REVALIDATED,
        ),
    )


def test_exhaustive_guard_products_match_reference_predicates():
    assert exhaustive_guard_findings() == ()


def test_model_checker_detects_authorized_to_executing_shortcut():
    mutated = dict(_ALLOWED)
    mutated[TransactionState.AUTHORIZED] = mutated[TransactionState.AUTHORIZED] | frozenset(
        {TransactionState.EXECUTING}
    )
    findings = graph_safety_findings(graph=mutated)
    assert any(f.invariant in {"G1_G2_G13", "G13"} for f in findings)


def test_model_checker_detects_unknown_outcome_retry_edge():
    mutated = dict(_ALLOWED)
    mutated[TransactionState.EXECUTION_OUTCOME_UNKNOWN] = mutated[
        TransactionState.EXECUTION_OUTCOME_UNKNOWN
    ] | frozenset({TransactionState.EXECUTING})
    findings = graph_safety_findings(graph=mutated)
    assert any(f.invariant == "REPLAY_UNKNOWN" for f in findings)


def test_model_checker_detects_postcondition_fail_direct_close():
    mutated = dict(_ALLOWED)
    mutated[TransactionState.POSTCONDITION_FAILED] = mutated[TransactionState.POSTCONDITION_FAILED] | frozenset(
        {TransactionState.CLOSED}
    )
    findings = graph_safety_findings(graph=mutated)
    assert any(f.invariant == "G15" for f in findings)


def test_execution_paths_always_include_executing():
    assert all_paths_include(
        TransactionState.EXECUTED,
        (TransactionState.EXECUTING,),
    )


def test_small_state_composition_recovery_and_concurrency_have_no_findings():
    assert small_state_findings() == ()


def test_composition_checker_detects_unsafe_allow_all_evaluator():
    def unsafe_evaluator(*args, **kwargs):
        return True

    findings = composition_findings(evaluator=unsafe_evaluator)
    assert any(f.invariant == "G14_COMPOSITION" for f in findings)


def test_recovery_checker_detects_execution_history_erasure():
    def unsafe_classifier(**kwargs):
        return WorkflowOutcome(
            execution_state=ExecutionState.FAILED,
            postcondition_state=kwargs["postcondition_state"],
            recovery_required=False,
            recovery_mode=None,
        )

    findings = recovery_findings(classifier=unsafe_classifier)
    assert any(f.invariant == "G15_RECOVERY" for f in findings)


def test_idempotency_checker_detects_multiple_competing_winners():
    class UnsafeLedger(InMemoryIdempotencyLedger):
        def claim(self, key, action_digest):
            return None

        def mark_unknown(self, key, action_digest):
            return None

    findings = idempotency_interleaving_findings(ledger_factory=UnsafeLedger)
    assert any(f.invariant == "IDEMPOTENCY_CONCURRENCY" for f in findings)
