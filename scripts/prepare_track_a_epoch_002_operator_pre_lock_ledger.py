#!/usr/bin/env python3
"""Prepare a retrospective, non-authorizing Epoch 002 pre-lock result ledger."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NamedTuple, NoReturn

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DEFAULT_RETENTION_DIR = Path.home() / "DGAF-Epoch002-Retention"
PRE_LOCK_LEDGER_NAME = "track_a_epoch_002_pre_lock_result_ledger.json"
ADMISSION_RECORD_NAME = "track_a_epoch_002_operator_collection_admission.json"
EXECUTION_RECEIPT_NAME = "track_a_epoch_002_operator_execution_receipt.json"
PRODUCER_SYSTEM = "DGAF_TRACK_A_EPOCH_002_OPERATOR_PRE_LOCK_LEDGER_PREPARER"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_OPERATOR_PRE_LOCK_LEDGER_PREP_FAIL: {message}")


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
    "epoch_002_operator_admission_validator",
)
dataset_lock = load_module(
    SCRIPTS / "validate_track_a_epoch_002_dataset_lock.py",
    "epoch_002_dataset_lock_validator_for_pre_lock",
)
operator_admission_preparer = load_module(
    SCRIPTS / "prepare_track_a_epoch_002_operator_collection_admission.py",
    "epoch_002_operator_admission_preparer_for_pre_lock",
)
structural_ledger = load_module(
    SCRIPTS / "validate_track_a_epoch_002_result_ledger.py",
    "epoch_002_result_ledger_validator_for_pre_lock",
)
semantic_ledger = load_module(
    SCRIPTS / "validate_track_a_epoch_002_result_record_semantics.py",
    "epoch_002_result_semantics_validator_for_pre_lock",
)


class OperatorInputs(NamedTuple):
    admission_record_path: Path
    execution_receipt_path: Path
    public_archive: Path
    protected_archive: Path


class RetainedEvidence(NamedTuple):
    auth: dict[str, Any]
    admission_record: dict[str, Any]
    admission_record_sha256: str
    seed_digests: dict[int, str]


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _inside_repository(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def require_external_retention_dir(path: Path) -> Path:
    return operator_admission_preparer.require_external_retention_dir(path)


def require_external_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if _inside_repository(resolved):
        fail(f"{label} must remain outside the repository")
    if not resolved.is_file():
        fail(f"{label} missing: {resolved}")
    return resolved


def write_new_or_identical(path: Path, content: bytes) -> None:
    operator_admission_preparer.write_new_or_identical(path, content)


def resolve_inputs(
    *,
    retention_dir: Path,
    admission_record_path: Path | None = None,
    execution_receipt_path: Path | None = None,
    public_archive: Path | None = None,
    protected_archive: Path | None = None,
) -> OperatorInputs:
    retention_dir = require_external_retention_dir(retention_dir)
    admission_record_path = admission_record_path or retention_dir / ADMISSION_RECORD_NAME
    execution_receipt_path = execution_receipt_path or retention_dir / EXECUTION_RECEIPT_NAME
    public_archive, protected_archive = operator_admission_preparer.resolve_archives(
        retention_dir,
        public_archive,
        protected_archive,
    )
    return OperatorInputs(
        admission_record_path=require_external_file(admission_record_path, "operator admission record"),
        execution_receipt_path=require_external_file(execution_receipt_path, "operator execution receipt"),
        public_archive=require_external_file(public_archive, "public retained archive"),
        protected_archive=require_external_file(protected_archive, "protected retained archive"),
    )


def seed_digests_from_public_members(members: dict[str, bytes]) -> dict[int, str]:
    digests: dict[int, str] = {}
    for seed in admission.SEEDS:
        name = f"track_a_epoch_002_seed_{seed}.json"
        sidecar_name = f"{name}.sha256"
        if name not in members or sidecar_name not in members:
            fail(f"seed digest panel missing retained bytes for seed {seed}")
        digest = sha256_bytes(members[name])
        sidecar_digest = admission._read_sidecar_bytes(
            members[sidecar_name],
            name,
            f"public seed {seed}",
        )
        if sidecar_digest != digest:
            fail(f"public seed {seed} sidecar digest mismatch")
        digests[seed] = digest
    return digests


def validate_and_load_retained_evidence(inputs: OperatorInputs) -> RetainedEvidence:
    record = admission.load_object(inputs.admission_record_path, "operator admission record")
    admission.validate_evidence_acceptance(
        record,
        inputs.execution_receipt_path,
        inputs.public_archive,
        inputs.protected_archive,
    )
    public_members = admission._tar_members(inputs.public_archive, admission.PUBLIC_NAMES, "public")
    return RetainedEvidence(
        auth=admission.accepted_authorization(),
        admission_record=record,
        admission_record_sha256=sha256_bytes(inputs.admission_record_path.read_bytes()),
        seed_digests=seed_digests_from_public_members(public_members),
    )


def _base_record(
    *,
    record_type: str,
    record_id: str,
    generated_at_utc: str,
    producer_commit: str,
    immutable_subject: dict[str, Any],
    evidence_scope: str,
    predecessor_record_ids: list[str],
) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema_version": 1,
        "protocol_id": admission.PROTOCOL_ID,
        "epoch": 2,
        "record_id": record_id,
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": PRODUCER_SYSTEM,
            "version_or_commit": producer_commit,
        },
        "immutable_subject": immutable_subject,
        "evidence_scope": evidence_scope,
        "non_effects": list(dataset_lock.FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": predecessor_record_ids,
        "authorization_effect": "NONE",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def build_pre_lock_ledger(
    *,
    auth: dict[str, Any],
    admission_record: dict[str, Any],
    admission_record_sha256: str,
    seed_digests: dict[int, str],
    generated_at_utc: str,
    producer_commit: str,
) -> list[dict[str, Any]]:
    expected_seeds = set(admission.SEEDS)
    if set(seed_digests) != expected_seeds:
        fail(
            "seed digest panel must contain exactly the authorized 50 seeds; "
            f"missing={sorted(expected_seeds - set(seed_digests))} "
            f"extra={sorted(set(seed_digests) - expected_seeds)}"
        )
    for seed, digest in seed_digests.items():
        if not isinstance(digest, str) or not admission.HEX64.fullmatch(digest):
            fail(f"seed digest panel contains malformed SHA-256 for seed {seed}")
    if not admission.HEX64.fullmatch(admission_record_sha256):
        fail("admission record SHA-256 malformed")

    records: list[dict[str, Any]] = []

    def append(
        record_type: str,
        record_id: str,
        immutable_subject: dict[str, Any],
        evidence_scope: str,
    ) -> None:
        predecessor = [] if not records else [records[-1]["record_id"]]
        records.append(
            _base_record(
                record_type=record_type,
                record_id=record_id,
                generated_at_utc=generated_at_utc,
                producer_commit=producer_commit,
                immutable_subject=immutable_subject,
                evidence_scope=evidence_scope,
                predecessor_record_ids=predecessor,
            )
        )

    append(
        "PRECOLLECTION_GATE_CHECKLIST",
        "E002:GATE:RETROSPECTIVE_OPERATOR",
        {
            "commit_sha": auth["frozen_candidate_sha"],
            "tree_sha": auth["frozen_candidate_tree_sha"],
        },
        "RETROSPECTIVE_OPERATOR_CONTENT_ADDRESSED_RECONSTRUCTION_OF_ACCEPTED_COLLECTION_GATE_BINDINGS",
    )
    append(
        "COLLECTION_START_RECEIPT",
        "E002:START:RETROSPECTIVE_OPERATOR",
        {
            "commit_sha": admission.AUTHORIZATION_SHA,
            "sha256": admission_record["collection_execution_receipt_sha256"],
        },
        "RETROSPECTIVE_OPERATOR_CONTENT_ADDRESSED_BINDING_TO_COMPLETED_AUTHORIZED_COLLECTION_RECEIPT",
    )
    for seed in admission.SEEDS:
        append(
            "PER_SEED_EXECUTION_RECORD",
            f"E002:SEED:{seed}:RETROSPECTIVE_OPERATOR",
            {
                "commit_sha": auth["frozen_candidate_sha"],
                "sha256": seed_digests[seed],
            },
            "RETROSPECTIVE_OPERATOR_BLINDED_PER_SEED_BYTE_IDENTITY_ONLY_NO_OUTCOME_AGGREGATION",
        )
    append(
        "QC_LEDGER",
        "E002:QC:RETROSPECTIVE_OPERATOR",
        {
            "commit_sha": admission.AUTHORIZATION_SHA,
            "sha256": admission_record_sha256,
        },
        "RETROSPECTIVE_OPERATOR_STRUCTURAL_AND_PROVENANCE_QC_ONLY_PENDING_DATASET_LOCK",
    )
    return records


def validate_ledger(path: Path) -> None:
    try:
        structural_ledger.validate_ledger(path)
        semantic_ledger.validate_ledger(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        fail(f"pre-lock ledger validation failed: {exc}")


def source_fingerprint() -> str:
    return f"source-sha256:{sha256_bytes(Path(__file__).read_bytes())}"


def generated_at_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_before_persisting(ledger: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory(prefix="dgaf-epoch002-pre-lock-") as temporary:
        path = Path(temporary) / PRE_LOCK_LEDGER_NAME
        path.write_bytes(canonical_json_bytes(ledger))
        validate_ledger(path)


def prepare(
    *,
    retention_dir: Path,
    admission_record_path: Path | None = None,
    execution_receipt_path: Path | None = None,
    public_archive: Path | None = None,
    protected_archive: Path | None = None,
    write: bool = False,
) -> list[dict[str, Any]]:
    retention_dir = require_external_retention_dir(retention_dir)
    inputs = resolve_inputs(
        retention_dir=retention_dir,
        admission_record_path=admission_record_path,
        execution_receipt_path=execution_receipt_path,
        public_archive=public_archive,
        protected_archive=protected_archive,
    )

    evidence = validate_and_load_retained_evidence(inputs)
    ledger = build_pre_lock_ledger(
        auth=evidence.auth,
        admission_record=evidence.admission_record,
        admission_record_sha256=evidence.admission_record_sha256,
        seed_digests=evidence.seed_digests,
        generated_at_utc=generated_at_utc(),
        producer_commit=source_fingerprint(),
    )
    validate_before_persisting(ledger)

    output = retention_dir / PRE_LOCK_LEDGER_NAME
    if write:
        write_new_or_identical(output, canonical_json_bytes(ledger))
        validate_ledger(output)
        print("TRACK_A_EPOCH_002_PRE_LOCK_LEDGER=PASS_NONAUTHORIZING")
        print(f"PRE_LOCK_LEDGER={output}")
        print(f"PRE_LOCK_LEDGER_SHA256={sha256_bytes(output.read_bytes())}")
    else:
        print("TRACK_A_EPOCH_002_PRE_LOCK_LEDGER=PASS_DRY_RUN_NOT_WRITTEN")

    print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retention-dir", type=Path, default=DEFAULT_RETENTION_DIR)
    parser.add_argument("--admission-record", type=Path)
    parser.add_argument("--execution-receipt", type=Path)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    prepare(
        retention_dir=args.retention_dir,
        admission_record_path=args.admission_record,
        execution_receipt_path=args.execution_receipt,
        public_archive=args.public_archive,
        protected_archive=args.protected_archive,
        write=args.write,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
