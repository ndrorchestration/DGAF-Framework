"""Fail-closed readiness gate for any future matched SBCF comparator study.

This module does not run a benchmark and does not convert unrelated runtime
evidence into matched policy-effect evidence. It only validates a frozen
readiness manifest.
"""

from dataclasses import dataclass

_REQUIRED_SYSTEMS = frozenset({"sbcf", "acs", "openshell"})
_REQUIRED_TOP_LEVEL = frozenset({"schema_version", "status", "systems", "gates"})
_REQUIRED_SYSTEM_FIELDS = frozenset(
    {
        "version",
        "source",
        "matched_effect_tier",
        "reproduced",
        "effect_boundary",
        "scope",
    }
)
_ALLOWED_EFFECT_TIERS = frozenset(
    {
        "synthetic_effect",
        "reference_runtime_effect",
        "enforced_runtime_effect",
        "independent_runtime_effect",
    }
)
_RUNTIME_EFFECT_TIERS = frozenset({"enforced_runtime_effect", "independent_runtime_effect"})
_REQUIRED_GATES = frozenset(
    {
        "exact_system_versions_pinned",
        "common_effect_semantics_frozen",
        "common_policy_intent_frozen",
        "common_failure_posture_frozen",
        "common_outcome_witness_defined",
        "evidence_tier_reporting_frozen",
        "matched_runtime_effect_evidence_for_all",
        "trial_fixture_packet_frozen",
        "statistics_preregistered",
        "outside_operator_assigned",
        "raw_evidence_retention_ready",
    }
)


@dataclass(frozen=True)
class ComparatorReadiness:
    ready: bool
    blockers: tuple[str, ...]


def _strict_bool(value: object) -> bool:
    return type(value) is bool


def validate_manifest(manifest: dict) -> None:
    if type(manifest) is not dict or set(manifest) != _REQUIRED_TOP_LEVEL:
        raise ValueError("invalid top-level comparator manifest schema")
    if manifest["schema_version"] != "sbcf-matched-comparator-v1":
        raise ValueError("unsupported comparator manifest version")
    if manifest["status"] != "PRE_FREEZE_FAIL_CLOSED":
        raise ValueError("comparator manifest must remain pre-freeze/fail-closed")

    systems = manifest["systems"]
    if type(systems) is not dict or set(systems) != _REQUIRED_SYSTEMS:
        raise ValueError("comparator manifest requires exactly SBCF, ACS and OpenShell")
    for system_id, record in systems.items():
        if type(record) is not dict or set(record) != _REQUIRED_SYSTEM_FIELDS:
            raise ValueError(f"invalid system record: {system_id}")
        for key in (
            "version",
            "source",
            "matched_effect_tier",
            "effect_boundary",
            "scope",
        ):
            if type(record[key]) is not str or not record[key].strip():
                raise ValueError(f"invalid {key}: {system_id}")
        if record["matched_effect_tier"] not in _ALLOWED_EFFECT_TIERS:
            raise ValueError(f"invalid matched effect tier: {system_id}")
        if not _strict_bool(record["reproduced"]):
            raise ValueError(f"reproduced must be strict boolean: {system_id}")

    gates = manifest["gates"]
    if type(gates) is not dict or set(gates) != _REQUIRED_GATES:
        raise ValueError("comparator manifest gate schema mismatch")
    for gate, value in gates.items():
        if not _strict_bool(value):
            raise ValueError(f"gate must be strict boolean: {gate}")


def evaluate_readiness(manifest: dict) -> ComparatorReadiness:
    validate_manifest(manifest)
    blockers = [gate for gate, value in manifest["gates"].items() if value is False]

    for system_id, record in manifest["systems"].items():
        if record["reproduced"] is False:
            blockers.append(f"system_not_reproduced:{system_id}")

    if manifest["gates"]["matched_runtime_effect_evidence_for_all"]:
        for system_id, record in manifest["systems"].items():
            if record["matched_effect_tier"] not in _RUNTIME_EFFECT_TIERS:
                blockers.append(f"matched_runtime_effect_missing:{system_id}")

    return ComparatorReadiness(not blockers, tuple(sorted(blockers)))
