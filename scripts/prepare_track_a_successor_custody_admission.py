#!/usr/bin/env python3
"""Prepare the exact non-secret Track A successor custody pair for admission.

This helper never reads private-key bytes, backup files, passphrases, or
blinding material. It does not commit, push, freeze, or authorize collection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

EXPECTED_CERT_SHA256 = "5d14c89c20e0d22586045dea9fbb5de9a7ec6e7bbe7be4cd5b4da3ce9693db4e"
EXPECTED_BRANCH = "track-a-successor-custody-evidence-v2"
SOURCE_CERT_NAME = "track_a_successor_custody_cert.pem"
SOURCE_RECEIPT_NAME = "track_a_successor_solo_custody_receipt.json"
DEST_CERT = Path("docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem")
DEST_RECEIPT = Path(
    "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json"
)
EXPECTED_STAGED_PATHS = [DEST_CERT.as_posix(), DEST_RECEIPT.as_posix()]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_receipt(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"non-secret custody receipt is unreadable or invalid JSON: {exc}") from exc
    _require(isinstance(payload, dict), "non-secret custody receipt must be a JSON object")
    return payload


def validate_source_evidence(
    source_dir: Path,
    *,
    expected_cert_sha256: str = EXPECTED_CERT_SHA256,
) -> dict[str, Any]:
    """Validate only the public certificate and non-secret receipt in source_dir."""

    source_dir = source_dir.expanduser().resolve()
    certificate_path = source_dir / SOURCE_CERT_NAME
    receipt_path = source_dir / SOURCE_RECEIPT_NAME

    _require(certificate_path.is_file(), f"public certificate not found: {certificate_path}")
    _require(receipt_path.is_file(), f"non-secret custody receipt not found: {receipt_path}")

    certificate_sha256 = _sha256_file(certificate_path)
    _require(
        certificate_sha256 == expected_cert_sha256,
        "certificate SHA-256 does not match the expected successful-drill artifact",
    )

    payload = _load_receipt(receipt_path)
    _require(payload.get("schema_version") == 2, "custody receipt must use schema_version 2")
    _require(
        payload.get("record_type") == "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "custody receipt record_type is invalid",
    )
    _require(
        payload.get("certificate_sha256") == certificate_sha256,
        "receipt certificate_sha256 does not match the exact public certificate bytes",
    )
    _require(
        payload.get("keypair_created_before_collection") is True,
        "keypair_created_before_collection must remain true",
    )
    _require(
        payload.get("private_key_in_repository") is False,
        "private_key_in_repository must remain false",
    )
    _require(
        payload.get("private_key_in_notion") is False,
        "private_key_in_notion must remain false",
    )
    _require(
        payload.get("private_key_in_chat") is False,
        "private_key_in_chat must remain false",
    )
    _require(payload.get("recovery_drill") == "PASS", "recovery_drill must PASS")
    _require(
        payload.get("custody_class") == "SAME_SYSTEM_NONINDEPENDENT",
        "custody_class must remain SAME_SYSTEM_NONINDEPENDENT",
    )
    _require(
        payload.get("independent_custody") is False,
        "independent_custody must remain false",
    )
    _require(
        payload.get("empirical_collection_authorized") is False,
        "empirical_collection_authorized must remain false",
    )
    _require(
        payload.get("scientific_state_effect") == "NONE",
        "scientific_state_effect must remain NONE",
    )
    _require(
        payload.get("canonical_dgaf_efficacy") == "NOT_ESTABLISHED",
        "canonical DGAF efficacy must remain NOT_ESTABLISHED",
    )
    _require(
        payload.get("certificate_public_key_der_sha256")
        == payload.get("recovered_public_key_der_sha256"),
        "recovered public key identity must match the collection certificate",
    )

    return {
        "source_dir": source_dir,
        "certificate_path": certificate_path,
        "receipt_path": receipt_path,
        "certificate_sha256": certificate_sha256,
        "receipt": payload,
    }


def find_source_dir(
    home: Path,
    *,
    expected_cert_sha256: str = EXPECTED_CERT_SHA256,
) -> Path:
    """Find exactly one successful public custody-output directory under home."""

    home = home.expanduser().resolve()
    matches: list[Path] = []
    for candidate in sorted(home.glob("DGAF-Custody-Working-*")):
        if not candidate.is_dir():
            continue
        certificate_path = candidate / SOURCE_CERT_NAME
        receipt_path = candidate / SOURCE_RECEIPT_NAME
        if not certificate_path.is_file() or not receipt_path.is_file():
            continue
        try:
            if _sha256_file(certificate_path) != expected_cert_sha256:
                continue
            validate_source_evidence(candidate, expected_cert_sha256=expected_cert_sha256)
        except RuntimeError:
            continue
        matches.append(candidate.resolve())

    _require(
        len(matches) == 1,
        "expected exactly one matching custody source directory; "
        "use --source-dir to select the exact successful drill output",
    )
    return matches[0]


def _git(
    repo_root: Path,
    *args: str,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        capture_output=True,
        text=text,
    )


def _git_text(repo_root: Path, *args: str) -> str:
    result = _git(repo_root, *args, text=True)
    assert isinstance(result.stdout, str)
    return result.stdout.strip()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _ensure_source_outside_repository(source_dir: Path, repo_root: Path) -> None:
    source_dir = source_dir.resolve()
    repo_root = repo_root.resolve()
    _require(
        not _is_relative_to(source_dir, repo_root),
        "source directory must remain outside the repository",
    )


def _ensure_byte_preserving_attributes(repo_root: Path) -> None:
    for path in EXPECTED_STAGED_PATHS:
        output = _git_text(repo_root, "check-attr", "text", "--", path)
        _require(
            output.endswith("text: unset"),
            f"Git text normalization is not disabled for {path}",
        )


def _ensure_repo_state(repo_root: Path, *, refresh_origin: bool) -> None:
    branch = _git_text(repo_root, "branch", "--show-current")
    _require(branch == EXPECTED_BRANCH, f"must run on branch {EXPECTED_BRANCH}")

    if refresh_origin:
        _git(repo_root, "fetch", "--quiet", "origin", "main")

    head = _git_text(repo_root, "rev-parse", "HEAD")
    origin_main = _git_text(repo_root, "rev-parse", "refs/remotes/origin/main")
    _require(head == origin_main, "HEAD must exactly match origin/main before custody evidence admission")

    status = _git_text(repo_root, "status", "--porcelain")
    _require(not status, "custody admission requires a clean index and working tree")

    for relative_path in EXPECTED_STAGED_PATHS:
        _require(
            not (repo_root / relative_path).exists(),
            f"custody evidence destination already exists: {relative_path}",
        )

    _ensure_byte_preserving_attributes(repo_root)


def _copy_exact(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    _require(
        _sha256_file(source) == _sha256_file(destination),
        f"byte-preserving copy verification failed for {destination.name}",
    )


def copy_and_stage_evidence(
    source_dir: Path,
    repo_root: Path,
    *,
    expected_cert_sha256: str = EXPECTED_CERT_SHA256,
    refresh_origin: bool = True,
) -> dict[str, Any]:
    """Copy exact public artifacts and stage only their canonical repository paths."""

    source_dir = source_dir.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve()
    _ensure_source_outside_repository(source_dir, repo_root)
    evidence = validate_source_evidence(source_dir, expected_cert_sha256=expected_cert_sha256)
    _ensure_repo_state(repo_root, refresh_origin=refresh_origin)

    destination_certificate = repo_root / DEST_CERT
    destination_receipt = repo_root / DEST_RECEIPT
    try:
        _copy_exact(evidence["certificate_path"], destination_certificate)
        _copy_exact(evidence["receipt_path"], destination_receipt)

        _git(repo_root, "add", "--", *EXPECTED_STAGED_PATHS)
        staged = _git_text(repo_root, "diff", "--cached", "--name-only").splitlines()
        _require(
            staged == EXPECTED_STAGED_PATHS,
            "Git index must contain exactly the two canonical non-secret custody evidence paths",
        )

        _require(
            _sha256_file(destination_certificate) == evidence["certificate_sha256"],
            "staged certificate working-tree bytes changed during admission preparation",
        )
        _require(
            _sha256_file(destination_receipt) == _sha256_file(evidence["receipt_path"]),
            "staged receipt working-tree bytes changed during admission preparation",
        )
    except Exception:
        _git(repo_root, "reset", "--quiet", "--", *EXPECTED_STAGED_PATHS, check=False)
        for destination in (destination_certificate, destination_receipt):
            try:
                destination.unlink()
            except FileNotFoundError:
                pass
        raise

    return {
        "certificate_sha256": evidence["certificate_sha256"],
        "staged_paths": EXPECTED_STAGED_PATHS.copy(),
        "source_dir": source_dir,
    }


def _run_repository_receipt_validator(repo_root: Path, receipt_path: Path) -> None:
    validator = repo_root / "scripts" / "validate_track_a_successor_solo_custody_receipt.py"
    _require(validator.is_file(), f"repository receipt validator missing: {validator}")
    result = subprocess.run(
        [sys.executable, str(validator), str(receipt_path)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    _require(
        result.returncode == 0,
        "repository schema-v2 custody receipt validator rejected the source receipt",
    )
    _require(
        "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECEIPT=PASS_CURRENT_V2" in result.stdout,
        "repository custody receipt validator did not emit the current-v2 PASS marker",
    )


def _resolve_repo_root(argument: Path | None) -> Path:
    if argument is not None:
        return argument.expanduser().resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage the exact public Track A successor custody evidence pair without committing or pushing."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="Exact successful DGAF-Custody-Working-* directory; auto-discovered when omitted.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="DGAF repository root; defaults to the current Git worktree.",
    )
    args = parser.parse_args()

    repo_root = _resolve_repo_root(args.repo_root)
    source_dir = args.source_dir.expanduser().resolve() if args.source_dir else find_source_dir(Path.home())
    evidence = validate_source_evidence(source_dir)
    _run_repository_receipt_validator(repo_root, evidence["receipt_path"])
    result = copy_and_stage_evidence(source_dir, repo_root)

    print("TRACK_A_SUCCESSOR_CUSTODY_ADMISSION_PREP=PASS_STAGED")
    print(f"CERTIFICATE_SHA256={result['certificate_sha256']}")
    print("STAGED_PATHS=" + ",".join(result["staged_paths"]))
    print("NO_COMMIT_OR_PUSH_PERFORMED=TRUE")
    print("EMPIRICAL_COLLECTION_AUTHORIZED=FALSE")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
