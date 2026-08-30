from __future__ import annotations

from task_engine import AttemptStatus, ConsensusTask


def test_dgaf_failure_retains_governance_audit_trace() -> None:
    result = ConsensusTask(topology="ring", failure_count=0, condition="dgaf").run_detailed(
        seed=20260817,
        attempt=1,
    )

    assert result.attempt_status is AttemptStatus.FAILURE
    assert result.governance_trace
    trace = result.governance_trace[0]
    assert trace["event_type"] == "TGL_TURN_AUDIT"
    assert trace["turn_index"] == 1
    assert trace["decision"] == "FAIL_CLOSED"
    assert trace["seal_hash"]
    assert trace["outcome"] == AttemptStatus.FAILURE.value


def test_governance_trace_is_empty_for_non_dgaf_conditions() -> None:
    result = ConsensusTask(topology="ring", failure_count=0, condition="simple").run_detailed(
        seed=20260817,
        attempt=1,
    )
    assert result.attempt_status is AttemptStatus.SUCCESS
    assert result.governance_trace == ()
