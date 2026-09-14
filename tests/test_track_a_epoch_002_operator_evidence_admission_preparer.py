from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/prepare_track_a_epoch_002_operator_evidence_admission.py"


def load_preparer():
    assert MODULE_PATH.is_file(), "production evidence-admission preparer missing"
    spec = importlib.util.spec_from_file_location(
        "epoch002_operator_evidence_admission_preparer",
        MODULE_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.strip()


def init_repo(repo: Path) -> None:
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "tests@example.invalid")
    git(repo, "config", "user.name", "DGAF Tests")
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "fixture")


def install_validation_stubs(
    monkeypatch: pytest.MonkeyPatch,
    preparer,
) -> None:
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_evidence_file",
        lambda path: (
            {
                "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
                "evidence_execution_class": "OPERATOR_CODESPACE",
                "collection_execution_class": "OPERATOR_CODESPACE",
            },
            "a" * 64,
        ),
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_pre_lock_ledger",
        lambda path, evidence: None,
    )


def test_dry_run_validates_without_writing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    retention = tmp_path / "retention"
    init_repo(repo)
    retention.mkdir()
    evidence = retention / preparer.EVIDENCE_NAME
    ledger = retention / preparer.LEDGER_NAME
    evidence.write_bytes(b'{"evidence":true}\n')
    ledger.write_bytes(b"[]\n")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validation_stubs(monkeypatch, preparer)

    destinations = preparer.prepare(
        retention_dir=retention,
        write=False,
    )

    assert destinations == (
        repo / preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        repo / preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    assert not destinations[0].exists()
    assert not destinations[1].exists()
    assert git(repo, "status", "--porcelain") == ""


def test_write_copies_exact_bytes_and_only_two_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    retention = tmp_path / "retention"
    init_repo(repo)
    retention.mkdir()
    evidence = retention / preparer.EVIDENCE_NAME
    ledger = retention / preparer.LEDGER_NAME
    evidence_bytes = b'{"exact":"evidence"}\n'
    ledger_bytes = b'[{"exact":"ledger"}]\n'
    evidence.write_bytes(evidence_bytes)
    ledger.write_bytes(ledger_bytes)
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validation_stubs(monkeypatch, preparer)

    evidence_dest, ledger_dest = preparer.prepare(
        retention_dir=retention,
        write=True,
    )

    assert evidence_dest.read_bytes() == evidence_bytes
    assert ledger_dest.read_bytes() == ledger_bytes
    assert sorted(
        git(repo, "status", "--porcelain", "--untracked-files=all").splitlines()
    ) == sorted(
        [
            f"?? {preparer.dataset_lock.OPERATOR_EVIDENCE_REL}",
            f"?? {preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL}",
        ]
    )


def test_refuses_dirty_or_unrelated_repository_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    retention = tmp_path / "retention"
    init_repo(repo)
    retention.mkdir()
    (retention / preparer.EVIDENCE_NAME).write_text("{}\n", encoding="utf-8")
    (retention / preparer.LEDGER_NAME).write_text("[]\n", encoding="utf-8")
    (repo / "unrelated.txt").write_text("dirty\n", encoding="utf-8")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validation_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="clean repository"):
        preparer.prepare(retention_dir=retention, write=False)


def test_refuses_existing_canonical_destination(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    retention = tmp_path / "retention"
    init_repo(repo)
    retention.mkdir()
    (retention / preparer.EVIDENCE_NAME).write_text("{}\n", encoding="utf-8")
    (retention / preparer.LEDGER_NAME).write_text("[]\n", encoding="utf-8")
    evidence_dest = repo / preparer.dataset_lock.OPERATOR_EVIDENCE_REL
    evidence_dest.parent.mkdir(parents=True, exist_ok=True)
    evidence_dest.write_text("already here\n", encoding="utf-8")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validation_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="destination already exists"):
        preparer.prepare(retention_dir=retention, write=False)


def test_refuses_repository_local_source_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    local_retention = repo / "retention"
    local_retention.mkdir()
    (local_retention / preparer.EVIDENCE_NAME).write_text(
        "{}\n",
        encoding="utf-8",
    )
    (local_retention / preparer.LEDGER_NAME).write_text(
        "[]\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validation_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="outside the repository"):
        preparer.prepare(retention_dir=local_retention, write=False)
