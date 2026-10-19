"""Real loopback-effect tests for the bounded SBCF reference adapter."""

from __future__ import annotations

import socket
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from experiments.sbcf.runtime_effect_adapter import BoundLoopbackHTTPEffectAdapter
from scripts.dgaf_capability_pep import (
    ApprovalState,
    EnforcementContext,
    VerificationState,
)
from scripts.dgaf_capability_policy import Authority
from scripts.dgaf_capability_reference_transaction import (
    TransactionIdentity,
    TransactionMetadata,
    run_reference_transaction,
)

NOW = datetime(2026, 10, 19, 6, 30, tzinfo=timezone.utc)


class RecordingHandler(BaseHTTPRequestHandler):
    def log_message(self, _format, *_args):
        return

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.server.events.append(("POST", self.path, body))  # type: ignore[attr-defined]
        self.send_response(204)
        self.end_headers()

    def do_GET(self):  # noqa: N802
        self.server.events.append(("GET", self.path, b""))  # type: ignore[attr-defined]
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "http://example.com/")
        else:
            self.send_response(200)
        self.end_headers()


def authority(capabilities, resources):
    return Authority(frozenset(capabilities), frozenset(resources))


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), RecordingHandler)
    server.events = []  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def metadata(resource_id, *, method="POST", body="authorized"):
    return TransactionMetadata(
        capability_id="sbcf.loopback.http",
        capability_version="0.1.0",
        resource={"id": resource_id},
        parameters={"method": method, "body": body},
        initiating_principal="agent:sbcf-test",
        executing_principal="gateway:loopback-reference",
        delegation_chain_id="delegation:sbcf-loopback",
        policy_id="policy:sbcf-loopback-reference",
        policy_version="0.1.0",
        state_guards={"fixture": "matched-effect-v0"},
        nonce="nonce:sbcf-loopback-v0",
        adapter_identity="sbcf-loopback-http-reference",
        runtime_identity="runtime:local-loopback-test",
    )


def identities():
    return TransactionIdentity(
        workflow_id="workflow:sbcf-loopback-v0",
        invocation_id="invoke:sbcf-loopback-v0",
        authorization_id="auth:sbcf-loopback-v0",
        idempotency_key="idem:sbcf-loopback-v0",
        event_id="audit:sbcf-loopback-v0",
    )


def context_factory(meta, *, active=True, resource_override=None):
    def factory(digest):
        capability = meta.capability_id
        resource = resource_override or meta.resource["id"]
        allowed = authority({capability}, {resource})
        return EnforcementContext(
            capability=capability,
            resource=meta.resource["id"],
            protected_side_effect=True,
            requester_authority=allowed,
            delegation_authority=allowed,
            executor_authority=allowed,
            policy_authority=allowed,
            authorization_status="ACTIVE" if active else "REVOKED",
            authorization_not_before=NOW - timedelta(minutes=5),
            authorization_expires_at=NOW + timedelta(minutes=5),
            commit_digest=digest,
            approval=ApprovalState(
                requester=meta.initiating_principal,
                approver="human:reviewer",
                approved_digest=digest,
                consumed=False,
            ),
            verification=VerificationState(required=True, passed=True),
            required_state_guards=meta.state_guards,
            observed_state_guards=meta.state_guards,
            now=NOW,
        )

    return factory


def run_effect(meta, adapter, *, request=None, active=True, resource_override=None):
    return run_reference_transaction(
        request=dict(meta.parameters) if request is None else request,
        identity=identities(),
        metadata=meta,
        context_factory=context_factory(
            meta,
            active=active,
            resource_override=resource_override,
        ),
        dispatcher=adapter.dispatch,
        postcondition=lambda response: response["http_status"] in {200, 204, 302},
        timestamp=NOW,
        evidence_ids=["evidence:sbcf-loopback-reference"],
        verifier_ids=["verifier:capability-pep-reference"],
    )


