"""Prospective, non-collecting AOSS Stage-A runtime binding.

This module verifies only the proposed exact interpreter and direct-dependency
lock. It does not import ACP, execute a source driver, create a study attempt,
or establish collection execution readiness.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = "registry/aoss_v0_6_stage_a_runtime_binding_v1.json"
LOCK_REL = "requirements-aoss-stage-a.lock"
EXPECTED_IMPLEMENTATION = "cpython"
EXPECTED_VERSION = "3.12.0"
EXPECTED_LOCK_SHA256 = "81c1ade0b76ff38cbdcbe4ddbc615c273f02dc97a9ff055c8c2889940a2ca6bd"


class RuntimeBindingError(RuntimeError):
    """Raised when the prospective runtime binding fails closed."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        super().__init__(code if not detail else f"{code}: {detail}")


@dataclass(frozen=True)
class RuntimeFacts:
    implementation: str
    version: str
    platform_system: str
    platform_machine: str
    executable: str
    prefix: str
    base_prefix: str


def inspect_runtime_facts() -> RuntimeFacts:
    """Observe current runtime facts without importing or executing ACP."""

    return RuntimeFacts(
        implementation=sys.implementation.name,
        version=platform.python_version(),
        platform_system=platform.system(),
        platform_machine=platform.machine(),
        executable=sys.executable,
        prefix=sys.prefix,
        base_prefix=sys.base_prefix,
    )


def _sha256(path: Path) -> str:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise RuntimeBindingError("DEPENDENCY_LOCK_MISSING", str(path)) from exc
    return hashlib.sha256(data).hexdigest()


def load_runtime_contract(root: Path) -> dict[str, Any]:
    """Load the prospective runtime contract from an explicit repository root."""

    path = Path(root) / CONTRACT_REL
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RuntimeBindingError("RUNTIME_CONTRACT_MISSING", str(path)) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeBindingError("RUNTIME_CONTRACT_INVALID_JSON", str(exc)) from exc
    if not isinstance(value, dict):
        raise RuntimeBindingError("RUNTIME_CONTRACT_NOT_OBJECT")
    return value


def _validate_contract(contract: Mapping[str, Any]) -> None:
    if contract.get("record_type") != "AOSS_V0_6_STAGE_A_RUNTIME_BINDING":
        raise RuntimeBindingError("RUNTIME_CONTRACT_TYPE_MISMATCH")
    if contract.get("status") != "PROPOSED_NON_COLLECTING_RUNTIME_BINDING":
        raise RuntimeBindingError("RUNTIME_CONTRACT_STATUS_MISMATCH")
    if contract.get("controller_issue") != 901:
        raise RuntimeBindingError("RUNTIME_CONTRACT_CONTROLLER_MISMATCH")

    interpreter = contract.get("interpreter")
    if not isinstance(interpreter, dict):
        raise RuntimeBindingError("RUNTIME_INTERPRETER_CONTRACT_INVALID")
    if interpreter.get("implementation") != EXPECTED_IMPLEMENTATION:
        raise RuntimeBindingError("RUNTIME_CONTRACT_IMPLEMENTATION_DRIFT")
    if interpreter.get("version") != EXPECTED_VERSION:
        raise RuntimeBindingError("RUNTIME_CONTRACT_VERSION_DRIFT")
    if interpreter.get("historical_runtime_equivalence_claimed") is not False:
        raise RuntimeBindingError("RUNTIME_HISTORICAL_EQUIVALENCE_INVALID")

    dependency = contract.get("dependency_lock")
    if not isinstance(dependency, dict):
        raise RuntimeBindingError("DEPENDENCY_LOCK_CONTRACT_INVALID")
    if dependency.get("path") != LOCK_REL:
        raise RuntimeBindingError("DEPENDENCY_LOCK_PATH_DRIFT")
    if dependency.get("sha256") != EXPECTED_LOCK_SHA256:
        raise RuntimeBindingError("DEPENDENCY_LOCK_CONTRACT_DIGEST_DRIFT")
    if dependency.get("direct_third_party_dependencies") != []:
        raise RuntimeBindingError("DIRECT_RUNTIME_DEPENDENCY_SET_DRIFT")
    if dependency.get("acp_install_from_package_index") is not False:
        raise RuntimeBindingError("ACP_PACKAGE_INDEX_INSTALL_PROHIBITED")
    if dependency.get("acp_identity_bound_as_exact_source_checkout") is not True:
        raise RuntimeBindingError("ACP_EXACT_SOURCE_BINDING_REQUIRED")

    if contract.get("platform_binding") != "OBSERVED_NOT_ACCEPTED":
        raise RuntimeBindingError("PLATFORM_BINDING_STATUS_DRIFT")
    if contract.get("installed_environment_manifest_required_before_collection") is not True:
        raise RuntimeBindingError("INSTALLED_ENVIRONMENT_MANIFEST_REQUIREMENT_DRIFT")
    if contract.get("installed_environment_manifest") != "NOT_ESTABLISHED":
        raise RuntimeBindingError("INSTALLED_ENVIRONMENT_MANIFEST_PREMATURE")
    if contract.get("source_driver_binding") != "NOT_ESTABLISHED":
        raise RuntimeBindingError("SOURCE_DRIVER_BINDING_PREMATURE")
    if contract.get("collection_execution_readiness") != "NOT_ESTABLISHED":
        raise RuntimeBindingError("COLLECTION_READINESS_PREMATURE")
    if contract.get("outcomes_generated") is not False:
        raise RuntimeBindingError("OUTCOME_GENERATION_PREMATURE")
    if contract.get("scientific_n_increment") != 0:
        raise RuntimeBindingError("SCIENTIFIC_N_INCREMENT_INVALID")


def verify_runtime_binding(
    root: Path,
    facts: RuntimeFacts | None = None,
    *,
    contract: Mapping[str, Any] | None = None,
    lock_path: Path | None = None,
) -> dict[str, object]:
    """Verify the prospective exact runtime without promoting readiness."""

    root = Path(root)
    selected = dict(contract) if contract is not None else load_runtime_contract(root)
    _validate_contract(selected)

    actual_lock = Path(lock_path) if lock_path is not None else root / LOCK_REL
    digest = _sha256(actual_lock)
    if digest != EXPECTED_LOCK_SHA256:
        raise RuntimeBindingError(
            "DEPENDENCY_LOCK_DIGEST_MISMATCH",
            f"{digest} != {EXPECTED_LOCK_SHA256}",
        )

    observed = facts if facts is not None else inspect_runtime_facts()
    if observed.implementation != EXPECTED_IMPLEMENTATION:
        raise RuntimeBindingError(
            "RUNTIME_IMPLEMENTATION_MISMATCH",
            observed.implementation,
        )
    if observed.version != EXPECTED_VERSION:
        raise RuntimeBindingError("RUNTIME_VERSION_MISMATCH", observed.version)

    return {
        "record_type": "AOSS_STAGE_A_RUNTIME_BINDING_REPORT",
        "runtime_binding": "PASS_PROSPECTIVE_NON_COLLECTING",
        "implementation": observed.implementation,
        "version": observed.version,
        "dependency_lock_sha256": digest,
        "direct_third_party_dependencies": [],
        "platform_system": observed.platform_system,
        "platform_machine": observed.platform_machine,
        "platform_binding": "OBSERVED_NOT_ACCEPTED",
        "installed_environment_manifest": "NOT_ESTABLISHED",
        "source_driver_binding": "NOT_ESTABLISHED",
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
