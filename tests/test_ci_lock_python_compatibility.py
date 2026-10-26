"""Non-empirical regression contracts for the CI Python-metadata compatibility preflight."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.ci_lock_python_compatibility import LockEvidenceError, LOCKS, evaluate_matrix

METADATA_SOURCE = "https://pypi.org/project/filelock/4.2.1/"


@pytest.fixture
def fake_locks(tmp_path: Path) -> Path:
    for filename, minor in LOCKS:
        (tmp_path / filename).write_text(
            f"# python_minor: {minor}\n"
            f"# python_full: {minor}.21\n"
            "filelock==4.0.3 \\\n"
            "    --hash=sha256:" + "a" * 64 + "\n"
            "setuptools==83.0.0 \\\n"
            "    --hash=sha256:" + "b" * 64 + "\n",
            encoding="utf-8",
        )
    return tmp_path


def test_filelock_fixed_release_blocks_python_310_only(fake_locks: Path) -> None:
    report = evaluate_matrix(fake_locks, "filelock", "4.2.1", ">=3.11", METADATA_SOURCE)
    assert report["classification"] == "INCOMPATIBLE"
    assert report["security_clearance"] == "NOT_ESTABLISHED"
    assert report["approval"] == "NOT_AUTHORIZED"
    assert report["metadata_authenticated"] is False
    assert len(report["locks"]) == 4
    assert report["locks"][0]["python_minor"] == "3.10"
    assert report["locks"][0]["candidate_supported"] is False
    assert all(row["candidate_supported"] for row in report["locks"][1:])
    assert all(len(row["lock_sha256"]) == 64 for row in report["locks"])


def test_setuptools_metadata_compatible_does_not_imply_security_approval(fake_locks: Path) -> None:
    report = evaluate_matrix(
        fake_locks,
        "setuptools",
        "84.1.0",
        ">=3.10",
        "https://pypi.org/project/setuptools/84.1.0/",
    )
    assert report["classification"] == "METADATA_COMPATIBLE_ONLY"
    assert all(row["candidate_supported"] for row in report["locks"])
    assert report["security_clearance"] == "NOT_ESTABLISHED"
    assert report["metadata_authenticated"] is False


def test_missing_lock_rejected(fake_locks: Path) -> None:
    (fake_locks / LOCKS[0][0]).unlink()
    with pytest.raises(LockEvidenceError, match="missing"):
        evaluate_matrix(fake_locks, "filelock", "4.2.1", ">=3.11", METADATA_SOURCE)


def test_duplicate_lock_pin_rejected(fake_locks: Path) -> None:
    target = fake_locks / LOCKS[0][0]
    with target.open("a", encoding="utf-8") as handle:
        handle.write("filelock==4.0.3 \\\n    --hash=sha256:" + "c" * 64 + "\n")
    with pytest.raises(LockEvidenceError, match="exactly one match"):
        evaluate_matrix(fake_locks, "filelock", "4.2.1", ">=3.11", METADATA_SOURCE)


def test_mismatched_interpreter_header_rejected(fake_locks: Path) -> None:
    target = fake_locks / LOCKS[0][0]
    source = target.read_text(encoding="utf-8").replace("# python_minor: 3.10", "# python_minor: 3.11")
    target.write_text(source, encoding="utf-8")
    with pytest.raises(LockEvidenceError, match="expected Python 3.10"):
        evaluate_matrix(fake_locks, "filelock", "4.2.1", ">=3.11", METADATA_SOURCE)


@pytest.mark.parametrize("candidate,requirement", [("bogus", ">=3.11"), ("4.2.1", ">==3.11")])
def test_invalid_release_metadata_rejected(fake_locks: Path, candidate: str, requirement: str) -> None:
    with pytest.raises(LockEvidenceError, match="invalid release metadata"):
        evaluate_matrix(fake_locks, "filelock", candidate, requirement, METADATA_SOURCE)


def test_untrusted_or_malformed_package_input_rejected(fake_locks: Path) -> None:
    with pytest.raises(LockEvidenceError, match="package name"):
        evaluate_matrix(fake_locks, "../../filelock", "4.2.1", ">=3.11", METADATA_SOURCE)
    with pytest.raises(LockEvidenceError, match="HTTPS"):
        evaluate_matrix(fake_locks, "filelock", "4.2.1", ">=3.11", "http://untrusted.test")

def test_checked_in_canonical_locks_produce_bounded_metadata_report() -> None:
    """Exercise the real four-lock parser; do not assert future lock versions."""
    root = Path(__file__).resolve().parents[1]
    report = evaluate_matrix(root, "filelock", "4.2.1", ">=3.11", METADATA_SOURCE)
    assert len(report["locks"]) == len(LOCKS)
    assert [entry["python_minor"] for entry in report["locks"]] == [minor for _, minor in LOCKS]
    assert all(len(entry["lock_sha256"]) == 64 for entry in report["locks"])
    assert all(entry["installed_pin"] for entry in report["locks"])
    assert report["metadata_authenticated"] is False
    assert report["security_clearance"] == "NOT_ESTABLISHED"
    assert report["classification"] in {"INCOMPATIBLE", "METADATA_COMPATIBLE_ONLY"}