def test_authorized_digest_bound_post_reaches_real_loopback_effect():
    server, thread = start_server()
    try:
        resource = f"http://127.0.0.1:{server.server_port}/effect"
        meta = metadata(resource)
        adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters)

        result = run_effect(meta, adapter)

        assert server.events == [("POST", "/effect", b"authorized")]  # type: ignore[attr-defined]
        assert result.audit_event["decision"] == "ALLOW"
        assert result.execution_receipt["execution_state"] == "EXECUTED"
        assert result.execution_receipt["postcondition_state"] == "VERIFIED"
        assert result.response["effect_boundary"] == "loopback_http_reference_runtime"
        assert result.response["http_status"] == 204
        assert result.response["redirect_followed"] is False
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_revoked_authorization_blocks_before_real_effect():
    server, thread = start_server()
    try:
        resource = f"http://127.0.0.1:{server.server_port}/effect"
        meta = metadata(resource)
        adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters)

        result = run_effect(meta, adapter, active=False)

        assert server.events == []  # type: ignore[attr-defined]
        assert result.audit_event["decision"] == "DENY"
        assert result.execution_receipt is None
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_adjacent_resource_scope_is_blocked_before_real_effect():
    server, thread = start_server()
    try:
        resource = f"http://127.0.0.1:{server.server_port}/effect"
        adjacent = f"http://127.0.0.1:{server.server_port}/other"
        meta = metadata(resource)
        adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters)

        result = run_effect(meta, adapter, resource_override=adjacent)

        assert server.events == []  # type: ignore[attr-defined]
        assert result.audit_event["decision"] == "DENY"
        assert "effective authority" in result.audit_event["decision_reasons"][0]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_runtime_request_mismatch_is_blocked_before_real_effect():
    server, thread = start_server()
    try:
        resource = f"http://127.0.0.1:{server.server_port}/effect"
        meta = metadata(resource)
        adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters)

        result = run_effect(
            meta,
            adapter,
            request={"method": "POST", "body": "tampered"},
        )

        assert server.events == []  # type: ignore[attr-defined]
        assert result.audit_event["decision"] == "DENY"
        assert "digest-bound adapter action" in result.audit_event["decision_reasons"][0]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_redirect_response_is_observed_but_not_followed():
    server, thread = start_server()
    try:
        resource = f"http://127.0.0.1:{server.server_port}/redirect"
        meta = metadata(resource, method="GET", body="")
        adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters)

        result = run_effect(meta, adapter)

        assert server.events == [("GET", "/redirect", b"")]  # type: ignore[attr-defined]
        assert result.response["http_status"] == 302
        assert result.response["redirect_followed"] is False
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.mark.parametrize(
    "resource",
    [
        "https://127.0.0.1:443/effect",
        "http://localhost:8080/effect",
        "http://example.com:8080/effect",
        "http://127.0.0.1/effect",
        "http://user:pass@127.0.0.1:8080/effect",
        "http://127.0.0.1:8080/effect?query=yes",
        "http://127.0.0.1:8080/effect#fragment",
    ],
)
def test_adapter_rejects_non_exact_loopback_resource(resource):
    with pytest.raises(ValueError):
        BoundLoopbackHTTPEffectAdapter(
            resource,
            {"method": "POST", "body": "authorized"},
        )


def test_adapter_rejects_unsupported_method():
    with pytest.raises(ValueError):
        BoundLoopbackHTTPEffectAdapter(
            "http://127.0.0.1:8080/effect",
            {"method": "DELETE", "body": ""},
        )


def test_get_requires_empty_body():
    with pytest.raises(ValueError):
        BoundLoopbackHTTPEffectAdapter(
            "http://127.0.0.1:8080/effect",
            {"method": "GET", "body": "unexpected"},
        )


def test_unreachable_loopback_effect_fails_to_unknown_without_false_success():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    resource = f"http://127.0.0.1:{port}/effect"
    meta = metadata(resource)
    adapter = BoundLoopbackHTTPEffectAdapter(resource, meta.parameters, timeout_seconds=0.5)

    result = run_effect(meta, adapter)

    assert result.response is None
    assert result.reconciliation_required is True
    assert result.execution_receipt["execution_state"] == "EXECUTION_OUTCOME_UNKNOWN"
    assert result.audit_event["decision"] == "ALLOW"
    assert "outcome_unknown" in result.audit_event["decision_reasons"]
