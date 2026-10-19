"""Closed-schema contract for the matched-effect calibration receiver candidate."""

from dataclasses import dataclass

from scripts.dgaf_capability_canonicalize import sha256_digest

_EFFECT_DIGEST = "sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff"
_CUSTODY_DIGEST = "sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5"
_OBSERVATION_PROTOCOL_DIGEST = "sha256:d01d33de9f14d9bdace222528325d5766f5422088c8a4fa4c109adc1465e55cf"
_SYSTEMS = ("sbcf", "acs", "openshell")

_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "effect_contract_digest",
        "receiver_custody_digest",
        "negative_observation_protocol_digest",
        "receiver_build",
        "system_runtime_mappings",
        "receipt_contract",
        "separation",
    }
)
_REQUIRED_BUILD = frozenset({"status", "build_id", "source_sha256"})
_REQUIRED_MAPPING = frozenset({"status", "runtime_mapping_digest"})
_REQUIRED_RECEIPT = frozenset(
    {
        "calibration_source",
        "clock_domain",
        "custody_envelope_required",
        "analysis_fields_prohibited",
        "trial_outcomes_prohibited",
    }
)
_REQUIRED_SEPARATION = frozenset(
    {
        "receiver_operator_requirement_inherited",
        "durable_retention_requirement_inherited",
        "analysis_authorization_separate",
        "independent_validation_not_implied",
    }
)


@dataclass(frozen=True)
class CalibrationReceiverReadiness:
    ready: bool
    blockers: tuple[str, ...]


def _optional_text(value: object, field: str) -> None:
    if value is not None and (type(value) is not str or not value.strip()):
        raise ValueError(f"invalid {field}")


def _optional_sha256(value: object, field: str) -> None:
    if value is None:
        return
    if type(value) is not str or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"invalid {field}")


def validate_calibration_receiver_contract(contract: dict) -> None:
    if type(contract) is not dict or set(contract) != _REQUIRED_TOP:
        raise ValueError("invalid calibration receiver contract schema")
    if contract["schema_version"] != "sbcf-calibration-receiver-v0":
        raise ValueError("unsupported calibration receiver contract version")
    if contract["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid calibration receiver contract status")
    if contract["effect_contract_digest"] != _EFFECT_DIGEST:
        raise ValueError("receiver contract not bound to exact v1 effect contract")
    if contract["receiver_custody_digest"] != _CUSTODY_DIGEST:
        raise ValueError("receiver contract not bound to exact custody contract")
    if contract["negative_observation_protocol_digest"] != _OBSERVATION_PROTOCOL_DIGEST:
        raise ValueError("receiver contract not bound to exact observation protocol")

    build = contract["receiver_build"]
    if type(build) is not dict or set(build) != _REQUIRED_BUILD:
        raise ValueError("invalid receiver build schema")
    if build["status"] not in {"UNFROZEN", "FROZEN"}:
        raise ValueError("invalid receiver build status")
    _optional_text(build["build_id"], "receiver build id")
    _optional_sha256(build["source_sha256"], "receiver source sha256")
    if build["status"] == "UNFROZEN" and (build["build_id"] is not None or build["source_sha256"] is not None):
        raise ValueError("unfrozen receiver build cannot contain identity")
    if build["status"] == "FROZEN" and (build["build_id"] is None or build["source_sha256"] is None):
        raise ValueError("frozen receiver build requires exact identity")

    mappings = contract["system_runtime_mappings"]
    if type(mappings) is not dict or tuple(mappings) != _SYSTEMS:
        raise ValueError("system runtime mapping schema mismatch")
    for system_id, mapping in mappings.items():
        if type(mapping) is not dict or set(mapping) != _REQUIRED_MAPPING:
            raise ValueError(f"invalid runtime mapping record: {system_id}")
        if mapping["status"] not in {"UNFROZEN", "FROZEN"}:
            raise ValueError(f"invalid runtime mapping status: {system_id}")
        _optional_text(mapping["runtime_mapping_digest"], f"{system_id} runtime mapping digest")
        if mapping["status"] == "UNFROZEN" and mapping["runtime_mapping_digest"] is not None:
            raise ValueError(f"unfrozen runtime mapping cannot contain digest: {system_id}")
        if mapping["status"] == "FROZEN" and mapping["runtime_mapping_digest"] is None:
            raise ValueError(f"frozen runtime mapping requires digest: {system_id}")

    receipt = contract["receipt_contract"]
    if type(receipt) is not dict or set(receipt) != _REQUIRED_RECEIPT:
        raise ValueError("invalid calibration receipt contract")
    if receipt["calibration_source"] != "POSITIVE_CONTROLS_ONLY":
        raise ValueError("calibration source must remain positive controls only")
    if receipt["clock_domain"] != "RECEIVER_MONOTONIC":
        raise ValueError("calibration receiver must use receiver monotonic clock")
    for field in ("custody_envelope_required", "analysis_fields_prohibited", "trial_outcomes_prohibited"):
        if receipt[field] is not True:
            raise ValueError(f"calibration receipt safeguard weakened: {field}")

    separation = contract["separation"]
    if type(separation) is not dict or set(separation) != _REQUIRED_SEPARATION:
        raise ValueError("invalid calibration receiver separation schema")
    if any(value is not True for value in separation.values()):
        raise ValueError("calibration receiver separation cannot be weakened")


def evaluate_calibration_receiver_contract(contract: dict) -> CalibrationReceiverReadiness:
    validate_calibration_receiver_contract(contract)
    blockers = []
    if contract["status"] != "FROZEN":
        blockers.append("calibration_receiver_contract_not_frozen")
    if contract["receiver_build"]["status"] != "FROZEN":
        blockers.append("receiver_build_unfrozen")
    for system_id, mapping in contract["system_runtime_mappings"].items():
        if mapping["status"] != "FROZEN":
            blockers.append(f"runtime_mapping_unfrozen:{system_id}")
    return CalibrationReceiverReadiness(not blockers, tuple(sorted(blockers)))


def calibration_receiver_contract_digest(contract: dict) -> str:
    validate_calibration_receiver_contract(contract)
    return sha256_digest(contract)
