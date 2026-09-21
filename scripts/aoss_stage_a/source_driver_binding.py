"""Validate the proposed, non-collecting Stage-A source-driver binding.

This contract binds the frozen synthetic recipe catalog to the exact ACP source
identity. It does not accept an executable, destination, ACP execution, or
collection readiness.
"""

from __future__ import annotations

from typing import Any, Mapping

RECORD_TYPE = "AOSS_V0_6_STAGE_A_SOURCE_DRIVER_BINDING"
EXPECTED_STATUS = "PROPOSED_NON_COLLECTING_SYNTHETIC_ONLY"
EXPECTED_CONTROLLER_ISSUE = 901
EXPECTED_CATALOG_PATH = "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"
EXPECTED_RECIPE_VERSION = "AOSS_V0_6_STAGE_A_SYNTHETIC_RECIPE_CATALOG_V1"
EXPECTED_SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
EXPECTED_SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
EXPECTED_RECIPE_CLASSES = (
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

_REQUIRED_FIELDS = {
    "record_type",
    "schema_version",
    "status",
    "controller_issue",
    "catalog_path",
    "recipe_version",
    "recipe_classes",
    "source_repository",
    "source_commit",
    "driver_import_allowed",
    "acp_execution_allowed",
    "accepted_outcome_artifacts",
    "executable_identity",
    "destination_identity",
    "source_driver_binding",
    "collection_execution_readiness",
    "outcomes_generated",
    "scientific_n_increment",
    "canonical_dgaf_efficacy",
    "high_assurance",
}


class SourceDriverBindingError(ValueError):
    """Raised when the proposed source-driver boundary drifts."""


def _fail(code: str) -> None:
    raise SourceDriverBindingError(code)


def validate_unaccepted_source_driver_binding(
    binding: Mapping[str, Any],
) -> dict[str, object]:
    """Verify catalog/source identity while preserving the unaccepted boundary."""

    if set(binding) != _REQUIRED_FIELDS:
        _fail("SOURCE_DRIVER_BINDING_FIELD_SET_MISMATCH")
    if binding["record_type"] != RECORD_TYPE:
        _fail("SOURCE_DRIVER_BINDING_RECORD_TYPE_MISMATCH")
    if binding["schema_version"] != 1:
        _fail("SOURCE_DRIVER_BINDING_SCHEMA_VERSION_MISMATCH")
    if binding["status"] != EXPECTED_STATUS:
        _fail("SOURCE_DRIVER_BINDING_STATUS_MISMATCH")
    if binding["controller_issue"] != EXPECTED_CONTROLLER_ISSUE:
        _fail("SOURCE_DRIVER_BINDING_CONTROLLER_MISMATCH")
    if binding["catalog_path"] != EXPECTED_CATALOG_PATH:
        _fail("RECIPE_CATALOG_PATH_MISMATCH")
    if binding["recipe_version"] != EXPECTED_RECIPE_VERSION:
        _fail("RECIPE_VERSION_MISMATCH")
    if binding["recipe_classes"] != list(EXPECTED_RECIPE_CLASSES):
        _fail("RECIPE_CLASS_SET_MISMATCH")
    if binding["source_repository"] != EXPECTED_SOURCE_REPOSITORY:
        _fail("SOURCE_REPOSITORY_MISMATCH")
    if binding["source_commit"] != EXPECTED_SOURCE_COMMIT:
        _fail("SOURCE_COMMIT_MISMATCH")
    if binding["driver_import_allowed"] is not False:
        _fail("DRIVER_IMPORT_PREMATURE")
    if binding["acp_execution_allowed"] is not False:
        _fail("ACP_EXECUTION_PREMATURE")
    if binding["accepted_outcome_artifacts"] is not False:
        _fail("OUTCOME_ARTIFACT_ACCEPTANCE_PREMATURE")
    if binding["executable_identity"] is not None:
        _fail("EXECUTABLE_BINDING_PREMATURE")
    if binding["destination_identity"] is not None:
        _fail("DESTINATION_BINDING_PREMATURE")
    if binding["source_driver_binding"] != "NOT_ESTABLISHED":
        _fail("SOURCE_DRIVER_ACCEPTANCE_PREMATURE")
    if binding["collection_execution_readiness"] != "NOT_ESTABLISHED":
        _fail("COLLECTION_READINESS_PREMATURE")
    if binding["outcomes_generated"] is not False:
        _fail("OUTCOME_GENERATION_PREMATURE")
    if binding["scientific_n_increment"] != 0:
        _fail("SCIENTIFIC_N_INCREMENT_INVALID")
    if binding["canonical_dgaf_efficacy"] != "NOT_ESTABLISHED":
        _fail("EFFICACY_PREMATURE")
    if binding["high_assurance"] != "NOT_AUTHORIZED":
        _fail("HIGH_ASSURANCE_PREMATURE")

    return {
        "record_type": "AOSS_STAGE_A_SOURCE_DRIVER_BINDING_REPORT",
        "catalog_binding": "PASS_PROPOSED_NON_COLLECTING",
        "source_repository": EXPECTED_SOURCE_REPOSITORY,
        "source_commit": EXPECTED_SOURCE_COMMIT,
        "driver_execution": "NOT_PERFORMED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "executable_identity": None,
        "destination_identity": None,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
