import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = ROOT / "package.json"
PACKAGE_LOCK = ROOT / "package-lock.json"
WORKFLOW = ROOT / ".github" / "workflows" / "npm-lockfile-validation.yml"
REVIEW = ROOT / "docs" / "security" / "DEPENDENCY_PIN_REVIEW_2026-09-09.md"
EXPECTED_LOCK_SHA256 = "d4af9d2195f8b23975ce9389754e74ec4415c087ea633afc9a6b5146743503f6"


def test_lockfile_matches_root_manifest_contract() -> None:
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    root = lock["packages"][""]

    assert lock["lockfileVersion"] == 3
    assert lock["name"] == package["name"]
    assert lock["version"] == package["version"]
    assert root["name"] == package["name"]
    assert root["version"] == package["version"]
    assert root.get("dependencies", {}) == package.get("dependencies", {})
    assert root.get("devDependencies", {}) == package.get("devDependencies", {})


def test_retained_lockfile_bytes_match_bootstrap_provenance() -> None:
    digest = hashlib.sha256(PACKAGE_LOCK.read_bytes()).hexdigest()
    assert digest == EXPECTED_LOCK_SHA256
    review = REVIEW.read_text(encoding="utf-8")
    assert EXPECTED_LOCK_SHA256 in review
    assert "34427479869" in review
    assert "10133208552" in review


def test_permanent_workflow_is_read_only_and_lock_consuming() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "npm ci" in workflow
    assert "npm run build" in workflow
    assert "npm install" in workflow
    assert "--package-lock-only" in workflow
    assert "cmp --silent /tmp/package-lock.before.json package-lock.json" in workflow
    assert "git diff --exit-code -- package-lock.json" in workflow
    assert "git push" not in workflow
    assert "package-lock.json" in workflow


def test_one_time_bootstrap_workflow_is_not_retained() -> None:
    assert not (ROOT / ".github" / "workflows" / "npm-lockfile-bootstrap.yml").exists()
