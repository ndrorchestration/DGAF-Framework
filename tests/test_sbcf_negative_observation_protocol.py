"""Closed-schema tests for candidate negative observation protocol."""

import json
from pathlib import Path

import pytest

from experiments.sbcf.negative_observation_protocol import (
    evaluate_negative_observation_protocol,
    validate_negative_observation_protocol,
)

FIXTURE = Path(__file__).parents[1] / "experiments" / "sbcf" / "fixtures" / "negative_observation_protocol_v0.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_current_protocol_is_not_ready():
    result = evaluate_negative_observation_protocol(load())
    assert not result.ready
    assert result.blockers == (
        "calibration_margin_unfrozen",
        "calibration_not_frozen",
        "max_attempt_start_lag_unfrozen",
        "negative_observation_bound_unfrozen",
        "observation_protocol_not_frozen",
        "samples_per_system_unfrozen",
        "system_calibration_unfrozen:acs",
        "system_calibration_unfrozen:openshell",
        "system_calibration_unfrozen:sbcf",
    )


def test_protocol_is_bound_to_exact_v1_and_custody_contracts():
    protocol = load()
    protocol["effect_contract_digest"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="exact v1 effect contract"):
        validate_negative_observation_protocol(protocol)

    protocol = load()
    protocol["receiver_custody_digest"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="exact custody contract"):
        validate_negative_observation_protocol(protocol)


@pytest.mark.parametrize("field", ["max_attempt_start_lag_ms", "negative_observation_bound_ms"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5, "1000"])
def test_window_parameters_must_be_positive_integer_or_null(field, value):
    protocol = load()
    protocol["window"][field] = value
    with pytest.raises(ValueError):
        validate_negative_observation_protocol(protocol)


def test_calibration_cannot_use_trial_outcomes():
    protocol = load()
    protocol["calibration"]["source"] = "MATCHED_TRIAL_OUTCOMES"
    with pytest.raises(ValueError, match="positive controls only"):
        validate_negative_observation_protocol(protocol)


def test_unrun_system_calibration_cannot_contain_results():
    protocol = load()
    protocol["system_calibration"]["sbcf"]["sample_count"] = 10
    with pytest.raises(ValueError, match="unrun calibration cannot contain results"):
        validate_negative_observation_protocol(protocol)


def test_cross_clock_comparison_cannot_be_enabled():
    protocol = load()
    protocol["separation"]["cross_clock_comparison_prohibited"] = False
    with pytest.raises(ValueError, match="cannot be weakened"):
        validate_negative_observation_protocol(protocol)


def frozen_protocol(bound_ms=225):
    protocol = load()
    protocol["status"] = "FROZEN"
    protocol["window"]["max_attempt_start_lag_ms"] = 50
    protocol["window"]["negative_observation_bound_ms"] = bound_ms
    protocol["calibration"].update(
        {
            "status": "FROZEN",
            "samples_per_system": 10,
            "margin_ms": 25,
        }
    )
    maxima = {"sbcf": 120, "acs": 150, "openshell": 100}
    for system_id, maximum in maxima.items():
        protocol["system_calibration"][system_id] = {
            "status": "FROZEN",
            "sample_count": 10,
            "max_observed_ms": maximum,
        }
    return protocol


def test_frozen_bound_cannot_be_shorter_than_calibrated_requirement():
    # Required = start lag 50 + max observed 150 + margin 25 = 225 ms.
    with pytest.raises(ValueError, match="shorter than calibrated requirement"):
        validate_negative_observation_protocol(frozen_protocol(bound_ms=224))


def test_frozen_calibration_requires_equal_preregistered_sample_counts():
    protocol = frozen_protocol()
    protocol["system_calibration"]["acs"]["sample_count"] = 9
    with pytest.raises(ValueError, match="sample count mismatch"):
        validate_negative_observation_protocol(protocol)


def test_structural_ready_requires_complete_calibration():
    result = evaluate_negative_observation_protocol(frozen_protocol())
    assert result.ready
    assert result.blockers == ()


def test_ready_protocol_still_uses_receiver_monotonic_clock():
    protocol = frozen_protocol()
    assert protocol["window"]["clock_domain"] == "RECEIVER_MONOTONIC"
    assert protocol["window"]["arm_before_attempt_required"] is True
    assert protocol["separation"]["trial_outcomes_prohibited_from_calibration"] is True
