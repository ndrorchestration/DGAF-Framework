"""Deterministic staging/circuit-breaker evidence harness.

This test is deliberately a local control-plane model, not a claim that the
production DGAF runtime has been exercised. It produces a machine-readable
transition trace suitable for CI artifact capture.

Acceptance sequence:
STAGING -> ACTIVE -> BREAKER_OPEN -> FROZEN -> ROLLBACK -> VERIFIED

The fault is deterministic and injected by the test; no network, credentials,
or production services are contacted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


ARTIFACT = Path("test-artifacts/staging-circuit-breaker-evidence.json")


@dataclass(frozen=True)
class Transition:
    step: int
    state: str
    trigger: str
    fault_score: float


class StagingCircuitBreaker:
    """Minimal deterministic model for evidence of the required control flow."""

    BREAKER_THRESHOLD = 0.80

    def __init__(self) -> None:
        self.state = "STAGING"
        self.trace: list[Transition] = []
        self._record("STAGING", "initialized", 0.0)

    def _record(self, state: str, trigger: str, fault_score: float) -> None:
        self.state = state
        self.trace.append(
            Transition(len(self.trace), state, trigger, fault_score)
        )

    def activate(self) -> None:
        if self.state != "STAGING":
            raise RuntimeError(f"cannot activate from {self.state}")
        self._record("ACTIVE", "controlled_activation", 0.0)

    def observe(self, fault_score: float) -> None:
        if self.state != "ACTIVE":
            raise RuntimeError(f"cannot observe from {self.state}")
        if fault_score >= self.BREAKER_THRESHOLD:
            self._record("BREAKER_OPEN", "threshold_crossed", fault_score)
        else:
            self._record("ACTIVE", "within_threshold", fault_score)

    def freeze(self) -> None:
        if self.state != "BREAKER_OPEN":
            raise RuntimeError(f"cannot freeze from {self.state}")
        self._record("FROZEN", "execution_halted", self.trace[-1].fault_score)

    def rollback(self) -> None:
        if self.state != "FROZEN":
            raise RuntimeError(f"cannot rollback from {self.state}")
        self._record("ROLLBACK", "last_known_good_restored", 0.0)

    def verify(self) -> None:
        if self.state != "ROLLBACK":
            raise RuntimeError(f"cannot verify from {self.state}")
        self._record("VERIFIED", "recovery_confirmed", 0.0)


def test_staging_circuit_breaker_rollback_sequence() -> None:
    harness = StagingCircuitBreaker()
    harness.activate()
    harness.observe(0.95)  # deterministic injected fault
    harness.freeze()
    harness.rollback()
    harness.verify()

    states = [item.state for item in harness.trace]
    assert states == [
        "STAGING",
        "ACTIVE",
        "BREAKER_OPEN",
        "FROZEN",
        "ROLLBACK",
        "VERIFIED",
    ]
    assert harness.trace[2].fault_score == 0.95
    assert harness.state == "VERIFIED"

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(
            {
                "schema": "staging-circuit-breaker-evidence/v1",
                "model_scope": "deterministic local control-flow harness",
                "production_execution": False,
                "acceptance_sequence": states,
                "breaker_threshold": harness.BREAKER_THRESHOLD,
                "injected_fault_score": 0.95,
                "trace": [asdict(item) for item in harness.trace],
                "result": "PASS",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def test_breaker_does_not_open_below_threshold() -> None:
    harness = StagingCircuitBreaker()
    harness.activate()
    harness.observe(0.79)
    assert harness.state == "ACTIVE"
    assert harness.trace[-1].trigger == "within_threshold"
