"""Validate synthetic and explicitly unaccepted environment observations.

This module does not accept an installed environment, import ACP, execute a
source driver, create a study attempt, or establish collection readiness.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from scripts.aoss_stage_a.runtime_binding import RuntimeFacts, inspect_runtime_facts

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
    """Raised when a manifest is incomplete or overclaims."""


def _fail(code: str) -> None:
    raise EnvironmentManifestError(code)


def validate_synthetic_manifest(manifest: Mapping[str, Any]) -> dict[str, object]:
    """Validate one explicit fixture; never treat it as installed evidence."""

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
    return _validate_common_fields(manifest, "PASS_SYNTHETIC_FIXTURE_NON_COLLECTING")


def observe_unaccepted_environment_manifest(
    observed_at: str | None = None,
) -> dict[str, object]:
    """Observe CI runtime facts while preserving an explicit unaccepted status."""

    observed_facts = facts or inspect_runtime_facts()
    timestamp = observed_at or (datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
    return {
        "record_type": MANIFEST_CONTRACT,
        "status": "OBSERVED_NOT_ACCEPTED",
        "manifest_id": (
            f"runtime-observation-{facts.implementation}-{facts.version}-"
            f"{facts.platform_system}-{facts.platform_machine}"
        ),
        "manifest_status": "NOT_ESTABLISHED",
        "runtime_binding_record_type": "AOSS_V0_6_STAGE_A_RUNTIME_BINDING",
        "interpreter_implementation": observed_facts.implementation,
        "interpreter_version": observed_facts.version,
        "dependency_lock_sha256": EXPECTED_LOCK_SHA256,
        "platform_system": observed_facts.platform_system,
        "platform_machine": observed_facts.platform_machine,
        "environment_observed_at": timestamp,
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }


def validate_unaccepted_environment_manifest(
    manifest: Mapping[str, Any],
) -> dict[str, object]:
    """Validate an observation without upgrading it to installed evidence."""

    if manifest.get("record_type") != MANIFEST_CONTRACT:
        _fail("MANIFEST_RECORD_TYPE_MISMATCH")
    if manifest.get("status") != "OBSERVED_NOT_ACCEPTED":
        _fail("MANIFEST_STATUS_MUST_REMAIN_UNACCEPTED")
    if set(manifest) != _REQUIRED_FIELDS | {
        "record_type",
        "status",
        "manifest_status",
        "source_driver_binding",
    }:
        _fail("MANIFEST_FIELD_SET_MISMATCH")
    return _validate_common_fields(manifest, "PASS_OBSERVED_NOT_ACCEPTED")


def _validate_common_fields(
    manifest: Mapping[str, Any],
    validation_status: str,
) -> dict[str, object]:
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
        "manifest_validation": validation_status,
        "manifest_status": "NOT_ESTABLISHED",
        "platform_binding": "OBSERVED_NOT_ACCEPTED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
