from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from scripts.dgaf_capability_pep import (
    ApprovalState,
    EnforcementContext,
    EnforcementRefusal,
    VerificationState,
    governed_dispatch,
)
from scripts.dgaf_capability_policy import Authority


NOW = datetime(2026, 9, 25, 13, 0, tzinfo=timezone.utc)


def authority(capabilities, resources):
    return Authority(frozenset(capabilities), frozenset(resources))


def base_context(**changes):
    digest = "sha256:" + "a" * 64
    values = dict(
        capability="dgaf.local.materialize",
        resource="dgaf.local.materialized_input",
        protected_side_effect=True,
        requester_authority=authority({"dgaf.local.materialize"}, {"dgaf.local.materialized_input"}),
        delegation_authority=authority({"dgaf.local.materialize"}, {"dgaf.local.materialized_input"}),
        executor_authority=authority({"dgaf.local.materialize"}, {"dgaf.local.materialized_input"}),
        policy_authority=authority({"dgaf.local.materialize"}, {"dgaf.local.materialized_input"}),
        authorization_status="ACTIVE",
        authorization_not_before=NOW - timedelta(minutes=5),
        authorization_expires_at=NOW + timedelta(minutes=5),
        commit_digest=digest,
        approval=ApprovalState(
            requester="agent:operator",
            approver="human:reviewer",
            approved_digest=digest,
            consumed=False,
        ),
        verification=VerificationState(required=True, passed=True),
        required_state_guards={"input_sha": "abc"},
        observed_state_guards={"input_sha": "abc"},
        now=NOW,
    )
    values.update(changes)
    return EnforcementContext(**values)


def counting_dispatcher(calls):
    def dispatch(request):
        calls.append(request)
        return {"status": "PASS", "action": request["action"]}
    return dispatch
def test_g1_g2_authorized_materialize_reaches_dispatcher():
    calls = []
    result = governed_dispatch(
        {"action": "materialize"},
        base_context(),
        dispatcher=counting_dispatcher(calls),
    )
    assert result["status"] == "PASS"
    assert calls == [{"action": "materialize"}]


def test_g1_inactive_authorization_blocks_before_side_effect():
    calls = []
    with pytest.raises(EnforcementRefusal, match="authorization is inactive"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(authorization_status="REVOKED"),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g2_missing_effective_authority_blocks_before_dispatch():
    calls = []
    denied = authority({"dgaf.local.status"}, {"dgaf.local.state"})
    with pytest.raises(EnforcementRefusal, match="effective authority"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(requester_authority=denied),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g3_authorization_scope_does_not_transfer_to_adjacent_resource():
    calls = []
    wrong_scope = authority(
        {"dgaf.local.materialize"},
        {"dgaf.local.other-materialized-input"},
    )
    with pytest.raises(EnforcementRefusal, match="effective authority"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(delegation_authority=wrong_scope),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g4_self_approval_is_blocked():
    calls = []
    digest = "sha256:" + "a" * 64
    with pytest.raises(EnforcementRefusal, match="approval separation failed"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(
                approval=ApprovalState(
                    requester="agent:operator",
                    approver="agent:operator",
                    approved_digest=digest,
                )
            ),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g8_required_verifier_failure_blocks():
    calls = []
    with pytest.raises(EnforcementRefusal, match="required verification"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(verification=VerificationState(required=True, passed=False)),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g12_digest_substitution_blocks_dispatch():
    calls = []
    approval = ApprovalState(
        requester="agent:operator",
        approver="human:reviewer",
        approved_digest="sha256:" + "b" * 64,
    )
    with pytest.raises(EnforcementRefusal, match="does not match commit"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(approval=approval),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_g13_commit_guard_drift_blocks_dispatch():
    calls = []
    with pytest.raises(EnforcementRefusal, match="state guards failed"):
        governed_dispatch(
            {"action": "materialize"},
            base_context(observed_state_guards={"input_sha": "def"}),
            dispatcher=counting_dispatcher(calls),
        )
    assert calls == []


def test_unprotected_read_can_dispatch_without_authorization_gate():
    calls = []
    context = base_context(
        capability="dgaf.local.status",
        resource="dgaf.local.state",
        protected_side_effect=False,
        authorization_status="REVOKED",
        verification=VerificationState(required=False, passed=False),
        approval=ApprovalState(
            requester="agent:any",
            approver=None,
            approved_digest=None,
        ),
    )
    result = governed_dispatch(
        {"action": "status"},
        context,
        dispatcher=counting_dispatcher(calls),
    )
    assert result["action"] == "status"
    assert calls == [{"action": "status"}]
