"""Validate a synthetic environment-manifest shape without accepting a real environment.

This module does not inspect the host, install dependencies, import ACP, execute
a source driver, create a study attempt, or establish collection readiness.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

MANIFEST_CONTRACT = "AOSS_V0_6_STAGE_A_ENVIRONMENT_MANIFEST"
EXPECTED_INTERPRETER = "cpython"
EXPECTED_VERSION = "3.12.3"
EXPECTED_LOCK_SHA256 = "81c1ade0b76ff38cbdcbe4ddbc615c273f02dc97a9ff055c8c2889940a2ca6bd"
_REQUIRED_FIELDS = {
    "manifest_id",
    "runtime_binding_record_type",
    "interpreter_implementation",
    "interpreter_version",
    "dependency_lock_sha256",
    "platform_system",
    "platform_machine",
    "environment_observed_at",
    "collection_execution_readiness",
    "outcomes_generated",
    "scientific_n_increment",
}


class EnvironmentManifestError(ValueError):
    """Raised when a synthetic manifest is incomplete or overclaims."""


def _fail(code: str) -> None:
    raise EnvironmentManifestError(code)


def validate_synthetic_manifest(manifest: Mapping[str, Any]) -> dict[str, object]:
    """Validate one explicit fixture; never treat it as installed-environment evidence."""

    if manifest.get("record_type") != MANIFEST_CONTRACT:
        _fail("MANIFEST_RECORD_TYPE_MISMATCH")
    if manifest.get("status") != "SYNTHETIC_FIXTURE_NOT_INSTALLED_ENVIRONMENT":
        _fail("MANIFEST_STATUS_MUST_REMAIN_SYNTHETIC")
    if set(manifest) != _REQUIRED_FIELDS | {
        "record_type",
        "status",
        "manifest_status",
        "source_driver_binding",
    }:
        _fail("MANIFEST_FIELD_SET_MISMATCH")
    if manifest.get("manifest_status") != "NOT_ESTABLISHED":
        _fail("INSTALLED_MANIFEST_PREMATURE")
    if manifest.get("runtime_binding_record_type") != "AOSS_V0_6_STAGE_A_RUNTIME_BINDING":
        _fail("RUNTIME_BINDING_RECORD_MISMATCH")
    if manifest.get("interpreter_implementation") != EXPECTED_INTERPRETER:
        _fail("INTERPRETER_IMPLEMENTATION_MISMATCH")
    if manifest.get("interpreter_version") != EXPECTED_VERSION:
        _fail("INTERPRETER_VERSION_MISMATCH")
    if manifest.get("dependency_lock_sha256") != EXPECTED_LOCK_SHA256:
        _fail("DEPENDENCY_LOCK_DIGEST_MISMATCH")
    if not isinstance(manifest.get("manifest_id"), str) or not manifest["manifest_id"]:
        _fail("MANIFEST_ID_MISSING")
    if not isinstance(manifest.get("platform_system"), str) or not manifest["platform_system"]:
        _fail("PLATFORM_SYSTEM_MISSING")
    if not isinstance(manifest.get("platform_machine"), str) or not manifest["platform_machine"]:
        _fail("PLATFORM_MACHINE_MISSING")
    try:
        datetime.fromisoformat(str(manifest["environment_observed_at"]).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        _fail("ENVIRONMENT_TIMESTAMP_INVALID")
    if manifest.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        _fail("COLLECTION_READINESS_PREMATURE")
    if manifest.get("source_driver_binding") != "NOT_ESTABLISHED":
        _fail("SOURCE_DRIVER_BINDING_PREMATURE")
    if manifest.get("outcomes_generated") is not False:
        _fail("OUTCOME_GENERATION_PREMATURE")
    if manifest.get("scientific_n_increment") != 0:
        _fail("SCIENTIFIC_N_INCREMENT_INVALID")

    return {
        "record_type": "AOSS_STAGE_A_ENVIRONMENT_MANIFEST_REPORT",
        "manifest_validation": "PASS_SYNTHETIC_FIXTURE_NON_COLLECTING",
        "manifest_status": "NOT_ESTABLISHED",
        "platform_binding": "OBSERVED_NOT_ACCEPTED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
