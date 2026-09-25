from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from scripts.dgaf_capability_canonicalize import (
    canonical_action_envelope,
    sha256_digest,
)
from scripts.dgaf_capability_pep import (
    EnforcementContext,
    EnforcementRefusal,
    governed_dispatch,
)
from scripts.dgaf_capability_workflow import (
    ExecutionState,
    PostconditionState,
)


class ExecutionOutcomeUnknown(RuntimeError):
    """Dispatcher may have completed the side effect, but outcome is unknown."""


@dataclass(frozen=True)
class TransactionIdentity:
    workflow_id: str
    invocation_id: str
    authorization_id: str
    idempotency_key: str
    event_id: str
@dataclass(frozen=True)
class TransactionMetadata:
    capability_id: str
    capability_version: str
    resource: dict[str, Any]
    parameters: dict[str, Any]
    initiating_principal: str
    executing_principal: str
    delegation_chain_id: str | None
    policy_id: str
    policy_version: str
    state_guards: dict[str, Any]
    nonce: str
    adapter_identity: str
    runtime_identity: str


@dataclass(frozen=True)
class TransactionResult:
    action_envelope: dict[str, Any]
    action_digest: str
    response: dict[str, Any] | None
    execution_receipt: dict[str, Any] | None
    audit_event: dict[str, Any]
    reconciliation_required: bool


def _iso(timestamp: datetime) -> str:
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
def _receipt(
    *,
    identity: TransactionIdentity,
    metadata: TransactionMetadata,
    action_digest: str,
    timestamp: datetime,
    execution_state: ExecutionState,
    provider_receipt: dict[str, Any] | None,
    postcondition_state: PostconditionState,
    recovery_state: str,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1-draft",
        "invocation_id": identity.invocation_id,
        "workflow_id": identity.workflow_id,
        "authorization_id": identity.authorization_id,
        "capability_id": metadata.capability_id,
        "action_digest": action_digest,
        "idempotency_key": identity.idempotency_key,
        "attempt": 1,
        "execution_state": execution_state.value,
        "executor_identity": metadata.executing_principal,
        "adapter_identity": metadata.adapter_identity,
        "provider_receipt": provider_receipt,
        "timestamp": _iso(timestamp),
        "postcondition_state": postcondition_state.value,
        "recovery_state": recovery_state,
    }


def _audit(
    *,
    identity: TransactionIdentity,
    metadata: TransactionMetadata,
    action_digest: str,
    timestamp: datetime,
    decision: str,
    decision_reasons: list[str],
    execution_state: str,
    postcondition_state: str,
    recovery_state: str,
    provider_receipt_id: str | None = None,
    evidence_ids: list[str] | None = None,
    verifier_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1-draft",
        "event_id": identity.event_id,
        "event_type": "EXECUTION",
        "timestamp": _iso(timestamp),
        "initiating_principal": metadata.initiating_principal,
        "executing_principal": metadata.executing_principal,
        "workflow_id": identity.workflow_id,
        "invocation_id": identity.invocation_id,
        "capability_id": metadata.capability_id,
        "capability_version": metadata.capability_version,
        "policy": {"id": metadata.policy_id, "version": metadata.policy_version},
        "authorization_id": identity.authorization_id,
        "delegation_chain_id": metadata.delegation_chain_id,
        "action_digest": action_digest,
        "decision": decision,
        "decision_reasons": decision_reasons,
        "evidence_ids": evidence_ids or [],
        "verifier_ids": verifier_ids or [],
        "adapter_identity": metadata.adapter_identity,
        "runtime_identity": metadata.runtime_identity,
        "provider_receipt_id": provider_receipt_id,
        "execution_state": execution_state,
        "postcondition_state": postcondition_state,
        "recovery_state": recovery_state,
        "secret_material_present": False,
    }


def run_reference_transaction(
    *,
    request: dict[str, Any],
    identity: TransactionIdentity,
    metadata: TransactionMetadata,
    context_factory: Callable[[str], EnforcementContext],
    dispatcher: Callable[[dict[str, Any]], dict[str, Any]],
    postcondition: Callable[[dict[str, Any]], bool],
    timestamp: datetime,
    evidence_ids: list[str] | None = None,
    verifier_ids: list[str] | None = None,
) -> TransactionResult:
    envelope = canonical_action_envelope(
        capability_id=metadata.capability_id,
        capability_version=metadata.capability_version,
        resource=metadata.resource,
        parameters=metadata.parameters,
        initiating_principal=metadata.initiating_principal,
        executing_principal=metadata.executing_principal,
        delegation_chain_id=metadata.delegation_chain_id,
        policy_id=metadata.policy_id,
        policy_version=metadata.policy_version,
        state_guards=metadata.state_guards,
        nonce=metadata.nonce,
    )
    digest = sha256_digest(envelope)
    context = context_factory(digest)

    try:
        response = governed_dispatch(
            request,
            context,
            dispatcher=dispatcher,
        )
    except EnforcementRefusal as exc:
        audit = _audit(
            identity=identity,
            metadata=metadata,
            action_digest=digest,
            timestamp=timestamp,
            decision="DENY",
            decision_reasons=[str(exc)],
            execution_state="NOT_STARTED",
            postcondition_state="NOT_CHECKED",
            recovery_state="NONE",
            evidence_ids=evidence_ids,
            verifier_ids=verifier_ids,
        )
        return TransactionResult(envelope, digest, None, None, audit, False)
    except ExecutionOutcomeUnknown:
        receipt = _receipt(
            identity=identity,
            metadata=metadata,
            action_digest=digest,
            timestamp=timestamp,
            execution_state=ExecutionState.EXECUTION_OUTCOME_UNKNOWN,
            provider_receipt=None,
            postcondition_state=PostconditionState.INCONCLUSIVE,
            recovery_state="PENDING",
        )
        audit = _audit(
            identity=identity,
            metadata=metadata,
            action_digest=digest,
            timestamp=timestamp,
            decision="ALLOW",
            decision_reasons=["authorization_and_commit_checks_passed", "outcome_unknown"],
            execution_state="EXECUTION_OUTCOME_UNKNOWN",
            postcondition_state="INCONCLUSIVE",
            recovery_state="PENDING",
            evidence_ids=evidence_ids,
            verifier_ids=verifier_ids,
        )
        return TransactionResult(envelope, digest, None, receipt, audit, True)

    verified = postcondition(response)
    post_state = PostconditionState.VERIFIED if verified else PostconditionState.FAILED
    recovery_state = "NONE" if verified else "PENDING"
    receipt = _receipt(
        identity=identity,
        metadata=metadata,
        action_digest=digest,
        timestamp=timestamp,
        execution_state=ExecutionState.EXECUTED,
        provider_receipt=response,
        postcondition_state=post_state,
        recovery_state=recovery_state,
    )
    provider_receipt_id = None
    if isinstance(response.get("evidence_sha256"), str):
        provider_receipt_id = "sha256:" + response["evidence_sha256"].removeprefix("sha256:")

    audit = _audit(
        identity=identity,
        metadata=metadata,
        action_digest=digest,
        timestamp=timestamp,
        decision="ALLOW",
        decision_reasons=["authorization_and_commit_checks_passed"],
        execution_state="EXECUTED",
        postcondition_state=post_state.value,
        recovery_state=recovery_state,
        provider_receipt_id=provider_receipt_id,
        evidence_ids=evidence_ids,
        verifier_ids=verifier_ids,
    )
    return TransactionResult(envelope, digest, response, receipt, audit, False)
