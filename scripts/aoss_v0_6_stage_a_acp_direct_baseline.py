"""Prospective ACP direct-event baseline for AOSS v0.6 Stage A.

This baseline replaces the unrecoverable historical OMR comparator for the
Stage-A primary comparison. It is frozen before Stage-A outcome collection and
uses only source-native ACP lifecycle event kinds plus structural manifest
identity checks. It does not reconstruct O, M, or R.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

BASELINE_VERSION = "AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1"
EXPECTED_SCHEMA = "agent-control-plane.provenance.v1"

Decision = Literal["RECORD_OUTCOME", "ESCALATE_BLOCK", "HOLD"]

_TERMINAL_DECISIONS: dict[str, Decision] = {
    "task.completed": "RECORD_OUTCOME",
    "task.denied": "ESCALATE_BLOCK",
    "task.rejected": "ESCALATE_BLOCK",
    "task.failed": "ESCALATE_BLOCK",
    "task.cancelled": "ESCALATE_BLOCK",
    "task.budget_exhausted": "ESCALATE_BLOCK",
}
_KNOWN_EVENT_KINDS = {"task.started", *_TERMINAL_DECISIONS}


@dataclass(frozen=True)
class BaselineResult:
    baseline_version: str
    decision: Decision
    matched_rule: str
    input_valid: bool
    terminal_event_kind: str | None
    terminal_event_count: int


def evaluate_baseline(manifest: dict[str, Any]) -> BaselineResult:
    """Evaluate only structural identity and source-native terminal event kinds."""

    if not isinstance(manifest, dict):
        return BaselineResult(BASELINE_VERSION, "HOLD", "INVALID_MANIFEST_OBJECT", False, None, 0)
    if manifest.get("schema") != EXPECTED_SCHEMA:
        return BaselineResult(BASELINE_VERSION, "HOLD", "SCHEMA_MISMATCH", False, None, 0)

    run_id = manifest.get("run_id")
    events = manifest.get("events")
    event_count = manifest.get("event_count")
    if not isinstance(run_id, str) or not run_id:
        return BaselineResult(BASELINE_VERSION, "HOLD", "INVALID_RUN_ID", False, None, 0)
    if not isinstance(events, list) or type(event_count) is not int or event_count != len(events):
        return BaselineResult(BASELINE_VERSION, "HOLD", "INVALID_EVENT_CONTAINER", False, None, 0)

    terminal_kinds: list[str] = []
    for event in events:
        if not isinstance(event, dict):
            return BaselineResult(BASELINE_VERSION, "HOLD", "INVALID_EVENT_OBJECT", False, None, 0)
        if event.get("run_id") != run_id:
            return BaselineResult(BASELINE_VERSION, "HOLD", "EVENT_RUN_ID_MISMATCH", False, None, 0)
        event_kind = event.get("event")
        if not isinstance(event_kind, str) or event_kind not in _KNOWN_EVENT_KINDS:
            return BaselineResult(BASELINE_VERSION, "HOLD", "INVALID_EVENT_KIND", False, None, 0)
        if event_kind in _TERMINAL_DECISIONS:
            terminal_kinds.append(event_kind)

    if not terminal_kinds:
        return BaselineResult(BASELINE_VERSION, "HOLD", "NO_TERMINAL_EVENT", True, None, 0)
    if len(terminal_kinds) != 1:
        return BaselineResult(
            BASELINE_VERSION,
            "HOLD",
            "MULTIPLE_TERMINAL_EVENTS",
            True,
            None,
            len(terminal_kinds),
        )

    terminal = terminal_kinds[0]
    return BaselineResult(
        BASELINE_VERSION,
        _TERMINAL_DECISIONS[terminal],
        terminal,
        True,
        terminal,
        1,
    )
