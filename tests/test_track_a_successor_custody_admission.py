import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts import prepare_track_a_successor_custody_admission as admission


def test_admission_helper_is_repository_file() -> None:
    assert Path(admission.__file__).name == "prepare_track_a_successor_custody_admission.py"


def test_admission_helper_exposes_source_validator() -> None:
    assert callable(admission.validate_source_evidence)


def _write_valid_source(source: Path, certificate_bytes: bytes) -> str:
    source.mkdir(parents=True)
    cert_sha = hashlib.sha256(certificate_bytes).hexdigest()
    (source / admission.SOURCE_CERT_NAME).write_bytes(certificate_bytes)
    receipt = {
        "record_type": "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT",
        "schema_version": 2,
        "recovery_verified_at": "2026-09-10T08:56:01.184982+00:00",
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "keypair_created_before_collection": True,
        "private_key_in_repository": False,
        "private_key_in_notion": False,
        "private_key_in_chat": False,
        "encrypted_private_key_sha256": "1" * 64,
        "certificate_sha256": cert_sha,
        "certificate_public_key_der_sha256": "2" * 64,
        "recovered_public_key_der_sha256": "2" * 64,
        "recovery_drill": "PASS",
        "backup_refs": [
            {
                "class": "ENCRYPTED_LOCAL_ARCHIVE",
                "nonsecret_id": "recovery-copy-a",
                "encrypted": True,
                "user_controlled": True,
                "encrypted_private_key_sha256": "1" * 64,
                "recovered_public_key_der_sha256": "2" * 64,
                "recovery_drill": "PASS",
            },
            {
                "class": "ENCRYPTED_OFFSITE_ARCHIVE",
                "nonsecret_id": "recovery-copy-b",
                "encrypted": True,
                "user_controlled": True,
                "encrypted_private_key_sha256": "1" * 64,
                "recovered_public_key_der_sha256": "2" * 64,
                "recovery_drill": "PASS",
            },
        ],
        "empirical_collection_authorized": False,
        "scientific_state_effect": "NONE",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    (source / admission.SOURCE_RECEIPT_NAME).write_text(
        json.dumps(receipt, indent=2) + "\r\n",
        encoding="utf-8",
        newline="",
    )
    return cert_sha


def _git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=repo, text=text).strip() if text else subprocess.check_output(
        ["git", *args], cwd=repo
    )


def _init_repo(repo: Path) -> None:
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    attrs = (
        f"{admission.DEST_CERT.as_posix()} -text\n"
        f"{admission.DEST_RECEIPT.as_posix()} -text\n"
    )
    (repo / ".gitattributes").write_text(attrs, encoding="utf-8")
    subprocess.run(["git", "add", ".gitattributes"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "-M", admission.EXPECTED_BRANCH], cwd=repo, check=True)
    head = _git(repo, "rev-parse", "HEAD")
    assert isinstance(head, str)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", head], cwd=repo, check=True)


def test_validate_source_evidence_accepts_exact_non_authorizing_pair(tmp_path: Path) -> None:
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    cert_bytes = b"-----BEGIN CERTIFICATE-----\r\nPUBLIC\r\n-----END CERTIFICATE-----\r\n"
    expected = _write_valid_source(source, cert_bytes)

    result = admission.validate_source_evidence(source, expected_cert_sha256=expected)

    assert result["certificate_sha256"] == expected
    assert result["certificate_path"].read_bytes() == cert_bytes
    assert result["receipt_path"].name == admission.SOURCE_RECEIPT_NAME


def test_validate_source_evidence_rejects_certificate_hash_mismatch(tmp_path: Path) -> None:
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _write_valid_source(source, b"certificate-a\r\n")

    with pytest.raises(RuntimeError, match="certificate SHA-256"):
        admission.validate_source_evidence(source, expected_cert_sha256="f" * 64)


