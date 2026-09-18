#!/usr/bin/env python3
"""Local fail-closed operator bridge for Track A Epoch 002 materialization.

This process is intentionally local-only and exposes no network listener.
It accepts one JSON request per invocation and returns one sanitized JSON response.

Supported actions:
- status
- verify_inputs
- materialize
- get_evidence

Secret-bearing paths are read only from local environment variables and are never
returned in responses.

PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, NoReturn

from prepare_track_a_epoch_002_operator_materialization import (
    EVIDENCE_NAME,
    prepare_operator_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET_LOCK_EVIDENCE_PATH = ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json"
PRIMARY_ANALYSIS_AUTH_PATH = (
    ROOT / "docs/experiment/track_a_runs/" "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json"
)
LOCKED_ANALYSIS_RESULT_PATH = (
    ROOT / "docs/experiment/track_a_runs/" "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
)

ENV_PUBLIC = "DGAF_PUBLIC_ARCHIVE"
ENV_PROTECTED = "DGAF_PROTECTED_ARCHIVE"
ENV_KEY = "DGAF_CUSTODY_PRIVATE_KEY"
ENV_OUTPUT = "DGAF_MATERIALIZATION_OUTPUT_DIR"
ENV_RETENTION = "DGAF_RETENTION_ID"

ALLOWED_ACTIONS = {"status", "verify_inputs", "materialize", "get_evidence"}

SENSITIVE_TOKENS = (
    "private_key",
    "passphrase",
    "protected_plaintext",
    "decrypted_mapping",
    "secret_material",
)


class BridgeRefusal(RuntimeError):
    pass


def refuse(message: str) -> NoReturn:
    raise BridgeRefusal(message)


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        refuse(f"{label} is absent")
    except json.JSONDecodeError as exc:
        refuse(f"{label} is invalid JSON: {exc}")
    if not isinstance(value, dict):
        refuse(f"{label} must be a JSON object")
    return value


def configured_path(name: str) -> Path:
    raw = os.environ.get(name, "").strip()
    if not raw:
        refuse(f"required local environment variable is unset: {name}")
    return Path(raw).expanduser().resolve()


def configured_retention_id() -> str:
    value = os.environ.get(ENV_RETENTION, "").strip()
    if not value:
        refuse(f"required local environment variable is unset: {ENV_RETENTION}")
    lowered = value.lower()
    if any(token in lowered for token in SENSITIVE_TOKENS):
        refuse("retention ID appears to contain prohibited secret-bearing text")
    return value


def outside_repository(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return True
    return False


def require_regular_external_file(path: Path, label: str) -> None:
    if path.is_symlink():
        refuse(f"{label} must not be a symlink")
    if not path.is_file():
        refuse(f"{label} is not a regular file")
    if not outside_repository(path):
        refuse(f"{label} must remain outside the repository")


def require_external_output_dir(path: Path) -> None:
    if not outside_repository(path):
        refuse("materialization output directory must remain outside the repository")
    if path.exists() and path.is_symlink():
        refuse("materialization output directory must not be a symlink")


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def locked_artifact_contracts() -> tuple[dict[str, Any], dict[str, Any]]:
    record = load_json(DATASET_LOCK_EVIDENCE_PATH, "dataset-lock evidence")
    public = record.get("public_artifact")
    protected = record.get("protected_artifact")
    if not isinstance(public, dict) or not isinstance(protected, dict):
        refuse("dataset-lock evidence is missing artifact contracts")
    return public, protected


def verify_artifact(path: Path, contract: dict[str, Any], label: str) -> dict[str, Any]:
    require_regular_external_file(path, label)
    expected_size = contract.get("size_bytes")
    expected_sha = contract.get("archive_sha256")
    if not isinstance(expected_size, int) or not isinstance(expected_sha, str):
        refuse(f"{label} contract is malformed")
    actual_size = path.stat().st_size
    if actual_size != expected_size:
        refuse(f"{label} size mismatch")
    actual_sha = sha256_file(path)
    if actual_sha != expected_sha:
        refuse(f"{label} digest mismatch")
    return {"size_bytes": actual_size, "sha256": actual_sha, "verified": True}


def resolve_configuration() -> dict[str, Any]:
    public = configured_path(ENV_PUBLIC)
    protected = configured_path(ENV_PROTECTED)
    key = configured_path(ENV_KEY)
    output = configured_path(ENV_OUTPUT)
    retention_id = configured_retention_id()

    public_contract, protected_contract = locked_artifact_contracts()
    public_status = verify_artifact(public, public_contract, "public archive")
    protected_status = verify_artifact(protected, protected_contract, "protected archive")
    require_regular_external_file(key, "custody private key")
    require_external_output_dir(output)

    return {
        "public": public,
        "protected": protected,
        "key": key,
        "output": output,
        "retention_id": retention_id,
        "public_status": public_status,
        "protected_status": protected_status,
    }


def status_response() -> dict[str, Any]:
    return {
        "bridge": "DGAF_LOCAL_OPERATOR_BRIDGE",
        "schema_version": 1,
        "execution_class": "LOCAL_OPERATOR_ONLY",
        "network_listener": False,
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "primary_analysis_authorized": PRIMARY_ANALYSIS_AUTH_PATH.exists(),
        "primary_analysis_result_present": LOCKED_ANALYSIS_RESULT_PATH.exists(),
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def verify_inputs_response() -> dict[str, Any]:
    config = resolve_configuration()
    return {
        "bridge": "DGAF_LOCAL_OPERATOR_BRIDGE",
        "action": "verify_inputs",
        "status": "PASS",
        "public_artifact": config["public_status"],
        "protected_artifact": config["protected_status"],
        "custody_private_key_present": True,
        "output_directory_external": True,
        "retention_id_present": True,
        "secret_material_returned": False,
        "primary_analysis_run": False,
    }


def materialize_response() -> dict[str, Any]:
    config = resolve_configuration()
    digests = prepare_operator_bundle(
        config["public"],
        config["protected"],
        config["key"],
        config["output"],
        retention_id=config["retention_id"],
    )
    return {
        "bridge": "DGAF_LOCAL_OPERATOR_BRIDGE",
        "action": "materialize",
        "status": "PASS",
        "bundle_member_count": 5,
        "evidence_filename": EVIDENCE_NAME,
        "digests": digests,
        "secret_material_returned": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "next_governed_event": "MATERIALIZATION_EVIDENCE_ADMISSION",
    }


def get_evidence_response() -> dict[str, Any]:
    output = configured_path(ENV_OUTPUT)
    require_external_output_dir(output)
    evidence_path = output / EVIDENCE_NAME
    evidence = load_json(evidence_path, "materialization evidence")

    serialized = json.dumps(evidence, sort_keys=True).lower()
    for token in SENSITIVE_TOKENS:
        if token in serialized:
            refuse("materialization evidence contains prohibited secret-bearing text")

    if evidence.get("primary_analysis_authorized") is not False:
        refuse("evidence does not preserve primary-analysis non-authorization")
    if evidence.get("primary_analysis_run") is not False:
        refuse("evidence does not preserve primary-analysis non-execution")
    if evidence.get("scientific_n_increment") != 0:
        refuse("evidence does not preserve scientific N")

    return {
        "bridge": "DGAF_LOCAL_OPERATOR_BRIDGE",
        "action": "get_evidence",
        "status": "PASS",
        "evidence": evidence,
        "evidence_sha256": sha256_file(evidence_path),
        "secret_material_returned": False,
    }


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action")
    if action not in ALLOWED_ACTIONS:
        refuse("unsupported action")
    if set(request) != {"action"}:
        refuse("requests may contain only the action field")

    if action == "status":
        return status_response()
    if action == "verify_inputs":
        return verify_inputs_response()
    if action == "materialize":
        return materialize_response()
    if action == "get_evidence":
        return get_evidence_response()
    refuse("unsupported action")


def main() -> int:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            refuse("request must be a JSON object")
        response = dispatch(request)
    except (BridgeRefusal, json.JSONDecodeError) as exc:
        response = {
            "bridge": "DGAF_LOCAL_OPERATOR_BRIDGE",
            "status": "REFUSED",
            "reason": str(exc),
            "secret_material_returned": False,
            "primary_analysis_run": False,
        }
        print(json.dumps(response, sort_keys=True))
        return 2

    print(json.dumps(response, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
