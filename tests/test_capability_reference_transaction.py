from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jsonschema

from scripts.dgaf_capability_idempotency import (
    IdempotencyState,
    InMemoryIdempotencyLedger,
)
from scripts.dgaf_capability_pep import (
    ApprovalState,
    EnforcementContext,
    VerificationState,
)
from scripts.dgaf_capability_policy import Authority
from scripts.dgaf_capability_reference_transaction import (
    ExecutionOutcomeUnknown,
    TransactionIdentity,
    TransactionMetadata,
    run_reference_transaction,
)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 9, 25, 13, 45, tzinfo=timezone.utc)


def authority(capabilities, resources):
    return Authority(frozenset(capabilities), frozenset(resources))


def identities():
    return TransactionIdentity(
        workflow_id="workflow:reference-1",
        invocation_id="invoke:reference-1",
        authorization_id="auth:reference-1",
        idempotency_key="idem:reference-1",
        event_id="audit:reference-1",
    )


def protected_metadata():
    return TransactionMetadata(
        capability_id="dgaf.local.materialize",
        capability_version="0.1.0",
        resource={"id": "dgaf.local.materialized_input"},
        parameters={"action": "materialize"},
        initiating_principal="agent:operator",
        executing_principal="gateway:local",
        delegation_chain_id="delegation:reference-1",
        policy_id="policy:local-materialization",
        policy_version="0.1.0",
        state_guards={"input_sha": "abc"},
        nonce="nonce-reference-1",
        adapter_identity="dgaf-local-mcp-adapter",
        runtime_identity="runtime:local-test",
    )


def status_metadata():
    return TransactionMetadata(
        capability_id="dgaf.local.status",
        capability_version="0.1.0",
        resource={"id": "dgaf.local.state"},
        parameters={"action": "status"},
        initiating_principal="agent:observer",
        executing_principal="gateway:local",
        delegation_chain_id=None,
        policy_id="policy:local-status",
        policy_version="0.1.0",
        state_guards={},
        nonce="nonce-status-1",
        adapter_identity="dgaf-local-mcp-adapter",
        runtime_identity="runtime:local-test",
    )


def context_factory(metadata, *, protected=True, active=True):
    def factory(digest):
        cap = metadata.capability_id
        resource = metadata.resource["id"]
        allowed = authority({cap}, {resource})
        status = "ACTIVE" if active else "REVOKED"
        return EnforcementContext(
            capability=cap,
            resource=resource,
            protected_side_effect=protected,
            requester_authority=allowed,
            delegation_authority=allowed,
            executor_authority=allowed,
            policy_authority=allowed,
            authorization_status=status,
            authorization_not_before=NOW - timedelta(minutes=5),
            authorization_expires_at=NOW + timedelta(minutes=5),
            commit_digest=digest,
            approval=ApprovalState(
                requester=metadata.initiating_principal,
                approver="human:reviewer",
                approved_digest=digest,
                consumed=False,
            ),
            verification=VerificationState(required=protected, passed=True),
            required_state_guards=metadata.state_guards,
            observed_state_guards=metadata.state_guards,
            now=NOW,
        )

    return factory


def validate_result(result):
    receipt_schema = json.loads((ROOT / "schemas" / "execution_receipt.schema.json").read_text(encoding="utf-8"))
    audit_schema = json.loads((ROOT / "schemas" / "capability_audit_event.schema.json").read_text(encoding="utf-8"))
    if result.execution_receipt is not None:
        jsonschema.validate(result.execution_receipt, receipt_schema)
    jsonschema.validate(result.audit_event, audit_schema)


def test_protected_reference_transaction_emits_receipt_and_audit():
    metadata = protected_metadata()
    calls = []

    def dispatcher(request):
        calls.append(request)
        return {
            "status": "PASS",
            "action": "materialize",
            "synthetic_reference_only": True,
            "secret_material_returned": False,
            "scientific_n_increment": 0,
        }

    result = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=dispatcher,
        postcondition=lambda response: response["status"] == "PASS",
        timestamp=NOW,
        evidence_ids=["evidence:synthetic-reference"],
        verifier_ids=["verifier:reference"],
    )
    assert calls == [{"action": "materialize"}]
    assert result.audit_event["decision"] == "ALLOW"
    assert result.execution_receipt["execution_state"] == "EXECUTED"
    assert result.execution_receipt["postcondition_state"] == "VERIFIED"
    assert result.reconciliation_required is False
    validate_result(result)


def test_denied_reference_transaction_never_calls_dispatcher():
    metadata = protected_metadata()
    calls = []

    result = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata, active=False),
        dispatcher=lambda request: calls.append(request) or {"status": "PASS"},
        postcondition=lambda response: True,
        timestamp=NOW,
    )

    assert calls == []
    assert result.execution_receipt is None
    assert result.audit_event["decision"] == "DENY"
    assert result.audit_event["execution_state"] == "NOT_STARTED"
    validate_result(result)


