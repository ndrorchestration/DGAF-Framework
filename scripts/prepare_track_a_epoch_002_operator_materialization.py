"""Prepare the non-secret Track A Epoch 002 operator materialization bundle.

This wrapper preserves the accepted Stage-1 materializer byte-for-byte. It
loads the immutable repository contracts, invokes that accepted materializer
in an operator-controlled environment, and emits only non-secret,
content-addressed Stage-2 evidence artifacts.

PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
MATERIALIZER_REL = "scripts/materialize_track_a_epoch_002_unblinded_input.py"
MATERIALIZER_PATH = ROOT / MATERIALIZER_REL
VALIDATOR_REL = "scripts/validate_track_a_epoch_002_materialization.py"
VALIDATOR_PATH = ROOT / VALIDATOR_REL
EVIDENCE_SCHEMA_REL = "docs/experiment/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE_SCHEMA.json"
EXECUTION_RECEIPT_SCHEMA_REL = (
    "docs/experiment/TRACK_A_EPOCH_002_OPERATOR_MATERIALIZATION_EXECUTION_RECEIPT_SCHEMA.json"
)
EXECUTION_RECEIPT_SCHEMA_PATH = ROOT / EXECUTION_RECEIPT_SCHEMA_REL
DATASET_LOCK_EVIDENCE_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json"
DATASET_LOCK_RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
UNBLINDING_DECISION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_UNBLINDING_DECISION_RECORD.json"

DATASET_LOCK_COMMIT = "e7ba2fe6fc6b3587957c59231da81ae107cacab2"
UNBLINDING_DECISION_COMMIT = "bf6279b9989f211e324ff3e9012788bed95e5c84"
EVIDENCE_TOOLING_COMMIT = "84e3a9ca5af8f87f63c14b06de8aa21430542ada"
MATERIALIZER_COMMIT = "cf32a62bbf08a1b8db39709f4989be1be800d64e"
MATERIALIZER_BLOB = "3a825b026423952c2844cb18664eb6395b72fdc1"

OUTPUT_NAME = "track_a_epoch_002_unblinded_analysis_input.json"
SIDECAR_NAME = OUTPUT_NAME + ".sha256"
MANIFEST_NAME = "track_a_epoch_002_materialization_manifest.json"
EXECUTION_RECEIPT_NAME = "track_a_epoch_002_materialization_execution_receipt.json"
EVIDENCE_NAME = "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json"
BUNDLE_NAMES = (
    OUTPUT_NAME,
    SIDECAR_NAME,
    MANIFEST_NAME,
    EXECUTION_RECEIPT_NAME,
    EVIDENCE_NAME,
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"operator materialization refused: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def canonical(value: Any) -> bytes:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return (text + "\n").encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json_bytes(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        fail(f"{label} is not valid JSON: {error}")
    if not isinstance(parsed, dict):
        fail(f"{label} must be a JSON object")
    return parsed


def validate_operator_execution_receipt(receipt: dict[str, Any]) -> None:
    schema = load_json_bytes(
        EXECUTION_RECEIPT_SCHEMA_PATH.read_bytes(),
        "operator materialization execution receipt schema",
    )
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(receipt), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        fail(f"operator execution receipt schema violation at {location}: {first.message}")


def git_bytes(*arguments: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", *arguments],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        fail(f"git provenance lookup failed: {error}")
    raise AssertionError("unreachable")


def git_text(*arguments: str) -> str:
    return git_bytes(*arguments).decode("utf-8").strip()


def require_accepted_file(commit: str, relative_path: str) -> bytes:
    current = (ROOT / relative_path).read_bytes()
    accepted = git_bytes("show", f"{commit}:{relative_path}")
    require(current == accepted, f"{relative_path} drifted from its accepted commit")
    return current


def validator_bound_digest(commit: str, relative_path: str) -> str:
    validator_view = git_text("show", f"{commit}:{relative_path}").encode("utf-8")
    return digest_bytes(validator_view)


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_repository_contracts() -> dict[str, Any]:
    dataset_lock_evidence_bytes = require_accepted_file(
        DATASET_LOCK_COMMIT,
        DATASET_LOCK_EVIDENCE_REL,
    )
    dataset_lock_receipt_bytes = require_accepted_file(
        DATASET_LOCK_COMMIT,
        DATASET_LOCK_RECEIPT_REL,
    )
    unblinding_decision_bytes = require_accepted_file(
        UNBLINDING_DECISION_COMMIT,
        UNBLINDING_DECISION_REL,
    )
    require_accepted_file(EVIDENCE_TOOLING_COMMIT, EVIDENCE_SCHEMA_REL)
    require_accepted_file(EVIDENCE_TOOLING_COMMIT, VALIDATOR_REL)
    require_accepted_file(MATERIALIZER_COMMIT, MATERIALIZER_REL)

    dataset_lock_evidence = load_json_bytes(
        dataset_lock_evidence_bytes,
        "dataset-lock evidence",
    )
    dataset_lock_receipt = load_json_bytes(
        dataset_lock_receipt_bytes,
        "dataset-lock receipt",
    )
    unblinding_decision = load_json_bytes(
        unblinding_decision_bytes,
        "unblinding decision",
    )

    require(
        git_text("rev-parse", f"{MATERIALIZER_COMMIT}:{MATERIALIZER_REL}") == MATERIALIZER_BLOB,
        "accepted materializer blob identity mismatch",
    )
    require(
        git_text("merge-base", "--is-ancestor", EVIDENCE_TOOLING_COMMIT, MATERIALIZER_COMMIT) == "",
        "evidence tooling is not an ancestor of the accepted materializer",
    )

    return {
        "dataset_lock_evidence": dataset_lock_evidence,
        "dataset_lock_receipt": dataset_lock_receipt,
        "dataset_lock_receipt_sha256": validator_bound_digest(
            DATASET_LOCK_COMMIT,
            DATASET_LOCK_RECEIPT_REL,
        ),
        "dataset_lock_receipt_canonical_sha256": digest_bytes(canonical(dataset_lock_receipt)),
        "dataset_lock_commit_sha": DATASET_LOCK_COMMIT,
        "unblinding_decision": unblinding_decision,
        "unblinding_decision_sha256": validator_bound_digest(
            UNBLINDING_DECISION_COMMIT,
            UNBLINDING_DECISION_REL,
        ),
        "unblinding_decision_canonical_sha256": digest_bytes(canonical(unblinding_decision)),
        "unblinding_decision_commit_sha": UNBLINDING_DECISION_COMMIT,
        "evidence_tooling_commit_sha": EVIDENCE_TOOLING_COMMIT,
        "materializer_commit_sha": MATERIALIZER_COMMIT,
        "materializer_blob_sha": MATERIALIZER_BLOB,
    }


def build_bundle_documents(
    *,
    materialized_input: bytes,
    contracts: dict[str, Any],
    retention_id: str,
) -> dict[str, bytes]:
    materialized_input_sha256 = digest_bytes(materialized_input)
    sidecar = f"{materialized_input_sha256}  {OUTPUT_NAME}\n".encode()
    sidecar_sha256 = digest_bytes(sidecar)
    dataset_lock = contracts["dataset_lock_evidence"]
    dataset_lock_receipt = contracts["dataset_lock_receipt"]
    unblinding_decision = contracts["unblinding_decision"]

    manifest = {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_MANIFEST",
        "schema_version": 1,
        "protocol_id": PROTOCOL,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "materializer_path": MATERIALIZER_REL,
        "materializer_commit_sha": contracts["materializer_commit_sha"],
        "materializer_blob_sha": contracts["materializer_blob_sha"],
        "dataset_lock_record_id": dataset_lock_receipt["record_id"],
        "dataset_lock_commit_sha": contracts["dataset_lock_commit_sha"],
        "dataset_lock_receipt_sha256": contracts["dataset_lock_receipt_sha256"],
        "unblinding_decision_record_id": unblinding_decision["record_id"],
        "unblinding_decision_commit_sha": contracts["unblinding_decision_commit_sha"],
        "unblinding_decision_sha256": contracts["unblinding_decision_sha256"],
        "materialized_input_name": OUTPUT_NAME,
        "materialized_input_sha256": materialized_input_sha256,
        "paired_seed_units": 50,
        "record_count": 2250,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    manifest_bytes = canonical(manifest)
    manifest_sha256 = digest_bytes(manifest_bytes)

    execution_receipt = {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_MATERIALIZATION_EXECUTION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL,
        "status": "PASS",
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "materializer_path": MATERIALIZER_REL,
        "materializer_commit_sha": contracts["materializer_commit_sha"],
        "materializer_blob_sha": contracts["materializer_blob_sha"],
        "materialized_input_sha256": materialized_input_sha256,
        "materialization_manifest_sha256": manifest_sha256,
        "materialization_sidecar_sha256": sidecar_sha256,
        "paired_seed_units": 50,
        "record_count": 2250,
        "secret_material_persisted": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "repository_materialization_established": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "authorization_effect": "NONE",
    }
    execution_receipt_bytes = canonical(execution_receipt)

    evidence = {
        "record_type": "TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE",
        "schema_version": 1,
        "protocol_id": PROTOCOL,
        "epoch": 2,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "operator_execution_receipt_sha256": digest_bytes(execution_receipt_bytes),
        "evidence_tooling_commit_sha": contracts["evidence_tooling_commit_sha"],
        "materializer_path": MATERIALIZER_REL,
        "materializer_commit_sha": contracts["materializer_commit_sha"],
        "materializer_blob_sha": contracts["materializer_blob_sha"],
        "dataset_lock_record_id": dataset_lock_receipt["record_id"],
        "dataset_lock_commit_sha": contracts["dataset_lock_commit_sha"],
        "dataset_lock_receipt_sha256": contracts["dataset_lock_receipt_sha256"],
        "unblinding_decision_record_id": unblinding_decision["record_id"],
        "unblinding_decision_commit_sha": contracts["unblinding_decision_commit_sha"],
        "unblinding_decision_sha256": contracts["unblinding_decision_sha256"],
        "public_artifact": dict(dataset_lock["public_artifact"]),
        "protected_artifact": dict(dataset_lock["protected_artifact"]),
        "materialized_input_sha256": materialized_input_sha256,
        "materialization_manifest_sha256": manifest_sha256,
        "materialization_sidecar_sha256": sidecar_sha256,
        "paired_seed_units": 50,
        "record_count": 2250,
        "structure_validation": "PASS",
        "durable_retention": {
            "class": "LOCAL_CUSTODY_ARCHIVE",
            "id": retention_id,
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "secret_material_persisted": False,
        "outcome_aggregation_performed": False,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "historical_pooling_allowed": False,
        "epoch_001_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "materialization_evidence_status": ("MATERIALIZATION_PASS_PENDING_REPOSITORY_RECEIPT"),
    }
    return {
        SIDECAR_NAME: sidecar,
        MANIFEST_NAME: manifest_bytes,
        EXECUTION_RECEIPT_NAME: execution_receipt_bytes,
        EVIDENCE_NAME: canonical(evidence),
    }


def preflight_output_paths(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = [name for name in BUNDLE_NAMES if (output_dir / name).exists()]
    require(
        not existing,
        f"refusing to overwrite existing bundle path: {existing[0] if existing else ''}",
    )


def write_exclusive(path: Path, payload: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError:
        fail(f"refusing to overwrite {path.name}")


def prepare_operator_bundle(
    public_archive: Path,
    protected_archive: Path,
    custody_private_key: Path,
    output_dir: Path,
    *,
    retention_id: str,
) -> dict[str, str]:
    require(bool(retention_id.strip()), "durable retention ID is required")
    output_dir = Path(output_dir)
    preflight_output_paths(output_dir)
    contracts = load_repository_contracts()
    materializer = load_module(MATERIALIZER_PATH, "epoch002_accepted_materializer")
    validator = load_module(VALIDATOR_PATH, "epoch002_materialization_validator")

    materializer_contracts = {
        "dataset_lock_evidence": contracts["dataset_lock_evidence"],
        "dataset_lock_receipt": contracts["dataset_lock_receipt"],
        "dataset_lock_receipt_sha256": contracts["dataset_lock_receipt_canonical_sha256"],
        "unblinding_decision": contracts["unblinding_decision"],
        "unblinding_decision_sha256": contracts["unblinding_decision_canonical_sha256"],
    }
    stage_dir = Path(
        tempfile.mkdtemp(
            prefix=f".{output_dir.name}.stage-",
            dir=output_dir.parent,
        )
    )
    promoted = False
    try:
        result = materializer.materialize(
            Path(public_archive),
            Path(protected_archive),
            Path(custody_private_key),
            stage_dir,
            contracts=materializer_contracts,
        )
        output_path = stage_dir / OUTPUT_NAME
        materialized_input = output_path.read_bytes()
        require(
            result.get("materialized_input_sha256") == digest_bytes(materialized_input),
            "accepted materializer returned an inconsistent output digest",
        )

        bundle = build_bundle_documents(
            materialized_input=materialized_input,
            contracts=contracts,
            retention_id=retention_id,
        )
        execution_receipt = load_json_bytes(
            bundle[EXECUTION_RECEIPT_NAME],
            "operator materialization execution receipt",
        )
        validate_operator_execution_receipt(execution_receipt)
        evidence = load_json_bytes(bundle[EVIDENCE_NAME], "materialization evidence")
        validator.validate_evidence_against_dataset_lock(
            evidence,
            contracts["dataset_lock_evidence"],
        )
        for name, payload in bundle.items():
            write_exclusive(stage_dir / name, payload)

        staged_names = {path.name for path in stage_dir.iterdir()}
        require(
            staged_names == set(BUNDLE_NAMES),
            "staged materialization bundle member set is not exact",
        )
        digests = {
            "materialized_input_sha256": digest_bytes(materialized_input),
            "materialization_manifest_sha256": digest_bytes(bundle[MANIFEST_NAME]),
            "materialization_sidecar_sha256": digest_bytes(bundle[SIDECAR_NAME]),
            "operator_execution_receipt_sha256": digest_bytes(bundle[EXECUTION_RECEIPT_NAME]),
            "materialization_evidence_sha256": digest_bytes(bundle[EVIDENCE_NAME]),
        }

        output_dir.rmdir()
        stage_dir.replace(output_dir)
        promoted = True
        return digests
    finally:
        if not promoted:
            shutil.rmtree(stage_dir, ignore_errors=True)
            output_dir.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-archive", type=Path, required=True)
    parser.add_argument("--protected-archive", type=Path, required=True)
    parser.add_argument("--custody-private-key", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--retention-id", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = prepare_operator_bundle(
        args.public_archive,
        args.protected_archive,
        args.custody_private_key,
        args.output_dir,
        retention_id=args.retention_id,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
