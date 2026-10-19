"""Closed candidate mapping for pinned OpenShell matched HTTP semantics."""

from dataclasses import dataclass

_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "upstream",
        "effect_contract_digest",
        "baseline_receiver",
        "cases",
    }
)
_REQUIRED_UPSTREAM = frozenset({"repository", "commit", "tag", "runner"})
_REQUIRED_RECEIVER = frozenset({"identity", "matches_common_receiver", "blocker"})
_REQUIRED_CASE = frozenset({"id", "mapping_state", "system_decision", "blocker"})

_PINNED_UPSTREAM = {
    "repository": "NVIDIA/OpenShell",
    "commit": "5a7728c304b5528e954e9ae900cf21f84e1a12b1",
    "tag": "v0.1.4",
    "runner": "ubuntu-24.04",
}
_EFFECT_DIGEST = "sha256:f4b153a6a922e49516e0d01c59817feab1d69e7a05e571b69c395e07a54b0b7b"
_EXPECTED_CASES = {
    "exact_allow": (
        "SEMANTIC_CANDIDATE_UNMATCHED_RECEIVER",
        "ALLOW",
        "external_receiver_identity_not_matched",
    ),
    "adjacent_host": (
        "SEMANTIC_CANDIDATE_UNMATCHED_RECEIVER",
        "DENY",
        "external_receiver_identity_not_matched",
    ),
    "adjacent_method": (
        "SEMANTIC_CANDIDATE_UNMATCHED_RECEIVER",
        "DENY",
        "external_receiver_identity_not_matched",
    ),
    "revoked_authority": (
        "EXECUTABLE_CANDIDATE_UNMATCHED_RECEIVER",
        "DENY",
        "external_receiver_identity_not_matched",
    ),
    "control_plane_unavailable": (
        "OBSERVED_SEMANTIC_MISMATCH",
        "ALLOW",
        "candidate_expected_deny_observed_allow",
    ),
}


@dataclass(frozen=True)
class OpenShellMappingReadiness:
    complete: bool
    blockers: tuple[str, ...]


def validate_openshell_mapping(mapping: dict) -> None:
    if type(mapping) is not dict or set(mapping) != _REQUIRED_TOP:
        raise ValueError("invalid OpenShell matched mapping schema")
    if mapping["schema_version"] != "sbcf-openshell-matched-http-mapping-v0":
        raise ValueError("unsupported OpenShell matched mapping version")
    if mapping["status"] not in {"CANDIDATE_PARTIAL_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid OpenShell matched mapping status")
    if mapping["upstream"] != _PINNED_UPSTREAM:
        raise ValueError("OpenShell upstream identity changed")
    if mapping["effect_contract_digest"] != _EFFECT_DIGEST:
        raise ValueError("OpenShell mapping effect contract digest changed")

    receiver = mapping["baseline_receiver"]
    if type(receiver) is not dict or set(receiver) != _REQUIRED_RECEIVER:
        raise ValueError("invalid OpenShell baseline receiver schema")
    if receiver != {
        "identity": "https://api.github.com",
        "matches_common_receiver": False,
        "blocker": "external_receiver_identity_not_matched",
    }:
        raise ValueError("OpenShell baseline receiver semantics changed")

    cases = mapping["cases"]
    if type(cases) is not list or len(cases) != len(_EXPECTED_CASES):
        raise ValueError("OpenShell matched mapping requires exactly five cases")
    seen = set()
    for record in cases:
        if type(record) is not dict or set(record) != _REQUIRED_CASE:
            raise ValueError("invalid OpenShell matched case schema")
        case_id = record["id"]
        if case_id in seen or case_id not in _EXPECTED_CASES:
            raise ValueError("invalid or duplicate OpenShell matched case")
        seen.add(case_id)
        actual = (
            record["mapping_state"],
            record["system_decision"],
            record["blocker"],
        )
        if actual != _EXPECTED_CASES[case_id]:
            raise ValueError(f"OpenShell matched case semantics changed: {case_id}")


def evaluate_openshell_mapping(mapping: dict) -> OpenShellMappingReadiness:
    validate_openshell_mapping(mapping)
    blockers = []
    if mapping["status"] != "FROZEN":
        blockers.append("openshell_mapping_not_frozen")
    if not mapping["baseline_receiver"]["matches_common_receiver"]:
        blockers.append("openshell_receiver_unmatched")
    for record in mapping["cases"]:
        if record["mapping_state"] != "FROZEN":
            blockers.append(f"openshell_case_unfrozen:{record['id']}")
        if record["blocker"] is not None:
            blockers.append(f"openshell_case_blocked:{record['id']}:{record['blocker']}")
    return OpenShellMappingReadiness(not blockers, tuple(sorted(blockers)))
