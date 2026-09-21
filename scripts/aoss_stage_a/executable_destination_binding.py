"""Validate a proposed, non-collecting executable/destination identity envelope.

This contract records exact source-module provenance and synthetic fixture identities.
It does not accept a collector executable, destination, attempt, ACP execution, or
collection readiness.
"""

from __future__ import annotations

from typing import Any, Mapping

RECORD_TYPE = "AOSS_V0_6_STAGE_A_EXECUTABLE_DESTINATION_BINDING"
EXPECTED_CONTROLLER_ISSUE = 901
EXPECTED_STATUS = "PROPOSED_NON_COLLECTING_IDENTITY_ONLY"
EXPECTED_SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
EXPECTED_SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
EXPECTED_SOURCE_MODULE = "src/agent_control_plane/core.py"
EXPECTED_SOURCE_MODULE_BLOB = "1341df7296a426b336b76ac6b1e4df67611ec931"
EXPECTED_EXECUTABLE_IDENTITY = {
    "kind": "SOURCE_MODULE_PROVENANCE_ONLY",
    "repository": EXPECTED_SOURCE_REPOSITORY,
    "commit": EXPECTED_SOURCE_COMMIT,
    "path": EXPECTED_SOURCE_MODULE,
    "blob": EXPECTED_SOURCE_MODULE_BLOB,
}
EXPECTED_DESTINATION_IDENTITY = {
    "kind": "SYNTHETIC_FIXTURE_ONLY",
    "uri": "fixture://aoss-v0.6-stage-a/non-collecting",
}
EXPECTED_ATTEMPT_IDENTITY = {
    "kind": "SYNTHETIC_FIXTURE_ONLY",
    "attempt_id": "aoss-stage-a-fixture-0001",
}

_REQUIRED_FIELDS = {
    "record_type",
    "schema_version",
    "controller_issue",
    "status",
    "source_repository",
    "source_commit",
    "source_module",
    "source_module_blob",
    "executable_identity",
    "destination_identity",
    "attempt_identity",
    "executable_acceptance",
    "destination_acceptance",
    "execution_allowed",
    "outcomes_generated",
    "collection_execution_readiness",
    "scientific_n_increment",
    "canonical_dgaf_efficacy",
    "high_assurance",
}


class ExecutableDestinationBindingError(ValueError):
    """Raised when the proposed identity envelope drifts."""


def _fail(code: str) -> None:
    raise ExecutableDestinationBindingError(code)


def validate_proposed_executable_destination_binding(
    binding: Mapping[str, Any],
) -> dict[str, object]:
    """Verify provenance and fixture identities without accepting execution."""

    if set(binding) != _REQUIRED_FIELDS:
        _fail("EXECUTABLE_DESTINATION_FIELD_SET_MISMATCH")
    if binding["record_type"] != RECORD_TYPE:
        _fail("EXECUTABLE_DESTINATION_RECORD_TYPE_MISMATCH")
    if binding["schema_version"] != 1:
        _fail("EXECUTABLE_DESTINATION_SCHEMA_VERSION_MISMATCH")
    if binding["controller_issue"] != EXPECTED_CONTROLLER_ISSUE:
        _fail("EXECUTABLE_DESTINATION_CONTROLLER_MISMATCH")
    if binding["status"] != EXPECTED_STATUS:
        _fail("EXECUTABLE_DESTINATION_STATUS_MISMATCH")
    if binding["source_repository"] != EXPECTED_SOURCE_REPOSITORY:
        _fail("SOURCE_REPOSITORY_MISMATCH")
    if binding["source_commit"] != EXPECTED_SOURCE_COMMIT:
        _fail("SOURCE_COMMIT_MISMATCH")
    if binding["source_module"] != EXPECTED_SOURCE_MODULE:
        _fail("SOURCE_MODULE_MISMATCH")
    if binding["source_module_blob"] != EXPECTED_SOURCE_MODULE_BLOB:
        _fail("SOURCE_MODULE_BLOB_MISMATCH")
    if binding["executable_identity"] != EXPECTED_EXECUTABLE_IDENTITY:
        _fail("EXECUTABLE_IDENTITY_MISMATCH")
    if binding["destination_identity"] != EXPECTED_DESTINATION_IDENTITY:
        _fail("DESTINATION_FIXTURE_BOUNDARY")
    if binding["attempt_identity"] != EXPECTED_ATTEMPT_IDENTITY:
        _fail("ATTEMPT_FIXTURE_BOUNDARY")
    if binding["executable_acceptance"] != "NOT_ESTABLISHED":
        _fail("EXECUTABLE_ACCEPTANCE_PREMATURE")
    if binding["destination_acceptance"] != "NOT_ESTABLISHED":
        _fail("DESTINATION_ACCEPTANCE_PREMATURE")
    if binding["execution_allowed"] is not False:
        _fail("EXECUTION_PREMATURE")
    if binding["outcomes_generated"] is not False:
        _fail("OUTCOME_GENERATION_PREMATURE")
    if binding["collection_execution_readiness"] != "NOT_ESTABLISHED":
        _fail("COLLECTION_READINESS_PREMATURE")
    if binding["scientific_n_increment"] != 0:
        _fail("SCIENTIFIC_N_INCREMENT_INVALID")
    if binding["canonical_dgaf_efficacy"] != "NOT_ESTABLISHED":
        _fail("EFFICACY_PREMATURE")
    if binding["high_assurance"] != "NOT_AUTHORIZED":
        _fail("HIGH_ASSURANCE_PREMATURE")

    return {
        "record_type": "AOSS_STAGE_A_EXECUTABLE_DESTINATION_BINDING_REPORT",
        "identity_contract": "PASS_PROPOSED_NON_COLLECTING",
        "source_repository": EXPECTED_SOURCE_REPOSITORY,
        "source_commit": EXPECTED_SOURCE_COMMIT,
        "source_module": EXPECTED_SOURCE_MODULE,
        "source_module_blob": EXPECTED_SOURCE_MODULE_BLOB,
        "executable_acceptance": "NOT_ESTABLISHED",
        "destination_acceptance": "NOT_ESTABLISHED",
        "execution": "NOT_PERFORMED",
        "outcomes_generated": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
