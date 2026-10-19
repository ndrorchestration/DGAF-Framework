"""Independent pre-policy benchmark envelope check; do not rewrite frozen rules.

This gate is applied identically to every comparator in a *versioned*
engineering characterization. INPUT_REJECTED != DENY by the historical policy.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

CONTRACT_FILE = Path(__file__).with_name("input_envelope_v1.json")
REJECTED = "INPUT_REJECTED"


@dataclass(frozen=True)
class GateResult:
    status: str
    errors: tuple[str, ...]
    admitted: dict[str, Any] | None


def contract_sha256() -> str:
    return hashlib.sha256(CONTRACT_FILE.read_bytes()).hexdigest()


def _valid_type(value: object, expected: str) -> bool:
    return type(value) is bool if expected == "boolean" else type(value) is str


def validate(case: object) -> GateResult:
    """Return a separate typed reject, or a complete, copied common policy input.

    Strictly JSON-shaped: all domain keys/types are exact. Root metadata fields
    may be present but are not trusted as authorization inputs.
    """
    spec = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    if type(case) is not dict:
        return GateResult(REJECTED, ("root:object_required",), None)

    errors: list[str] = []
    raw: dict[str, Any] = case
    domains: dict[str, Any] = spec["domains"]
    metadata: dict[str, str] = spec["metadata"]
    legal = set(domains) | set(metadata)
    for key in sorted(raw.keys(), key=str):
        if type(key) is not str:
            errors.append("root:non_string_key")
        elif key not in legal:
            errors.append(f"root:unexpected:{key}")

    for key, expected in metadata.items():
        if key in raw and not _valid_type(raw[key], expected):
            errors.append(f"{key}:{expected}_required")

    admitted: dict[str, Any] = {}
    for domain, rules in domains.items():
        if domain not in raw:
            if domain in spec["root_required"]:
                errors.append(f"{domain}:required")
            admitted[domain] = None
            continue
        value = raw[domain]
        if value is None and rules["nullable"]:
            admitted[domain] = None
            continue
        if type(value) is not dict:
            errors.append(f"{domain}:object_required")
            continue
        fields: dict[str, str] = rules["required"]
        for key in sorted(value.keys(), key=str):
            if type(key) is not str:
                errors.append(f"{domain}:non_string_key")
            elif key not in fields:
                errors.append(f"{domain}:unexpected:{key}")
        for field, expected in fields.items():
            if field not in value:
                errors.append(f"{domain}.{field}:required")
            elif not _valid_type(value[field], expected):
                errors.append(f"{domain}.{field}:{expected}_required")
        admitted[domain] = {key: value[key] for key in fields if key in value}

    if errors:
        return GateResult(REJECTED, tuple(sorted(set(errors))), None)
    for key in metadata:
        if key in raw:
            admitted[key] = raw[key]
    return GateResult("ADMITTED_FOR_COMPARISON", (), admitted)


def evaluate_all(
    case: object, comparators: dict[str, Callable[[dict[str, Any]], tuple[str, list[str]]]]
) -> dict[str, Any]:
    """One common pre-gate, no invocation of any policy on an invalid case."""
    result = validate(case)
    if result.status == REJECTED:
        return {
            "input_state": REJECTED,
            "input_errors": list(result.errors),
            "policy_results": {name: "NOT_EVALUATED" for name in comparators},
        }
    assert result.admitted is not None
    decisions = {}
    for name, fn in comparators.items():
        decision, _ = fn(result.admitted)
        if decision not in ("ALLOW", "DENY"):
            raise ValueError(f"UNSUPPORTED_COMPARATOR_DECISION:{name}")
        decisions[name] = decision
    return {"input_state": result.status, "input_errors": [], "policy_results": decisions}
