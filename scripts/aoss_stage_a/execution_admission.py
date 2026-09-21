"""Read-only execution-admission blocker assessment for AOSS Stage A.

This module does not accept an environment, executable, destination, or attempt.
It only reports which explicit pre-admission conditions remain unresolved and
fails closed if a pre-admission record tries to enable execution prematurely.
"""

from __future__ import annotations

from typing import Any, Mapping

_BLOCKER_ENV_MANIFEST = "INSTALLED_ENVIRONMENT_MANIFEST_NOT_ESTABLISHED"
_BLOCKER_ENV_ACCEPTANCE = "INSTALLED_ENVIRONMENT_ACCEPTANCE_NOT_ESTABLISHED"
_BLOCKER_DRIVER = "SOURCE_DRIVER_BINDING_NOT_ESTABLISHED"
_BLOCKER_EXECUTABLE = "EXECUTABLE_ACCEPTANCE_NOT_ESTABLISHED"
_BLOCKER_EXECUTABLE_IDENTITY = "EXECUTABLE_IDENTITY_NOT_ADMITTED"
_BLOCKER_DESTINATION = "DESTINATION_ACCEPTANCE_NOT_ESTABLISHED"
_BLOCKER_DESTINATION_FIXTURE = "DESTINATION_FIXTURE_ONLY"
_BLOCKER_ATTEMPT_FIXTURE = "ATTEMPT_FIXTURE_ONLY"


class ExecutionAdmissionBoundaryError(ValueError):
    """Raised when a purported pre-admission record crosses the fail-closed boundary."""


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ExecutionAdmissionBoundaryError(f"{label}_INVALID")
    return value


def assess_execution_admission_blockers(
    runtime_binding: Mapping[str, Any],
    environment_manifest: Mapping[str, Any],
    source_driver_binding: Mapping[str, Any],
    executable_destination_binding: Mapping[str, Any],
) -> dict[str, object]:
    """Return unresolved admission blockers without granting execution readiness."""

    if executable_destination_binding.get("execution_allowed") is not False:
        raise ExecutionAdmissionBoundaryError("EXECUTION_ENABLED_BEFORE_ACCEPTANCE")
    if executable_destination_binding.get("outcomes_generated") is not False:
        raise ExecutionAdmissionBoundaryError("OUTCOMES_PRESENT_BEFORE_ACCEPTANCE")
    if executable_destination_binding.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        raise ExecutionAdmissionBoundaryError("READINESS_PROMOTED_BEFORE_ACCEPTANCE")
    if executable_destination_binding.get("scientific_n_increment") != 0:
        raise ExecutionAdmissionBoundaryError("SCIENTIFIC_N_CHANGED_BEFORE_ACCEPTANCE")

    blockers: list[str] = []

    if runtime_binding.get("installed_environment_manifest") == "NOT_ESTABLISHED":
        blockers.append(_BLOCKER_ENV_MANIFEST)
    if environment_manifest.get("installed_environment_acceptance") == "NOT_ESTABLISHED":
        blockers.append(_BLOCKER_ENV_ACCEPTANCE)
    if source_driver_binding.get("source_driver_binding") == "NOT_ESTABLISHED":
        blockers.append(_BLOCKER_DRIVER)
    if executable_destination_binding.get("executable_acceptance") == "NOT_ESTABLISHED":
        blockers.append(_BLOCKER_EXECUTABLE)
    if executable_destination_binding.get("destination_acceptance") == "NOT_ESTABLISHED":
        blockers.append(_BLOCKER_DESTINATION)

    executable_identity = _mapping(
        executable_destination_binding.get("executable_identity"),
        "EXECUTABLE_IDENTITY",
    )
    if executable_identity.get("kind") == "SOURCE_MODULE_PROVENANCE_ONLY":
        blockers.append(_BLOCKER_EXECUTABLE_IDENTITY)

    destination_identity = _mapping(
        executable_destination_binding.get("destination_identity"),
        "DESTINATION_IDENTITY",
    )
    if destination_identity.get("kind") == "SYNTHETIC_FIXTURE_ONLY":
        blockers.append(_BLOCKER_DESTINATION_FIXTURE)

    attempt_identity = _mapping(
        executable_destination_binding.get("attempt_identity"),
        "ATTEMPT_IDENTITY",
    )
    if attempt_identity.get("kind") == "SYNTHETIC_FIXTURE_ONLY":
        blockers.append(_BLOCKER_ATTEMPT_FIXTURE)

    return {
        "record_type": "AOSS_STAGE_A_EXECUTION_ADMISSION_BLOCKER_REPORT",
        "status": "BLOCKED" if blockers else "NO_BLOCKERS_REPORTED",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "execution_allowed": False,
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
