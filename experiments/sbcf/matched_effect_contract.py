"""Candidate common HTTP-effect semantics for a future matched comparator.

This module freezes nothing by itself. It validates a closed candidate contract
and reports every blocker that prevents the contract from being declared
FROZEN.
"""

from dataclasses import dataclass

from scripts.dgaf_capability_canonicalize import sha256_digest

_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "effect_kind",
        "effect_identity_fields",
        "witness",
        "system_mappings",
        "cases",
    }
)
_REQUIRED_WITNESS = frozenset(
    {
        "kind",
        "positive_rule",
        "negative_rule",
        "negative_observation_bound_ms",
    }
)
_REQUIRED_CASE = frozenset(
    {
        "id",
        "authority_state",
        "target_relation",
        "method_relation",
        "control_plane",
        "expected_decision",
        "expected_effect",
    }
)
_SYSTEMS = frozenset({"sbcf", "acs", "openshell"})
_MAPPING_STATES = frozenset(
    {
        "UNRESOLVED",
        "CANDIDATE_REFERENCE_RUNTIME",
        "CANDIDATE_ENFORCED_RUNTIME",
        "FROZEN",
    }
)
_EXPECTED_CASES = {
    "exact_allow": (
        "ACTIVE",
        "EXACT",
        "EXACT",
        "AVAILABLE",
        "ALLOW",
        "COMMITTED",
    ),
    "adjacent_host": (
        "ACTIVE",
        "ADJACENT",
        "EXACT",
        "AVAILABLE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "adjacent_method": (
        "ACTIVE",
        "EXACT",
        "ADJACENT",
        "AVAILABLE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "revoked_authority": (
        "REVOKED",
        "EXACT",
        "EXACT",
        "AVAILABLE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "control_plane_unavailable": (
        "ACTIVE",
        "EXACT",
        "EXACT",
        "UNAVAILABLE",
        "DENY",
        "NOT_OBSERVED",
    ),
}


@dataclass(frozen=True)
class EffectContractReadiness:
    ready: bool
    blockers: tuple[str, ...]


def validate_effect_contract(contract: dict) -> None:
    if type(contract) is not dict or set(contract) != _REQUIRED_TOP:
        raise ValueError("invalid matched effect contract schema")
    if contract["schema_version"] != "sbcf-matched-http-effect-v0":
        raise ValueError("unsupported matched effect contract version")
    if contract["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid matched effect contract status")
    if contract["effect_kind"] != "HTTP_REQUEST":
        raise ValueError("unsupported matched effect kind")

    identity_fields = contract["effect_identity_fields"]
    if identity_fields != [
        "trial_id",
        "method",
        "scheme",
        "host",
        "port",
        "path",
        "body_sha256",
    ]:
        raise ValueError("matched effect identity fields changed")

    witness = contract["witness"]
    if type(witness) is not dict or set(witness) != _REQUIRED_WITNESS:
        raise ValueError("invalid outcome witness schema")
    for field in ("kind", "positive_rule", "negative_rule"):
        if type(witness[field]) is not str or not witness[field].strip():
            raise ValueError(f"invalid witness field: {field}")
    bound = witness["negative_observation_bound_ms"]
    if bound is not None and (type(bound) is not int or bound <= 0):
        raise ValueError("negative observation bound must be null or a positive integer")

    mappings = contract["system_mappings"]
    if type(mappings) is not dict or set(mappings) != _SYSTEMS:
        raise ValueError("system mapping schema mismatch")
    if any(value not in _MAPPING_STATES for value in mappings.values()):
        raise ValueError("invalid system mapping state")

    cases = contract["cases"]
    if type(cases) is not list or len(cases) != len(_EXPECTED_CASES):
        raise ValueError("matched effect contract requires exactly five cases")
    seen = set()
    for record in cases:
        if type(record) is not dict or set(record) != _REQUIRED_CASE:
            raise ValueError("invalid matched effect case schema")
        case_id = record["id"]
        if case_id in seen or case_id not in _EXPECTED_CASES:
            raise ValueError("invalid or duplicate matched effect case")
        seen.add(case_id)
        actual = (
            record["authority_state"],
            record["target_relation"],
            record["method_relation"],
            record["control_plane"],
            record["expected_decision"],
            record["expected_effect"],
        )
        if actual != _EXPECTED_CASES[case_id]:
            raise ValueError(f"matched effect case semantics changed: {case_id}")
    if seen != set(_EXPECTED_CASES):
        raise ValueError("matched effect case set mismatch")


def evaluate_effect_contract(contract: dict) -> EffectContractReadiness:
    validate_effect_contract(contract)
    blockers = []
    if contract["status"] != "FROZEN":
        blockers.append("contract_not_frozen")
    if contract["witness"]["negative_observation_bound_ms"] is None:
        blockers.append("negative_observation_bound_unfrozen")
    for system_id, state in contract["system_mappings"].items():
        if state != "FROZEN":
            blockers.append(f"system_mapping_unfrozen:{system_id}")
    return EffectContractReadiness(not blockers, tuple(sorted(blockers)))


def effect_contract_digest(contract: dict) -> str:
    validate_effect_contract(contract)
    return sha256_digest(contract)
