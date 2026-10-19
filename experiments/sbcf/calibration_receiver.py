"""Receiver-monotonic positive-control calibration instrument.

This module measures receiver-arm -> attempt-start -> receipt timing in one
monotonic clock domain. It is a candidate calibration instrument only; it does
not freeze any sample count, margin, observation bound, or custody role.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from threading import Lock
from typing import Callable

_REQUIRED_SOURCE = "POSITIVE_CONTROL"
_REQUIRED_CLOCK = "RECEIVER_MONOTONIC"


def _positive_int(value: object, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{field} must be positive integer")
    return value


def _non_negative_int(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be non-negative integer")
    return value


@dataclass(frozen=True)
class CalibrationReceipt:
    schema_version: str
    source: str
    clock_domain: str
    trial_id: str
    system_id: str
    receiver_build_id: str
    runtime_mapping_digest: str
    armed_ns: int
    attempt_started_ns: int
    received_ns: int
    effect_identity_sha256: str

    @property
    def arm_to_attempt_ms(self) -> int:
        return (self.attempt_started_ns - self.armed_ns + 999_999) // 1_000_000

    @property
    def attempt_to_received_ms(self) -> int:
        return (self.received_ns - self.attempt_started_ns + 999_999) // 1_000_000

    def canonical_bytes(self) -> bytes:
        payload = asdict(self)
        payload["arm_to_attempt_ms"] = self.arm_to_attempt_ms
        payload["attempt_to_received_ms"] = self.attempt_to_received_ms
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


@dataclass
class _ArmedTrial:
    source: str
    system_id: str
    receiver_build_id: str
    runtime_mapping_digest: str
    effect_identity_sha256: str
    armed_ns: int
    attempt_started_ns: int | None = None


class PositiveControlCalibrationReceiver:
    """Single-process candidate receiver timing instrument."""

    def __init__(self, monotonic_ns: Callable[[], int]):
        self._monotonic_ns = monotonic_ns
        self._lock = Lock()
        self._trials: dict[str, _ArmedTrial] = {}

    def arm(
        self,
        *,
        trial_id: str,
        source: str,
        system_id: str,
        receiver_build_id: str,
        runtime_mapping_digest: str,
        effect_identity_sha256: str,
    ) -> None:
        if source != _REQUIRED_SOURCE:
            raise ValueError("calibration source must be POSITIVE_CONTROL")
        for field, value in (
            ("trial_id", trial_id),
            ("system_id", system_id),
            ("receiver_build_id", receiver_build_id),
            ("runtime_mapping_digest", runtime_mapping_digest),
        ):
            if type(value) is not str or not value:
                raise ValueError(f"{field} must be non-empty string")
        if (
            type(effect_identity_sha256) is not str
            or len(effect_identity_sha256) != 64
            or any(character not in "0123456789abcdef" for character in effect_identity_sha256)
        ):
            raise ValueError("effect identity must be lowercase sha256 hex")
        now = _non_negative_int(self._monotonic_ns(), "monotonic time")
        with self._lock:
            if trial_id in self._trials:
                raise ValueError("trial already armed")
            self._trials[trial_id] = _ArmedTrial(
                source=source,
                system_id=system_id,
                receiver_build_id=receiver_build_id,
                runtime_mapping_digest=runtime_mapping_digest,
                effect_identity_sha256=effect_identity_sha256,
                armed_ns=now,
            )

    def mark_attempt_started(self, trial_id: str) -> None:
        now = _non_negative_int(self._monotonic_ns(), "monotonic time")
        with self._lock:
            trial = self._trials.get(trial_id)
            if trial is None:
                raise ValueError("receiver must be armed before attempt")
            if trial.attempt_started_ns is not None:
                raise ValueError("attempt already started")
            if now < trial.armed_ns:
                raise ValueError("monotonic clock moved backward")
            trial.attempt_started_ns = now

    def record_receipt(
        self,
        *,
        trial_id: str,
        effect_identity_sha256: str,
    ) -> CalibrationReceipt:
        now = _non_negative_int(self._monotonic_ns(), "monotonic time")
        with self._lock:
            trial = self._trials.get(trial_id)
            if trial is None:
                raise ValueError("receiver not armed")
            if trial.attempt_started_ns is None:
                raise ValueError("attempt start not recorded")
            if effect_identity_sha256 != trial.effect_identity_sha256:
                raise ValueError("effect identity mismatch")
            if now < trial.attempt_started_ns:
                raise ValueError("monotonic clock moved backward")
            receipt = CalibrationReceipt(
                schema_version="sbcf-positive-control-calibration-receipt-v0",
                source=trial.source,
                clock_domain=_REQUIRED_CLOCK,
                trial_id=trial_id,
                system_id=trial.system_id,
                receiver_build_id=trial.receiver_build_id,
                runtime_mapping_digest=trial.runtime_mapping_digest,
                armed_ns=trial.armed_ns,
                attempt_started_ns=trial.attempt_started_ns,
                received_ns=now,
                effect_identity_sha256=trial.effect_identity_sha256,
            )
            del self._trials[trial_id]
            return receipt


def custody_record(receipt: CalibrationReceipt) -> tuple[bytes, dict]:
    """Return raw calibration bytes plus the existing receiver-custody envelope."""

    raw_bytes = receipt.canonical_bytes()
    return raw_bytes, {
        "trial_id": receipt.trial_id,
        "effect_identity_sha256": receipt.effect_identity_sha256,
        "observed_effect": "COMMITTED",
        "raw_record_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "byte_count": len(raw_bytes),
    }


def summarize_positive_controls(
    receipts: list[CalibrationReceipt],
    *,
    expected_system_id: str,
    expected_receiver_build_id: str,
    expected_runtime_mapping_digest: str,
    expected_sample_count: int,
) -> dict:
    _positive_int(expected_sample_count, "expected sample count")
    if len(receipts) != expected_sample_count:
        raise ValueError("calibration sample count mismatch")
    if not receipts:
        raise ValueError("calibration receipts required")

    seen_trials: set[str] = set()
    for receipt in receipts:
        if receipt.source != _REQUIRED_SOURCE:
            raise ValueError("non-positive-control receipt prohibited")
        if receipt.clock_domain != _REQUIRED_CLOCK:
            raise ValueError("receiver clock domain mismatch")
        if receipt.system_id != expected_system_id:
            raise ValueError("system identity mismatch")
        if receipt.receiver_build_id != expected_receiver_build_id:
            raise ValueError("receiver build mismatch")
        if receipt.runtime_mapping_digest != expected_runtime_mapping_digest:
            raise ValueError("runtime mapping mismatch")
        if receipt.trial_id in seen_trials:
            raise ValueError("duplicate calibration trial")
        seen_trials.add(receipt.trial_id)
        if receipt.attempt_started_ns < receipt.armed_ns:
            raise ValueError("attempt precedes receiver arm")
        if receipt.received_ns < receipt.attempt_started_ns:
            raise ValueError("receipt precedes attempt")

    return {
        "status": "CALIBRATION_OBSERVED",
        "sample_count": len(receipts),
        "max_attempt_start_lag_ms": max(receipt.arm_to_attempt_ms for receipt in receipts),
        "max_observed_ms": max(receipt.attempt_to_received_ms for receipt in receipts),
        "receipt_sha256": [receipt.sha256() for receipt in receipts],
    }
