#!/usr/bin/env python3
"""Prepare and validate non-authorizing admission of retained Epoch 002 operator evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_operator_collection_admission.py"
DEFAULT_RETENTION_DIR = Path.home() / "DGAF-Epoch002-Retention"
EXECUTION_RECEIPT_NAME = "track_a_epoch_002_operator_execution_receipt.json"
ADMISSION_RECORD_NAME = "track_a_epoch_002_operator_collection_admission.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_ADMISSION_PREP_FAIL: {message}")


def load_admission_validator() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_epoch_002_operator_admission", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        fail("operator admission validator cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


admission = load_admission_validator()


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as exc:
        fail(f"cannot hash {path}: {exc}")


def _inside_repository(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def require_external_retention_dir(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if _inside_repository(resolved):
        fail("retention/output directory must remain outside the repository")
    if not resolved.is_dir():
        fail(f"retention directory missing: {resolved}")
    return resolved


def require_external_archive(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if _inside_repository(resolved):
        fail(f"{label} archive must remain outside the repository")
    if not resolved.is_file():
        fail(f"{label} archive missing: {resolved}")
    return resolved


def archive_member_names(path: Path) -> frozenset[str] | None:
    if not path.is_file():
        return None
    try:
        with tarfile.open(path, "r:") as archive:
            names: set[str] = set()
            for member in archive.getmembers():
                normalized = member.name.removeprefix("./")
                if normalized in ("", ".") and member.isdir():
                    continue
                names.add(normalized)
            return frozenset(names)
    except (OSError, tarfile.TarError):
        return None


def classify_archive(path: Path) -> str | None:
    names = archive_member_names(path)
    if names == admission.PUBLIC_NAMES:
        return "public"
    if names == admission.PROTECTED_NAMES:
        return "protected"
    return None


def discover_archives(retention_dir: Path) -> tuple[Path, Path]:
    retention_dir = require_external_retention_dir(retention_dir)
    public: list[Path] = []
    protected: list[Path] = []
    for path in sorted(retention_dir.iterdir()):
        kind = classify_archive(path)
        if kind == "public":
            public.append(path)
        elif kind == "protected":
            protected.append(path)
    if len(public) != 1:
        fail(f"expected exactly one public archive by member set; found {[str(path) for path in public]}")
    if len(protected) != 1:
        fail(f"expected exactly one protected archive by member set; found {[str(path) for path in protected]}")
    return public[0], protected[0]


def build_execution_receipt(auth: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_EXECUTION_RECEIPT",
        "schema_version": 1,
        "protocol_id": admission.PROTOCOL_ID,
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": admission.AUTHORIZATION_SHA,
        "frozen_candidate_sha": auth["frozen_candidate_sha"],
        "frozen_candidate_tree_sha": auth["frozen_candidate_tree_sha"],
        "python_version": admission.PYTHON_VERSION,
        "requirements_lock_blob_sha": auth["requirements_lock_blob_sha"],
        "completion_status": "COMPLETE",
        "runner_terminal_result": admission.RUNNER_RESULT,
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "outcomes_inspected_for_receipt": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def build_admission_record(
    *,
    auth: dict[str, Any],
    receipt_bytes: bytes,
    public_archive: Path,
    protected_archive: Path,
) -> dict[str, Any]:
    public_members = admission._tar_members(public_archive, admission.PUBLIC_NAMES, "public")
    protected_members = admission._tar_members(protected_archive, admission.PROTECTED_NAMES, "protected")

    manifest_bytes = public_members["track_a_epoch_002_manifest.json"]
    cert_bytes = protected_members["track_a_epoch_002_custody_cert.pem"]
    ciphertext_bytes = protected_members["track_a_epoch_002_protected.cms"]
    plaintext_commitment = admission._read_sidecar_bytes(
        protected_members["track_a_epoch_002_protected_plaintext_tar.sha256"],
        "track_a_epoch_002_protected.tar",
        "protected plaintext commitment",
    )

    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION",
        "schema_version": 1,
        "protocol_id": admission.PROTOCOL_ID,
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": admission.AUTHORIZATION_SHA,
        "frozen_candidate_sha": auth["frozen_candidate_sha"],
        "frozen_candidate_tree_sha": auth["frozen_candidate_tree_sha"],
        "python_version": admission.PYTHON_VERSION,
        "requirements_lock_blob_sha": auth["requirements_lock_blob_sha"],
        "collection_execution_receipt_sha256": sha256_bytes(receipt_bytes),
        "paired_seed_units": 50,
        "blinded_observations": 2250,
        "public_retention": {
            "name": "track-a-epoch-002-public-blinded",
            "size_bytes": public_archive.stat().st_size,
            "archive_sha256": sha256_file(public_archive),
            "manifest_sha256": sha256_bytes(manifest_bytes),
        },
        "protected_retention": {
            "name": "track-a-epoch-002-protected-encrypted",
            "size_bytes": protected_archive.stat().st_size,
            "archive_sha256": sha256_file(protected_archive),
            "ciphertext_sha256": sha256_bytes(ciphertext_bytes),
            "plaintext_tar_sha256": plaintext_commitment,
            "custody_certificate_sha256": sha256_bytes(cert_bytes),
            "custody_certificate_public_key_der_sha256": auth[
                "custody_certificate_public_key_der_sha256"
            ],
        },
        "custody_class": auth["custody_class"],
        "independent_custody": False,
        "outcomes_inspected_for_admission": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "admission_status": "CONTENT_ADDRESSED_PENDING_DATASET_LOCK",
    }


def write_new_or_identical(path: Path, content: bytes) -> None:
    if path.exists():
        try:
            existing = path.read_bytes()
        except OSError as exc:
            fail(f"cannot read existing output {path}: {exc}")
        if existing != content:
            fail(f"refusing to overwrite different bytes at {path}")
        return
    try:
        path.write_bytes(content)
    except OSError as exc:
        fail(f"cannot write {path}: {exc}")


def resolve_archives(
    retention_dir: Path,
    public_archive: Path | None,
    protected_archive: Path | None,
) -> tuple[Path, Path]:
    if public_archive is None or protected_archive is None:
        discovered_public, discovered_protected = discover_archives(retention_dir)
        public_archive = public_archive or discovered_public
        protected_archive = protected_archive or discovered_protected
    public_archive = require_external_archive(public_archive, "public")
    protected_archive = require_external_archive(protected_archive, "protected")
    return public_archive, protected_archive


def prepare(
    *,
    retention_dir: Path,
    public_archive: Path | None = None,
    protected_archive: Path | None = None,
    write: bool = False,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    retention_dir = require_external_retention_dir(retention_dir)
    public_archive, protected_archive = resolve_archives(retention_dir, public_archive, protected_archive)
    auth = admission.accepted_authorization()
    receipt = build_execution_receipt(auth)
    receipt_bytes = canonical_json_bytes(receipt)
    record = build_admission_record(
        auth=auth,
        receipt_bytes=receipt_bytes,
        public_archive=public_archive,
        protected_archive=protected_archive,
    )
    admission.validate_record(record)

    if write:
        receipt_path = retention_dir / EXECUTION_RECEIPT_NAME
        record_path = retention_dir / ADMISSION_RECORD_NAME
        write_new_or_identical(receipt_path, receipt_bytes)
        write_new_or_identical(record_path, canonical_json_bytes(record))
        admission.validate_evidence_acceptance(
            record,
            receipt_path,
            public_archive,
            protected_archive,
        )
        print("TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=PASS_NONAUTHORIZING")
        print(f"EXECUTION_RECEIPT={receipt_path}")
        print(f"ADMISSION_RECORD={record_path}")
    else:
        with tempfile.TemporaryDirectory(prefix="dgaf-epoch002-admission-") as temporary:
            receipt_path = Path(temporary) / EXECUTION_RECEIPT_NAME
            receipt_path.write_bytes(receipt_bytes)
            admission.validate_evidence_acceptance(
                record,
                receipt_path,
                public_archive,
                protected_archive,
            )
        print("TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=PASS_DRY_RUN_NOT_WRITTEN")

    print(f"PUBLIC_ARCHIVE={public_archive}")
    print(f"PROTECTED_ARCHIVE={protected_archive}")
    print(f"EXECUTION_RECEIPT_SHA256={record['collection_execution_receipt_sha256']}")
    print(f"PUBLIC_ARCHIVE_SHA256={record['public_retention']['archive_sha256']}")
    print(f"PROTECTED_ARCHIVE_SHA256={record['protected_retention']['archive_sha256']}")
    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return receipt, record, public_archive, protected_archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retention-dir", type=Path, default=DEFAULT_RETENTION_DIR)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    prepare(
        retention_dir=args.retention_dir,
        public_archive=args.public_archive,
        protected_archive=args.protected_archive,
        write=args.write,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
