import inspect
import subprocess
from dataclasses import replace
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


def _valid_repositories(tmp_path, *, extra_before_receipt=False):
    from scripts.aoss_stage_a.preflight import ExpectedBindings

    dgaf = tmp_path / "dgaf"
    acp = tmp_path / "acp"
    _init_repo(dgaf)
    _init_repo(acp)

    registry = dgaf / "registry"
    registry.mkdir()
    (dgaf / "README.md").write_text("basis\n", encoding="utf-8")
    frozen_path = registry / "frozen.json"
    frozen_path.write_text('{"frozen":true}\n', encoding="utf-8")
    replay_path = registry / "replay.json"
    replay_path.write_text('{"replay":true}\n', encoding="utf-8")
    basis = _commit_all(dgaf, "basis")
    frozen_blob = _git(dgaf, "rev-parse", f"{basis}:registry/frozen.json")
    replay_blob = _git(dgaf, "rev-parse", f"{basis}:registry/replay.json")

    auth_path = registry / "aoss_v0_6_stage_a_collection_authorization_v1.json"
    auth_path.write_text(
        '{"outcome_collection_authorized":true,' '"status":"AUTHORIZED_BOUNDED_STAGE_A_COLLECTION"}\n',
        encoding="utf-8",
    )
    auth_commit = _commit_all(dgaf, "authorization")

    if extra_before_receipt:
        (dgaf / "between.txt").write_text("between\n", encoding="utf-8")
        _commit_all(dgaf, "intermediate")

    receipt_path = registry / "aoss_v0_6_stage_a_precollection_receipt_v1.json"
    receipt_path.write_text(
        '{"outcomes_generated_before_receipt":false,' '"scientific_n_increment":0,"status":"PASS"}\n',
        encoding="utf-8",
    )
    receipt_commit = _commit_all(dgaf, "receipt")

    (acp / "README.md").write_text("acp\n", encoding="utf-8")
    acp_commit = _commit_all(acp, "acp")

    bindings = ExpectedBindings(
        dgaf_receipt_commit=receipt_commit,
        dgaf_authorization_commit=auth_commit,
        protected_source_basis=basis,
        acp_commit=acp_commit,
        contract_blobs={"registry/frozen.json": frozen_blob},
        executable_blobs={},
        authorization_parent_commit=basis,
        auxiliary_blobs={"registry/replay.json": replay_blob},
    )
    return dgaf, acp, bindings


def test_clean_private_preflight_passes_without_writes(tmp_path):
    from scripts.aoss_stage_a.preflight import _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    before = {
        "dgaf_head": _git(dgaf, "rev-parse", "HEAD"),
        "dgaf_status": _git(dgaf, "status", "--porcelain=v1", "--untracked-files=all"),
        "dgaf_index": _git(dgaf, "ls-files", "-s"),
        "acp_head": _git(acp, "rev-parse", "HEAD"),
        "acp_status": _git(acp, "status", "--porcelain=v1", "--untracked-files=all"),
        "acp_index": _git(acp, "ls-files", "-s"),
    }

    report = _inspect_preflight(dgaf, acp, bindings)

    assert report["static_identity_checks"] == "PASS"
    assert report["collection_readiness"] == "NOT_ESTABLISHED"
    assert report["mapping_binding"] == "NOT_ESTABLISHED"
    assert report["runtime_binding"] == "NOT_ESTABLISHED"
    assert report["scientific_n_increment"] == 0
    assert report["outcomes_generated"] is False
    after = {
        "dgaf_head": _git(dgaf, "rev-parse", "HEAD"),
        "dgaf_status": _git(dgaf, "status", "--porcelain=v1", "--untracked-files=all"),
        "dgaf_index": _git(dgaf, "ls-files", "-s"),
        "acp_head": _git(acp, "rev-parse", "HEAD"),
        "acp_status": _git(acp, "status", "--porcelain=v1", "--untracked-files=all"),
        "acp_index": _git(acp, "ls-files", "-s"),
    }
    assert after == before


