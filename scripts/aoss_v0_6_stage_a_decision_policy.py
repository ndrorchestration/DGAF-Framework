"""Prospective, fail-closed AOSS v0.6 Stage-A decision policy.

This is a new pre-data v0.6 policy freeze. It is not a reconstruction of an
unlocated v0.5 executable implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

POLICY_VERSION = "AOSS_V0_6_STAGE_A_POLICY_V1"

TriState = Literal["TRUE", "FALSE", "INCONCLUSIVE"]
Decision = Literal[
    "RECORD_OUTCOME",
    "ESCALATE_BLOCK",
    "PERTURB",
    "ESCALATE_CONFLICT",
    "REQUEST_EVIDENCE",
    "EXECUTE",
    "REQUEST_AUTHORIZATION",
    "HOLD",
]

_ALLOWED_TRI_STATES = {"TRUE", "FALSE", "INCONCLUSIVE"}


@dataclass(frozen=True)
class PolicyInput:
    terminal: bool = False
    blocked: bool = False
    deadlock_candidate: bool = False
    conflicted: bool = False
    uncertain: bool = False
    authorization: TriState = "INCONCLUSIVE"
    validation: TriState = "INCONCLUSIVE"
    provenance_valid: TriState = "INCONCLUSIVE"
    required_predicate_inconclusive: bool = False


@dataclass(frozen=True)
class PolicyResult:
    policy_version: str
    decision: Decision
    matched_rule: str
    input_valid: bool


def _boolean_fields_are_valid(state: PolicyInput) -> bool:
    return all(
        type(value) is bool
        for value in (
            state.terminal,
            state.blocked,
            state.deadlock_candidate,
            state.conflicted,
            state.uncertain,
            state.required_predicate_inconclusive,
        )
    )


def evaluate_policy(state: PolicyInput) -> PolicyResult:
    """Evaluate the prospectively frozen Stage-A policy deterministically."""

    if not _boolean_fields_are_valid(state):
        return PolicyResult(POLICY_VERSION, "HOLD", "INVALID_BOOLEAN_INPUT", False)

    tri_states = (state.authorization, state.validation, state.provenance_valid)
    if any(value not in _ALLOWED_TRI_STATES for value in tri_states):
        return PolicyResult(POLICY_VERSION, "HOLD", "INVALID_TRI_STATE_INPUT", False)

    required_inconclusive = state.required_predicate_inconclusive or any(
        value == "INCONCLUSIVE" for value in tri_states
    )

    # Prospective precedence is frozen exactly here. All non-EXECUTE actions
    # are control/advisory outputs. EXECUTE is the sole execution-bearing action.
    if state.terminal:
        return PolicyResult(POLICY_VERSION, "RECORD_OUTCOME", "TERMINAL", True)
    if state.blocked:
        return PolicyResult(POLICY_VERSION, "ESCALATE_BLOCK", "BLOCKED", True)
    if state.deadlock_candidate:
        return PolicyResult(POLICY_VERSION, "PERTURB", "DEADLOCK_CANDIDATE", True)
    if state.conflicted:
        return PolicyResult(POLICY_VERSION, "ESCALATE_CONFLICT", "CONFLICTED", True)
    if state.uncertain:
        return PolicyResult(POLICY_VERSION, "REQUEST_EVIDENCE", "UNCERTAIN", True)
    if (
        state.authorization == "TRUE"
        and state.validation == "TRUE"
        and state.provenance_valid == "TRUE"
        and not required_inconclusive
    ):
        return PolicyResult(
            POLICY_VERSION,
            "EXECUTE",
            "AUTHORIZED_AND_VALIDATED_AND_PROVENANCE_VALID",
            True,
        )
    if state.validation == "TRUE" and state.authorization == "FALSE":
        return PolicyResult(
            POLICY_VERSION,
            "REQUEST_AUTHORIZATION",
            "VALIDATED_AND_NOT_AUTHORIZED",
            True,
        )
    if required_inconclusive:
        return PolicyResult(
            POLICY_VERSION,
            "HOLD",
            "REQUIRED_PREDICATE_INCONCLUSIVE",
            True,
        )
    return PolicyResult(POLICY_VERSION, "HOLD", "DEFAULT_FAIL_CLOSED", True)
