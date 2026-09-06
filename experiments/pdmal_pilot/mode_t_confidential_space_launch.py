"""Fail-closed prelaunch contract for the bounded DGAF Mode-T admission attempt.

This validates a *planned* Google Confidential Space launch configuration before any
cloud action occurs. It does not call GCP, build an image, create a VM, grant access,
or establish P4. The real admission must later reconcile these declared values with
independently verified attestation claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SERVICE_ACCOUNT_RE = re.compile(r"^[a-z0-9][a-z0-9-]{4,28}[a-z0-9]@[a-z][a-z0-9-]{4,28}[a-z0-9]\.iam\.gserviceaccount\.com$")

REQUIRED_IMAGE_FAMILY = "confidential-space"
REQUIRED_COMPUTE_TYPE = "TDX"
REQUIRED_MAINTENANCE_POLICY = "TERMINATE"
REQUIRED_RESTART_POLICY = "Never"

REQUIRED_LAUNCH_POLICIES = {
    "tee.launch_policy.allow_capabilities": "false",
    "tee.launch_policy.allow_cgroups": "false",
    "tee.launch_policy.allow_cmd_override": "false",
    "tee.launch_policy.allow_env_override": "",
    "tee.launch_policy.allow_mount_destinations": "",
    "tee.launch_policy.log_redirect": "never",
    "tee.launch_policy.monitoring_memory_allow": "never",
}

REQUIRED_METADATA = {
    "tee-restart-policy": "Never",
    "tee-container-log-redirect": "false",
    "tee-monitoring-memory-enable": "false",
}

FORBIDDEN_METADATA_KEYS = {
    "tee-added-capabilities",
    "tee-cgroup-ns",
    "tee-cmd",
    "tee-mount",
    "tee-impersonate-service-accounts",
    "tee-install-gpu-driver",
    "ita-api-key",
    "ita-region",
}


class LaunchContractError(ValueError):
    """Raised when a proposed real-admission launch is not review-safe."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LaunchContractError(message)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} must be non-empty")
    _require("<" not in value and ">" not in value, f"{label} must not contain placeholders")
    return value


def canonical_sha256(value: Mapping[str, Any]) -> str:
    raw = json.dumps(dict(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate_launch_contract(config: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize one predeclared Confidential Space launch contract."""
    root = _mapping(config, "launch contract")
    _require(root.get("schema_version") == "dgaf-mode-t-launch-v1", "unexpected launch schema")
    _require(root.get("synthetic_admission_only") is True, "first admission must be synthetic-only")
    _require(root.get("empirical_n") == 0, "launch contract must preserve empirical N=0")

    project_id = _string(root.get("project_id"), "project_id")
    zone = _string(root.get("zone"), "zone")
    instance_name = _string(root.get("instance_name"), "instance_name")
    service_account = _string(root.get("service_account"), "service_account")
    _require(_SERVICE_ACCOUNT_RE.fullmatch(service_account) is not None, "invalid workload service account")

    candidate_sha = _string(root.get("candidate_sha"), "candidate_sha")
    _require(re.fullmatch(r"[0-9a-f]{40}", candidate_sha) is not None, "candidate_sha must be full lowercase commit SHA")
    freeze_sha = _string(root.get("freeze_sha256"), "freeze_sha256")
    _require(_SHA256_RE.fullmatch(freeze_sha) is not None, "freeze_sha256 must be lowercase SHA-256")

    image_digest = _string(root.get("workload_image_digest"), "workload_image_digest")
    _require(_IMAGE_DIGEST_RE.fullmatch(image_digest) is not None, "workload image digest must be sha256:<hex>")
    image_reference = _string(root.get("workload_image_reference"), "workload_image_reference")
    _require(
        image_reference.endswith("@" + image_digest),
        "workload image reference must be digest-pinned to workload_image_digest",
    )
    _require(":latest" not in image_reference, "mutable latest tag is forbidden")

    _require(root.get("confidential_compute_type") == REQUIRED_COMPUTE_TYPE, "first admission requires TDX")
    _require(root.get("shielded_secure_boot") is True, "Shielded Secure Boot must be enabled")
    _require(root.get("maintenance_policy") == REQUIRED_MAINTENANCE_POLICY, "maintenance policy must be TERMINATE")
    _require(root.get("confidential_space_image_family") == REQUIRED_IMAGE_FAMILY, "debug/non-production Confidential Space image is forbidden")

    metadata = dict(_mapping(root.get("metadata"), "metadata"))
    _require(metadata.get("tee-image-reference") == image_reference, "tee-image-reference must equal the digest-pinned workload image")
    for key, expected in REQUIRED_METADATA.items():
        _require(metadata.get(key) == expected, f"metadata {key} must be exactly {expected!r}")
    for key in metadata:
        _require(not key.startswith("tee-env-"), "operator environment injection metadata is forbidden")
        _require(key not in FORBIDDEN_METADATA_KEYS, f"forbidden Confidential Space metadata: {key}")
    allowed_metadata = {"tee-image-reference", *REQUIRED_METADATA.keys()}
    _require(set(metadata) == allowed_metadata, "unreviewed Confidential Space metadata key present")

    policies = dict(_mapping(root.get("launch_policies"), "launch_policies"))
    _require(policies == REQUIRED_LAUNCH_POLICIES, "launch policies must exactly match fail-closed policy set")

    _require(root.get("automatic_restart") is False, "GCE automatic restart must be disabled")
    _require(root.get("delete_on_termination") is True, "synthetic admission VM must be disposable")
    _require(root.get("container_logs_expected") is False, "container logs must remain disabled")
    _require(root.get("memory_monitoring_expected") is False, "memory monitoring must remain disabled")
    _require(root.get("operational_secret_in_metadata_or_env") is False, "operational secrets must not be supplied by metadata/env")

    normalized = {
        "schema_version": "dgaf-mode-t-launch-v1",
        "project_id": project_id,
        "zone": zone,
        "instance_name": instance_name,
        "service_account": service_account,
        "candidate_sha": candidate_sha,
        "freeze_sha256": freeze_sha,
        "workload_image_reference": image_reference,
        "workload_image_digest": image_digest,
        "confidential_compute_type": REQUIRED_COMPUTE_TYPE,
        "shielded_secure_boot": True,
        "maintenance_policy": REQUIRED_MAINTENANCE_POLICY,
        "confidential_space_image_family": REQUIRED_IMAGE_FAMILY,
        "metadata": metadata,
        "launch_policies": policies,
        "automatic_restart": False,
        "delete_on_termination": True,
        "container_logs_expected": False,
        "memory_monitoring_expected": False,
        "operational_secret_in_metadata_or_env": False,
        "synthetic_admission_only": True,
        "empirical_n": 0,
    }
    return {
        "launch_contract": "PASS_PREDECLARED_ONLY",
        "launch_contract_sha256": canonical_sha256(normalized),
        "normalized_launch": normalized,
        "real_gcp_configuration_verified": False,
        "real_confidential_space_admission": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    print(json.dumps(validate_launch_contract(config), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
