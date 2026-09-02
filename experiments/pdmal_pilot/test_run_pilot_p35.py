"""P-35 premise-hook regression coverage for the pilot runner."""
from __future__ import annotations

import pytest

from dgaf_tgl_adapter import DGAF_TGLAdapter
from task_engine import AttemptStatus


def reject_premises(_input_text: str, _context: object) -> bool:
    return False


def raise_premise_error(_input_text: str, _context: object) -> bool:
    raise RuntimeError("boom")


def test_adapter_requires_explicit_p35_checker() -> None:
    with pytest.raises(TypeError, match="explicit callable"):
        DGAF_TGLAdapter("session", None)  # type: ignore[arg-type]


def test_adapter_accepts_explicit_p35_checker() -> None:
    adapter = DGAF_TGLAdapter("session", reject_premises)
    assert adapter.premise_check_fn is reject_premises


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
        for gate in trace[0]["gates"]
    )
