"""Tests for the receiver-monotonic positive-control calibration instrument."""

from __future__ import annotations

from dataclasses import replace

import pytest

from experiments.sbcf.calibration_receiver import (
    PositiveControlCalibrationReceiver,
    custody_record,
    summarize_positive_controls,
)

EFFECT = "a" * 64


class Clock:
    def __init__(self, *values):
        self.values = iter(values)

    def __call__(self):
        return next(self.values)


def make_receiver(*times):
    return PositiveControlCalibrationReceiver(Clock(*times))


def arm(receiver, *, trial_id="cal-1", source="POSITIVE_CONTROL", system_id="sbcf"):
    receiver.arm(
        trial_id=trial_id,
        source=source,
        system_id=system_id,
        receiver_build_id="receiver:build-1",
        runtime_mapping_digest="sha256:mapping-1",
        effect_identity_sha256=EFFECT,
    )


def complete_receipt(
    *,
    trial_id="cal-1",
    system_id="sbcf",
    times=(1_000_000_000, 1_010_000_000, 1_025_000_000),
):
    receiver = make_receiver(*times)
    arm(receiver, trial_id=trial_id, system_id=system_id)
    receiver.mark_attempt_started(trial_id)
    return receiver.record_receipt(trial_id=trial_id, effect_identity_sha256=EFFECT)


def test_positive_control_receipt_uses_one_monotonic_clock_domain():
    receipt = complete_receipt()

    assert receipt.source == "POSITIVE_CONTROL"
    assert receipt.clock_domain == "RECEIVER_MONOTONIC"
    assert receipt.arm_to_attempt_ms == 10
    assert receipt.attempt_to_received_ms == 15
    assert len(receipt.sha256()) == 64


def test_matched_trial_outcome_cannot_be_armed_as_calibration():
    receiver = make_receiver(1)
    with pytest.raises(ValueError, match="POSITIVE_CONTROL"):
        arm(receiver, source="MATCHED_TRIAL_OUTCOME")


def test_receiver_must_be_armed_before_attempt():
    receiver = make_receiver(1)
    with pytest.raises(ValueError, match="armed before attempt"):
        receiver.mark_attempt_started("missing")


def test_attempt_must_be_recorded_before_receipt():
    receiver = make_receiver(1, 2)
    arm(receiver)
    with pytest.raises(ValueError, match="attempt start not recorded"):
        receiver.record_receipt(trial_id="cal-1", effect_identity_sha256=EFFECT)


def test_effect_identity_mismatch_is_rejected():
    receiver = make_receiver(1, 2, 3)
    arm(receiver)
    receiver.mark_attempt_started("cal-1")
    with pytest.raises(ValueError, match="effect identity mismatch"):
        receiver.record_receipt(trial_id="cal-1", effect_identity_sha256="b" * 64)


def test_duplicate_arm_and_duplicate_attempt_are_rejected():
    receiver = make_receiver(1, 2, 3, 4)
    arm(receiver)
    with pytest.raises(ValueError, match="already armed"):
        arm(receiver)

    receiver.mark_attempt_started("cal-1")
    with pytest.raises(ValueError, match="attempt already started"):
        receiver.mark_attempt_started("cal-1")


@pytest.mark.parametrize("bad_effect", ["", "A" * 64, "g" * 64, "0" * 63, True])
def test_effect_identity_requires_lowercase_sha256_hex(bad_effect):
    receiver = make_receiver(1)
    with pytest.raises(ValueError, match="effect identity"):
        receiver.arm(
            trial_id="cal-1",
            source="POSITIVE_CONTROL",
            system_id="sbcf",
            receiver_build_id="receiver:build-1",
            runtime_mapping_digest="sha256:mapping-1",
            effect_identity_sha256=bad_effect,
        )


def test_monotonic_clock_rollback_is_rejected_at_attempt():
    receiver = make_receiver(10, 9)
    arm(receiver)
    with pytest.raises(ValueError, match="clock moved backward"):
        receiver.mark_attempt_started("cal-1")


def test_monotonic_clock_rollback_is_rejected_at_receipt():
    receiver = make_receiver(10, 20, 19)
    arm(receiver)
    receiver.mark_attempt_started("cal-1")
    with pytest.raises(ValueError, match="clock moved backward"):
        receiver.record_receipt(trial_id="cal-1", effect_identity_sha256=EFFECT)


def test_custody_record_matches_existing_receiver_contract_shape():
    receipt = complete_receipt()
    raw_bytes, record = custody_record(receipt)

    assert set(record) == {
        "trial_id",
        "effect_identity_sha256",
        "observed_effect",
        "raw_record_sha256",
        "byte_count",
    }
    assert record["trial_id"] == "cal-1"
    assert record["effect_identity_sha256"] == EFFECT
    assert record["observed_effect"] == "COMMITTED"
    assert record["raw_record_sha256"] == receipt.sha256()
    assert record["byte_count"] == len(raw_bytes)
    assert b"analysis" not in raw_bytes.lower()


def test_summary_requires_exact_sample_count_and_identity_binding():
    receipts = [
        complete_receipt(trial_id="cal-1", times=(0, 5_000_000, 15_000_000)),
        complete_receipt(trial_id="cal-2", times=(0, 8_000_000, 20_000_000)),
    ]

    summary = summarize_positive_controls(
        receipts,
        expected_system_id="sbcf",
        expected_receiver_build_id="receiver:build-1",
        expected_runtime_mapping_digest="sha256:mapping-1",
        expected_sample_count=2,
    )

    assert summary["status"] == "CALIBRATION_OBSERVED"
    assert summary["sample_count"] == 2
    assert summary["max_attempt_start_lag_ms"] == 8
    assert summary["max_observed_ms"] == 12
    assert len(summary["receipt_sha256"]) == 2


def test_summary_rejects_wrong_count_duplicate_trials_and_mixed_identity():
    receipts = [
        complete_receipt(trial_id="cal-1"),
        complete_receipt(trial_id="cal-2"),
    ]

    with pytest.raises(ValueError, match="sample count mismatch"):
        summarize_positive_controls(
            receipts,
            expected_system_id="sbcf",
            expected_receiver_build_id="receiver:build-1",
            expected_runtime_mapping_digest="sha256:mapping-1",
            expected_sample_count=3,
        )

    duplicate = [receipts[0], replace(receipts[1], trial_id="cal-1")]
    with pytest.raises(ValueError, match="duplicate calibration trial"):
        summarize_positive_controls(
            duplicate,
            expected_system_id="sbcf",
            expected_receiver_build_id="receiver:build-1",
            expected_runtime_mapping_digest="sha256:mapping-1",
            expected_sample_count=2,
        )

    mixed = [receipts[0], replace(receipts[1], receiver_build_id="receiver:other")]
    with pytest.raises(ValueError, match="receiver build mismatch"):
        summarize_positive_controls(
            mixed,
            expected_system_id="sbcf",
            expected_receiver_build_id="receiver:build-1",
            expected_runtime_mapping_digest="sha256:mapping-1",
            expected_sample_count=2,
        )


def test_summary_rejects_non_positive_control_receipt():
    receipt = complete_receipt()
    invalid = replace(receipt, source="MATCHED_TRIAL_OUTCOME")

    with pytest.raises(ValueError, match="non-positive-control"):
        summarize_positive_controls(
            [invalid],
            expected_system_id="sbcf",
            expected_receiver_build_id="receiver:build-1",
            expected_runtime_mapping_digest="sha256:mapping-1",
            expected_sample_count=1,
        )