def test_unknown_execution_outcome_requires_reconciliation():
    metadata = protected_metadata()

    def dispatcher(_request):
        raise ExecutionOutcomeUnknown("provider timed out after dispatch")

    result = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=dispatcher,
        postcondition=lambda response: False,
        timestamp=NOW,
    )

    assert result.response is None
    assert result.reconciliation_required is True
    assert result.execution_receipt["execution_state"] == "EXECUTION_OUTCOME_UNKNOWN"
    assert result.execution_receipt["postcondition_state"] == "INCONCLUSIVE"
    assert result.audit_event["recovery_state"] == "PENDING"
    validate_result(result)


def load_bridge():
    scripts = ROOT / "scripts"
    bridge_path = scripts / "dgaf_local_operator_bridge.py"
    spec = importlib.util.spec_from_file_location("dgaf_local_operator_bridge", bridge_path)
    assert spec is not None and spec.loader is not None
    import sys

    original = list(sys.path)
    try:
        sys.path.insert(0, str(scripts))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original
    return module


def test_real_bridge_status_flows_through_reference_transaction_without_promotion():
    bridge = load_bridge()
    metadata = status_metadata()

    result = run_reference_transaction(
        request={"action": "status"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata, protected=False, active=False),
        dispatcher=bridge.dispatch,
        postcondition=lambda response: (
            response["network_listener"] is False
            and response["scientific_n_increment"] == 0
            and response["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
        ),
        timestamp=NOW,
    )

    assert result.response["bridge"] == "DGAF_LOCAL_OPERATOR_BRIDGE"
    assert result.response["scientific_n_increment"] == 0
    assert result.response["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert result.execution_receipt["execution_state"] == "EXECUTED"
    assert result.execution_receipt["postcondition_state"] == "VERIFIED"
    validate_result(result)


def test_failed_postcondition_preserves_execution_and_marks_recovery_pending():
    metadata = protected_metadata()

    result = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=lambda request: {
            "status": "PASS",
            "action": request["action"],
            "synthetic_reference_only": True,
        },
        postcondition=lambda response: False,
        timestamp=NOW,
    )

    assert result.execution_receipt["execution_state"] == "EXECUTED"
    assert result.execution_receipt["postcondition_state"] == "FAILED"
    assert result.execution_receipt["recovery_state"] == "PENDING"
    assert result.audit_event["execution_state"] == "EXECUTED"
    validate_result(result)


def test_completed_idempotent_replay_does_not_dispatch_twice():
    metadata = protected_metadata()
    ledger = InMemoryIdempotencyLedger()
    calls = []

    def dispatcher(request):
        calls.append(request)
        return {
            "status": "PASS",
            "action": request["action"],
            "synthetic_reference_only": True,
        }

    first = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=dispatcher,
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )
    second = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=dispatcher,
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )

    assert calls == [{"action": "materialize"}]
    assert first.replayed is False
    assert second.replayed is True
    assert second.action_digest == first.action_digest
    assert ledger.get(identities().idempotency_key).state == IdempotencyState.COMPLETED


def test_idempotency_key_cannot_bind_different_action_digest():
    ledger = InMemoryIdempotencyLedger()
    metadata = protected_metadata()
    calls = []
    first = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=lambda request: calls.append(request) or {"status": "PASS"},
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )

    changed = TransactionMetadata(
        **{
            **metadata.__dict__,
            "parameters": {"action": "materialize", "variant": "changed"},
        }
    )
    second = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=changed,
        context_factory=context_factory(changed),
        dispatcher=lambda request: calls.append(request) or {"status": "PASS"},
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )
    assert first.audit_event["decision"] == "ALLOW"
    assert second.audit_event["decision"] == "DENY"
    assert "different action digest" in second.audit_event["decision_reasons"][0]
    assert len(calls) == 1


def test_unknown_outcome_blocks_retry_until_reconciled():
    ledger = InMemoryIdempotencyLedger()
    metadata = protected_metadata()
    calls = []

    def unknown_dispatcher(request):
        calls.append(request)
        raise ExecutionOutcomeUnknown("timeout after provider dispatch")

    first = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=unknown_dispatcher,
        postcondition=lambda response: False,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )
    retry = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=lambda request: calls.append(request) or {"status": "PASS"},
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )

    assert first.reconciliation_required is True
    assert ledger.get(identities().idempotency_key).state == IdempotencyState.OUTCOME_UNKNOWN
    assert retry.audit_event["decision"] == "ESCALATE"
    assert retry.reconciliation_required is True
    assert len(calls) == 1


def test_reconciled_failed_unknown_outcome_can_retry():
    ledger = InMemoryIdempotencyLedger()
    metadata = protected_metadata()
    calls = []
    first = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=lambda request: (_ for _ in ()).throw(ExecutionOutcomeUnknown("timeout after provider dispatch")),
        postcondition=lambda response: False,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )
    ledger.reconcile_failed(
        identities().idempotency_key,
        first.action_digest,
    )

    retry = run_reference_transaction(
        request={"action": "materialize"},
        identity=identities(),
        metadata=metadata,
        context_factory=context_factory(metadata),
        dispatcher=lambda request: calls.append(request) or {"status": "PASS"},
        postcondition=lambda response: True,
        timestamp=NOW,
        idempotency_ledger=ledger,
    )

    assert retry.audit_event["decision"] == "ALLOW"
    assert retry.execution_receipt["execution_state"] == "EXECUTED"
    assert calls == [{"action": "materialize"}]
