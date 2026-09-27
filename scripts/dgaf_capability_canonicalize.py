from __future__ import annotations

import hashlib
import json
from typing import Any

CANONICALIZATION_ID = "dgaf-json-v0.1"


class CanonicalizationError(ValueError):
    """Raised when an object cannot be represented by DGAF JSON v0.1."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for digest binding.

    DGAF JSON v0.1 uses sorted object keys, no insignificant whitespace,
    UTF-8 output, preserved Unicode, and rejects NaN/Infinity.
    """
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalizationError(str(exc)) from exc
    return text.encode("utf-8")


def sha256_digest(value: Any) -> str:
    payload = canonical_json_bytes(value)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def canonical_action_envelope(
    *,
    capability_id: str,
    capability_version: str,
    resource: dict[str, Any],
    parameters: dict[str, Any],
    initiating_principal: str,
    executing_principal: str,
    delegation_chain_id: str | None,
    policy_id: str,
    policy_version: str,
    state_guards: dict[str, Any] | None = None,
    nonce: str,
) -> dict[str, Any]:
    """Build the minimum digest-bound action envelope."""
    return {
        "canonicalization": CANONICALIZATION_ID,
        "capability": {
            "id": capability_id,
            "version": capability_version,
        },
        "resource": resource,
        "parameters": parameters,
        "initiating_principal": initiating_principal,
        "executing_principal": executing_principal,
        "delegation_chain_id": delegation_chain_id,
        "policy": {"id": policy_id, "version": policy_version},
        "state_guards": state_guards or {},
        "nonce": nonce,
    }
