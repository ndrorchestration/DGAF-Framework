from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from scripts.dgaf_capability_policy import (
    approval_matches_commit,
    authorization_is_active,
    commit_guards_pass,
    permitted_by_effective_authority,
    Authority,
)


class EnforcementRefusal(RuntimeError):
    pass


@dataclass(frozen=True)
class VerificationState:
    required: bool
    passed: bool


@dataclass(frozen=True)
class ApprovalState:
    requester: str
    approver: str | None
    approved_digest: str | None
    consumed: bool = False
@dataclass(frozen=True)
class EnforcementContext:
    capability: str
    resource: str
    protected_side_effect: bool
    requester_authority: Authority
    delegation_authority: Authority
    executor_authority: Authority
    policy_authority: Authority
    authorization_status: str
    authorization_not_before: datetime
    authorization_expires_at: datetime
    commit_digest: str
    approval: ApprovalState
    verification: VerificationState
    required_state_guards: dict[str, Any]
    observed_state_guards: dict[str, Any]
    now: datetime


def required_verification_passes(state: VerificationState) -> bool:
    return (not state.required) or state.passed


def approval_separation_passes(state: ApprovalState) -> bool:
    if state.approver is None:
        return False
    return state.requester != state.approver
def enforce_before_dispatch(context: EnforcementContext) -> None:
    if not context.protected_side_effect:
        return

    if not authorization_is_active(
        context.authorization_status,
        not_before=context.authorization_not_before,
        expires_at=context.authorization_expires_at,
        now=context.now,
    ):
        raise EnforcementRefusal("authorization is inactive")

    if not permitted_by_effective_authority(
        context.capability,
        context.resource,
        requester=context.requester_authority,
        delegation=context.delegation_authority,
        executor=context.executor_authority,
        policy=context.policy_authority,
    ):
        raise EnforcementRefusal("effective authority does not permit capability/resource")

    if not required_verification_passes(context.verification):
        raise EnforcementRefusal("required verification did not pass")

    if not approval_separation_passes(context.approval):
        raise EnforcementRefusal("approval separation failed")
    if context.approval.approved_digest is None:
        raise EnforcementRefusal("action-specific approval is absent")

    if not approval_matches_commit(
        approved_digest=context.approval.approved_digest,
        commit_digest=context.commit_digest,
        authorization_status=context.authorization_status,
        consumed=context.approval.consumed,
    ):
        raise EnforcementRefusal("approval does not match commit action")

    if not commit_guards_pass(
        context.required_state_guards,
        context.observed_state_guards,
    ):
        raise EnforcementRefusal("commit-time state guards failed")


def governed_dispatch(
    request: dict[str, Any],
    context: EnforcementContext,
    *,
    dispatcher: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    enforce_before_dispatch(context)
    return dispatcher(request)
