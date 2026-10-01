import hashlib
import json
import runpy
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_semantic_source_git_bindings.py"

module = runpy.run_path(str(SCRIPT))
verify_manifest_bindings = module["verify_manifest_bindings"]


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def init_repo(tmp_path: Path) -> tuple[Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Semantic Binding Test")

    artifact = repo / "artifact.txt"
    artifact.write_text("alpha\n", encoding="utf-8")
    git(repo, "add", "artifact.txt")
    git(repo, "commit", "-m", "seed")

    commit = git(repo, "rev-parse", "HEAD")
    blob = git(repo, "rev-parse", "HEAD:artifact.txt")
    return repo, commit, blob


def manifest(commit: str, blob: str) -> dict:
    return {
        "repository_commit": commit,
        "artifacts": [
            {
                "path": "artifact.txt",
                "git_blob_sha1": blob,
                "role": "fixture",
            }
        ],
    }


def test_correct_path_blob_binding_passes(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    assert verify_manifest_bindings(manifest(commit, blob), repo) == []


def test_declared_blob_mismatch_fails(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    value = manifest(commit, "f" * 40)
    errors = verify_manifest_bindings(value, repo)
    assert len(errors) == 1
    assert "does not match" in errors[0]
    assert blob in errors[0]


def test_missing_path_fails(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    value = manifest(commit, blob)
    value["artifacts"][0]["path"] = "missing.txt"
    errors = verify_manifest_bindings(value, repo)
    assert len(errors) == 1
    assert "missing.txt" in errors[0]


def test_historical_commit_binding_is_verified_not_worktree_state(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    (repo / "artifact.txt").write_text("beta\n", encoding="utf-8")
    git(repo, "add", "artifact.txt")
    git(repo, "commit", "-m", "advance")

    assert verify_manifest_bindings(manifest(commit, blob), repo) == []


def test_worktree_bytes_do_not_substitute_for_git_object_identity(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    (repo / "artifact.txt").write_text("uncommitted-change\n", encoding="utf-8")
    assert verify_manifest_bindings(manifest(commit, blob), repo) == []


def test_blob_identity_matches_git_blob_hash_construction(tmp_path):
    repo, commit, blob = init_repo(tmp_path)
    payload = b"alpha\n"
    expected = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
    assert blob == expected
    assert verify_manifest_bindings(manifest(commit, blob), repo) == []
