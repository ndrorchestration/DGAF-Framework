from __future__ import annotations

from dataclasses import dataclass

import pytest

from pptl.control_plane import _ALLOWED, ControlPlane, ControlTask, TaskState
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget


@dataclass(frozen=True)
class LivenessAdjudication:
    issue: int
    edge: tuple[TaskState, TaskState]
    disposition: str
    rationale: str
    authoritative_effect: str = "NONE"
    scientific_state_effect: str = "NONE"
    scientific_n_increment: int = 0


RECEIVED_TERMINATED_ADJUDICATION = LivenessAdjudication(
    issue=1037,
    edge=(TaskState.RECEIVED, TaskState.TERMINATED),
    disposition="STALE_PUBLIC_POLICY_EDGE",
    rationale=(
        "ControlPlane.submit() immediately moves a registered task from RECEIVED to "
        "PREFLIGHT, while ControlPlane.terminate(task_id) only operates on registered "
        "tasks. The declared RECEIVED -> TERMINATED edge therefore has no public "
        "controller path and must not be counted as positive-path liveness coverage."
    ),
)


def budget() -> ResourceBudget:
    return ResourceBudget(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=3,
        max_nodes=8,
        max_depth=2,
        max_concurrency=2,
    )


def envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="root-trace",
        task_id="root",
        authority_scope=frozenset({"research", "draft"}),
        permitted_tools=frozenset({"read", "search"}),
        data_classes=frozenset({"public", "internal"}),
        prohibited_actions=frozenset({"delete", "send"}),
        budget=budget(),
    )


def test_received_terminated_edge_has_explicit_non_promoting_adjudication():
    record = RECEIVED_TERMINATED_ADJUDICATION

    assert record.issue == 1037
    assert record.edge == (TaskState.RECEIVED, TaskState.TERMINATED)
    assert record.disposition == "STALE_PUBLIC_POLICY_EDGE"
    assert record.authoritative_effect == "NONE"
    assert record.scientific_state_effect == "NONE"
    assert record.scientific_n_increment == 0


def test_received_terminated_edge_is_declared_but_not_publicly_reachable():
    record = RECEIVED_TERMINATED_ADJUDICATION
    source, target = record.edge

    assert target in _ALLOWED[source]

    plane = ControlPlane()
    task = ControlTask("root", envelope())

    with pytest.raises(KeyError):
        plane.terminate("root")
    assert task.state is TaskState.RECEIVED

    plane.submit(task)
    assert task.state is TaskState.PREFLIGHT
    assert task.state is not TaskState.RECEIVED

    plane.terminate("root")
    assert task.state is TaskState.TERMINATED


def test_public_liveness_scope_excludes_only_adjudicated_stale_edge():
    declared = {(source, target) for source, targets in _ALLOWED.items() for target in targets}
    adjudicated_exclusions = {RECEIVED_TERMINATED_ADJUDICATION.edge}
    public_liveness_scope = declared - adjudicated_exclusions

    assert RECEIVED_TERMINATED_ADJUDICATION.edge in declared
    assert len(adjudicated_exclusions) == 1
    assert RECEIVED_TERMINATED_ADJUDICATION.edge not in public_liveness_scope
    assert all(source is not TaskState.TERMINATED for source, _target in public_liveness_scope)
