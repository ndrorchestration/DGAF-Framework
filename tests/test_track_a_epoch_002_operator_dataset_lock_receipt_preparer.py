from __future__ import annotations

import hashlib
import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/prepare_track_a_epoch_002_operator_dataset_lock_receipt.py"


def load_preparer():
    assert MODULE_PATH.is_file(), "production operator dataset-lock receipt preparer missing"
    spec = importlib.util.spec_from_file_location(
        "epoch002_operator_dataset_lock_receipt_preparer",
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


def admit_evidence(repo: Path, evidence_rel: str, ledger_rel: str) -> str:
    evidence = repo / evidence_rel
    ledger = repo / ledger_rel
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_bytes(b'{"operator":"evidence"}\n')
    ledger.write_bytes(b'[{"ledger":true}]\n')
    git(repo, "add", evidence_rel, ledger_rel)
    git(repo, "commit", "-m", "admit operator evidence")
    return git(repo, "rev-parse", "HEAD")


def install_validator_stubs(
    monkeypatch: pytest.MonkeyPatch,
    preparer,
    evidence_sha: str | None = None,
):
    evidence = {
        "record_type": "TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE",
        "schema_version": 1,
        "evidence_execution_class": "OPERATOR_CODESPACE",
        "collection_execution_class": "OPERATOR_CODESPACE",
        "qc_ledger_record_id": "E002-QC-TEST",
        "evidence_tooling_commit_sha": "d" * 40,
    }
    actual_sha = evidence_sha or "f" * 64
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_evidence_file",
        lambda path: (evidence, actual_sha),
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_pre_lock_ledger",
        lambda path, value: None,
    )
    monkeypatch.setattr(
        preparer.dataset_lock,
        "validate_operator_receipt_object",
        lambda *args, **kwargs: None,
    )
    return evidence


def test_dry_run_derives_shared_admission_commit_and_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    admission_commit = admit_evidence(
        repo,
        preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    evidence_path = repo / preparer.dataset_lock.OPERATOR_EVIDENCE_REL
    expected_sha = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    monkeypatch.setattr(preparer, "ROOT", repo)
    evidence = install_validator_stubs(
        monkeypatch,
        preparer,
        evidence_sha=expected_sha,
    )
    captured = {}

    def fake_expected(
        value,
        evidence_sha256,
        *,
        evidence_admission_commit_sha,
        generated_at_utc,
    ):
        captured.update(
            evidence=value,
            evidence_sha256=evidence_sha256,
            admission_commit=evidence_admission_commit_sha,
            generated_at=generated_at_utc,
        )
        return {"receipt": "valid", "generated_at_utc": generated_at_utc}

    monkeypatch.setattr(
        preparer.dataset_lock,
        "expected_operator_receipt",
        fake_expected,
    )

    receipt = preparer.prepare(
        write=False,
        generated_at_utc="2026-09-14T13:30:00Z",
    )

    assert receipt["receipt"] == "valid"
    assert captured["evidence"] == evidence
    assert captured["evidence_sha256"] == expected_sha
    assert captured["admission_commit"] == admission_commit
    assert captured["generated_at"] == "2026-09-14T13:30:00Z"
    assert not (repo / preparer.dataset_lock.RECEIPT_REL).exists()
    assert git(repo, "status", "--porcelain") == ""


def test_write_creates_only_canonical_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    admit_evidence(
        repo,
        preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validator_stubs(monkeypatch, preparer)
    monkeypatch.setattr(
        preparer.dataset_lock,
        "expected_operator_receipt",
        lambda *args, **kwargs: {
            "record_type": "DATASET_LOCK_RECEIPT",
            "generated_at_utc": kwargs["generated_at_utc"],
        },
    )

    preparer.prepare(
        write=True,
        generated_at_utc="2026-09-14T13:31:00Z",
    )

    receipt = repo / preparer.dataset_lock.RECEIPT_REL
    assert receipt.is_file()
    assert git(repo, "status", "--porcelain") == (
        f"?? {preparer.dataset_lock.RECEIPT_REL}"
    )


def test_refuses_missing_committed_operator_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    monkeypatch.setattr(preparer, "ROOT", repo)

    with pytest.raises(SystemExit, match="admitted operator evidence"):
        preparer.prepare(write=False)


def test_refuses_divergent_evidence_and_ledger_history(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    evidence = repo / preparer.dataset_lock.OPERATOR_EVIDENCE_REL
    ledger = repo / preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("{}\n", encoding="utf-8")
    git(repo, "add", preparer.dataset_lock.OPERATOR_EVIDENCE_REL)
    git(repo, "commit", "-m", "evidence first")
    ledger.write_text("[]\n", encoding="utf-8")
    git(repo, "add", preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL)
    git(repo, "commit", "-m", "ledger later")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validator_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="share one immutable admission event"):
        preparer.prepare(write=False)


def test_refuses_dirty_repository_before_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    admit_evidence(
        repo,
        preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    (repo / "unrelated.txt").write_text("dirty\n", encoding="utf-8")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validator_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="clean repository"):
        preparer.prepare(write=False)


def test_refuses_existing_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    admit_evidence(
        repo,
        preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    receipt = repo / preparer.dataset_lock.RECEIPT_REL
    receipt.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validator_stubs(monkeypatch, preparer)

    with pytest.raises(SystemExit, match="receipt already exists"):
        preparer.prepare(write=False)


def test_refuses_nonancestor_admission_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = load_preparer()
    repo = tmp_path / "repo"
    init_repo(repo)
    admit_evidence(
        repo,
        preparer.dataset_lock.OPERATOR_EVIDENCE_REL,
        preparer.dataset_lock.OPERATOR_PRE_LOCK_LEDGER_REL,
    )
    monkeypatch.setattr(preparer, "ROOT", repo)
    install_validator_stubs(monkeypatch, preparer)
    monkeypatch.setattr(
        preparer,
        "git_is_ancestor",
        lambda ancestor, descendant: False,
    )

    with pytest.raises(SystemExit, match="not an ancestor"):
        preparer.prepare(write=False)
