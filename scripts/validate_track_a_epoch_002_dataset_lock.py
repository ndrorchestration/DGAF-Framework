#!/usr/bin/env python3
"""Fail-closed validator for Track A Epoch 002 content-addressed dataset locking.

This module is deliberately non-authorizing. It can validate a future retained
dataset-lock evidence bundle and a separate one-file repository receipt, but it
cannot execute collection, decrypt protected mappings, authorize unblinding,
run primary analysis, or change scientific N.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE_SCHEMA.json"
RESULT_SCHEMA_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RESULT_RECORD_SCHEMA.json"
STRUCTURAL_LEDGER_VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_result_ledger.py"
SEMANTICS_VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_result_record_semantics.py"

RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json"
RECEIPT_PATH = ROOT / RECEIPT_REL

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
EVIDENCE_ARTIFACT_NAME = "track-a-epoch-002-dataset-lock-evidence"
PUBLIC_ARTIFACT_NAME = "track-a-epoch-002-public-blinded"
PROTECTED_ARTIFACT_NAME = "track-a-epoch-002-protected-encrypted"
EVIDENCE_SCOPE = "CONTENT_ADDRESSED_EPOCH_002_BLINDED_DATASET_LOCK_BEFORE_UNBLINDING"
SEEDS = tuple(range(20270201, 20270251))
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
PER_SEED_RECORD_COUNT = 45
PRE_LOCK_LEDGER_RECORD_COUNT = 53
PUBLIC_RECORD_KEYS = frozenset(
    {
        "protocol_id",
        "algorithm_id",
        "frozen_candidate_sha",
        "seed_id",
        "blinded_topology_id",
        "failure_count",
        "ffcr_success",
        "excluded",
    }
)
PUBLIC_SEED_DOCUMENT_KEYS = frozenset(
    {
        "record_type",
        "schema_version",
        "protocol_id",
        "seed_id",
        "records",
        "environment_fingerprint",
        "runtime_seconds",
        "outcomes_inspected_by_collection_workflow",
        "unblinding_authorized",
        "primary_analysis_authorized",
    }
)
PUBLIC_MANIFEST_KEYS = frozenset(
    {
        "record_type",
        "schema_version",
        "protocol_id",
        "frozen_candidate_sha",
        "seed_count",
        "expected_observations",
        "custody_receipt_blob_sha",
        "custody_certificate_sha256",
        "custody_certificate_public_key_der_sha256",
        "rows",
        "outcomes_inspected_by_collection_workflow",
        "outcome_aggregation_performed",
        "unblinding_authorized",
        "primary_analysis_authorized",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
    }
)
PUBLIC_MANIFEST_ROW_KEYS = frozenset(
    {
        "seed_id",
        "public_dataset_sha256",
        "protected_mapping_sha256",
        "record_count",
    }
)
PROTECTED_FILES = frozenset(
    {
        "track_a_epoch_002_custody_cert.pem",
        "track_a_epoch_002_custody_cert.sha256",
        "track_a_epoch_002_protected.cms",
        "track_a_epoch_002_protected_ciphertext.sha256",
        "track_a_epoch_002_protected_plaintext_tar.sha256",
    }
)
FULL_NON_EFFECTS = (
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"TRACK_A_EPOCH_002_DATASET_LOCK_FAIL: {message}")


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")


def load_object(path: Path, label: str) -> dict[str, Any]:
    value = load_json(path, label)
    if not isinstance(value, dict):
        fail(f"{label} must be one JSON object")
    return value


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"cannot load {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def schema_validator(path: Path) -> Draft202012Validator:
    schema = load_object(path, f"schema {path.name}")
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_against(
    validator: Draft202012Validator,
    value: dict[str, Any],
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "<root>"
        fail(f"{label} schema-invalid at {location}: {error.message}")


def validate_evidence_object(evidence: dict[str, Any]) -> None:
    validate_against(
        schema_validator(EVIDENCE_SCHEMA_PATH),
        evidence,
        "dataset-lock evidence",
    )
    public = evidence["public_artifact"]
    protected = evidence["protected_artifact"]
    if public["artifact_id"] == protected["artifact_id"]:
        fail("public and protected artifacts must have distinct artifact IDs")
    if evidence["collection_authorization_commit_sha"] == evidence["frozen_candidate_sha"]:
        fail("collection authorization must be later than the frozen candidate")
    if evidence["evidence_tooling_commit_sha"] == evidence["collection_authorization_commit_sha"]:
        fail("evidence tooling identity must not masquerade as collection authorization")


def validate_evidence_file(path: Path) -> tuple[dict[str, Any], str]:
    evidence = load_object(path, "dataset-lock evidence")
    validate_evidence_object(evidence)
    return evidence, sha256_file(path)


def _read_sidecar(sidecar: Path, expected_name: str) -> str:
    try:
        text = sidecar.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read sidecar {sidecar}: {exc}")
    lines = text.splitlines()
    if len(lines) != 1:
        fail(f"sidecar {sidecar.name} must contain exactly one line")
    parts = lines[0].split()
    if len(parts) != 2 or parts[1] != expected_name or not HEX64.fullmatch(parts[0]):
        fail(f"sidecar {sidecar.name} has invalid digest/name binding")
    return parts[0]


def _require_sidecar(target: Path) -> str:
    sidecar = target.with_suffix(target.suffix + ".sha256")
    expected = _read_sidecar(sidecar, target.name)
    actual = sha256_file(target)
    if actual != expected:
        fail(f"sidecar digest mismatch for {target.name}")
    return actual


def validate_pre_lock_ledger(path: Path, evidence: dict[str, Any]) -> None:
    digest = sha256_file(path)
    if digest != evidence["pre_lock_result_ledger_sha256"]:
        fail("pre-lock result ledger SHA-256 mismatch")
    structural = load_module(
        STRUCTURAL_LEDGER_VALIDATOR_PATH,
        "epoch_002_dataset_lock_structural_ledger",
    )
    semantics = load_module(
        SEMANTICS_VALIDATOR_PATH,
        "epoch_002_dataset_lock_semantics",
    )
    try:
        structural.validate_ledger(path)
        semantics.validate_ledger(path)
        records = structural.load_records(path)
    except (ValueError, OSError, json.JSONDecodeError, SystemExit) as exc:
        fail(f"pre-lock result ledger validation failed: {exc}")
    if len(records) != PRE_LOCK_LEDGER_RECORD_COUNT:
        fail("pre-lock result ledger must stop at QC_LEDGER with " f"{PRE_LOCK_LEDGER_RECORD_COUNT} records")
    last = records[-1]
    if last.get("record_type") != "QC_LEDGER" or last.get("status") != "PASS":
        fail("pre-lock result ledger must terminate in PASS QC_LEDGER")
    if last.get("record_id") != evidence["qc_ledger_record_id"]:
        fail("dataset-lock evidence qc_ledger_record_id mismatch")


def _validate_public_seed_document(
    path: Path,
    *,
    seed: int,
    frozen_candidate_sha: str,
) -> None:
    doc = load_object(path, f"public seed {seed}")
    if set(doc) != PUBLIC_SEED_DOCUMENT_KEYS:
        fail(f"public seed {seed} top-level schema drift")
    if doc["record_type"] != "TRACK_A_EPOCH_002_BLINDED_SEED_DATASET":
        fail(f"public seed {seed} record_type drift")
    if doc["schema_version"] != 1 or doc["protocol_id"] != PROTOCOL_ID:
        fail(f"public seed {seed} identity drift")
    if doc["seed_id"] != seed:
        fail(f"public seed {seed} seed_id mismatch")
    if doc["outcomes_inspected_by_collection_workflow"] is not False:
        fail(f"public seed {seed} claims outcome inspection")
    if doc["unblinding_authorized"] is not False:
        fail(f"public seed {seed} claims unblinding authority")
    if doc["primary_analysis_authorized"] is not False:
        fail(f"public seed {seed} claims primary-analysis authority")
    if not isinstance(doc["environment_fingerprint"], dict):
        fail(f"public seed {seed} environment_fingerprint must be object")
    if not isinstance(doc["runtime_seconds"], (int, float)) or isinstance(doc["runtime_seconds"], bool):
        fail(f"public seed {seed} runtime_seconds malformed")

    records = doc["records"]
    if not isinstance(records, list) or len(records) != PER_SEED_RECORD_COUNT:
        fail(f"public seed {seed} record count mismatch")
    cells: set[tuple[str, int]] = set()
    blinded_ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != PUBLIC_RECORD_KEYS:
            fail(f"public seed {seed} record schema drift")
        if record["protocol_id"] != PROTOCOL_ID:
            fail(f"public seed {seed} protocol drift")
        if record["frozen_candidate_sha"] != frozen_candidate_sha:
            fail(f"public seed {seed} candidate drift")
        if record["seed_id"] != seed:
            fail(f"public seed {seed} record seed mismatch")
        blinded = record["blinded_topology_id"]
        failure_count = record["failure_count"]
        if not isinstance(blinded, str) or not re.fullmatch(
            r"topology_[0-9a-f]{20}",
            blinded,
        ):
            fail(f"public seed {seed} malformed blinded topology")
        if type(failure_count) is not int or failure_count not in FAILURE_COUNTS:
            fail(f"public seed {seed} failure-count drift")
        # Type-check the endpoint without branching on, tallying, or interpreting it.
        if type(record["ffcr_success"]) is not bool:
            fail(f"public seed {seed} endpoint is not strict boolean")
        if record["excluded"] is not False:
            fail(f"public seed {seed} contains an unregistered exclusion")
        cell = (blinded, failure_count)
        if cell in cells:
            fail(f"public seed {seed} duplicate blinded matrix cell")
        cells.add(cell)
        blinded_ids.add(blinded)
    if len(blinded_ids) != 5:
        fail(f"public seed {seed} blinded topology cardinality mismatch")
    for blinded in blinded_ids:
        failures = {failure for topology, failure in cells if topology == blinded}
        if failures != set(FAILURE_COUNTS):
            fail(f"public seed {seed} incomplete failure panel")


def _validate_flat_member_set(root: Path, expected_names: set[str] | frozenset[str], label: str) -> None:
    entries = list(root.iterdir())
    unsafe = sorted(path.name for path in entries if path.is_symlink() or not path.is_file())
    if unsafe:
        fail(f"{label} artifact contains non-regular top-level members: {unsafe}")
    actual_names = {path.name for path in entries}
    if actual_names != set(expected_names):
        fail(
            f"{label} artifact member set mismatch: "
            f"missing={sorted(set(expected_names) - actual_names)} "
            f"extra={sorted(actual_names - set(expected_names))}"
        )


def validate_public_root(root: Path, evidence: dict[str, Any]) -> None:
    if not root.is_dir():
        fail("public artifact extraction root missing")
    expected_names = {
        "track_a_epoch_002_manifest.json",
        "track_a_epoch_002_manifest.json.sha256",
    }
    for seed in SEEDS:
        expected_names.add(f"track_a_epoch_002_seed_{seed}.json")
        expected_names.add(f"track_a_epoch_002_seed_{seed}.json.sha256")
    _validate_flat_member_set(root, expected_names, "public")

    manifest_path = root / "track_a_epoch_002_manifest.json"
    manifest_digest = _require_sidecar(manifest_path)
    if manifest_digest != evidence["public_artifact"]["manifest_sha256"]:
        fail("public manifest SHA-256 mismatch")
    manifest = load_object(manifest_path, "public collection manifest")
    if set(manifest) != PUBLIC_MANIFEST_KEYS:
        fail("public collection manifest schema drift")
    if manifest["record_type"] != "TRACK_A_EPOCH_002_BLINDED_COLLECTION_MANIFEST":
        fail("public collection manifest record_type drift")
    if manifest["schema_version"] != 1 or manifest["protocol_id"] != PROTOCOL_ID:
        fail("public collection manifest identity drift")
    if manifest["frozen_candidate_sha"] != evidence["frozen_candidate_sha"]:
        fail("public collection manifest candidate drift")
    if manifest["seed_count"] != 50 or manifest["expected_observations"] != 2250:
        fail("public collection manifest size drift")
    if manifest["custody_receipt_blob_sha"] != evidence["custody_receipt_blob_sha"]:
        fail("public collection manifest custody receipt drift")
    protected = evidence["protected_artifact"]
    if manifest["custody_certificate_sha256"] != protected["custody_certificate_sha256"]:
        fail("public collection manifest custody certificate drift")
    if manifest["custody_certificate_public_key_der_sha256"] != protected["custody_certificate_public_key_der_sha256"]:
        fail("public collection manifest custody public-key drift")
    for field in (
        "outcomes_inspected_by_collection_workflow",
        "outcome_aggregation_performed",
        "unblinding_authorized",
        "primary_analysis_authorized",
        "historical_pooling_allowed",
        "epoch_004_substitution_allowed",
    ):
        if manifest[field] is not False:
            fail(f"public collection manifest must keep {field}=false")

    rows = manifest["rows"]
    if not isinstance(rows, list) or len(rows) != 50:
        fail("public collection manifest must contain 50 rows")
    if [row.get("seed_id") for row in rows if isinstance(row, dict)] != list(SEEDS):
        fail("public collection manifest seed panel drift")

    total = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != PUBLIC_MANIFEST_ROW_KEYS:
            fail("public collection manifest row schema drift")
        seed = row["seed_id"]
        if row["record_count"] != PER_SEED_RECORD_COUNT:
            fail(f"public collection manifest seed {seed} count drift")
        for digest_field in ("public_dataset_sha256", "protected_mapping_sha256"):
            if not isinstance(row[digest_field], str) or not HEX64.fullmatch(row[digest_field]):
                fail(f"public collection manifest seed {seed} digest malformed")
        seed_path = root / f"track_a_epoch_002_seed_{seed}.json"
        seed_digest = _require_sidecar(seed_path)
        if seed_digest != row["public_dataset_sha256"]:
            fail(f"public collection manifest seed {seed} digest mismatch")
        _validate_public_seed_document(
            seed_path,
            seed=seed,
            frozen_candidate_sha=evidence["frozen_candidate_sha"],
        )
        total += row["record_count"]
    if total != 2250:
        fail("public collection manifest total observation count drift")


def certificate_public_key_der_sha256(path: Path) -> str:
    if shutil.which("openssl") is None:
        fail("OpenSSL is required to verify the public custody certificate")
    public_pem = subprocess.check_output(
        ["openssl", "x509", "-in", str(path), "-pubkey", "-noout"],
        stderr=subprocess.DEVNULL,
    )
    public_der = subprocess.check_output(
        ["openssl", "pkey", "-pubin", "-outform", "DER"],
        input=public_pem,
        stderr=subprocess.DEVNULL,
    )
    return hashlib.sha256(public_der).hexdigest()


def validate_protected_root(root: Path, evidence: dict[str, Any]) -> None:
    if not root.is_dir():
        fail("protected artifact extraction root missing")
    _validate_flat_member_set(root, PROTECTED_FILES, "protected")
    protected = evidence["protected_artifact"]
    ciphertext = root / "track_a_epoch_002_protected.cms"
    cert = root / "track_a_epoch_002_custody_cert.pem"
    if _require_sidecar(ciphertext) != protected["ciphertext_sha256"]:
        fail("protected ciphertext SHA-256 mismatch")
    if _require_sidecar(cert) != protected["custody_certificate_sha256"]:
        fail("protected custody certificate SHA-256 mismatch")
    plaintext_commitment = _read_sidecar(
        root / "track_a_epoch_002_protected_plaintext_tar.sha256",
        "track_a_epoch_002_protected.tar",
    )
    if plaintext_commitment != protected["plaintext_tar_sha256"]:
        fail("protected plaintext-tar commitment mismatch")
    public_key_digest = certificate_public_key_der_sha256(cert)
    if public_key_digest != protected["custody_certificate_public_key_der_sha256"]:
        fail("protected custody certificate public-key fingerprint mismatch")


def validate_archive(path: Path, spec: dict[str, Any], label: str) -> None:
    if not path.is_file():
        fail(f"{label} archive missing")
    if path.stat().st_size != spec["size_bytes"]:
        fail(f"{label} archive size mismatch")
    if sha256_file(path) != spec["archive_sha256"]:
        fail(f"{label} archive SHA-256 mismatch")


def expected_receipt(
    evidence: dict[str, Any],
    evidence_sha256: str,
    *,
    evidence_artifact_id: int,
    generated_at_utc: str,
) -> dict[str, Any]:
    return {
        "record_type": "DATASET_LOCK_RECEIPT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch": 2,
        "record_id": f"E002-DATASET-LOCK-{evidence_sha256[:16].upper()}",
        "generated_at_utc": generated_at_utc,
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_DATASET_LOCK_VALIDATOR",
            "version_or_commit": evidence["evidence_tooling_commit_sha"],
        },
        "immutable_subject": {
            "commit_sha": evidence["collection_authorization_commit_sha"],
            "workflow_run_id": evidence["evidence_workflow_run_id"],
            "artifact_id": evidence_artifact_id,
            "sha256": evidence_sha256,
        },
        "evidence_scope": EVIDENCE_SCOPE,
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": [evidence["qc_ledger_record_id"]],
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def validate_receipt_object(
    receipt: dict[str, Any],
    evidence: dict[str, Any],
    evidence_sha256: str,
) -> None:
    validate_against(
        schema_validator(RESULT_SCHEMA_PATH),
        receipt,
        "dataset-lock receipt",
    )
    semantics = load_module(
        SEMANTICS_VALIDATOR_PATH,
        "epoch_002_dataset_lock_receipt_semantics",
    )
    try:
        policy = semantics.validate_policy()
        semantics.validate_record_semantics(receipt, policy)
    except SystemExit as exc:
        fail(f"dataset-lock receipt semantic validation failed: {exc}")

    immutable = receipt.get("immutable_subject")
    if not isinstance(immutable, dict):
        fail("dataset-lock receipt immutable_subject missing")
    artifact_id = immutable.get("artifact_id")
    if type(artifact_id) is not int or artifact_id < 1:
        fail("dataset-lock receipt must bind the exact evidence artifact ID")
    generated_at = receipt.get("generated_at_utc")
    if not isinstance(generated_at, str):
        fail("dataset-lock receipt generated_at_utc missing")

    expected = expected_receipt(
        evidence,
        evidence_sha256,
        evidence_artifact_id=artifact_id,
        generated_at_utc=generated_at,
    )
    if receipt != expected:
        missing = sorted(set(expected) - set(receipt))
        extra = sorted(set(receipt) - set(expected))
        mismatched = sorted(
            key for key in set(expected) & set(receipt) if expected[key] != receipt[key]
        )
        fail(
            "dataset-lock receipt exact contract mismatch: "
            f"missing={missing} extra={extra} mismatched={mismatched}"
        )


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def git_object_exists(spec: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", spec],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def validate_tooling_only() -> None:
    if RECEIPT_PATH.exists():
        fail("tooling mode requires the canonical dataset-lock receipt to remain absent")
    schema_validator(EVIDENCE_SCHEMA_PATH).check_schema(
        load_object(EVIDENCE_SCHEMA_PATH, "dataset-lock evidence schema")
    )
    semantics = load_module(
        SEMANTICS_VALIDATOR_PATH,
        "epoch_002_dataset_lock_tooling_semantics",
    )
    try:
        policy = semantics.validate_policy()
    except SystemExit as exc:
        fail(f"result-record semantic policy invalid: {exc}")
    dataset_policy = policy["records"].get("DATASET_LOCK_RECEIPT")
    if dataset_policy != {
        "authority_class": "NONAUTHORIZING_STATE_TRANSITION",
        "pass_profile": "DATASET_LOCK_PASS",
        "requires_separate_exact_commit_for": "UNBLINDING_DECISION_RECORD",
    }:
        fail("DATASET_LOCK_RECEIPT semantic policy drift")
    profile = policy["profiles"].get("DATASET_LOCK_PASS")
    if (
        not isinstance(profile, dict)
        or profile.get("authorization_effect") != "REQUIRES_SEPARATE_EXACT_COMMIT"
        or set(profile.get("required_non_effects", [])) != set(FULL_NON_EFFECTS)
        or profile.get("forbidden_non_effects") != []
    ):
        fail("DATASET_LOCK_PASS authority ceiling drift")


def validate_receipt_event(
    evidence_path: Path,
    pre_lock_ledger_path: Path,
    public_archive: Path,
    protected_archive: Path,
    public_root: Path,
    protected_root: Path,
) -> None:
    evidence, evidence_sha256 = validate_evidence_file(evidence_path)
    validate_pre_lock_ledger(pre_lock_ledger_path, evidence)
    validate_archive(public_archive, evidence["public_artifact"], "public")
    validate_archive(protected_archive, evidence["protected_artifact"], "protected")
    validate_public_root(public_root, evidence)
    validate_protected_root(protected_root, evidence)

    if not RECEIPT_PATH.is_file():
        fail("canonical dataset-lock receipt missing")
    receipt = load_object(RECEIPT_PATH, "dataset-lock receipt")
    validate_receipt_object(receipt, evidence, evidence_sha256)

    head = git("rev-parse", "HEAD")
    parent_fields = git("rev-list", "--parents", "-n", "1", head).split()
    if len(parent_fields) != 2:
        fail("dataset-lock receipt HEAD must have exactly one parent")
    parent = parent_fields[1]
    changed = sorted(
        line
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            head,
        ).splitlines()
        if line
    )
    if changed != [RECEIPT_REL]:
        fail("dataset-lock receipt event must change exactly one file " f"{RECEIPT_REL}; got {changed}")
    if git_object_exists(f"{parent}:{RECEIPT_REL}"):
        fail("dataset-lock receipt unexpectedly existed at event parent")
    history = [line for line in git("log", "--format=%H", "--", RECEIPT_REL).splitlines() if line]
    if history != [head]:
        fail(f"dataset-lock receipt must have first-and-only history at HEAD; got {history}")

    authorization = evidence["collection_authorization_commit_sha"]
    tooling = evidence["evidence_tooling_commit_sha"]
    if not git_object_exists(f"{authorization}^{{commit}}"):
        fail("collection authorization commit is not present in repository history")
    if not git_is_ancestor(authorization, parent):
        fail("collection authorization commit is not ancestor of dataset-lock parent")
    if not git_object_exists(f"{tooling}^{{commit}}"):
        fail("evidence tooling commit is not present in repository history")
    if not git_is_ancestor(tooling, parent):
        fail("evidence tooling commit is not ancestor of dataset-lock parent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tooling-only", action="store_true")
    mode.add_argument("--evidence-only", action="store_true")
    mode.add_argument("--receipt-event", action="store_true")
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--pre-lock-ledger", type=Path)
    parser.add_argument("--public-archive", type=Path)
    parser.add_argument("--protected-archive", type=Path)
    parser.add_argument("--public-root", type=Path)
    parser.add_argument("--protected-root", type=Path)
    args = parser.parse_args()

    if args.tooling_only:
        validate_tooling_only()
        print("TRACK_A_EPOCH_002_DATASET_LOCK_TOOLING=PASS_NONAUTHORIZING")
        print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    elif args.evidence_only:
        if args.evidence is None or args.pre_lock_ledger is None:
            fail("--evidence-only requires --evidence and --pre-lock-ledger")
        evidence, _ = validate_evidence_file(args.evidence)
        validate_pre_lock_ledger(args.pre_lock_ledger, evidence)
        print("TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE=PASS_STRUCTURAL_ONLY")
        print("TRACK_A_EPOCH_002_DATASET_LOCK=NOT_ESTABLISHED")
    else:
        required = {
            "--evidence": args.evidence,
            "--pre-lock-ledger": args.pre_lock_ledger,
            "--public-archive": args.public_archive,
            "--protected-archive": args.protected_archive,
            "--public-root": args.public_root,
            "--protected-root": args.protected_root,
        }
        missing = [name for name, value in required.items() if value is None]
        if missing:
            fail(f"--receipt-event missing required inputs: {missing}")
        validate_receipt_event(
            args.evidence,
            args.pre_lock_ledger,
            args.public_archive,
            args.protected_archive,
            args.public_root,
            args.protected_root,
        )
        print("TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT_EVENT=PASS_PENDING_MERGE")
        print("TRACK_A_EPOCH_002_DATASET_LOCK=PENDING_VALIDATED_MERGE")

    print("SUCCESSOR_COLLECTION_AUTHORIZATION_UNCHANGED=TRUE")
    print("UNBLINDING_AUTHORIZED=FALSE")
    print("PRIMARY_ANALYSIS_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
