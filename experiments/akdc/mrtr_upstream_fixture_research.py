"""Gate 10: bounded observation of source-pinned MCP 2026 MRTR examples.

Fixture-level capability negative control only; no trusted negotiation,
SDK execution, MRTR retry, authorization, or transport capture.
"""

from __future__ import annotations

from typing import Any

from experiments.akdc.raw_wire_research import (
    CapturedObservation,
    ReceiverWitness,
    normalize_mcp_tools_call,
)

SUPPORTED_MRTR_METHODS = frozenset({"elicitation/create", "sampling/createMessage", "roots/list"})


def observe_mrtr_example(
    request: dict[str, Any],
    response: dict[str, Any],
    witness: ReceiverWitness,
    *,
    negotiated_version: str,
    capture_key: bytes,
    key_id: str,
    declared_methods: frozenset[str],
) -> CapturedObservation:
    """Fail closed on unrecognized or undeclared embedded input methods.

    The methods are claimed by the local caller; this is NOT verification
    of a remote peer's authenticated capabilities.
    """
    if type(declared_methods) is not frozenset or not all(
        isinstance(item, str) for item in declared_methods
    ):
        raise ValueError("explicit, well-formed declared_methods frozenset required")
    if not isinstance(response, dict) or not isinstance(response.get("result"), dict):
        raise ValueError("MRTR fixture requires a JSON-RPC result object")
    result = response["result"]
    if result.get("resultType") != "input_required":
        raise ValueError("MRTR fixture must be input_required")
    input_requests = result.get("inputRequests", {})
    if not isinstance(input_requests, dict):
        raise ValueError("MRTR inputRequests must be an object")
    for request_key, embedded_request in input_requests.items():
        if not isinstance(request_key, str) or not request_key:
            raise ValueError("MRTR input request identifier must be nonempty")
        if not isinstance(embedded_request, dict):
            raise ValueError("MRTR embedded request must be object")
        method = embedded_request.get("method")
        if not isinstance(method, str) or method not in SUPPORTED_MRTR_METHODS:
            raise ValueError("unsupported MRTR embedded method")
        if method not in declared_methods:
            raise ValueError("MRTR method not declared supported by fixture peer")
        if not isinstance(embedded_request.get("params"), dict):
            raise ValueError("MRTR embedded request params must be object")
    return normalize_mcp_tools_call(
        request,
        response,
        witness,
        negotiated_version=negotiated_version,
        capture_key=capture_key,
        key_id=key_id,
    )
