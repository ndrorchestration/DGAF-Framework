"""AKDC research: A2A/MCP observation to non-authoritative DGAF record.

Not a transport, authentication mechanism, policy engine, or production adapter.
No network I/O, execution, authorization, scientific state, or custody access.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any

BRIDGE_VERSION = "0.3.0-research"
A2A_VERSION = "1.0.1"
MCP_VERSION = "2026-07-28"
OPAQUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")

A2A_STATES = frozenset({
    "TASK_STATE_SUBMITTED", "TASK_STATE_WORKING", "TASK_STATE_COMPLETED",
    "TASK_STATE_FAILED", "TASK_STATE_CANCELED", "TASK_STATE_INPUT_REQUIRED",
    "TASK_STATE_REJECTED", "TASK_STATE_AUTH_REQUIRED", "TASK_STATE_UNSPECIFIED",
})
A2A_TERMINAL = frozenset({
    "TASK_STATE_COMPLETED", "TASK_STATE_FAILED", "TASK_STATE_CANCELED",
    "TASK_STATE_REJECTED",
})


def canonical_bytes(item: Any) -> bytes:
    return json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def content_digest(item: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(item)).hexdigest()


def _identifier(text: str, name: str) -> str:
    if not isinstance(text, str) or not OPAQUE.fullmatch(text):
        raise ValueError(f"invalid {name}")
    return text


def _timestamp(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("missing timestamp")
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("malformed timestamp") from exc
    if dt.tzinfo is None:
        raise ValueError("timestamp must include UTC offset")
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ProtocolObservation:
    protocol: str
    version: str
    provider_id: str
    runtime_id: str
    source_id: str
    event_id: str
    effect_id: str
    observed_at: str
    payload: dict[str, Any]


def _classify_a2a(payload: dict[str, Any]) -> str:
    # A2A 1.0.1 uses TASK_STATE_*; other versions must have separate adapters.
    if set(payload) != {"task_id", "context_id", "state", "sequence"}:
        raise ValueError("A2A event shape unsupported")
    _identifier(payload["task_id"], "task_id")
    _identifier(payload["context_id"], "context_id")
    if type(payload["sequence"]) is not int or payload["sequence"] < 0:
        raise ValueError("invalid A2A sequence")
    state = payload["state"]
    if not isinstance(state, str) or state not in A2A_STATES:
        raise ValueError("unknown or unpinned A2A state")
    return "A2A_OBSERVED_" + state


def _classify_mcp(payload: dict[str, Any]) -> str:
    # Strict research fixture for a raw tools/call JSON-RPC response.
    if set(payload) != {"method", "response"} or payload["method"] != "tools/call":
        raise ValueError("only MCP tools/call response observations supported")
    response = payload["response"]
    if not isinstance(response, dict) or response.get("jsonrpc") != "2.0":
        raise ValueError("invalid JSON-RPC response")
    if ("id" not in response or isinstance(response["id"], bool)
            or not isinstance(response["id"], (int, str))):
        raise ValueError("response correlation id required")
    if ("result" in response) == ("error" in response):
        raise ValueError("exactly one of JSON-RPC result or error required")
    if "error" in response:
        error = response["error"]
        if (not isinstance(error, dict) or type(error.get("code")) is not int
                or not isinstance(error.get("message"), str)):
            raise ValueError("malformed JSON-RPC error")
        return "MCP_PROTOCOL_ERROR_OBSERVED"
    result = response["result"]
    if not isinstance(result, dict):
        raise ValueError("MCP result must be object for this fixture")
    result_type = result.get("resultType")
    # MCP 2026-07-28 wire schema requires resultType. Older missing-field
    # fallback is deliberately NOT used for the pinned 2026 protocol.
    if result_type is None:
        raise ValueError("MCP 2026-07-28 requires resultType")
    if result_type == "input_required":
        return "MCP_INPUT_REQUIRED_OBSERVED"
    if result_type != "complete":
        raise ValueError("MCP task/future result not supported by this bridge")
    if not isinstance(result.get("isError", False), bool):
        raise ValueError("isError must be bool")
    if not isinstance(result.get("content"), list):
        raise ValueError("MCP CallToolResult content must be list")
    return "MCP_TOOL_ERROR_OBSERVED" if result.get("isError", False) else "MCP_TOOL_RESULT_OBSERVED"


def classify(observation: ProtocolObservation) -> str:
    if not isinstance(observation.payload, dict):
        raise ValueError("payload must be an object")
    if (observation.protocol, observation.version) == ("a2a", A2A_VERSION):
        return _classify_a2a(observation.payload)
    if (observation.protocol, observation.version) == ("mcp", MCP_VERSION):
        return _classify_mcp(observation.payload)
    raise ValueError("unsupported protocol/version pair")


def make_dgaf_envelope(observation: ProtocolObservation) -> dict[str, Any]:
    """Build ONLY a record-only, unverified external observation for DGAF."""
    state = classify(observation)
    for name in ("provider_id", "runtime_id", "source_id", "event_id", "effect_id"):
        _identifier(getattr(observation, name), name)
    normalized = {
        "protocol": observation.protocol,
        "protocol_version": observation.version,
        "observed_state": state,
        "external_payload": json.loads(canonical_bytes(observation.payload)),
        "bridge_version": BRIDGE_VERSION,
    }
    return {
        "schema_version": "DGAF_EXTERNAL_RUNTIME_ENVELOPE_V1",
        "provider": {
            "provider_id": observation.provider_id,
            "runtime_id": observation.runtime_id,
            "adapter_id": "akdc-observation-bridge",
            "adapter_version": "0.3.0",
        },
        "identity": {
            "event_id": observation.event_id,
            "effect_id": observation.effect_id,
            "source_id": observation.source_id,
        },
        "evidence": {
            "evidence_class": "EXTERNAL_UNTRUSTED_OBSERVATION",
            "observed_at": _timestamp(observation.observed_at),
            "content_digest": content_digest(normalized),
            "payload": normalized,
        },
        "provenance": {
            "producer_id": observation.provider_id,
            "producer_run_id": observation.runtime_id,
            "source_bindings": [observation.source_id],
        },
        "request": {
            "action_class": "NON_CONSEQUENTIAL_RECORD_INGRESS",
            "requested_transition": "RECORD_ONLY",
        },
        "assertions": {
            "verification_class": "EXTERNAL_UNVERIFIED",
            "authority": {"status": "EXTERNAL_OBSERVED_NOT_GRANTED"},
        },
        "risk": {
            "consequence_class": "NOT_APPLICABLE",
            "reversibility": "NOT_APPLICABLE",
        },
    }


class OrderingGate:
    """Single-process fixture ONLY; not durable, concurrent or a security gate."""
    def __init__(self) -> None:
        self._a2a: dict[tuple[str, str], tuple[int, str]] = {}
        self._effects: set[str] = set()
        self._events: dict[str, str] = {}

    def _check_ordering(self, observation: ProtocolObservation) -> None:
        classify(observation)
        if observation.effect_id in self._effects:
            raise ValueError("duplicate effect")
        if observation.event_id in self._events:
            raise ValueError("duplicate event")
        if observation.protocol == "a2a":
            task = (observation.source_id, observation.payload["task_id"])
            current = self._a2a.get(task)
            seq = observation.payload["sequence"]
            if current is not None:
                prev_seq, prev_state = current
                if seq <= prev_seq:
                    raise ValueError("duplicate/out-of-order task event")
                if prev_state in A2A_TERMINAL:
                    raise ValueError("terminal A2A task cannot transition")

    def _record(self, observation: ProtocolObservation, envelope: dict[str, Any]) -> None:
        if observation.protocol == "a2a":
            task = (observation.source_id, observation.payload["task_id"])
            self._a2a[task] = (observation.payload["sequence"], observation.payload["state"])
        self._events[observation.event_id] = content_digest(envelope)
        self._effects.add(observation.effect_id)

    def check_and_record(self, observation: ProtocolObservation) -> None:
        """Fixture helper; does not check DGAF admission."""
        self._check_ordering(observation)
        self._record(observation, make_dgaf_envelope(observation))

    def admit(self, observation: ProtocolObservation, validator, *, now: datetime) -> dict[str, Any]:
        """DGAF validates before toy replay-state mutation. Grants no authority."""
        self._check_ordering(observation)
        envelope = make_dgaf_envelope(observation)
        result = validator(envelope, seen_effect_ids=set(self._effects),
                           seen_events=dict(self._events), now=now)
        if not isinstance(result, dict):
            raise ValueError("invalid DGAF ingress result")
        if not result.get("admitted", False):
            return result
        if (result.get("authority_status") != "PRESENTED_NOT_GRANTED"
                or result.get("dgaf_verification_class") != "UNVERIFIED_EXTERNAL_ASSERTION"):
            raise ValueError("unexpected authority promotion at ingress boundary")
        self._record(observation, envelope)
        return result
