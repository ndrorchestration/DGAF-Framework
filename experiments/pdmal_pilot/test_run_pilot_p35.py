"""Tests for the explicit pilot-time P-35 checker boundary.

These tests validate configuration and real pilot-run precondition wiring only. They
never enable empirical execution or bypass freeze/authorization controls.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from run_pilot import AttemptStatus, require_pilot_premise_checker, run_pilot


def test_missing_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PDMAL_PREMISE_CHECKER", raising=False)
    with pytest.raises(SystemExit, match="PDMAL_PREMISE_CHECKER"):
        require_pilot_premise_checker()


def test_malformed_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "not-module-attribute")
    with pytest.raises(SystemExit, match="module:attribute"):
        require_pilot_premise_checker()


def test_unknown_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "module_that_does_not_exist:checker")
    with pytest.raises(SystemExit, match="unable to load P-35 checker"):
        require_pilot_premise_checker()


def test_non_callable_premise_checker_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "os:path")
    with pytest.raises(SystemExit, match="not callable"):
        require_pilot_premise_checker()


def allow_premises(_text, _invariant) -> bool:
    return True


def reject_premises(_text, _invariant) -> bool:
    return False


def test_explicit_premise_checker_is_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "test_run_pilot_p35:allow_premises")
    checker = require_pilot_premise_checker()
    assert checker("input", object()) is True


def test_run_pilot_requires_checker_before_task_construction(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr("run_pilot.require_frozen_commit", lambda: "a" * 40)
    monkeypatch.setattr("run_pilot.require_pilot_authorization", lambda: ("test-key", tmp_path))
    monkeypatch.delenv("PDMAL_PREMISE_CHECKER", raising=False)

    class UnexpectedTaskConstruction:
        def __init__(self, **_kwargs):
            raise AssertionError("ConsensusTask must not be constructed when the P-35 checker is absent")

    monkeypatch.setattr("run_pilot.ConsensusTask", UnexpectedTaskConstruction)
    with pytest.raises(SystemExit, match="PDMAL_PREMISE_CHECKER"):
        run_pilot(tmp_path / "output", seeds=1)


def test_run_pilot_passes_explicit_checker_to_dgaf_task(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr("run_pilot.require_frozen_commit", lambda: "b" * 40)
    monkeypatch.setattr("run_pilot.require_pilot_authorization", lambda: ("test-key", tmp_path))
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "test_run_pilot_p35:allow_premises")
    monkeypatch.setattr("run_pilot._trial_combinations", lambda: [("ring", "dgaf", 0)])
    monkeypatch.setattr("run_pilot._environment_fingerprint", lambda: "environment-test")
    monkeypatch.setattr("run_pilot.make_streams", lambda _seed: {"topology_construction": SimpleNamespace()})
    monkeypatch.setattr("run_pilot._write_and_validate_artifact", lambda *args, **kwargs: None)
    monkeypatch.setattr("run_pilot._retain", lambda *args, **kwargs: None)
    monkeypatch.setattr("run_pilot.graph_fingerprint", lambda _graph: "fallback-topology")
    monkeypatch.setattr("run_pilot.generate_topology", lambda *_args: object())
    monkeypatch.setattr("run_pilot.SEED_RUNTIME_CEILING_SECONDS", 60.0)

    captured: list[object] = []

    class FakeTask:
        def __init__(self, *, premise_check_fn, **kwargs):
            captured.append((premise_check_fn, kwargs))

        @staticmethod
        def trial_key(seed, topology, condition, failure_count):
            return f"trial-{seed}-{topology}-{condition}-{failure_count}"

        def run_detailed(self, *, seed, attempt):
            return SimpleNamespace(
                attempt_status=AttemptStatus.SUCCESS,
                failure_nodes=[],
                initial_values=[0.0],
                final_values=[0.0],
                final_std=0.0,
                topology_fingerprint="topology-test",
                iterations_completed=1,
                consensus_success=True,
                deviation=0.0,
                governance_trace=[],
            )

    monkeypatch.setattr("run_pilot.ConsensusTask", FakeTask)

    assert run_pilot(tmp_path / "output", seeds=1) == 0
    assert len(captured) == 1
    checker, kwargs = captured[0]
    assert checker is allow_premises
    assert kwargs["condition"] == "dgaf"


def test_run_pilot_real_consensus_task_invokes_explicit_p35_checker(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """Exercise run_pilot -> real ConsensusTask -> DGAF adapter -> TGL/P-35."""
    monkeypatch.setattr("run_pilot.require_frozen_commit", lambda: "c" * 40)
    monkeypatch.setattr(
        "run_pilot.require_pilot_authorization",
        lambda: ("test-key", tmp_path),
    )
    monkeypatch.setenv("PDMAL_PREMISE_CHECKER", "test_run_pilot_p35:reject_premises")
    monkeypatch.setattr("run_pilot._trial_combinations", lambda: [("ring", "dgaf", 0)])
    monkeypatch.setattr("run_pilot._environment_fingerprint", lambda: "environment-test")
    monkeypatch.setattr("run_pilot.SEED_RUNTIME_CEILING_SECONDS", 60.0)
    monkeypatch.setattr("run_pilot._retain", lambda *args, **kwargs: None)

    captured: list[dict] = []

    def capture(_path, document, *args, **kwargs):
        captured.extend(document["records"])

    monkeypatch.setattr("run_pilot._write_and_validate_artifact", capture)

    assert run_pilot(tmp_path / "output", seeds=1) == 0
    assert captured
    record = captured[0]
    assert record["blinded_condition_id"].startswith("blind_")
    assert record["status"] == "UNRECOVERED_FAILURE"
    assert record["ffcr_success"] is False
    trace = record["governance_trace"]
    assert trace
    assert trace[0]["final_status"] in {"KILL", "KILL_REC"}
    assert any(
        gate["pattern"] == "P-35" and gate["result"] == "KILL"
        for gate in trace[0]["gate_records"]
    )
