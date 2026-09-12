#!/usr/bin/env python3
"""Validate non-authorizing admission of the operator-executed Epoch 002 collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/experiment/TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION_SCHEMA.json"
AUTHORIZATION_PATH = (
    ROOT
    / "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"
)
AUTHORIZATION_SHA = "563152fdb254b8ee948a693c287126a8bf8314b8"
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
PYTHON_VERSION = "3.12.3"
RUNNER_RESULT = "TRACK_A_EPOCH_002_COLLECTION_COMPLETE: 50 seeds; 2250 observations"
SEEDS = tuple(range(20270201, 20270251))
PER_SEED_RECORD_COUNT = 45
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PUBLIC_NAMES = frozenset(
    {
        "track_a_epoch_002_manifest.json",
        "track_a_epoch_002_manifest.json.sha256",
        *{
            name
            for seed in SEEDS
            for name in (
                f"track_a_epoch_002_seed_{seed}.json",
                f"track_a_epoch_002_seed_{seed}.json.sha256",
            )
        },
    }
)
PROTECTED_NAMES = frozenset(
    {
        "track_a_epoch_002_custody_cert.pem",
        "track_a_epoch_002_custody_cert.sha256",
        "track_a_epoch_002_protected.cms",
        "track_a_epoch_002_protected_ciphertext.sha256",
        "track_a_epoch_002_protected_plaintext_tar.sha256",
    }
)
RECEIPT_KEYS = frozenset(
    {
        "record_type",
        "schema_version",
        "protocol_id",
        "epoch",
        "collection_execution_class",
        "collection_authorization_commit_sha",
        "frozen_candidate_sha",
        "frozen_candidate_tree_sha",
        "python_version",
        "requirements_lock_blob_sha",
        "completion_status",
        "runner_terminal_result",
        "paired_seed_units",
        "blinded_observations",
        "outcomes_inspected_for_receipt",
        "outcome_aggregation_performed",
        "unblinding_authorized",
        "primary_analysis_authorized",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
        "high_assurance_authorized",
        "scientific_n_increment",
        "canonical_dgaf_efficacy",
    }
)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_ADMISSION_FAIL: {message}")


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def accepted_authorization() -> dict[str, Any]:
    return load_object(AUTHORIZATION_PATH, "accepted collection authorization")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def schema_only_status() -> str:
    return "TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=NOT_ADMITTED_SCHEMA_ONLY"


def validate_record(record: dict[str, Any]) -> None:
    schema = load_object(SCHEMA, "operator admission schema")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "<root>"
        fail(f"schema-invalid at {location}: {error.message}")

    forbidden = {"collection_workflow_run_id", "evidence_workflow_run_id", "artifact_id"}
    if forbidden & set(record):
        fail("operator admission must not carry GitHub Actions collection identities")
    for retention_key in ("public_retention", "protected_retention"):
        retention = record[retention_key]
        if "artifact_id" in retention:
            fail("operator retention must not carry GitHub Actions artifact IDs")

    auth = accepted_authorization()
    bindings = {
        "collection_authorization_commit_sha": AUTHORIZATION_SHA,
        "frozen_candidate_sha": auth["frozen_candidate_sha"],
        "frozen_candidate_tree_sha": auth["frozen_candidate_tree_sha"],
        "python_version": PYTHON_VERSION,
        "requirements_lock_blob_sha": auth["requirements_lock_blob_sha"],
        "custody_class": auth["custody_class"],
    }
    for field, expected in bindings.items():
        if record[field] != expected:
            fail(f"{field} drift")

    protected = record["protected_retention"]
    if protected["custody_certificate_sha256"] != auth["custody_certificate_sha256"]:
        fail("custody certificate SHA-256 drift")
    if (
        protected["custody_certificate_public_key_der_sha256"]
        != auth["custody_certificate_public_key_der_sha256"]
    ):
        fail("custody public-key fingerprint drift")


def expected_execution_receipt(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "TRACK_A_EPOCH_002_OPERATOR_EXECUTION_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "collection_execution_class": "OPERATOR_CODESPACE",
        "collection_authorization_commit_sha": AUTHORIZATION_SHA,
        "frozen_candidate_sha": record["frozen_candidate_sha"],
        "frozen_candidate_tree_sha": record["frozen_candidate_tree_sha"],
        "python_version": PYTHON_VERSION,
        "requirements_lock_blob_sha": record["requirements_lock_blob_sha"],
        "completion_status": "COMPLETE",
        "runner_terminal_result": RUNNER_RESULT,
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


def validate_execution_receipt(record: dict[str, Any], receipt_path: Path) -> None:
    if not receipt_path.is_file():
        fail("execution receipt missing")
    raw = receipt_path.read_bytes()
    if sha256_bytes(raw) != record["collection_execution_receipt_sha256"]:
        fail("execution receipt SHA-256 mismatch")
    receipt = load_object(receipt_path, "operator execution receipt")
    if set(receipt) != set(RECEIPT_KEYS):
        fail("execution receipt field allowlist drift")
    if receipt != expected_execution_receipt(record):
        fail("execution receipt identity/completion binding drift")


def _tar_members(path: Path, allowed: frozenset[str], label: str) -> dict[str, bytes]:
    if not path.is_file():
        fail(f"{label} archive missing")
    values: dict[str, bytes] = {}
    try:
        with tarfile.open(path, "r:") as archive:
            for member in archive.getmembers():
                normalized = member.name.removeprefix("./")
                if normalized in ("", "."):
                    if member.isdir():
                        continue
                    fail(f"{label} archive has malformed root member")
                if not member.isfile() or member.issym() or member.islnk():
                    fail(f"{label} archive contains non-regular member {member.name!r}")
                if normalized not in allowed:
                    fail(f"{label} archive contains forbidden member {normalized!r}")
                if normalized in values:
                    fail(f"{label} archive contains duplicate member {normalized!r}")
                stream = archive.extractfile(member)
                if stream is None:
                    fail(f"cannot read {label} member {normalized!r}")
                values[normalized] = stream.read()
    except (OSError, tarfile.TarError) as exc:
        fail(f"cannot read {label} archive: {exc}")
    if set(values) != set(allowed):
        fail(
            f"{label} archive member-set mismatch: "
            f"missing={sorted(set(allowed) - set(values))} "
            f"extra={sorted(set(values) - set(allowed))}"
        )
    return values


def _read_sidecar_bytes(value: bytes, expected_name: str, label: str) -> str:
    try:
        lines = value.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"{label} sidecar is not UTF-8: {exc}")
    if len(lines) != 1:
        fail(f"{label} sidecar must contain exactly one line")
    parts = lines[0].split()
    if len(parts) != 2 or parts[1] != expected_name or not HEX64.fullmatch(parts[0]):
        fail(f"{label} sidecar binding malformed")
    return parts[0]


def validate_public_archive_members(path: Path, record: dict[str, Any]) -> None:
    values = _tar_members(path, PUBLIC_NAMES, "public")
    spec = record["public_retention"]
    if path.stat().st_size != spec["size_bytes"] or sha256_file(path) != spec["archive_sha256"]:
        fail("public archive outer identity mismatch")

    manifest_name = "track_a_epoch_002_manifest.json"
    manifest_bytes = values[manifest_name]
    manifest_digest = sha256_bytes(manifest_bytes)
    if manifest_digest != spec["manifest_sha256"]:
        fail("public manifest SHA-256 mismatch")
    if (
        _read_sidecar_bytes(
            values[manifest_name + ".sha256"], manifest_name, "public manifest"
        )
        != manifest_digest
    ):
        fail("public manifest sidecar mismatch")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"public manifest invalid: {exc}")
    if not isinstance(manifest, dict):
        fail("public manifest must be an object")
    auth = accepted_authorization()
    if manifest.get("protocol_id") != PROTOCOL_ID:
        fail("public manifest protocol drift")
    if manifest.get("frozen_candidate_sha") != auth["frozen_candidate_sha"]:
        fail("public manifest candidate drift")
    if manifest.get("seed_count") != 50 or manifest.get("expected_observations") != 2250:
        fail("public manifest collection-size drift")
    if manifest.get("custody_receipt_blob_sha") != auth["custody_receipt_blob_sha"]:
        fail("public manifest custody receipt drift")
    if manifest.get("custody_certificate_sha256") != auth["custody_certificate_sha256"]:
        fail("public manifest custody certificate drift")
    if (
        manifest.get("custody_certificate_public_key_der_sha256")
        != auth["custody_certificate_public_key_der_sha256"]
    ):
        fail("public manifest custody public-key drift")
    for field in (
        "outcomes_inspected_by_collection_workflow",
        "outcome_aggregation_performed",
        "unblinding_authorized",
        "primary_analysis_authorized",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
    ):
        if manifest.get(field) is not False:
            fail(f"public manifest must keep {field}=false")

    rows = manifest.get("rows")
    if not isinstance(rows, list) or len(rows) != 50:
        fail("public manifest must contain exactly 50 rows")
    if [row.get("seed_id") for row in rows if isinstance(row, dict)] != list(SEEDS):
        fail("public manifest seed panel drift")
    for row in rows:
        if not isinstance(row, dict):
            fail("public manifest row must be an object")
        seed = row.get("seed_id")
        if row.get("record_count") != PER_SEED_RECORD_COUNT:
            fail(f"public seed {seed} record-count drift")
        protected_digest = row.get("protected_mapping_sha256")
        if not isinstance(protected_digest, str) or not HEX64.fullmatch(protected_digest):
            fail(f"public seed {seed} protected commitment malformed")
        seed_name = f"track_a_epoch_002_seed_{seed}.json"
        seed_digest = sha256_bytes(values[seed_name])
        if row.get("public_dataset_sha256") != seed_digest:
            fail(f"public seed {seed} manifest digest mismatch")
        sidecar_digest = _read_sidecar_bytes(
            values[seed_name + ".sha256"], seed_name, f"public seed {seed}"
        )
        if sidecar_digest != seed_digest:
            fail(f"public seed {seed} sidecar mismatch")


def validate_protected_archive_members(path: Path, record: dict[str, Any]) -> None:
    values = _tar_members(path, PROTECTED_NAMES, "protected")
    spec = record["protected_retention"]
    if path.stat().st_size != spec["size_bytes"] or sha256_file(path) != spec["archive_sha256"]:
        fail("protected archive outer identity mismatch")

    cert_name = "track_a_epoch_002_custody_cert.pem"
    cert_digest = sha256_bytes(values[cert_name])
    cert_sidecar = _read_sidecar_bytes(
        values["track_a_epoch_002_custody_cert.sha256"], cert_name, "custody certificate"
    )
    if cert_digest != cert_sidecar or cert_digest != spec["custody_certificate_sha256"]:
        fail("protected custody certificate digest mismatch")

    cipher_name = "track_a_epoch_002_protected.cms"
    cipher_digest = sha256_bytes(values[cipher_name])
    cipher_sidecar = _read_sidecar_bytes(
        values["track_a_epoch_002_protected_ciphertext.sha256"],
        cipher_name,
        "protected ciphertext",
    )
    if cipher_digest != cipher_sidecar or cipher_digest != spec["ciphertext_sha256"]:
        fail("protected ciphertext digest mismatch")

    plaintext_commitment = _read_sidecar_bytes(
        values["track_a_epoch_002_protected_plaintext_tar.sha256"],
        "track_a_epoch_002_protected.tar",
        "protected plaintext commitment",
    )
    if plaintext_commitment != spec["plaintext_tar_sha256"]:
        fail("protected plaintext-tar commitment mismatch")


def validate_archives(
    record: dict[str, Any],
    public_archive: Path,
    protected_archive: Path,
) -> None:
    validate_public_archive_members(public_archive, record)
    validate_protected_archive_members(protected_archive, record)


def validate_evidence_acceptance(
    record: dict[str, Any],
    receipt_path: Path | None,
    public_archive: Path | None,
    protected_archive: Path | None,
) -> None:
    validate_record(record)
    if receipt_path is None or public_archive is None or protected_archive is None:
        fail("evidence acceptance requires execution receipt and both retained archives")
    validate_execution_receipt(record, receipt_path)
    validate_archives(record, public_archive, protected_archive)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--execution-receipt", type=Path)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    args = parser.parse_args()

    record = load_object(args.record, "operator admission record")
    if args.schema_only:
        if any(
            value is not None
            for value in (args.execution_receipt, args.public_archive, args.protected_archive)
        ):
            fail("--schema-only cannot be combined with evidence inputs")
        validate_record(record)
        print(schema_only_status())
    else:
        validate_evidence_acceptance(
            record,
            args.execution_receipt,
            args.public_archive,
            args.protected_archive,
        )
        print("TRACK_A_EPOCH_002_OPERATOR_COLLECTION_ADMISSION=PASS_NONAUTHORIZING")

    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
