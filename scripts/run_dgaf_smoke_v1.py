#!/usr/bin/env python3
"""Run the bounded DGAF Smoke Contract v1 and emit machine-readable evidence."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pptl.control_plane import (  # noqa: E402
    ControlPlane,
    ControlPlaneViolation,
    ControlTask,
    TaskState,
)
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget  # noqa: E402

SCHEMA = "dgaf.smoke.v1"
FIXTURES = {
    "allow": "GST-ALLOW-001",
    "deny": "GST-DENY-001",
    "ambiguous": "GST-AMBIGUOUS-001",
}


def _budget() -> ResourceBudget:
    return ResourceBudget(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=3,
        max_nodes=8,
        max_depth=2,
        max_concurrency=2,
    )


def _envelope() -> GovernanceEnvelope:
    return GovernanceEnvelope(
        trace_id="dgaf-smoke-root-trace",
        task_id="dgaf-smoke-root",
        authority_scope=frozenset({"research", "draft"}),
        permitted_tools=frozenset({"read", "search"}),
        data_classes=frozenset({"public", "internal"}),
        prohibited_actions=frozenset({"delete", "send"}),
        budget=_budget(),
        side_effect_mode="PROPOSE_ONLY",
        metadata={"fixture": FIXTURES["allow"]},
    )


def _record_gate(
    gates: dict[str, dict[str, Any]],
    name: str,
    fn: Callable[[], dict[str, Any]],
) -> None:
    try:
        detail = fn()
    except Exception as exc:
        gates[name] = {
            "outcome": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    else:
        gates[name] = {"outcome": "PASS", **detail}


def run_smoke() -> dict[str, Any]:
    context: dict[str, Any] = {}
    gates: dict[str, dict[str, Any]] = {}

    def boot() -> dict[str, Any]:
        plane = ControlPlane()
        task = ControlTask(task_id="dgaf-smoke-root", envelope=_envelope())
        context["plane"] = plane
        context["task"] = task
        return {
            "initial_state": task.state.value,
            "side_effect_mode": task.envelope.side_effect_mode,
        }

    def route() -> dict[str, Any]:
        plane: ControlPlane = context["plane"]
        task: ControlTask = context["task"]
        plane.submit(task)
        assert task.state is TaskState.PREFLIGHT
        plane.admit(task.task_id)
        assert task.state is TaskState.ADMITTED
        return {"state": task.state.value}

    def execute() -> dict[str, Any]:
        plane: ControlPlane = context["plane"]
        task: ControlTask = context["task"]
        plane.start_expansion(task.task_id)
        assert task.state is TaskState.EXPANDING
        plane.begin_evaluation(task.task_id)
        assert task.state is TaskState.EVALUATING
        return {"state": task.state.value}

    def provenance() -> dict[str, Any]:
        plane: ControlPlane = context["plane"]
        task: ControlTask = context["task"]
        snapshot = task.snapshot()
        assert snapshot["task_id"] == task.task_id
        assert snapshot["envelope_trace"] == task.envelope.trace_id
        state_events = [
            event["state"]
            for event in plane.events
            if event.get("event") == "STATE" and event.get("task_id") == task.task_id
        ]
        assert state_events == ["PREFLIGHT", "ADMITTED", "EXPANDING", "EVALUATING"]
        return {
            "task_id": snapshot["task_id"],
            "trace_id": snapshot["envelope_trace"],
            "state_events": state_events,
        }

    def deny() -> dict[str, Any]:
        parent = ControlPlane()
        root = ControlTask(task_id="deny-root", envelope=_envelope())
        parent.submit(root)
        parent.admit(root.task_id)

        before_ids = set(parent.tasks)
        denied = False
        try:
            parent.create_child(
                root.task_id,
                task_id="deny-child",
                trace_id="deny-child-trace",
                authority_scope={"research", "draft", "admin"},
                permitted_tools={"read"},
                data_classes={"public"},
                envelope_budget=ResourceBudget(
                    max_input_tokens=50,
                    max_output_tokens=50,
                    max_tool_calls=1,
                    max_elapsed_ms=500,
                    max_rounds=1,
                    max_nodes=1,
                    max_depth=1,
                    max_concurrency=1,
                ),
            )
        except PermissionError:
            denied = True

        assert denied is True
        assert set(parent.tasks) == before_ids
        assert "deny-child" not in parent.tasks
        assert root.state is TaskState.ADMITTED
        return {
            "fixture": FIXTURES["deny"],
            "rejected": True,
            "parent_state": root.state.value,
        }

    def state() -> dict[str, Any]:
        plane: ControlPlane = context["plane"]
        task: ControlTask = context["task"]
        before = task.state
        blocked = False
        try:
            plane.mark_merge_ready(task.task_id)
        except ControlPlaneViolation:
            blocked = True

        assert blocked is True
        assert before is TaskState.EVALUATING
        assert task.state is before
        assert task.last_tgl_status is None
        assert task.last_tgl_seal is None
        assert task.envelope.side_effect_mode == "PROPOSE_ONLY"
        return {
            "fixture": FIXTURES["ambiguous"],
            "promotion_blocked": True,
            "state": task.state.value,
        }

    for name, fn in (
        ("SMOKE_BOOT", boot),
        ("SMOKE_ROUTE", route),
        ("SMOKE_EXECUTE", execute),
        ("SMOKE_PROVENANCE", provenance),
        ("SMOKE_DENY", deny),
        ("SMOKE_STATE", state),
    ):
        _record_gate(gates, name, fn)

    outcome = "PASS" if all(gate["outcome"] == "PASS" for gate in gates.values()) else "FAIL"
    return {
        "schema": SCHEMA,
        "revision": os.environ.get("DGAF_REVISION") or os.environ.get("GITHUB_SHA") or "LOCAL_UNBOUND",
        "outcome": outcome,
        "fixtures": FIXTURES,
        "gates": gates,
        "boundary": {
            "scientific_n_increment": 0,
            "authorization_effect": "NONE",
            "independent_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/dgaf-smoke-v1/result.json")
    args = parser.parse_args()

    result = run_smoke()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["outcome"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
