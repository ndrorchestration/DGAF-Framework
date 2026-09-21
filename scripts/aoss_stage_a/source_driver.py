"""Non-collecting candidate boundary for the AOSS Stage-A ACP source driver.

This module intentionally cannot execute ACP.  It validates only the frozen
recipe identity and produces an immutable execution *plan*.  Admission of exact
executable bytes, environment acceptance, custody/replay, and collection
readiness remain separate gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

SOURCE_REPOSITORY: Final = "ndrorchestration/agent-control-plane"
SOURCE_COMMIT: Final = "dbab7c1afafec524ce7c18157de2089cafe79c87"
RECIPE_VERSION: Final = "AOSS_V0_6_STAGE_A_SYNTHETIC_RECIPE_CATALOG_V1"
DRIVER_STATUS: Final = "CANDIDATE_NON_EXECUTING"

RECIPE_CLASSES: Final = (
    "normal_completion",
    "policy_denial",
    "unknown_capability_rejection",
    "handler_failure",
    "cancellation",
    "exact_budget_success",
    "budget_exhaustion",
    "suppressed_budget_exception_fail_closed",
    "missing_event",
    "reordered_exported_events",
    "duplicate_replayed_event",
    "stale_timestamp",
    "malformed_manifest",
    "mismatched_run_id",
    "source_order_ambiguity",
    "missing_authority_evidence",
)


class SourceDriverBoundaryError(ValueError):
    """Raised when a candidate source-driver request crosses the frozen boundary."""


@dataclass(frozen=True)
class SourceExecutionPlan:
    recipe_class: str
    source_repository: str = SOURCE_REPOSITORY
    source_commit: str = SOURCE_COMMIT
    recipe_version: str = RECIPE_VERSION
    execution_status: str = DRIVER_STATUS


def plan_recipe(recipe_class: str) -> SourceExecutionPlan:
    """Return a non-executing exact-source plan for one frozen recipe class."""
    if type(recipe_class) is not str or recipe_class not in RECIPE_CLASSES:
        raise SourceDriverBoundaryError("SOURCE_DRIVER_RECIPE_NOT_FROZEN")
    return SourceExecutionPlan(recipe_class=recipe_class)


def execute_recipe(*_args: object, **_kwargs: object) -> None:
    """Fail closed: source execution is not admitted by this candidate."""
    raise SourceDriverBoundaryError("SOURCE_DRIVER_EXECUTION_NOT_ACCEPTED")
