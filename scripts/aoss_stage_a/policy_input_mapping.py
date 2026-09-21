"""Conservative synthetic-only bridge to the prospective Stage-A policy.

This module does not execute ACP or infer authorization, validation, or
provenance from event labels. It converts an explicitly supplied synthetic
observation into PolicyInput and fails closed when structural or freshness
evidence is missing or ambiguous.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from scripts.aoss_v0_6_stage_a_decision_policy import PolicyInput, TriState

MAPPING_VERSION = "AOSS_V0_6_STAGE_A_POLICY_INPUT_MAPPING_V1"
_FRESHNESS_STATES = {"FRESH", "STALE", "FUTURE_SKEW", "INCONCLUSIVE"}
_TERMINAL_KINDS = {
    "task.completed",
    "task.denied",
    "task.rejected",
    "task.failed",
    "task.cancelled",
    "task.budget_exhausted",
}
_BLOCKING_KINDS = _TERMINAL_KINDS - {"task.completed"}
_TRI_STATES = {"TRUE", "FALSE", "INCONCLUSIVE"}


class MappingError(ValueError):
    """Raised when a synthetic mapping input is absent or ambiguous."""


@dataclass(frozen=True)
class MappingObservation:
    terminal_event_kind: str | None
    terminal_event_count: int
    freshness: str
    source_order_ambiguous: bool
    authorization: TriState
    validation: TriState
    provenance_valid: TriState
    conflicted: bool
    deadlock_candidate: bool


def _require_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise MappingError(f"{name} must be boolean")
    return value


def _require_tri_state(value: Any, name: str) -> TriState:
    if type(value) is not str or value not in _TRI_STATES:
        raise MappingError(f"{name} must be TRUE, FALSE, or INCONCLUSIVE")
    return value  # type: ignore[return-value]


def observation_from_dict(value: Mapping[str, Any]) -> MappingObservation:
    required = {
        "terminal_event_kind",
        "terminal_event_count",
        "freshness",
        "source_order_ambiguous",
        "authorization",
        "validation",
        "provenance_valid",
        "conflicted",
        "deadlock_candidate",
    }
    missing = sorted(required - set(value))
    if missing:
        raise MappingError("required mapping fields missing: " + ",".join(missing))
    unexpected = [key for key in value if key not in required]
    if unexpected:
        raise MappingError(
            "unexpected mapping fields: " + ",".join(sorted(str(key) for key in unexpected))
        )

    kind = value["terminal_event_kind"]
    if kind is not None and (type(kind) is not str or kind not in _TERMINAL_KINDS):
        raise MappingError("terminal_event_kind is unknown")
    count = value["terminal_event_count"]
    if type(count) is not int or count < 0:
        raise MappingError("terminal_event_count must be a non-negative integer")
    if count == 1 and kind is None:
        raise MappingError("one terminal event requires its event kind")
    if count != 1 and kind is not None:
        raise MappingError("terminal_event_kind is ambiguous when count is not one")

    freshness = value["freshness"]
    if type(freshness) is not str or freshness not in _FRESHNESS_STATES:
        raise MappingError("freshness state is unknown")

    return MappingObservation(
        terminal_event_kind=kind,
        terminal_event_count=count,
        freshness=freshness,
        source_order_ambiguous=_require_bool(value["source_order_ambiguous"], "source_order_ambiguous"),
        authorization=_require_tri_state(value["authorization"], "authorization"),
        validation=_require_tri_state(value["validation"], "validation"),
        provenance_valid=_require_tri_state(value["provenance_valid"], "provenance_valid"),
        conflicted=_require_bool(value["conflicted"], "conflicted"),
        deadlock_candidate=_require_bool(value["deadlock_candidate"], "deadlock_candidate"),
    )


def map_observation(value: Mapping[str, Any]) -> PolicyInput:
    """Map one explicit synthetic observation without permissive inference."""

    observation = observation_from_dict(value)
    structurally_ambiguous = observation.terminal_event_count != 1 or observation.source_order_ambiguous
    evidence_inconclusive = (
        structurally_ambiguous
        or observation.freshness != "FRESH"
        or any(
            state == "INCONCLUSIVE"
            for state in (
                observation.authorization,
                observation.validation,
                observation.provenance_valid,
            )
        )
    )

    # Structural/freshness ambiguity cannot create a terminal or blocked action.
    # It is represented as uncertainty plus an explicit required-predicate hold.
    if evidence_inconclusive:
        terminal = False
        blocked = False
        deadlock_candidate = False
        conflicted = False
        uncertain = True
    else:
        terminal = observation.terminal_event_kind == "task.completed"
        blocked = observation.terminal_event_kind in _BLOCKING_KINDS
        deadlock_candidate = observation.deadlock_candidate
        conflicted = observation.conflicted
        uncertain = False

    return PolicyInput(
        terminal=terminal,
        blocked=blocked,
        deadlock_candidate=deadlock_candidate,
        conflicted=conflicted,
        uncertain=uncertain,
        authorization=observation.authorization,
        validation=observation.validation,
        provenance_valid=observation.provenance_valid,
        required_predicate_inconclusive=evidence_inconclusive,
    )
