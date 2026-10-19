"""Candidate protocol for freezing matched-effect negative observation windows."""

from dataclasses import dataclass

_EFFECT_DIGEST = "sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff"
_CUSTODY_DIGEST = "sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5"
_SYSTEMS = ("sbcf", "acs", "openshell")
_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "effect_contract_digest",
        "receiver_custody_digest",
        "window",
        "calibration",
        "system_calibration",
        "separation",
    }
)
_REQUIRED_WINDOW = frozenset(
    {
        "clock_domain",
        "arm_before_attempt_required",
        "max_attempt_start_lag_ms",
        "negative_observation_bound_ms",
    }
)
_REQUIRED_CALIBRATION = frozenset(
    {
        "status",
        "source",
        "estimator",
        "samples_per_system",
        "margin_ms",
        "same_receiver_build_required",
        "same_runtime_mapping_required",
        "raw_calibration_receipts_retained",
    }
)
_REQUIRED_SYSTEM_CALIBRATION = frozenset(
    {
        "status",
        "sample_count",
        "max_observed_ms",
    }
)
_REQUIRED_SEPARATION = frozenset(
    {
        "trial_outcomes_prohibited_from_calibration",
        "cross_clock_comparison_prohibited",
        "analysis_authorization_separate",
    }
)


@dataclass(frozen=True)
class NegativeObservationReadiness:
    ready: bool
    blockers: tuple[str, ...]


def _optional_positive_int(value, field):
    if value is not None and (type(value) is not int or value <= 0):
        raise ValueError(f"{field} must be null or positive integer")


def validate_negative_observation_protocol(protocol: dict) -> None:
    if type(protocol) is not dict or set(protocol) != _REQUIRED_TOP:
        raise ValueError("invalid negative observation protocol schema")
    if protocol["schema_version"] != "sbcf-negative-observation-bound-v0":
        raise ValueError("unsupported negative observation protocol version")
    if protocol["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid negative observation protocol status")
    if protocol["effect_contract_digest"] != _EFFECT_DIGEST:
        raise ValueError("negative observation protocol not bound to exact v1 effect contract")
    if protocol["receiver_custody_digest"] != _CUSTODY_DIGEST:
        raise ValueError("negative observation protocol not bound to exact custody contract")

    window = protocol["window"]
    if type(window) is not dict or set(window) != _REQUIRED_WINDOW:
        raise ValueError("invalid negative observation window schema")
    if window["clock_domain"] != "RECEIVER_MONOTONIC":
        raise ValueError("negative observation must use receiver monotonic clock")
    if window["arm_before_attempt_required"] is not True:
        raise ValueError("receiver must be armed before system attempt")
    _optional_positive_int(window["max_attempt_start_lag_ms"], "max attempt start lag")
    _optional_positive_int(window["negative_observation_bound_ms"], "negative observation bound")

    calibration = protocol["calibration"]
    if type(calibration) is not dict or set(calibration) != _REQUIRED_CALIBRATION:
        raise ValueError("invalid negative observation calibration schema")
    if calibration["status"] not in {"UNRUN", "FROZEN"}:
        raise ValueError("invalid calibration status")
    if calibration["source"] != "POSITIVE_CONTROLS_ONLY":
        raise ValueError("calibration must use positive controls only")
    if calibration["estimator"] != "MAX_OBSERVED_PLUS_MARGIN":
        raise ValueError("unsupported calibration estimator")
    _optional_positive_int(calibration["samples_per_system"], "samples per system")
    _optional_positive_int(calibration["margin_ms"], "calibration margin")
    for field in (
        "same_receiver_build_required",
        "same_runtime_mapping_required",
        "raw_calibration_receipts_retained",
    ):
        if calibration[field] is not True:
            raise ValueError(f"calibration safeguard weakened: {field}")

    systems = protocol["system_calibration"]
    if type(systems) is not dict or tuple(systems) != _SYSTEMS:
        raise ValueError("system calibration schema mismatch")
    for system_id, record in systems.items():
        if type(record) is not dict or set(record) != _REQUIRED_SYSTEM_CALIBRATION:
            raise ValueError(f"invalid system calibration record: {system_id}")
        if record["status"] not in {"UNRUN", "FROZEN"}:
            raise ValueError(f"invalid system calibration status: {system_id}")
        _optional_positive_int(record["sample_count"], f"{system_id} sample count")
        _optional_positive_int(record["max_observed_ms"], f"{system_id} max observed")
        if record["status"] == "UNRUN" and (
            record["sample_count"] is not None or record["max_observed_ms"] is not None
        ):
            raise ValueError(f"unrun calibration cannot contain results: {system_id}")

    separation = protocol["separation"]
    if type(separation) is not dict or set(separation) != _REQUIRED_SEPARATION:
        raise ValueError("invalid negative observation separation schema")
    if any(value is not True for value in separation.values()):
        raise ValueError("negative observation separation cannot be weakened")

    if calibration["status"] == "FROZEN":
        samples = calibration["samples_per_system"]
        margin = calibration["margin_ms"]
        start_lag = window["max_attempt_start_lag_ms"]
        bound = window["negative_observation_bound_ms"]
        if any(value is None for value in (samples, margin, start_lag, bound)):
            raise ValueError("frozen calibration requires complete timing parameters")
        maxima = []
        for system_id, record in systems.items():
            if record["status"] != "FROZEN":
                raise ValueError(f"frozen calibration requires system evidence: {system_id}")
            if record["sample_count"] != samples:
                raise ValueError(f"calibration sample count mismatch: {system_id}")
            maxima.append(record["max_observed_ms"])
        required_bound = start_lag + max(maxima) + margin
        if bound < required_bound:
            raise ValueError("negative observation bound is shorter than calibrated requirement")


def evaluate_negative_observation_protocol(protocol: dict) -> NegativeObservationReadiness:
    validate_negative_observation_protocol(protocol)
    blockers = []
    if protocol["status"] != "FROZEN":
        blockers.append("observation_protocol_not_frozen")
    window = protocol["window"]
    if window["max_attempt_start_lag_ms"] is None:
        blockers.append("max_attempt_start_lag_unfrozen")
    if window["negative_observation_bound_ms"] is None:
        blockers.append("negative_observation_bound_unfrozen")
    calibration = protocol["calibration"]
    if calibration["status"] != "FROZEN":
        blockers.append("calibration_not_frozen")
    if calibration["samples_per_system"] is None:
        blockers.append("samples_per_system_unfrozen")
    if calibration["margin_ms"] is None:
        blockers.append("calibration_margin_unfrozen")
    for system_id, record in protocol["system_calibration"].items():
        if record["status"] != "FROZEN":
            blockers.append(f"system_calibration_unfrozen:{system_id}")
    return NegativeObservationReadiness(not blockers, tuple(sorted(blockers)))
