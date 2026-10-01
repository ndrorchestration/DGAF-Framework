"""Thin adapters from canonical primitive receipts into Governed Repo decisions.

This module does not re-run Evidence Gate, ClaimGraph, or Action Admission
semantics. It validates only the serialized receipt envelope needed to prevent
effect/authority laundering, then preserves the primitive decision and reason.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional

from components.governed_repo import UpstreamDecision

EVIDENCE_GATE_SCHEMA_VERSION = "dgaf.evidence-gate.v0-candidate"
CLAIMGRAPH_RECEIPT_SCHEMA_VERSION = "claimgraph.validation-receipt.v0-candidate"
ACTION_ADMISSION_SCHEMA_VERSION = "agent-control-plane.action-admission.v0-candidate"


class PrimitiveReceiptError(ValueError):
    """Raised when a primitive receipt cannot be mapped without guessing."""


def _mapping(receipt: object, name: str) -> Mapping[str, Any]:
    if not isinstance(receipt, Mapping):
        raise PrimitiveReceiptError(f"{name} receipt must be an object")
    return receipt


def _required_string(receipt: Mapping[str, Any], key: str, name: str) -> str:
    value = receipt.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PrimitiveReceiptError(f"{name}.{key} must be a non-empty string")
    return value


def _required_bool(receipt: Mapping[str, Any], key: str, name: str) -> bool:
    value = receipt.get(key)
    if type(value) is not bool:
        raise PrimitiveReceiptError(f"{name}.{key} must be boolean")
    return value


def _optional_receipt_id(receipt_id: Optional[str]) -> Optional[str]:
    if receipt_id is None:
        return None
    if not isinstance(receipt_id, str) or not receipt_id.strip():
        raise PrimitiveReceiptError("receipt_id must be null or a non-empty string")
    return receipt_id


def evidence_gate_decision(
    receipt: object,
    *,
    receipt_id: Optional[str] = None,
) -> UpstreamDecision:
    value = _mapping(receipt, "evidence_gate")
    if _required_string(value, "schema_version", "evidence_gate") != EVIDENCE_GATE_SCHEMA_VERSION:
        raise PrimitiveReceiptError("unsupported Evidence Gate schema_version")
    if _required_string(value, "authorization_effect", "evidence_gate") != "NONE":
        raise PrimitiveReceiptError("Evidence Gate authorization_effect must be NONE")

    accepted = _required_bool(value, "admitted", "evidence_gate")
    reason_code = _required_string(value, "reason_code", "evidence_gate")
    return UpstreamDecision(
        decision_class="evidence",
        accepted=accepted,
        reason_code=reason_code,
        receipt_id=_optional_receipt_id(receipt_id),
    )


def claimgraph_decision(
    receipt: object,
    *,
    receipt_id: Optional[str] = None,
) -> UpstreamDecision:
    value = _mapping(receipt, "claimgraph")
    if (
        _required_string(value, "receipt_schema_version", "claimgraph")
        != CLAIMGRAPH_RECEIPT_SCHEMA_VERSION
    ):
        raise PrimitiveReceiptError("unsupported ClaimGraph receipt_schema_version")
    if _required_string(value, "truth_effect", "claimgraph") != "NONE":
        raise PrimitiveReceiptError("ClaimGraph truth_effect must be NONE")
    if _required_string(value, "authorization_effect", "claimgraph") != "NONE":
        raise PrimitiveReceiptError("ClaimGraph authorization_effect must be NONE")

    accepted = _required_bool(value, "valid", "claimgraph")
    reason_code = _required_string(value, "reason_code", "claimgraph")
    return UpstreamDecision(
        decision_class="claim_scope",
        accepted=accepted,
        reason_code=reason_code,
        receipt_id=_optional_receipt_id(receipt_id),
    )


def action_admission_decision(
    receipt: object,
    *,
    receipt_id: Optional[str] = None,
) -> UpstreamDecision:
    value = _mapping(receipt, "action_admission")
    if (
        _required_string(value, "schema_version", "action_admission")
        != ACTION_ADMISSION_SCHEMA_VERSION
    ):
        raise PrimitiveReceiptError("unsupported Action Admission schema_version")
    execution_enabled = _required_bool(value, "execution_enabled", "action_admission")
    if execution_enabled:
        raise PrimitiveReceiptError("Action Admission execution_enabled must be false")

    accepted = _required_bool(value, "admitted", "action_admission")
    reason_code = _required_string(value, "reason_code", "action_admission")
    return UpstreamDecision(
        decision_class="authority",
        accepted=accepted,
        reason_code=reason_code,
        receipt_id=_optional_receipt_id(receipt_id),
    )
