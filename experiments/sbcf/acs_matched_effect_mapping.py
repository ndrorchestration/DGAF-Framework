"""Closed candidate mapping for pinned OWASP ACS matched HTTP semantics.

This module does not declare the parent effect contract frozen. It records the
two cases the pinned ACS stock egress policy can execute and the three cases
that remain unresolved without inventing controls ACS has not demonstrated.
"""

from dataclasses import dataclass

_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "upstream",
        "effect_contract_digest",
        "policy_overlay",
        "cases",
    }
)
_REQUIRED_UPSTREAM = frozenset({"repository", "commit", "runtime"})
_REQUIRED_OVERLAY = frozenset({"kind", "base_file", "egress_allowlist", "frozen"})
_REQUIRED_CASE = frozenset({"id", "mapping_state", "system_decision", "blocker"})

_PINNED_REPOSITORY = "GenAI-Security-Project/agent-control-standard"
_PINNED_COMMIT = "9c05f0402d76dea6b67a12a93672c2131137e572"
_PINNED_RUNTIME = "Bun 1.3.11"
_EXPECTED_EFFECT_CONTRACT_DIGEST = "sha256:f4b153a6a922e49516e0d01c59817feab1d69e7a05e571b69c395e07a54b0b7b"

_EXPECTED_CASES = {
    "exact_allow": (
        "EXECUTABLE_CANDIDATE",
        "ALLOW",
        None,
    ),
    "adjacent_host": (
        "EXECUTABLE_CANDIDATE",
        "DENY",
        None,
    ),
    "adjacent_method": (
        "UNRESOLVED",
        None,
        "acs_stock_egress_does_not_bind_http_method",
    ),
    "revoked_authority": (
        "UNRESOLVED",
        None,
        "acs_reference_mapping_has_no_frozen_authority_revocation_semantics",
    ),
    "control_plane_unavailable": (
        "UNRESOLVED",
        None,
        "acs_failure_posture_not_frozen_to_deny_for_matched_fixture",
    ),
}


@dataclass(frozen=True)
class AcsMappingReadiness:
    complete: bool
    blockers: tuple[str, ...]


def validate_acs_mapping(mapping: dict) -> None:
    if type(mapping) is not dict or set(mapping) != _REQUIRED_TOP:
        raise ValueError("invalid ACS matched mapping schema")
    if mapping["schema_version"] != "sbcf-acs-matched-http-mapping-v0":
        raise ValueError("unsupported ACS matched mapping version")
    if mapping["status"] not in {"CANDIDATE_PARTIAL_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid ACS matched mapping status")

    upstream = mapping["upstream"]
    if type(upstream) is not dict or set(upstream) != _REQUIRED_UPSTREAM:
        raise ValueError("invalid ACS upstream identity schema")
    if upstream != {
        "repository": _PINNED_REPOSITORY,
        "commit": _PINNED_COMMIT,
        "runtime": _PINNED_RUNTIME,
    }:
        raise ValueError("ACS upstream identity changed")

    if mapping["effect_contract_digest"] != _EXPECTED_EFFECT_CONTRACT_DIGEST:
        raise ValueError("ACS mapping effect contract digest changed")

    overlay = mapping["policy_overlay"]
    if type(overlay) is not dict or set(overlay) != _REQUIRED_OVERLAY:
        raise ValueError("invalid ACS policy overlay schema")
    if overlay["kind"] != "CANDIDATE_BENCHMARK_FIXTURE_OVERLAY":
        raise ValueError("invalid ACS policy overlay kind")
    if overlay["base_file"] != "reference-implementations/agt/policy/lib/data.json":
        raise ValueError("ACS policy overlay base changed")
    if overlay["egress_allowlist"] != ["127.0.0.1"]:
        raise ValueError("ACS candidate egress allowlist changed")
    if type(overlay["frozen"]) is not bool:
        raise ValueError("ACS policy overlay frozen flag must be boolean")

    cases = mapping["cases"]
    if type(cases) is not list or len(cases) != len(_EXPECTED_CASES):
        raise ValueError("ACS matched mapping requires exactly five cases")

    seen = set()
    for record in cases:
        if type(record) is not dict or set(record) != _REQUIRED_CASE:
            raise ValueError("invalid ACS matched case schema")
        case_id = record["id"]
        if case_id in seen or case_id not in _EXPECTED_CASES:
            raise ValueError("invalid or duplicate ACS matched case")
        seen.add(case_id)
        actual = (
            record["mapping_state"],
            record["system_decision"],
            record["blocker"],
        )
        if actual != _EXPECTED_CASES[case_id]:
            raise ValueError(f"ACS matched case semantics changed: {case_id}")

    if seen != set(_EXPECTED_CASES):
        raise ValueError("ACS matched case set mismatch")


def evaluate_acs_mapping(mapping: dict) -> AcsMappingReadiness:
    validate_acs_mapping(mapping)
    blockers = []
    if mapping["status"] != "FROZEN":
        blockers.append("acs_mapping_not_frozen")
    if not mapping["policy_overlay"]["frozen"]:
        blockers.append("acs_policy_overlay_not_frozen")
    for record in mapping["cases"]:
        if record["mapping_state"] != "FROZEN":
            blockers.append(f"acs_case_unfrozen:{record['id']}")
        if record["blocker"] is not None:
            blockers.append(f"acs_case_blocked:{record['id']}:{record['blocker']}")
    return AcsMappingReadiness(not blockers, tuple(sorted(blockers)))
