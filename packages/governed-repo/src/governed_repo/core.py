"""Governed Repo v0: pure repository-promotion eligibility evaluator.

This module is deliberately non-mutating. It evaluates whether an exact
repository change is eligible for promotion under caller-supplied policy
and observed gate receipts. It does not merge, push, deploy, release, or
grant authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Iterable, Optional, Sequence


class PromotionReason(str, Enum):
    ELIGIBLE_FOR_PROMOTION = "ELIGIBLE_FOR_PROMOTION"
    INPUT_INVALID = "INPUT_INVALID"
    STALE_BASE = "STALE_BASE"
    HEAD_IDENTITY_MISMATCH = "HEAD_IDENTITY_MISMATCH"
    REQUIRED_CHECK_MISSING = "REQUIRED_CHECK_MISSING"
    REQUIRED_CHECK_NOT_TERMINAL = "REQUIRED_CHECK_NOT_TERMINAL"
    REQUIRED_CHECK_FAILED = "REQUIRED_CHECK_FAILED"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    CLAIM_SCOPE_INVALID = "CLAIM_SCOPE_INVALID"
    MUTATION_POLICY_BLOCKED = "MUTATION_POLICY_BLOCKED"
    AUTHORITY_UNRESOLVED = "AUTHORITY_UNRESOLVED"
    LIFECYCLE_BLOCKED = "LIFECYCLE_BLOCKED"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ChangeIdentity:
    repository: str
    change_id: str
    base_sha: str
    head_sha: str
    observed_base_sha: str
    observed_head_sha: str
    observed_at: str
    merge_ref_sha: Optional[str] = None


@dataclass(frozen=True)
class GateRequirement:
    gate_id: str
    gate_class: str
    required: bool = True
    accepted_conclusions: tuple[str, ...] = ("success",)
    require_head_binding: bool = True
    require_base_binding: bool = False


@dataclass(frozen=True)
class GateReceipt:
    gate_id: str
    status: str
    conclusion: Optional[str]
    observed_at: str
    source_identity: Optional[str] = None
    head_sha: Optional[str] = None
    base_sha: Optional[str] = None


@dataclass(frozen=True)
class UpstreamDecision:
    decision_class: str
    accepted: bool
    reason_code: str
    receipt_id: Optional[str] = None


@dataclass(frozen=True)
class PromotionPolicy:
    required_gates: tuple[GateRequirement, ...] = ()
    hold: bool = False
    lifecycle_blocked: bool = False
    require_evidence_acceptance: bool = False
    require_claim_scope_acceptance: bool = False
    require_mutation_policy_acceptance: bool = False
    require_authority_resolution: bool = False


@dataclass(frozen=True)
class PromotionReceipt:
    eligible: bool
    reason_code: PromotionReason
    repository: str
    change_id: str
    base_sha: str
    head_sha: str
    checked_gate_ids: tuple[str, ...]
    missing_gate_ids: tuple[str, ...]
    failed_gate_ids: tuple[str, ...]
    nonterminal_gate_ids: tuple[str, ...]
    upstream_receipt_ids: tuple[str, ...]
    merge_executed: bool = False
    mutation_executed: bool = False
    authorization_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.merge_executed or self.mutation_executed:
            raise ValueError("Governed Repo v0 never executes repository mutation")
        if self.authorization_effect != "NONE":
            raise ValueError("Governed Repo v0 never grants authorization")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["reason_code"] = self.reason_code.value
        value["checked_gate_ids"] = list(self.checked_gate_ids)
        value["missing_gate_ids"] = list(self.missing_gate_ids)
        value["failed_gate_ids"] = list(self.failed_gate_ids)
        value["nonterminal_gate_ids"] = list(self.nonterminal_gate_ids)
        value["upstream_receipt_ids"] = list(self.upstream_receipt_ids)
        return value


def _invalid(identity: ChangeIdentity, reason: PromotionReason) -> PromotionReceipt:
    return PromotionReceipt(
        eligible=False,
        reason_code=reason,
        repository=identity.repository,
        change_id=identity.change_id,
        base_sha=identity.base_sha,
        head_sha=identity.head_sha,
        checked_gate_ids=(),
        missing_gate_ids=(),
        failed_gate_ids=(),
        nonterminal_gate_ids=(),
        upstream_receipt_ids=(),
    )


def _validate_identity(identity: ChangeIdentity) -> Optional[PromotionReason]:
    required = (
        identity.repository,
        identity.change_id,
        identity.base_sha,
        identity.head_sha,
        identity.observed_base_sha,
        identity.observed_head_sha,
        identity.observed_at,
    )
    if any(not isinstance(value, str) or not value.strip() for value in required):
        return PromotionReason.INPUT_INVALID
    if identity.base_sha != identity.observed_base_sha:
        return PromotionReason.STALE_BASE
    if identity.head_sha != identity.observed_head_sha:
        return PromotionReason.HEAD_IDENTITY_MISMATCH
    return None


def _find_receipt(receipts: Sequence[GateReceipt], gate_id: str) -> Optional[GateReceipt]:
    matches = [receipt for receipt in receipts if receipt.gate_id == gate_id]
    if len(matches) != 1:
        return None
    return matches[0]


def _is_terminal(status: str) -> bool:
    return status.lower() == "completed"


def _upstream_receipt_ids(decisions: Iterable[UpstreamDecision]) -> tuple[str, ...]:
    return tuple(
        decision.receipt_id for decision in decisions if decision.receipt_id is not None and decision.receipt_id.strip()
    )


def assess_promotion(
    identity: ChangeIdentity,
    policy: PromotionPolicy,
    gate_receipts: Sequence[GateReceipt],
    *,
    evidence: Optional[UpstreamDecision] = None,
    claim_scope: Optional[UpstreamDecision] = None,
    mutation_policy: Optional[UpstreamDecision] = None,
    authority: Optional[UpstreamDecision] = None,
) -> PromotionReceipt:
    """Evaluate promotion eligibility for one exact repository change."""

    identity_error = _validate_identity(identity)
    if identity_error is not None:
        return _invalid(identity, identity_error)

    if policy.hold:
        return _invalid(identity, PromotionReason.HOLD)
    if policy.lifecycle_blocked:
        return _invalid(identity, PromotionReason.LIFECYCLE_BLOCKED)

    checked: list[str] = []
    missing: list[str] = []
    failed: list[str] = []
    nonterminal: list[str] = []

    for requirement in policy.required_gates:
        receipt = _find_receipt(gate_receipts, requirement.gate_id)
        if receipt is None:
            if requirement.required:
                missing.append(requirement.gate_id)
            continue

        checked.append(requirement.gate_id)

        if requirement.require_head_binding and receipt.head_sha != identity.head_sha:
            failed.append(requirement.gate_id)
            continue
        if requirement.require_base_binding and receipt.base_sha != identity.base_sha:
            failed.append(requirement.gate_id)
            continue
        if not _is_terminal(receipt.status):
            nonterminal.append(requirement.gate_id)
            continue
        if receipt.conclusion not in requirement.accepted_conclusions:
            failed.append(requirement.gate_id)

    if missing:
        return PromotionReceipt(
            False,
            PromotionReason.REQUIRED_CHECK_MISSING,
            identity.repository,
            identity.change_id,
            identity.base_sha,
            identity.head_sha,
            tuple(checked),
            tuple(missing),
            tuple(failed),
            tuple(nonterminal),
            (),
        )
    if nonterminal:
        return PromotionReceipt(
            False,
            PromotionReason.REQUIRED_CHECK_NOT_TERMINAL,
            identity.repository,
            identity.change_id,
            identity.base_sha,
            identity.head_sha,
            tuple(checked),
            (),
            tuple(failed),
            tuple(nonterminal),
            (),
        )
    if failed:
        return PromotionReceipt(
            False,
            PromotionReason.REQUIRED_CHECK_FAILED,
            identity.repository,
            identity.change_id,
            identity.base_sha,
            identity.head_sha,
            tuple(checked),
            (),
            tuple(failed),
            (),
            (),
        )

    upstream = tuple(
        decision for decision in (evidence, claim_scope, mutation_policy, authority) if decision is not None
    )
    upstream_ids = _upstream_receipt_ids(upstream)

    if policy.require_evidence_acceptance and (evidence is None or not evidence.accepted):
        reason = PromotionReason.EVIDENCE_INSUFFICIENT
    elif policy.require_claim_scope_acceptance and (claim_scope is None or not claim_scope.accepted):
        reason = PromotionReason.CLAIM_SCOPE_INVALID
    elif policy.require_mutation_policy_acceptance and (mutation_policy is None or not mutation_policy.accepted):
        reason = PromotionReason.MUTATION_POLICY_BLOCKED
    elif policy.require_authority_resolution and (authority is None or not authority.accepted):
        reason = PromotionReason.AUTHORITY_UNRESOLVED
    else:
        return PromotionReceipt(
            True,
            PromotionReason.ELIGIBLE_FOR_PROMOTION,
            identity.repository,
            identity.change_id,
            identity.base_sha,
            identity.head_sha,
            tuple(checked),
            (),
            (),
            (),
            upstream_ids,
        )

    return PromotionReceipt(
        False,
        reason,
        identity.repository,
        identity.change_id,
        identity.base_sha,
        identity.head_sha,
        tuple(checked),
        (),
        (),
        (),
        upstream_ids,
    )
