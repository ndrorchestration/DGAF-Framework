"""AKDC Gate 6: version-pinned raw-frame *fixtures*, never an authenticated transport.

This module accepts already-decoded JSON objects and receiver-captured context.
It does not negotiate protocols, attest identity, inspect network packets, or
establish total ordering across reconnects. Always treat output as unverified.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from experiments.akdc.akdc_ingress_bridge import (
    A2A_STATES,
    ProtocolObservation,
    canonical_bytes,
    content_digest,
    make_dgaf_envelope,
)

A2A_PIN = "1.0.1"
MCP_PIN = "2026-07-28"
MAX_FRAME_SIZE = 65536


@dataclass(frozen=True)
class ReceiverWitness:
    """Locally supplied facts; *not* protocol origin or authenticated order."""

    provider_id: str
    runtime_id: str
    source_id: str
    stream_id: str
    receipt_number: int
    observed_at: str


@dataclass(frozen=True)
class CapturedObservation:
    observation: ProtocolObservation
    canonical_frame_digest: str
    receiver_stream_id: str
    receiver_receipt_number: int
    ordering_basis: str

    def record_only_envelope(self) -> dict[str, Any]:
        """DGAF ingress still has to verify; admission grants no authority."""
        envelope = make_dgaf_envelope(self.observation)
        evidence = envelope["evidence"]
        evidence["payload"]["capture_reference"] = {
            "canonical_decoded_frame_digest": self.canonical_frame_digest,
            "receiver_stream_id": self.receiver_stream_id,
            "receiver_receipt_number": self.receiver_receipt_number,
            "ordering_basis": self.ordering_basis,
            "capture_attestation": "NOT_ESTABLISHED",
        }
        evidence["content_digest"] = content_digest(evidence["payload"])
        return envelope


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    if len(canonical_bytes(value)) > MAX_FRAME_SIZE:
        raise ValueError(f"{label} exceeds bounded research frame size")
    return value


def _witness(witness: ReceiverWitness) -> None:
    if type(witness.receipt_number) is not int or witness.receipt_number < 1:
        raise ValueError("positive receiver receipt_number required")
    if not isinstance(witness.stream_id, str) or not witness.stream_id.strip():
        raise ValueError("explicit receiver stream identity required")
    for key in ("provider_id", "runtime_id", "source_id", "stream_id"):
        value = getattr(witness, key)
        if not isinstance(value, str) or not value.isascii() or not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"invalid untrusted witness identifier: {key}")


def _observed(payload: dict[str, Any], protocol: str, version: str, witness: ReceiverWitness, raw: Any):
    _witness(witness)
    digest = content_digest(raw)
    # Digest is for canonicalized, decoded JSON, NOT original wire bytes.
    # Stable for an identical captured frame and receipt; NOT stable across
    # independent stream IDs or transport reconnects. This is not dedup proof.
    identity = content_digest(
        [
            protocol,
            version,
            witness.provider_id,
            witness.runtime_id,
            witness.source_id,
            witness.stream_id,
            witness.receipt_number,
            digest,
        ]
    )[7:]
    obs = ProtocolObservation(
        protocol=protocol,
        version=version,
        provider_id=witness.provider_id,
        runtime_id=witness.runtime_id,
        source_id=witness.source_id,
        event_id="rxe-" + identity,
        effect_id="rxf-" + identity,
        observed_at=witness.observed_at,
        payload=payload,
    )
    return CapturedObservation(
        obs, digest, witness.stream_id, witness.receipt_number, "UNVERIFIED_RECEIVER_LOCAL_ORDER"
    )


def normalize_a2a_status_update(
    frame: dict[str, Any], witness: ReceiverWitness, *, negotiated_version: str
) -> CapturedObservation:
    """Normalize A2A v1.0.1 StreamResponse.statusUpdate, not an SDK test."""
    if negotiated_version != A2A_PIN:
        raise ValueError("unsupported or unnegotiated A2A version")
    obj = _object(frame, "A2A frame")
    if set(obj) != {"statusUpdate"}:
        raise ValueError("only one statusUpdate response branch supported")
    event = _object(obj["statusUpdate"], "A2A statusUpdate")
    if set(event) - {"taskId", "contextId", "status", "metadata"}:
        raise ValueError("unknown A2A status event fields")
    for name in ("taskId", "contextId"):
        if not isinstance(event.get(name), str) or not event[name]:
            raise ValueError(f"missing A2A {name}")
    status = _object(event.get("status"), "A2A status")
    state = status.get("state")
    if not isinstance(state, str) or state not in A2A_STATES:
        raise ValueError("unsupported A2A task state")
    if "metadata" in event and not isinstance(event["metadata"], dict):
        raise ValueError("malformed A2A metadata")
    if set(status) - {"state", "message", "timestamp"}:
        raise ValueError("unsupported A2A status fields")
    # The existing bridge's 'sequence' is a normalized LOCAL receipt counter.
    # A2A v1.0.1 does not define it on this wire event.
    payload = {
        "task_id": event["taskId"],
        "context_id": event["contextId"],
        "state": state,
        "sequence": witness.receipt_number,
    }
    return _observed(payload, "a2a", A2A_PIN, witness, obj)


def _request_id(value: Any) -> bool:
    return type(value) in (str, int)


def normalize_mcp_tools_call(
    request: dict[str, Any], response: dict[str, Any], witness: ReceiverWitness, *, negotiated_version: str
) -> CapturedObservation:
    """Pair raw MCP JSON-RPC request/response; never infer method from reply."""
    if negotiated_version != MCP_PIN:
        raise ValueError("unsupported or unnegotiated MCP version")
    req = _object(request, "MCP request")
    resp = _object(response, "MCP response")
    if req.get("jsonrpc") != "2.0" or req.get("method") != "tools/call":
        raise ValueError("not a captured tools/call request")
    if not _request_id(req.get("id")):
        raise ValueError("MCP request id must be nonnull string/int, not bool")
    params = req.get("params")
    if not isinstance(params, dict) or not isinstance(params.get("name"), str) or not params["name"]:
        raise ValueError("missing MCP tool name")
    if "_meta" not in params or not isinstance(params["_meta"], dict):
        raise ValueError("MCP 2026 wire request requires params._meta")
    if resp.get("jsonrpc") != "2.0" or resp.get("id") != req["id"] or type(resp.get("id")) is not type(req["id"]):
        raise ValueError("MCP response does not correlate to captured request")
    if ("result" in resp) == ("error" in resp):
        raise ValueError("MCP response must contain exactly one result or error")
    if "error" in resp:
        error = _object(resp["error"], "MCP protocol error")
        if type(error.get("code")) is not int or not isinstance(error.get("message"), str):
            raise ValueError("MCP error code/message malformed")
    else:
        result = _object(resp["result"], "MCP result")
        result_type = result.get("resultType")
        if result_type == "complete":
            if not isinstance(result.get("content"), list):
                raise ValueError("MCP complete requires content")
            if type(result.get("isError", False)) is not bool:
                raise ValueError("MCP isError must be bool")
        elif result_type == "input_required":
            # This fixture records only the discriminator, not an input workflow.
            if "content" in result or "isError" in result:
                raise ValueError("unsupported hybrid MCP input_required")
        else:
            raise ValueError("missing or unsupported MCP 2026 resultType")
    # Provide only the response shape expected by the preexisting bridge;
    # the request is linked by the digest of the CAPTURED PAIR below.
    payload = {"method": "tools/call", "response": resp}
    return _observed(payload, "mcp", MCP_PIN, witness, {"request": req, "response": resp})
