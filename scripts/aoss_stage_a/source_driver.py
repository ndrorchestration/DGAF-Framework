"""Implemented but unadmitted AOSS Stage-A source-driver candidate.

This module contains the exact recipe logic needed to drive the frozen ACP
source after admission. It deliberately does not import ACP, open a destination,
reserve an attempt, or decide whether execution is authorized. A future
collector may inject the independently verified frozen ACP API only after the
separate execution-admission predicates are accepted.

Importing or executing this candidate is not part of the current evidence run.
Current review is source/static only.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Final

SOURCE_REPOSITORY: Final = "ndrorchestration/agent-control-plane"
SOURCE_COMMIT: Final = "dbab7c1afafec524ce7c18157de2089cafe79c87"
SOURCE_CORE_BLOB: Final = "1341df7296a426b336b76ac6b1e4df67611ec931"
RECIPE_VERSION: Final = "AOSS_V0_6_STAGE_A_SYNTHETIC_RECIPE_CATALOG_V1"
RECIPE_CATALOG_SHA256: Final = "b3c0d883cd9463ec558ee8a3fab3376641b2603eb474a745c119a28d1cd15d77"
DRIVER_STATUS: Final = "IMPLEMENTED_NOT_ADMITTED"
STALE_INJECTION_START: Final = "2025-01-01T00:00:00+00:00"
STALE_INJECTION_END: Final = "2025-01-01T00:00:01+00:00"

RECIPE_SPECS: Final[dict[str, dict[str, Any]]] = {
    "normal_completion": {
        "native_operation": "normal_completion",
        "transform": None,
        "expected_terminal_event": "task.completed",
    },
    "policy_denial": {
        "native_operation": "policy_denial",
        "transform": None,
        "expected_terminal_event": "task.denied",
    },
    "unknown_capability_rejection": {
        "native_operation": "unknown_capability_rejection",
        "transform": None,
        "expected_terminal_event": "task.rejected",
    },
    "handler_failure": {
        "native_operation": "handler_failure",
        "transform": None,
        "expected_terminal_event": "task.failed",
    },
    "cancellation": {
        "native_operation": "cancellation",
        "transform": None,
        "expected_terminal_event": "task.cancelled",
    },
    "exact_budget_success": {
        "native_operation": "exact_budget_success",
        "transform": None,
        "expected_terminal_event": "task.completed",
    },
    "budget_exhaustion": {
        "native_operation": "budget_exhaustion",
        "transform": None,
        "expected_terminal_event": "task.budget_exhausted",
    },
    "suppressed_budget_exception_fail_closed": {
        "native_operation": "suppressed_budget_exception_fail_closed",
        "transform": None,
        "expected_terminal_event": "task.budget_exhausted",
    },
    "missing_event": {
        "native_operation": "normal_completion",
        "transform": "drop_terminal_event",
        "expected_terminal_event": None,
    },
    "reordered_exported_events": {
        "native_operation": "normal_completion",
        "transform": "reverse_events",
        "expected_terminal_event": "task.completed",
    },
    "duplicate_replayed_event": {
        "native_operation": "normal_completion",
        "transform": "duplicate_first_event",
        "expected_terminal_event": "task.completed",
    },
    "stale_timestamp": {
        "native_operation": "normal_completion",
        "transform": "inject_stale_timestamps",
        "expected_terminal_event": "task.completed",
    },
    "malformed_manifest": {
        "native_operation": "normal_completion",
        "transform": "unsupported_schema",
        "expected_terminal_event": None,
    },
    "mismatched_run_id": {
        "native_operation": "normal_completion",
        "transform": "mismatch_event_run_id",
        "expected_terminal_event": None,
    },
    "source_order_ambiguity": {
        "native_operation": "normal_completion",
        "transform": "equalize_event_timestamps",
        "expected_terminal_event": "task.completed",
    },
    "missing_authority_evidence": {
        "native_operation": "normal_completion",
        "transform": None,
        "expected_terminal_event": "task.completed",
    },
}


class SourceDriverError(ValueError):
    """Raised when recipe selection or injected source behavior is invalid."""


@dataclass(frozen=True)
class SourceEpisode:
    recipe_class: str
    native_operation: str
    transformation: str | None
    source_repository: str
    source_commit: str
    source_core_blob: str
    recipe_version: str
    original_manifest: dict[str, Any]
    exported_manifest: dict[str, Any]
    original_bytes: bytes
    exported_bytes: bytes
    original_sha256: str
    exported_sha256: str


def _canonical_bytes(value: Any) -> bytes:
    """Serialize retained source/export objects under the study bundle convention."""
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def recipe_spec(recipe_class: str) -> dict[str, Any]:
    """Return a defensive copy of one frozen source-driver recipe."""
    if type(recipe_class) is not str or recipe_class not in RECIPE_SPECS:
        raise SourceDriverError("SOURCE_DRIVER_RECIPE_NOT_FROZEN")
    return copy.deepcopy(RECIPE_SPECS[recipe_class])


def _run_native(api: Any, operation: str, *, run_id: str) -> dict[str, Any]:
    """Execute one native workload using an injected, already-admitted ACP API."""
    if not isinstance(run_id, str) or not run_id.strip():
        raise SourceDriverError("SOURCE_DRIVER_RUN_ID_INVALID")

    ControlPlane = api.ControlPlane
    Task = api.Task
    ExecutionBudget = api.ExecutionBudget
    BudgetExceeded = api.BudgetExceeded

    if operation == "normal_completion":
        plane = ControlPlane(run_id=run_id)

        def handler(task: Any) -> str:
            task.consume(steps=1)
            return "ok"

        plane.register("work", handler)
        plane.dispatch("work", Task(payload=None))
        return plane.provenance_manifest()

    if operation == "policy_denial":
        plane = ControlPlane(policy=lambda _capability, _task: "policy denied", run_id=run_id)
        plane.register("work", lambda task: task.payload)
        plane.dispatch("work", Task(payload=None))
        return plane.provenance_manifest()

    if operation == "unknown_capability_rejection":
        plane = ControlPlane(run_id=run_id)
        try:
            plane.dispatch("missing", Task(payload=None))
        except KeyError:
            pass
        else:
            raise SourceDriverError("SOURCE_DRIVER_UNKNOWN_CAPABILITY_DID_NOT_REJECT")
        return plane.provenance_manifest()

    if operation == "handler_failure":
        plane = ControlPlane(run_id=run_id)

        def fail(_task: Any) -> None:
            raise RuntimeError("boom")

        plane.register("work", fail)
        plane.dispatch("work", Task(payload=None))
        return plane.provenance_manifest()

    if operation == "cancellation":
        plane = ControlPlane(run_id=run_id)
        plane.cancel(Task(payload=None))
        return plane.provenance_manifest()

    if operation == "exact_budget_success":
        plane = ControlPlane(run_id=run_id)

        def exact(task: Any) -> str:
            task.consume(steps=2, tool_calls=1, tokens=100, cost=0.25)
            return "ok"

        plane.register("work", exact)
        task = Task(
            payload=None,
            budget=ExecutionBudget(
                max_steps=2,
                max_tool_calls=1,
                max_tokens=100,
                max_cost=0.25,
            ),
        )
        plane.dispatch("work", task)
        return plane.provenance_manifest()

    if operation == "budget_exhaustion":
        plane = ControlPlane(run_id=run_id)

        def exhaust(task: Any) -> str:
            task.consume(steps=1)
            task.consume(steps=2)
            return "unreachable"

        plane.register("work", exhaust)
        plane.dispatch("work", Task(payload=None, budget=ExecutionBudget(max_steps=2)))
        return plane.provenance_manifest()

    if operation == "suppressed_budget_exception_fail_closed":
        plane = ControlPlane(run_id=run_id)

        def suppress(task: Any) -> str:
            try:
                task.consume(tool_calls=2)
            except BudgetExceeded:
                pass
            return "suppressed"

        plane.register("work", suppress)
        plane.dispatch(
            "work",
            Task(payload=None, budget=ExecutionBudget(max_tool_calls=1)),
        )
        return plane.provenance_manifest()

    raise SourceDriverError("SOURCE_DRIVER_NATIVE_OPERATION_NOT_FROZEN")


def _apply_transform(manifest: dict[str, Any], transform: str | None) -> dict[str, Any]:
    """Apply only the declared post-export perturbation, preserving the input object."""
    exported = copy.deepcopy(manifest)
    if transform is None:
        return exported

    events = exported.get("events")
    if not isinstance(events, list):
        raise SourceDriverError("SOURCE_DRIVER_MANIFEST_EVENTS_INVALID")

    if transform == "drop_terminal_event":
        if not events:
            raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_REQUIRES_EVENT")
        exported["events"] = events[:-1]
        exported["event_count"] = len(exported["events"])
        return exported

    if transform == "reverse_events":
        exported["events"] = list(reversed(events))
        return exported

    if transform == "duplicate_first_event":
        if not events:
            raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_REQUIRES_EVENT")
        exported["events"] = [events[0], copy.deepcopy(events[0]), *events[1:]]
        exported["event_count"] = len(exported["events"])
        return exported

    if transform == "inject_stale_timestamps":
        if not events:
            raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_REQUIRES_EVENT")
        for index, event in enumerate(events):
            event["timestamp"] = STALE_INJECTION_START if index == 0 else STALE_INJECTION_END
        return exported

    if transform == "unsupported_schema":
        exported["schema"] = "agent-control-plane.provenance.v999"
        return exported

    if transform == "mismatch_event_run_id":
        if not events:
            raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_REQUIRES_EVENT")
        events[0]["run_id"] = "other-run"
        return exported

    if transform == "equalize_event_timestamps":
        if not events:
            raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_REQUIRES_EVENT")
        timestamp = events[0].get("timestamp")
        for event in events:
            event["timestamp"] = timestamp
        return exported

    raise SourceDriverError("SOURCE_DRIVER_TRANSFORM_NOT_FROZEN")


def generate_source_episode(api: Any, recipe_class: str, *, run_id: str) -> SourceEpisode:
    """Generate one source episode after an external caller has admitted execution.

    This function does not determine whether execution is authorized. The caller
    must not inject ACP until the separate environment, driver, executable,
    destination, attempt, reviewer, and local-adjudication predicates are
    accepted.
    """
    spec = recipe_spec(recipe_class)
    original = _run_native(api, spec["native_operation"], run_id=run_id)
    exported = _apply_transform(original, spec["transform"])
    original_bytes = _canonical_bytes(original)
    exported_bytes = _canonical_bytes(exported)
    return SourceEpisode(
        recipe_class=recipe_class,
        native_operation=spec["native_operation"],
        transformation=spec["transform"],
        source_repository=SOURCE_REPOSITORY,
        source_commit=SOURCE_COMMIT,
        source_core_blob=SOURCE_CORE_BLOB,
        recipe_version=RECIPE_VERSION,
        original_manifest=original,
        exported_manifest=exported,
        original_bytes=original_bytes,
        exported_bytes=exported_bytes,
        original_sha256=_sha256(original_bytes),
        exported_sha256=_sha256(exported_bytes),
    )
