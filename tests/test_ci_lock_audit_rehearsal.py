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
                    "vulns": [{"id": "CVE-SYNTHETIC-1", "fix_versions": ["4.2.1"]}] if vulnerable else [],
                },
                {"name": "setuptools", "version": "83.0.0", "vulns": []},
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
    assert all(entry["findings"][0]["advisory_ids"] == ["CVE-SYNTHETIC-1"] for entry in result["locks"][1:])


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


def test_auditor_exception_fails_closed_and_keeps_remaining_receipts(fixture_root: Path, tmp_path: Path) -> None:
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


def test_missing_package_cannot_be_reported_clean(fixture_root: Path, tmp_path: Path) -> None:
    def partial_runner(command, **kwargs):
        _ = kwargs
        raw = json.loads(scanner_json())
        if "--local" not in command:
            raw["dependencies"] = raw["dependencies"][:1]
        return SimpleNamespace(returncode=0, stdout=json.dumps(raw))

    report = rehearsal.rehearse(fixture_root, tmp_path / "partial.json", runner=partial_runner)
    assert report["result"] == "AUDIT_ERROR"
    assert all(item["status"] == "AUDIT_ERROR" for item in report["locks"][1:])
    assert all(item["coverage"] == "MISSING_SUBSTITUTED_OR_EXTRA_PACKAGE" for item in report["locks"][1:])


@pytest.mark.parametrize(
    "mutation",
    ["wrong-version", "unknown-package", "duplicate-package", "missing-version"],
)
def test_substituted_or_duplicate_packages_fail_closed(fixture_root: Path, tmp_path: Path, mutation: str) -> None:
    def tampered_runner(command, **kwargs):
        _ = kwargs
        payload = json.loads(scanner_json())
        if "--local" not in command:
            if mutation == "wrong-version":
                payload["dependencies"][0]["version"] = "4.2.1"
            elif mutation == "unknown-package":
                payload["dependencies"][1]["name"] = "invented"
            elif mutation == "duplicate-package":
                payload["dependencies"].append(payload["dependencies"][0].copy())
            else:
                payload["dependencies"][0].pop("version")
        return SimpleNamespace(returncode=0, stdout=json.dumps(payload))

    report = rehearsal.rehearse(fixture_root, tmp_path / "tampered.json", runner=tampered_runner)
    assert report["result"] == "AUDIT_ERROR"
    assert all(row["status"] == "AUDIT_ERROR" for row in report["locks"][1:])


def test_empty_installed_environment_scan_never_establishes_cleanliness(fixture_root: Path, tmp_path: Path) -> None:
    def empty_runner(command, **kwargs):
        _ = kwargs
        return SimpleNamespace(returncode=0, stdout='{"dependencies":[],"fixes":[]}')

    report = rehearsal.rehearse(fixture_root, tmp_path / "empty.json", runner=empty_runner)
    assert report["result"] == "AUDIT_ERROR"
    assert all(row["status"] == "AUDIT_ERROR" for row in report["locks"])


def test_source_binding_distinguishes_merge_sha_from_pr_head(
    fixture_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GITHUB_SHA", "merge-tree-sha")
    monkeypatch.setenv("PR_HEAD_SHA", "authored-head-sha")
    monkeypatch.setenv("PR_BASE_SHA", "base-sha")

    def safe_runner(command, **kwargs):
        _ = (command, kwargs)
        return SimpleNamespace(returncode=0, stdout=scanner_json())

    result = rehearsal.rehearse(fixture_root, tmp_path / "provenance.json", runner=safe_runner)
    assert result["result"] == "NO_REPORTED_VULNERABILITIES_ONLY"
    assert result["github_event_sha"] == "merge-tree-sha"
    assert result["pr_head_sha"] == "authored-head-sha"
    assert result["pr_base_sha"] == "base-sha"
    assert result["github_event_sha"] != result["pr_head_sha"]


@pytest.mark.parametrize("stage", ["during-scan", "before-next-scan"])
def test_changed_lock_bytes_invalidate_source_receipt(
    fixture_root: Path, tmp_path: Path, stage: str
) -> None:
    target = fixture_root / rehearsal.LOCKS[0][0]
    original = target.read_text(encoding="utf-8")

    def modifying_runner(command, **kwargs):
        _ = kwargs
        if stage == "during-scan" and str(target) in command:
            target.write_text(original + "# edited during scan\n", encoding="utf-8")
        if stage == "before-next-scan" and "--local" in command:
            target.write_text(original + "# edited before scan\n", encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout=scanner_json())

    report = rehearsal.rehearse(fixture_root, tmp_path / "mutation.json", runner=modifying_runner)
    assert report["result"] == "AUDIT_ERROR"
    assert report["locks"][1]["status"] == "AUDIT_ERROR"
    assert report["locks"][1]["error_type"] == "ValueError"

