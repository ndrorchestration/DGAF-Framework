from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "scripts/aoss_v0_6_stage_a_acp_direct_baseline.py"


def load_baseline():
    spec = importlib.util.spec_from_file_location("aoss_v06_acp_direct_baseline_test", BASELINE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def manifest(*event_kinds: str):
    events = [
        {
            "event": event_kind,
            "task_id": "task-1",
            "run_id": "run-1",
            "timestamp": "2026-09-18T10:00:00+00:00",
        }
        for event_kind in event_kinds
    ]
    return {
        "schema": "agent-control-plane.provenance.v1",
        "run_id": "run-1",
        "event_count": len(events),
        "events": events,
    }


def test_completed_terminal_records_outcome() -> None:
    baseline = load_baseline()
    result = baseline.evaluate_baseline(manifest("task.started", "task.completed"))
    assert result.decision == "RECORD_OUTCOME"
    assert result.matched_rule == "task.completed"
    assert result.input_valid is True


def test_negative_source_terminals_escalate_block() -> None:
    baseline = load_baseline()
    for terminal in (
        "task.denied",
        "task.rejected",
        "task.failed",
        "task.cancelled",
        "task.budget_exhausted",
    ):
        result = baseline.evaluate_baseline(manifest("task.started", terminal))
        assert result.decision == "ESCALATE_BLOCK"
        assert result.matched_rule == terminal
        assert result.input_valid is True


def test_missing_terminal_fails_closed() -> None:
    baseline = load_baseline()
    result = baseline.evaluate_baseline(manifest("task.started"))
    assert result.decision == "HOLD"
    assert result.matched_rule == "NO_TERMINAL_EVENT"
    assert result.input_valid is True


def test_multiple_terminals_fail_closed() -> None:
    baseline = load_baseline()
    result = baseline.evaluate_baseline(manifest("task.completed", "task.failed"))
    assert result.decision == "HOLD"
    assert result.matched_rule == "MULTIPLE_TERMINAL_EVENTS"
    assert result.terminal_event_count == 2


def test_structural_identity_errors_are_invalid_and_hold() -> None:
    baseline = load_baseline()

    bad_schema = manifest("task.completed")
    bad_schema["schema"] = "wrong"
    result = baseline.evaluate_baseline(bad_schema)
    assert result.decision == "HOLD"
    assert result.input_valid is False

    bad_run = manifest("task.completed")
    bad_run["events"][0]["run_id"] = "other"
    result = baseline.evaluate_baseline(bad_run)
    assert result.decision == "HOLD"
    assert result.input_valid is False


def test_baseline_ignores_richer_aoss_fields_by_contract() -> None:
    baseline = load_baseline()
    base = manifest("task.started", "task.completed")
    changed = manifest("task.started", "task.completed")
    changed["events"][0]["timestamp"] = "1900-01-01T00:00:00+00:00"
    changed["events"][1]["timestamp"] = "2999-01-01T00:00:00+00:00"
    changed["events"][0]["detail"] = "conflicting observer-relevant metadata"
    changed["events"][1]["state"] = "unexpected"
    assert baseline.evaluate_baseline(base).decision == baseline.evaluate_baseline(changed).decision


def test_baseline_does_not_depend_on_historical_omr_inputs() -> None:
    baseline = load_baseline()
    result = baseline.evaluate_baseline(manifest("task.completed"))
    assert result.baseline_version == "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"
    assert not hasattr(result, "O")
    assert not hasattr(result, "M")
    assert not hasattr(result, "R")
