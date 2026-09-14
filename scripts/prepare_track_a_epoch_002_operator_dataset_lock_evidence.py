#!/usr/bin/env python3
"""Prepare non-secret Epoch 002 dataset-lock evidence from admitted operator bytes."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DEFAULT_RETENTION_DIR = Path.home() / "DGAF-Epoch002-Retention"
ADMISSION_RECORD_NAME = "track_a_epoch_002_operator_collection_admission.json"
EXECUTION_RECEIPT_NAME = "track_a_epoch_002_operator_execution_receipt.json"
PRE_LOCK_LEDGER_NAME = "track_a_epoch_002_pre_lock_result_ledger.json"
EVIDENCE_NAME = "track_a_epoch_002_dataset_lock_evidence.json"
AUTHORIZATION_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_EVIDENCE_PREP_FAIL: {message}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


admission = load_module(
    SCRIPTS / "validate_track_a_epoch_002_operator_collection_admission.py",
    "epoch_002_operator_admission_for_dataset_lock_evidence",
)
dataset_lock = load_module(
    SCRIPTS / "validate_track_a_epoch_002_dataset_lock.py",
    "epoch_002_dataset_lock_for_operator_evidence",
)
admission_preparer = load_module(
    SCRIPTS / "prepare_track_a_epoch_002_operator_collection_admission.py",
    "epoch_002_operator_admission_preparer_for_dataset_lock_evidence",
)
pre_lock_preparer = load_module(
    SCRIPTS / "prepare_track_a_epoch_002_operator_pre_lock_ledger.py",
    "epoch_002_pre_lock_preparer_for_dataset_lock_evidence",
)


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as exc:
        fail(f"cannot hash {path}: {exc}")


def require_external_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    root = ROOT.resolve()
    if resolved == root or root in resolved.parents:
        fail(f"{label} must remain outside the repository")
    if not resolved.is_file():
        fail(f"{label} missing: {resolved}")
    return resolved


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def require_clean_tooling() -> str:
    critical = [
        "scripts/prepare_track_a_epoch_002_operator_dataset_lock_evidence.py",
        "scripts/validate_track_a_epoch_002_dataset_lock.py",
        "docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json",
    ]
    completed = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *critical],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        fail("dataset-lock evidence tooling has uncommitted drift")
    return git("rev-parse", "HEAD")


def materialize_members(root: Path, members: dict[str, bytes]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for name, value in members.items():
        if Path(name).name != name:
            fail(f"refusing non-flat retained member {name!r}")
        (root / name).write_bytes(value)


def build_evidence(
    *,
    auth: dict[str, Any],
    admission_record: dict[str, Any],
    admission_record_sha256: str,
    ledger: list[dict[str, Any]],
    ledger_sha256: str,
    evidence_tooling_commit_sha: str,
    collection_authorization_blob_sha: str,
) -> dict[str, Any]:
    if len(ledger) != dataset_lock.PRE_LOCK_LEDGER_RECORD_COUNT:
        fail("pre-lock ledger record count drift")
    qc = ledger[-1]
    if qc.get("record_type") != "QC_LEDGER" or qc.get("status") != "PASS":
        fail("pre-lock ledger must terminate in PASS QC_LEDGER")

    public = admission_record["public_retention"]
    protected = admission_record["protected_retention"]
    evidence = {
        "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
        "schema_version": 1,
        "protocol_id": admission.PROTOCOL_ID,
        "epoch": 2,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "evidence_tooling_commit_sha": evidence_tooling_commit_sha,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "operator_admission_record_sha256": admission_record_sha256,
        "collection_execution_receipt_sha256": admission_record["collection_execution_receipt_sha256"],
        "collection_authorization_commit_sha": admission.AUTHORIZATION_SHA,
        "collection_authorization_blob_sha": collection_authorization_blob_sha,
        "frozen_candidate_sha": auth["frozen_candidate_sha"],
        "frozen_candidate_tree_sha": auth["frozen_candidate_tree_sha"],
        "custody_receipt_blob_sha": auth["custody_receipt_blob_sha"],
        "qc_ledger_record_id": qc["record_id"],
        "pre_lock_result_ledger_sha256": ledger_sha256,
        "pre_lock_result_ledger_record_count": dataset_lock.PRE_LOCK_LEDGER_RECORD_COUNT,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_artifact": {
            "name": dataset_lock.PUBLIC_ARTIFACT_NAME,
            "size_bytes": public["size_bytes"],
            "archive_sha256": public["archive_sha256"],
            "manifest_sha256": public["manifest_sha256"],
        },
        "protected_artifact": {
            "name": dataset_lock.PROTECTED_ARTIFACT_NAME,
            "size_bytes": protected["size_bytes"],
            "archive_sha256": protected["archive_sha256"],
            "ciphertext_sha256": protected["ciphertext_sha256"],
            "plaintext_tar_sha256": protected["plaintext_tar_sha256"],
            "custody_certificate_sha256": protected["custody_certificate_sha256"],
            "custody_certificate_public_key_der_sha256": protected[
                "custody_certificate_public_key_der_sha256"
            ],
        },
        "structural_qc": {
            "public_archive_digest_verified": True,
            "protected_archive_digest_verified": True,
            "all_public_sidecars_verified": True,
            "whole_epoch_manifest_verified": True,
            "exact_seed_panel_verified": True,
            "exact_matrix_counts_verified": True,
            "public_schema_allowlist_verified": True,
            "protected_ciphertext_digest_verified": True,
            "protected_plaintext_not_decrypted": True,
            "protected_mapping_not_inspected": True,
            "private_key_not_used": True,
        },
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "outcomes_inspected_for_lock": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "dataset_lock_evidence_status": "STRUCTURAL_QC_PASS_PENDING_REPOSITORY_RECEIPT",
    }
    dataset_lock.validate_evidence_object(evidence)
    return evidence


def validate_retained_bytes(
    *,
    evidence: dict[str, Any],
    ledger_path: Path,
    public_archive: Path,
    protected_archive: Path,
) -> None:
    dataset_lock.validate_pre_lock_ledger(ledger_path, evidence)
    dataset_lock.validate_archive(public_archive, evidence["public_artifact"], "public")
    dataset_lock.validate_archive(protected_archive, evidence["protected_artifact"], "protected")

    public_members = admission._tar_members(public_archive, admission.PUBLIC_NAMES, "public")
    protected_members = admission._tar_members(protected_archive, admission.PROTECTED_NAMES, "protected")
    with tempfile.TemporaryDirectory(prefix="dgaf-epoch002-dataset-lock-evidence-") as temporary:
        root = Path(temporary)
        public_root = root / "public"
        protected_root = root / "protected"
        materialize_members(public_root, public_members)
        materialize_members(protected_root, protected_members)
        dataset_lock.validate_public_root(public_root, evidence)
        dataset_lock.validate_protected_root(protected_root, evidence)


def prepare(
    *,
    retention_dir: Path,
    admission_record_path: Path | None = None,
    execution_receipt_path: Path | None = None,
    pre_lock_ledger_path: Path | None = None,
    public_archive: Path | None = None,
    protected_archive: Path | None = None,
    write: bool = False,
) -> dict[str, Any]:
    retention_dir = admission_preparer.require_external_retention_dir(retention_dir)
    admission_record_path = require_external_file(
        admission_record_path or retention_dir / ADMISSION_RECORD_NAME,
        "operator admission record",
    )
    execution_receipt_path = require_external_file(
        execution_receipt_path or retention_dir / EXECUTION_RECEIPT_NAME,
        "operator execution receipt",
    )
    pre_lock_ledger_path = require_external_file(
        pre_lock_ledger_path or retention_dir / PRE_LOCK_LEDGER_NAME,
        "pre-lock result ledger",
    )
    public_archive, protected_archive = admission_preparer.resolve_archives(
        retention_dir,
        public_archive,
        protected_archive,
    )

    admission_record = admission.load_object(admission_record_path, "operator admission record")
    admission.validate_evidence_acceptance(
        admission_record,
        execution_receipt_path,
        public_archive,
        protected_archive,
    )
    ledger = json.loads(pre_lock_ledger_path.read_text(encoding="utf-8"))
    if not isinstance(ledger, list):
        fail("pre-lock result ledger must be an array")

    auth = admission.accepted_authorization()
    evidence_tooling_commit_sha = require_clean_tooling()
    collection_authorization_blob_sha = git(
        "rev-parse",
        f"{admission.AUTHORIZATION_SHA}:{AUTHORIZATION_REL}",
    )
    evidence = build_evidence(
        auth=auth,
        admission_record=admission_record,
        admission_record_sha256=sha256_file(admission_record_path),
        ledger=ledger,
        ledger_sha256=sha256_file(pre_lock_ledger_path),
        evidence_tooling_commit_sha=evidence_tooling_commit_sha,
        collection_authorization_blob_sha=collection_authorization_blob_sha,
    )
    validate_retained_bytes(
        evidence=evidence,
        ledger_path=pre_lock_ledger_path,
        public_archive=public_archive,
        protected_archive=protected_archive,
    )

    output = retention_dir / EVIDENCE_NAME
    payload = canonical_json_bytes(evidence)
    if write:
        admission_preparer.write_new_or_identical(output, payload)
        persisted, persisted_sha = dataset_lock.validate_evidence_file(output)
        if persisted != evidence or persisted_sha != sha256_bytes(payload):
            fail("persisted dataset-lock evidence drift")
        print("TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_EVIDENCE=PASS_NONAUTHORIZING")
        print(f"DATASET_LOCK_EVIDENCE={output}")
        print(f"DATASET_LOCK_EVIDENCE_SHA256={persisted_sha}")
    else:
        print("TRACK_A_EPOCH_002_OPERATOR_DATASET_LOCK_EVIDENCE=PASS_DRY_RUN_NOT_WRITTEN")

    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retention-dir", type=Path, default=DEFAULT_RETENTION_DIR)
    parser.add_argument("--admission-record", type=Path)
    parser.add_argument("--execution-receipt", type=Path)
    parser.add_argument("--pre-lock-ledger", type=Path)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    prepare(
        retention_dir=args.retention_dir,
        admission_record_path=args.admission_record,
        execution_receipt_path=args.execution_receipt,
        pre_lock_ledger_path=args.pre_lock_ledger,
        public_archive=args.public_archive,
        protected_archive=args.protected_archive,
        write=args.write,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
