"""Prospective v1 matched HTTP-effect contract.

v0 remains immutable historical characterization. v1 separates normative effect
cases from control-plane failure posture so a system-specific failure strategy is
not retroactively scored against a universal target chosen after observation.
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
        "failure_posture",
        "cases",
    }
)
_REQUIRED_WITNESS = frozenset(
    {
        "kind",
        "positive_rule",
        "negative_rule",
        "negative_observation_bound_ms",
        "trial_id_binding",
        "receiver_custody",
    }
)
_REQUIRED_TRIAL_BINDING = frozenset({"kind", "header_name"})
_REQUIRED_CUSTODY = frozenset(
    {
        "status",
        "independent_operator_required",
        "raw_receipt_retention_required",
    }
)
_REQUIRED_FAILURE_POSTURE = frozenset(
    {
        "status",
        "case_id",
        "comparison_mode",
        "normative_target",
        "allowed_postures",
        "system_postures",
        "efficacy_scoring",
    }
)
_REQUIRED_CASE = frozenset(
    {
        "id",
        "authority_state",
        "target_relation",
        "method_relation",
        "control_plane",
        "scoring_mode",
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
_ALLOWED_POSTURES = (
    "FAIL_CLOSED_DENY",
    "LAST_KNOWN_GOOD",
    "FAIL_OPEN_ALLOW",
)
_EXPECTED_CASES = {
    "exact_allow": (
        "ACTIVE",
        "EXACT",
        "EXACT",
        "AVAILABLE",
        "NORMATIVE",
        "ALLOW",
        "COMMITTED",
    ),
    "adjacent_host": (
        "ACTIVE",
        "ADJACENT",
        "EXACT",
        "AVAILABLE",
        "NORMATIVE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "adjacent_method": (
        "ACTIVE",
        "EXACT",
        "ADJACENT",
        "AVAILABLE",
        "NORMATIVE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "revoked_authority": (
        "REVOKED",
        "EXACT",
        "EXACT",
        "AVAILABLE",
        "NORMATIVE",
        "DENY",
        "NOT_OBSERVED",
    ),
    "control_plane_unavailable": (
        "ACTIVE",
        "EXACT",
        "EXACT",
        "UNAVAILABLE",
        "STRATIFIED_FAILURE_POSTURE",
        None,
        None,
    ),
}


@dataclass(frozen=True)
class EffectContractV1Readiness:
    ready: bool
    blockers: tuple[str, ...]


def validate_effect_contract_v1(contract: dict) -> None:
    if type(contract) is not dict or set(contract) != _REQUIRED_TOP:
        raise ValueError("invalid matched effect v1 schema")
    if contract["schema_version"] != "sbcf-matched-http-effect-v1":
        raise ValueError("unsupported matched effect v1 version")
    if contract["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid matched effect v1 status")
    if contract["effect_kind"] != "HTTP_REQUEST":
        raise ValueError("unsupported matched effect kind")

    if contract["effect_identity_fields"] != [
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
        raise ValueError("invalid v1 outcome witness schema")
    for field in ("kind", "positive_rule", "negative_rule"):
        if type(witness[field]) is not str or not witness[field].strip():
            raise ValueError(f"invalid witness field: {field}")
    bound = witness["negative_observation_bound_ms"]
    if bound is not None and (type(bound) is not int or bound <= 0):
        raise ValueError("negative observation bound must be null or positive integer")

    trial_binding = witness["trial_id_binding"]
    if type(trial_binding) is not dict or set(trial_binding) != _REQUIRED_TRIAL_BINDING:
        raise ValueError("invalid trial id binding schema")
    if trial_binding != {
        "kind": "FIXED_HEADER",
        "header_name": "X-SBCF-Trial-ID",
    }:
        raise ValueError("matched effect trial id binding changed")

    custody = witness["receiver_custody"]
    if type(custody) is not dict or set(custody) != _REQUIRED_CUSTODY:
        raise ValueError("invalid receiver custody schema")
    if custody["status"] not in {"UNRESOLVED", "FROZEN"}:
        raise ValueError("invalid receiver custody status")
    if custody["independent_operator_required"] is not True:
        raise ValueError("receiver custody must require an independent operator")
    if custody["raw_receipt_retention_required"] is not True:
        raise ValueError("receiver custody must require raw receipt retention")

    mappings = contract["system_mappings"]
    if type(mappings) is not dict or set(mappings) != _SYSTEMS:
        raise ValueError("system mapping schema mismatch")
    if any(value not in _MAPPING_STATES for value in mappings.values()):
        raise ValueError("invalid system mapping state")

    posture = contract["failure_posture"]
    if type(posture) is not dict or set(posture) != _REQUIRED_FAILURE_POSTURE:
        raise ValueError("invalid failure posture schema")
    if posture["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid failure posture status")
    if posture["case_id"] != "control_plane_unavailable":
        raise ValueError("failure posture case changed")
    if posture["comparison_mode"] != "STRATIFY_ONLY":
        raise ValueError("failure posture comparison mode changed")
    if posture["normative_target"] is not None:
        raise ValueError("v1 stratified failure posture must not define a normative target")
    if posture["allowed_postures"] != list(_ALLOWED_POSTURES):
        raise ValueError("failure posture vocabulary changed")
    if posture["efficacy_scoring"] != "EXCLUDED_UNLESS_NORMATIVE_TARGET_PREREGISTERED":
        raise ValueError("failure posture scoring rule changed")
    system_postures = posture["system_postures"]
    if type(system_postures) is not dict or set(system_postures) != _SYSTEMS:
        raise ValueError("failure posture system schema mismatch")
    allowed_values = {"UNRESOLVED", *_ALLOWED_POSTURES}
    if any(value not in allowed_values for value in system_postures.values()):
        raise ValueError("invalid system failure posture")

    cases = contract["cases"]
    if type(cases) is not list or len(cases) != len(_EXPECTED_CASES):
        raise ValueError("matched effect v1 requires exactly five cases")
    seen = set()
    for record in cases:
        if type(record) is not dict or set(record) != _REQUIRED_CASE:
            raise ValueError("invalid matched effect v1 case schema")
        case_id = record["id"]
        if case_id in seen or case_id not in _EXPECTED_CASES:
            raise ValueError("invalid or duplicate matched effect v1 case")
        seen.add(case_id)
        actual = (
            record["authority_state"],
            record["target_relation"],
            record["method_relation"],
            record["control_plane"],
            record["scoring_mode"],
            record["expected_decision"],
            record["expected_effect"],
        )
        if actual != _EXPECTED_CASES[case_id]:
            raise ValueError(f"matched effect v1 case semantics changed: {case_id}")


def evaluate_effect_contract_v1(contract: dict) -> EffectContractV1Readiness:
    validate_effect_contract_v1(contract)
    blockers = []
    if contract["status"] != "FROZEN":
        blockers.append("contract_not_frozen")
    if contract["witness"]["negative_observation_bound_ms"] is None:
        blockers.append("negative_observation_bound_unfrozen")
    if contract["witness"]["receiver_custody"]["status"] != "FROZEN":
        blockers.append("receiver_custody_unfrozen")
    for system_id, state in contract["system_mappings"].items():
        if state != "FROZEN":
            blockers.append(f"system_mapping_unfrozen:{system_id}")
    posture = contract["failure_posture"]
    if posture["status"] != "FROZEN":
        blockers.append("failure_posture_not_frozen")
    for system_id, state in posture["system_postures"].items():
        if state == "UNRESOLVED":
            blockers.append(f"failure_posture_unresolved:{system_id}")
    return EffectContractV1Readiness(not blockers, tuple(sorted(blockers)))


def effect_contract_v1_digest(contract: dict) -> str:
    validate_effect_contract_v1(contract)
    return sha256_digest(contract)