def test_validate_source_evidence_rejects_receipt_certificate_hash_mismatch(tmp_path: Path) -> None:
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    expected = _write_valid_source(source, b"certificate-a\r\n")
    receipt_path = source / admission.SOURCE_RECEIPT_NAME
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    payload["certificate_sha256"] = "0" * 64
    receipt_path.write_text(json.dumps(payload, indent=2) + "\r\n", encoding="utf-8", newline="")

    with pytest.raises(RuntimeError, match="receipt certificate_sha256"):
        admission.validate_source_evidence(source, expected_cert_sha256=expected)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("schema_version", 1, "schema_version 2"),
        ("keypair_created_before_collection", False, "keypair_created_before_collection must remain true"),
        ("private_key_in_repository", True, "private_key_in_repository must remain false"),
        ("private_key_in_notion", True, "private_key_in_notion must remain false"),
        ("private_key_in_chat", True, "private_key_in_chat must remain false"),
        ("recovery_drill", "FAIL", "recovery_drill must PASS"),
        ("custody_class", "INDEPENDENT", "SAME_SYSTEM_NONINDEPENDENT"),
        ("independent_custody", True, "independent_custody must remain false"),
        ("empirical_collection_authorized", True, "must remain false"),
        ("scientific_state_effect", "AUTHORIZED", "scientific_state_effect must remain NONE"),
        ("canonical_dgaf_efficacy", "ESTABLISHED", "efficacy must remain NOT_ESTABLISHED"),
    ],
)
def test_validate_source_evidence_rejects_authority_or_schema_drift(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    expected = _write_valid_source(source, b"certificate-a\r\n")
    receipt_path = source / admission.SOURCE_RECEIPT_NAME
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    payload[field] = value
    receipt_path.write_text(json.dumps(payload, indent=2) + "\r\n", encoding="utf-8", newline="")

    with pytest.raises(RuntimeError, match=message):
        admission.validate_source_evidence(source, expected_cert_sha256=expected)


def test_find_source_dir_selects_unique_hash_match(tmp_path: Path) -> None:
    bad = tmp_path / "DGAF-Custody-Working-20260910-080000"
    good = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _write_valid_source(bad, b"wrong-certificate\r\n")
    expected = _write_valid_source(good, b"right-certificate\r\n")

    assert admission.find_source_dir(tmp_path, expected_cert_sha256=expected) == good


def test_find_source_dir_fails_closed_on_multiple_matches(tmp_path: Path) -> None:
    first = tmp_path / "DGAF-Custody-Working-20260910-085601"
    second = tmp_path / "DGAF-Custody-Working-20260910-090000"
    expected = _write_valid_source(first, b"same-certificate\r\n")
    _write_valid_source(second, b"same-certificate\r\n")

    with pytest.raises(RuntimeError, match="exactly one matching custody source directory"):
        admission.find_source_dir(tmp_path, expected_cert_sha256=expected)


def test_copy_and_stage_evidence_preserves_exact_bytes_and_only_two_paths(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _init_repo(repo)
    cert_bytes = b"-----BEGIN CERTIFICATE-----\r\nPUBLIC\r\n-----END CERTIFICATE-----\r\n"
    expected = _write_valid_source(source, cert_bytes)
    source_receipt = (source / admission.SOURCE_RECEIPT_NAME).read_bytes()

    result = admission.copy_and_stage_evidence(
        source,
        repo,
        expected_cert_sha256=expected,
        refresh_origin=False,
    )

    expected_paths = [admission.DEST_CERT.as_posix(), admission.DEST_RECEIPT.as_posix()]
    staged = _git(repo, "diff", "--cached", "--name-only")
    assert isinstance(staged, str)
    assert staged.splitlines() == expected_paths
    assert _git(repo, "show", ":" + expected_paths[0], text=False) == cert_bytes
    assert _git(repo, "show", ":" + expected_paths[1], text=False) == source_receipt
    assert result["staged_paths"] == expected_paths
    assert result["certificate_sha256"] == expected


def test_copy_and_stage_evidence_rejects_source_inside_repository(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    source = repo / "unsafe-source"
    expected = _write_valid_source(source, b"certificate-a\r\n")

    with pytest.raises(RuntimeError, match="source directory must remain outside the repository"):
        admission.copy_and_stage_evidence(
            source,
            repo,
            expected_cert_sha256=expected,
            refresh_origin=False,
        )


def test_copy_and_stage_evidence_requires_clean_v2_branch(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _init_repo(repo)
    subprocess.run(["git", "branch", "-M", "wrong-branch"], cwd=repo, check=True)
    expected = _write_valid_source(source, b"certificate-a\r\n")

    with pytest.raises(RuntimeError, match=admission.EXPECTED_BRANCH):
        admission.copy_and_stage_evidence(
            source,
            repo,
            expected_cert_sha256=expected,
            refresh_origin=False,
        )


def test_copy_and_stage_evidence_rejects_stale_branch(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _init_repo(repo)
    expected = _write_valid_source(source, b"certificate-a\r\n")
    (repo / "advance.txt").write_text("new main\n", encoding="utf-8")
    subprocess.run(["git", "add", "advance.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "advance"], cwd=repo, check=True)
    advanced = _git(repo, "rev-parse", "HEAD")
    assert isinstance(advanced, str)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", advanced], cwd=repo, check=True)
    subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=repo, check=True, stdout=subprocess.DEVNULL)

    with pytest.raises(RuntimeError, match="HEAD must exactly match origin/main"):
        admission.copy_and_stage_evidence(
            source,
            repo,
            expected_cert_sha256=expected,
            refresh_origin=False,
        )


def test_copy_and_stage_evidence_rejects_dirty_tracked_or_staged_state(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _init_repo(repo)
    expected = _write_valid_source(source, b"certificate-a\r\n")
    attributes = repo / ".gitattributes"
    attributes.write_text(attributes.read_text(encoding="utf-8") + "# dirty\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="clean index"):
        admission.copy_and_stage_evidence(
            source,
            repo,
            expected_cert_sha256=expected,
            refresh_origin=False,
        )


def test_copy_and_stage_evidence_rejects_text_normalization_enabled(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    source = tmp_path / "DGAF-Custody-Working-20260910-085601"
    _init_repo(repo)
    expected = _write_valid_source(source, b"certificate-a\r\n")
    attrs = f"{admission.DEST_CERT.as_posix()} text\n{admission.DEST_RECEIPT.as_posix()} -text\n"
    (repo / ".gitattributes").write_text(attrs, encoding="utf-8")
    subprocess.run(["git", "add", ".gitattributes"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "bad attrs"], cwd=repo, check=True)
    head = _git(repo, "rev-parse", "HEAD")
    assert isinstance(head, str)
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", head], cwd=repo, check=True)

    with pytest.raises(RuntimeError, match="text normalization is not disabled"):
        admission.copy_and_stage_evidence(
            source,
            repo,
            expected_cert_sha256=expected,
            refresh_origin=False,
        )
