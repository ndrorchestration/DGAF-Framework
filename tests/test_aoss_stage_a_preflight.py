import inspect
import subprocess
from pathlib import Path

import pytest


def test_missing_acp_checkout_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, inspect_preflight

    with pytest.raises(PreflightError, match="ACP_REPOSITORY_MISSING"):
        inspect_preflight(Path.cwd(), tmp_path / "absent")


def test_preflight_has_no_outcome_destination():
    from scripts.aoss_stage_a.preflight import inspect_preflight

    assert list(inspect.signature(inspect_preflight).parameters) == ["dgaf", "acp"]


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _commit_all(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _init_repo(path):
    path.mkdir()
    _git(path, "init")
    _git(path, "config", "user.email", "test@example.invalid")
    _git(path, "config", "user.name", "DGAF Test")


def test_restored_authorization_history_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import ExpectedBindings, PreflightError, _inspect_preflight

    dgaf = tmp_path / "dgaf"
    acp = tmp_path / "acp"
    _init_repo(dgaf)
    _init_repo(acp)

    marker = dgaf / "README.md"
    marker.write_text("basis\n", encoding="utf-8")
    basis = _commit_all(dgaf, "basis")

    auth_path = dgaf / "registry" / "aoss_v0_6_stage_a_collection_authorization_v1.json"
    auth_path.parent.mkdir()
    auth_bytes = '{"outcome_collection_authorized":true,"status":"AUTHORIZED_BOUNDED_STAGE_A_COLLECTION"}\n'
    auth_path.write_text(auth_bytes, encoding="utf-8")
    auth_commit = _commit_all(dgaf, "authorization")

    receipt_path = dgaf / "registry" / "aoss_v0_6_stage_a_precollection_receipt_v1.json"
    receipt_path.write_text(
        '{"outcomes_generated_before_receipt":false,"scientific_n_increment":0,"status":"PASS"}\n',
        encoding="utf-8",
    )
    receipt_commit = _commit_all(dgaf, "receipt")

    auth_path.write_text('{"status":"TAMPERED"}\n', encoding="utf-8")
    _commit_all(dgaf, "tamper authorization")
    auth_path.write_text(auth_bytes, encoding="utf-8")
    _commit_all(dgaf, "restore authorization")

    (acp / "README.md").write_text("acp\n", encoding="utf-8")
    acp_commit = _commit_all(acp, "acp")

    bindings = ExpectedBindings(
        dgaf_receipt_commit=receipt_commit,
        dgaf_authorization_commit=auth_commit,
        protected_source_basis=basis,
        acp_commit=acp_commit,
        contract_blobs={},
        executable_blobs={},
    )

    with pytest.raises(PreflightError, match="AUTHORIZATION_EVENT_HISTORY_MUTATED"):
        _inspect_preflight(dgaf, acp, bindings)
