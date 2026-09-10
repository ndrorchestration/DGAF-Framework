import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = ROOT / "package.json"
PACKAGE_LOCK = ROOT / "package-lock.json"
WORKFLOW = ROOT / ".github" / "workflows" / "npm-lockfile-validation.yml"
REVIEW = ROOT / "docs" / "security" / "DEPENDENCY_PIN_REVIEW_2026-09-09.md"
BOOTSTRAP_LOCK_SHA256 = "d4af9d2195f8b23975ce9389754e74ec4415c087ea633afc9a6b5146743503f6"


class TestNpmLockfileContract(unittest.TestCase):
    def test_lockfile_matches_root_manifest_contract(self) -> None:
        package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
        root = lock["packages"][""]

        self.assertEqual(lock["lockfileVersion"], 3)
        self.assertEqual(lock["name"], package["name"])
        self.assertEqual(lock["version"], package["version"])
        self.assertEqual(root["name"], package["name"])
        self.assertEqual(root["version"], package["version"])
        self.assertEqual(root.get("dependencies", {}), package.get("dependencies", {}))
        self.assertEqual(
            root.get("devDependencies", {}), package.get("devDependencies", {})
        )

    def test_bootstrap_provenance_record_is_retained_not_current_lock_pin(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")

        self.assertIn("Bootstrap provenance:", review)
        self.assertIn(BOOTSTRAP_LOCK_SHA256, review)
        self.assertIn("34427479869", review)
        self.assertIn("10133208552", review)
        self.assertIn(
            "does not constrain the SHA-256 of future reviewed lockfile updates", review
        )

    def test_permanent_workflow_is_read_only_and_lock_consuming(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("python3 tests/test_npm_lockfile_contract.py", workflow)
        self.assertIn("npm ci", workflow)
        self.assertIn("npm run build", workflow)
        self.assertIn("npm install", workflow)
        self.assertIn("--package-lock-only", workflow)
        self.assertIn(
            "cmp --silent /tmp/package-lock.before.json package-lock.json", workflow
        )
        self.assertIn("git diff --exit-code -- package-lock.json", workflow)
        self.assertNotIn("git push", workflow)
        self.assertIn("package-lock.json", workflow)

    def test_one_time_bootstrap_workflow_is_not_retained(self) -> None:
        self.assertFalse(
            (ROOT / ".github" / "workflows" / "npm-lockfile-bootstrap.yml").exists()
        )


if __name__ == "__main__":
    unittest.main()
