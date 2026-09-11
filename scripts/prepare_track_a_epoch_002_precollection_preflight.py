#!/usr/bin/env python3
"""Prepare or validate the non-authorizing Track A Epoch 002 precollection preflight.

The helper consumes only the canonical public certificate and non-secret schema-v2
custody receipt already admitted to Git. It never creates, reads, requests, or
accepts a private key or passphrase, never authorizes collection, and never
executes empirical work.
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

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json"
RECEIPT_REL = "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json"
CERT_REL = "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem"
PREFLIGHT_REL = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json"
RECEIPT_PATH = ROOT / RECEIPT_REL
CERT_PATH = ROOT / CERT_REL
PREFLIGHT_PATH = ROOT / PREFLIGHT_REL
CUSTODY_VALIDATOR_REL = "scripts/validate_track_a_successor_solo_custody_receipt.py"
CUSTODY_VALIDATOR_PATH = ROOT / CUSTODY_VALIDATOR_REL

DOWNSTREAM_REL = (
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json",
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json",
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json",
    "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json",
)

SOURCE_BINDING_PATHS = {
    "preregistration_blob_sha": "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json",
    "analysis_lock_blob_sha": "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json",
    "analysis_blob_sha": "experiments/pdmal_pilot/track_a_epoch_002_analysis.py",
    "requirements_lock_blob_sha": "experiments/pdmal_pilot/requirements-full-lock.txt",
    "task_engine_blob_sha": "experiments/pdmal_pilot/task_engine.py",
    "harness_contract_blob_sha": "experiments/pdmal_pilot/harness_contract.py",
    "topology_utils_blob_sha": "experiments/pdmal_pilot/topology_utils.py",
    "successor_custody_contract_blob_sha": "docs/experiment/TRACK_A_SUCCESSOR_SOLO_CUSTODY_CONTRACT.md",
    "successor_custody_receipt_validator_blob_sha": CUSTODY_VALIDATOR_REL,
}

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"EPOCH_002_PREFLIGHT_FAIL: {message}")


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git {' '.join(args)} failed ({exc.returncode})")


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def git_path_exists(path: str, revision: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def git_path_history(path: str, revision: str) -> tuple[str, ...]:
    output = git("log", "--format=%H", revision, "--", path).lower()
    return tuple(line for line in output.splitlines() if line)


def git_blob(path: str, revision: str) -> str:
    return git("rev-parse", f"{revision}:{path}").lower()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate_public_key_der_sha256(path: Path) -> str:
    if shutil.which("openssl") is None:
        fail("OpenSSL is required to verify the public certificate")
    try:
        public_pem = subprocess.check_output(
            ["openssl", "x509", "-in", str(path), "-pubkey", "-noout"],
            cwd=ROOT,
        )
        public_der = subprocess.check_output(
            ["openssl", "pkey", "-pubin", "-outform", "DER"],
            input=public_pem,
            cwd=ROOT,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"public certificate verification failed ({exc.returncode})")
    return hashlib.sha256(public_der).hexdigest()


def load_custody_validator() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_successor_custody_validator", CUSTODY_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        fail("custody validator cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_contract_boundary(contract: dict[str, Any]) -> None:
    if contract.get("record_type") != "TRACK_A_EPOCH_002_RUNNER_CONTRACT":
        fail("unexpected runner contract record_type")
    if contract.get("schema_version") != 1:
        fail("runner contract schema_version drift")
    if contract.get("protocol_id") != "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002":
        fail("runner contract protocol drift")
    if contract.get("status") != "RUNNER_BOUND_NOT_AUTHORIZED":
        fail("runner contract status drift")
    if contract.get("track_a_freeze") != "NOT_ESTABLISHED":
        fail("runner contract unexpectedly establishes freeze")
    if contract.get("successor_collection") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes successor collection")
    if contract.get("primary_analysis") != "NOT_AUTHORIZED":
        fail("runner contract unexpectedly authorizes primary analysis")
    if contract.get("scientific_n_increment") != 0:
        fail("runner contract increments scientific N")

    authorization = contract.get("authorization")
    if not isinstance(authorization, dict):
        fail("runner contract authorization object missing")
    for field in (
        "pr_validation_can_authorize",
        "collection_authorized",
        "unblinding_authorized",
        "primary_analysis_authorized",
        "high_assurance_authorized",
    ):
        if authorization.get(field) is not False:
            fail(f"runner contract authorization.{field} must remain false")

    custody = contract.get("custody_precondition")
    if not isinstance(custody, dict):
        fail("runner contract custody_precondition missing")
    required = {
        "receipt_schema_version_required": 2,
        "legacy_receipt_authorizes_successor_collection": False,
        "each_recorded_backup_recovery_must_pass": True,
        "distinct_backup_storage_classes_required": True,
        "custody_class_required": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody_required": False,
        "minimum_distinct_encrypted_user_controlled_backups": 2,
        "custody_receipt_authorizes_collection": False,
    }
    for field, expected in required.items():
        if custody.get(field) != expected:
            fail(f"runner contract custody_precondition.{field} drift")


def require_candidate_sources(contract: dict[str, Any], candidate_sha: str) -> str:
    if not HEX40.fullmatch(candidate_sha):
        fail("malformed candidate SHA")
    candidate_tree = git("rev-parse", f"{candidate_sha}^{{tree}}").lower()
    if not HEX40.fullmatch(candidate_tree):
        fail("malformed candidate tree SHA")

    bindings = contract.get("source_bindings")
    if not isinstance(bindings, dict):
        fail("runner contract source_bindings missing")

    for binding, path in SOURCE_BINDING_PATHS.items():
        expected = bindings.get(binding)
        if not isinstance(expected, str) or not HEX40.fullmatch(expected):
            fail(f"runner contract {binding} missing or malformed")
        actual = git_blob(path, candidate_sha)
        if actual != expected:
            fail(f"candidate source drift {path}: {actual} != {expected}")

    prereg_merge = bindings.get("preregistration_merge_sha")
    analysis_merge = bindings.get("analysis_lock_merge_sha")
    for label, commit in (("preregistration", prereg_merge), ("analysis lock", analysis_merge)):
        if not isinstance(commit, str) or not HEX40.fullmatch(commit):
            fail(f"{label} merge SHA missing or malformed")
        if not is_ancestor(commit, candidate_sha):
            fail(f"{label} merge is not in candidate ancestry")

    return candidate_tree


def validate_custody_artifacts(candidate_sha: str, receipt: dict[str, Any]) -> dict[str, str]:
    if not git_path_exists(RECEIPT_REL, candidate_sha) or not git_path_exists(CERT_REL, candidate_sha):
        fail("custody receipt and public certificate must already be committed in candidate")

    try:
        load_custody_validator().validate_receipt(receipt)
    except (AttributeError, ValueError) as exc:
        fail(f"custody receipt validation failed ({exc})")

    if receipt.get("schema_version") != 2:
        fail("custody receipt must use schema version 2")
    if receipt.get("empirical_collection_authorized") is not False:
        fail("custody receipt must not authorize empirical collection")
    if not CERT_PATH.is_file():
        fail("public custody certificate absent from working tree")

    certificate_sha = sha256_file(CERT_PATH)
    certificate_public_sha = certificate_public_key_der_sha256(CERT_PATH)
    if receipt.get("certificate_sha256") != certificate_sha:
        fail("custody certificate SHA-256 mismatch")
    if receipt.get("certificate_public_key_der_sha256") != certificate_public_sha:
        fail("custody certificate public-key fingerprint mismatch")
    if receipt.get("recovered_public_key_der_sha256") != certificate_public_sha:
        fail("recovered custody key fingerprint does not match certificate")

    receipt_history = git_path_history(RECEIPT_REL, candidate_sha)
    cert_history = git_path_history(CERT_REL, candidate_sha)
    if len(receipt_history) != 1 or len(cert_history) != 1:
        fail("custody receipt and certificate must each have exactly one immutable history commit")
    if receipt_history[0] != cert_history[0]:
        fail("custody receipt and certificate must be introduced together")
    if not is_ancestor(receipt_history[0], candidate_sha):
        fail("custody evidence commit is not in candidate ancestry")

    return {
        "custody_receipt_blob_sha": git_blob(RECEIPT_REL, candidate_sha),
        "custody_certificate_blob_sha": git_blob(CERT_REL, candidate_sha),
        "custody_encrypted_private_key_sha256": str(receipt["encrypted_private_key_sha256"]),
        "custody_certificate_sha256": certificate_sha,
        "custody_certificate_public_key_der_sha256": certificate_public_sha,
    }


def expected_record(
    contract: dict[str, Any],
    *,
    candidate_sha: str,
    candidate_tree_sha: str,
    custody: dict[str, str],
) -> dict[str, Any]:
    bindings = contract["source_bindings"]
    matrix = contract["matrix"]
    return {
        "record_type": "TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT",
        "schema_version": 1,
        "protocol_id": contract["protocol_id"],
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree_sha,
        "preregistration_merge_sha": bindings["preregistration_merge_sha"],
        "analysis_lock_merge_sha": bindings["analysis_lock_merge_sha"],
        "analysis_blob_sha": bindings["analysis_blob_sha"],
        "analysis_config_sha256": bindings["analysis_config_sha256"],
        "requirements_lock_blob_sha": bindings["requirements_lock_blob_sha"],
        "algorithm_id": contract["algorithm_id"],
        "matrix_cells_per_seed": matrix["cells_per_seed"],
        "expected_observations": matrix["expected_total_observations"],
        **custody,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "custody_recovery_drill": "PASS",
        "preflight_status": "PASS",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_record(record: dict[str, Any], expected: dict[str, Any]) -> None:
    if record != expected:
        missing = sorted(set(expected) - set(record))
        extra = sorted(set(record) - set(expected))
        mismatched = sorted(key for key in set(expected) & set(record) if expected[key] != record[key])
        fail(f"preflight record mismatch missing={missing} extra={extra} mismatched={mismatched}")

    for field in ("candidate_sha", "candidate_tree_sha", "preregistration_merge_sha", "analysis_lock_merge_sha"):
        if not HEX40.fullmatch(str(record[field])):
            fail(f"malformed {field}")
    for field in (
        "analysis_config_sha256",
        "custody_encrypted_private_key_sha256",
        "custody_certificate_sha256",
        "custody_certificate_public_key_der_sha256",
    ):
        if not HEX64.fullmatch(str(record[field])):
            fail(f"malformed {field}")


def validate_gate_order(candidate_sha: str, *, require_preflight_history: bool) -> None:
    for path in DOWNSTREAM_REL:
        if git_path_exists(path, "HEAD") or (ROOT / path).exists():
            fail(f"downstream successor gate must remain absent: {path}")

    if git_path_exists(PREFLIGHT_REL, candidate_sha):
        fail("candidate must predate the preflight record")

    if require_preflight_history:
        history = git_path_history(PREFLIGHT_REL, "HEAD")
        if len(history) != 1:
            fail(f"preflight must have exactly one immutable history commit; history={list(history)}")


def ensure_preflight_only_delta(candidate_sha: str) -> None:
    changed = tuple(line for line in git("diff", "--name-only", f"{candidate_sha}...HEAD").splitlines() if line)
    if changed != (PREFLIGHT_REL,):
        fail(f"preflight validation branch must change only {PREFLIGHT_REL}; changed={list(changed)}")


def expected_record_for_candidate(candidate_sha: str) -> dict[str, Any]:
    """Reconstruct an accepted preflight without reapplying creation-time gate order."""
    contract = load_object(CONTRACT_PATH, "runner contract")
    validate_contract_boundary(contract)
    candidate_tree = require_candidate_sources(contract, candidate_sha)
    receipt = load_object(RECEIPT_PATH, "schema-v2 custody receipt")
    custody = validate_custody_artifacts(candidate_sha, receipt)
    return expected_record(
        contract,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        custody=custody,
    )


def prepare(candidate_sha: str) -> dict[str, Any]:
    record = expected_record_for_candidate(candidate_sha)
    validate_gate_order(candidate_sha, require_preflight_history=False)
    return record


def write_preflight() -> None:
    candidate_sha = git("rev-parse", "HEAD").lower()
    if PREFLIGHT_PATH.exists():
        fail("preflight record already exists; refusing to overwrite")
    record = prepare(candidate_sha)
    PREFLIGHT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREFLIGHT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("TRACK_A_EPOCH_002_PREFLIGHT_PREPARED_NONAUTHORIZING")
    print(f"CANDIDATE_SHA={candidate_sha}")
    print(f"OUTPUT={PREFLIGHT_REL}")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def validate_preflight(expected_candidate_sha: str | None) -> None:
    record = load_object(PREFLIGHT_PATH, "preflight record")
    candidate_sha = str(record.get("candidate_sha", "")).lower()
    if not HEX40.fullmatch(candidate_sha):
        fail("malformed candidate SHA")

    if expected_candidate_sha is not None:
        expected_candidate_sha = expected_candidate_sha.lower()
        if not HEX40.fullmatch(expected_candidate_sha):
            fail("malformed expected candidate SHA")
        if candidate_sha != expected_candidate_sha:
            fail(f"candidate must equal exact PR base {expected_candidate_sha}; got {candidate_sha}")

    if not is_ancestor(candidate_sha, git("rev-parse", "HEAD").lower()):
        fail("candidate is not an ancestor of preflight HEAD")

    if expected_candidate_sha is None:
        expected = expected_record_for_candidate(candidate_sha)
        validate_record(record, expected)
        history = git_path_history(PREFLIGHT_REL, "HEAD")
        if len(history) != 1:
            fail(f"preflight must have exactly one immutable history commit; history={list(history)}")
    else:
        expected = prepare(candidate_sha)
        validate_record(record, expected)
        validate_gate_order(candidate_sha, require_preflight_history=True)
        ensure_preflight_only_delta(candidate_sha)

    print("TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT_PASS_NONAUTHORIZING")
    print(f"CANDIDATE_SHA={record['candidate_sha']}")
    print(f"CANDIDATE_TREE_SHA={record['candidate_tree_sha']}")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def check_custody(expected_base_sha: str | None) -> None:
    candidate_sha = git("rev-parse", "HEAD").lower()
    _ = prepare(candidate_sha)

    if expected_base_sha is not None:
        expected_base_sha = expected_base_sha.lower()
        if not HEX40.fullmatch(expected_base_sha):
            fail("malformed expected base SHA")
        if not is_ancestor(expected_base_sha, candidate_sha):
            fail("expected base is not an ancestor of custody-admission HEAD")
        changed = {
            line for line in git("diff", "--name-only", f"{expected_base_sha}...{candidate_sha}").splitlines() if line
        }
        required = {RECEIPT_REL, CERT_REL}
        if changed != required:
            fail(f"custody admission PR must change exactly receipt + certificate; changed={sorted(changed)}")

    print("TRACK_A_SUCCESSOR_CUSTODY_EVIDENCE_PASS_FOR_PREFLIGHT_PREPARATION")
    print(f"CANDIDATE_SHA={candidate_sha}")
    print("INDEPENDENT_CUSTODY=FALSE")
    print("TRACK_A_FREEZE=NOT_ESTABLISHED")
    print("SUCCESSOR_COLLECTION_AUTHORIZED=FALSE")
    print("SCIENTIFIC_N_INCREMENT=0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--write",
        action="store_true",
        help="prepare the canonical preflight record against current HEAD",
    )
    mode.add_argument(
        "--validate",
        action="store_true",
        help="validate an existing canonical preflight record",
    )
    mode.add_argument(
        "--check-custody",
        action="store_true",
        help="validate admitted public custody evidence without writing preflight",
    )
    parser.add_argument("--expected-candidate-sha", default=None)
    args = parser.parse_args(argv)

    if args.write:
        if args.expected_candidate_sha is not None:
            fail("--expected-candidate-sha is valid only with --validate or --check-custody")
        write_preflight()
    elif args.validate:
        validate_preflight(args.expected_candidate_sha)
    else:
        check_custody(args.expected_candidate_sha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())