def test_wrong_acp_commit_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    (acp / "later.txt").write_text("drift\n", encoding="utf-8")
    _commit_all(acp, "drift")

    with pytest.raises(PreflightError, match="ACP_COMMIT_MISMATCH"):
        _inspect_preflight(dgaf, acp, bindings)


def test_dirty_tracked_dgaf_file_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    (dgaf / "README.md").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(PreflightError, match="DGAF_WORKTREE_DIRTY"):
        _inspect_preflight(dgaf, acp, bindings)


def test_untracked_import_shadow_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    (dgaf / "agent_control_plane.py").write_text("raise RuntimeError('shadow')\n", encoding="utf-8")

    with pytest.raises(PreflightError, match="DGAF_WORKTREE_DIRTY"):
        _inspect_preflight(dgaf, acp, bindings)


def test_changed_frozen_contract_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    (dgaf / "registry" / "frozen.json").write_text('{"frozen":false}\n', encoding="utf-8")
    _commit_all(dgaf, "change frozen contract")

    with pytest.raises(PreflightError, match="WORKTREE_BLOB_MISMATCH"):
        _inspect_preflight(dgaf, acp, bindings)


def test_receipt_with_wrong_parent_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path, extra_before_receipt=True)

    with pytest.raises(PreflightError, match="RECEIPT_AUTHORIZATION_LINEAGE_INVALID"):
        _inspect_preflight(dgaf, acp, bindings)


def test_git_replace_ref_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    _git(dgaf, "replace", bindings.dgaf_authorization_commit, bindings.dgaf_receipt_commit)

    with pytest.raises(PreflightError, match="DGAF_REPLACE_OBJECTS_PRESENT"):
        _inspect_preflight(dgaf, acp, bindings)


def test_shallow_acp_checkout_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    shallow = tmp_path / "shallow-acp"
    subprocess.run(
        ["git", "clone", "--depth", "1", acp.as_uri(), str(shallow)],
        check=True,
        capture_output=True,
        text=True,
    )

    with pytest.raises(PreflightError, match="ACP_SHALLOW_REPOSITORY"):
        _inspect_preflight(dgaf, shallow, bindings)


def test_restored_authorization_history_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    auth_path = dgaf / "registry" / "aoss_v0_6_stage_a_collection_authorization_v1.json"
    auth_bytes = auth_path.read_text(encoding="utf-8")

    auth_path.write_text('{"status":"TAMPERED"}\n', encoding="utf-8")
    _commit_all(dgaf, "tamper authorization")
    auth_path.write_text(auth_bytes, encoding="utf-8")
    _commit_all(dgaf, "restore authorization")

    with pytest.raises(PreflightError, match="AUTHORIZATION_EVENT_HISTORY_MUTATED"):
        _inspect_preflight(dgaf, acp, bindings)


def test_wrong_authorization_parent_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _inspect_preflight

    dgaf, acp, bindings = _valid_repositories(tmp_path)
    bad = replace(bindings, authorization_parent_commit="0" * 40)

    with pytest.raises(PreflightError, match="AUTHORIZATION_PARENT_INVALID"):
        _inspect_preflight(dgaf, acp, bad)


def test_default_bindings_include_replay_contract_and_schema():
    from scripts.aoss_stage_a.preflight import DEFAULT_BINDINGS

    assert DEFAULT_BINDINGS.auxiliary_blobs == {
        "registry/aoss_v0_6_stage_a_artifact_replay_receipt_contract_v1.json": (
            "1d2b44acb63f30660253e3c96f1a6cac602d62eb"
        ),
        "schemas/aoss_v0_6_stage_a_replay_receipt.schema.json": ("fa1f58aff79320352f285ba41ad85c237adc97cc"),
    }


def test_default_bindings_fix_authorization_parent():
    from scripts.aoss_stage_a.preflight import DEFAULT_BINDINGS

    assert DEFAULT_BINDINGS.authorization_parent_commit == "d11885b9338e7d05493f4cd58dc7f3b11942906e"
