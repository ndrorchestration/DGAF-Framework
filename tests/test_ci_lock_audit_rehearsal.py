"""Negative controls for the non-admitting hashed CI-lock audit rehearsal."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import ci_lock_audit_rehearsal as rehearsal


@pytest.fixture
def fixture_root(tmp_path: Path) -> Path:
    for filename, minor in rehearsal.LOCKS:
        source = (
            f"# python_minor: {minor}\n"
            "filelock==4.0.3 \\\n"
            "    --hash=sha256:" + "a" * 64 + "\n"
            "setuptools==83.0.0 \\\n"
            "    --hash=sha256:" + "b" * 64 + "\n"
        )
        (tmp_path / filename).write_text(source, encoding="utf-8")
    return tmp_path


def scanner_json(*, vulnerable: bool = False) -> str:
    return json.dumps(
        {
            "dependencies": [
                {
                    "name": "filelock",
                    "version": "4.0.3",
                    "vulns": [
                        {"id": "CVE-SYNTHETIC-1", "fix_versions": ["4.2.1"]}
                    ]
                    if vulnerable
                    else [],
                }
            ],
            "fixes": [],
        }
    )


def test_inspect_all_real_canonical_locks_without_mutating_them() -> None:
    root = Path(__file__).resolve().parents[1]
    found = rehearsal.inspect_locks(root)
    assert [row["filename"] for row in found] == [name for name, _ in rehearsal.LOCKS]
    assert [row["python_minor"] for row in found] == [minor for _, minor in rehearsal.LOCKS]
    assert all(len(row["sha256"]) == 64 and row["package_count"] > 0 for row in found)


def test_five_distinct_audit_targets_are_required(fixture_root: Path, tmp_path: Path) -> None:
    observed = []

    def safe_runner(command, **kwargs):
        observed.append(command)
        assert kwargs["capture_output"] is True
        assert kwargs["timeout"] == 180
        return SimpleNamespace(returncode=0, stdout=scanner_json())

    path = tmp_path / "rehearsal.json"
    result = rehearsal.rehearse(fixture_root, path, runner=safe_runner)
    assert result["result"] == "NO_REPORTED_VULNERABILITIES_ONLY"
    assert result["security_clearance"] == "NOT_ESTABLISHED"
    assert len(observed) == 5
    assert "--local" in observed[0]
    for cmd in observed[1:]:
        assert "--disable-pip" in cmd
        assert "--require-hashes" in cmd
        assert "--local" not in cmd
    assert json.loads(path.read_text(encoding="utf-8")) == result


def test_vulnerability_reports_block_and_preserve_advisory_ids(fixture_root: Path, tmp_path: Path) -> None:
    def vulnerable_runner(command, **kwargs):
        _ = kwargs
        vulnerable = "--local" not in command
        return SimpleNamespace(
            returncode=1 if vulnerable else 0,
            stdout=scanner_json(vulnerable=vulnerable),
        )

    result = rehearsal.rehearse(fixture_root, tmp_path / "report.json", runner=vulnerable_runner)
    assert result["result"] == "BLOCKED_VULNERABILITIES"
    assert all(entry["status"] == "VULNERABILITIES_FOUND" for entry in result["locks"][1:])
    assert all(
        entry["findings"][0]["advisory_ids"] == ["CVE-SYNTHETIC-1"]
        for entry in result["locks"][1:]
    )


@pytest.mark.parametrize("bad_output", ["not json", "{}", '{"dependencies":[{}]}'])
def test_missing_or_malformed_scanner_evidence_fails_closed(
    fixture_root: Path, tmp_path: Path, bad_output: str
) -> None:
    def invalid_runner(command, **kwargs):
        _ = (command, kwargs)
        return SimpleNamespace(returncode=0, stdout=bad_output)

    result = rehearsal.rehearse(fixture_root, tmp_path / "error.json", runner=invalid_runner)
    assert result["result"] == "AUDIT_ERROR"
    assert all(entry["status"] == "AUDIT_ERROR" for entry in result["locks"])


def test_nonzero_scan_without_findings_is_error(fixture_root: Path, tmp_path: Path) -> None:
    def ambiguous_runner(command, **kwargs):
        _ = (command, kwargs)
        return SimpleNamespace(returncode=1, stdout=scanner_json())

    report = rehearsal.rehearse(fixture_root, tmp_path / "failed.json", runner=ambiguous_runner)
    assert report["result"] == "AUDIT_ERROR"


def test_auditor_exception_fails_closed_and_keeps_remaining_receipts(
    fixture_root: Path, tmp_path: Path
) -> None:
    def timeout_runner(command, **kwargs):
        if "--local" in command:
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        return SimpleNamespace(returncode=0, stdout=scanner_json())

    report = rehearsal.rehearse(fixture_root, tmp_path / "timeout.json", runner=timeout_runner)
    assert report["result"] == "AUDIT_ERROR"
    assert report["locks"][0]["status"] == "AUDIT_ERROR"
    assert len(report["locks"]) == 5


def test_missing_or_unhashed_lock_never_calls_scanner(fixture_root: Path, tmp_path: Path) -> None:
    target = fixture_root / rehearsal.LOCKS[0][0]
    target.write_text(target.read_text().replace("--hash=sha256:", "--hash=sha1:"), encoding="utf-8")

    def must_not_run(command, **kwargs):
        raise AssertionError(f"scanner ran with invalid input: {command} {kwargs}")

    report = rehearsal.rehearse(fixture_root, tmp_path / "badlock.json", runner=must_not_run)
    assert report["result"] == "AUDIT_ERROR"
    assert report["locks"] == []


def test_missing_canonical_lock_blocks_without_network(fixture_root: Path, tmp_path: Path) -> None:
    (fixture_root / rehearsal.LOCKS[2][0]).unlink()
    report = rehearsal.rehearse(fixture_root, tmp_path / "missing.json")
    assert report["result"] == "AUDIT_ERROR"
    assert "missing canonical lock" in report["error"]


def test_reject_duplicate_package_versions(fixture_root: Path) -> None:
    path = fixture_root / rehearsal.LOCKS[0][0]
    path.write_text(
        path.read_text(encoding="utf-8") + "filelock==4.2.1 \\\n    --hash=sha256:" + "c" * 64 + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate"):
        rehearsal.inspect_locks(fixture_root)
