from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_pr_closure_keywords.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_pr_closure_keywords import find_dangerous_closure_syntax  # noqa: E402


class ClosureKeywordPatternTests(unittest.TestCase):
    def test_rejects_negated_close_phrase(self) -> None:
        findings = find_dangerous_closure_syntax("This does not close #310.")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["reference"], "#310")

    def test_rejects_closes_colon(self) -> None:
        self.assertEqual(len(find_dangerous_closure_syntax("Closes: #42")), 1)

    def test_rejects_closed_keyword(self) -> None:
        self.assertEqual(len(find_dangerous_closure_syntax("closed #42")), 1)

    def test_rejects_fix_family(self) -> None:
        for text in ("fix #1", "fixes #2", "fixed #3"):
            with self.subTest(text=text):
                self.assertEqual(len(find_dangerous_closure_syntax(text)), 1)

    def test_rejects_resolve_family(self) -> None:
        for text in ("resolve #1", "resolves #2", "resolved #3"):
            with self.subTest(text=text):
                self.assertEqual(len(find_dangerous_closure_syntax(text)), 1)

    def test_rejects_cross_repo_reference(self) -> None:
        findings = find_dangerous_closure_syntax("This wording does not fix ndrorchestration/DGAF-Framework#310.")
        self.assertEqual(len(findings), 1)

    def test_rejects_full_issue_url(self) -> None:
        findings = find_dangerous_closure_syntax(
            "Resolve https://github.com/ndrorchestration/DGAF-Framework/issues/310"
        )
        self.assertEqual(len(findings), 1)

    def test_rejects_markdown_linked_reference(self) -> None:
        findings = find_dangerous_closure_syntax("Closes [#310](https://example.invalid)")
        self.assertEqual(len(findings), 1)

    def test_neutral_related_reference_passes(self) -> None:
        self.assertEqual(find_dangerous_closure_syntax("Related: #310"), [])

    def test_explicit_open_state_passes(self) -> None:
        self.assertEqual(find_dangerous_closure_syntax("Issue #310 remains OPEN."), [])

    def test_keyword_without_issue_reference_passes(self) -> None:
        self.assertEqual(
            find_dangerous_closure_syntax("Avoid the close/fix/resolve keyword families."),
            [],
        )

    def test_non_issue_identifier_passes(self) -> None:
        self.assertEqual(find_dangerous_closure_syntax("closes ISSUE-310"), [])

    def test_line_provenance(self) -> None:
        findings = find_dangerous_closure_syntax("safe\nnot fixes #7\n")
        self.assertEqual(findings[0]["line"], 2)


class ClosureKeywordCliTests(unittest.TestCase):
    def run_cli(self, event: dict[str, object], *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "event.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--event-path", str(path), *extra],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_event_body_fails_closed(self) -> None:
        event = {
            "pull_request": {
                "body": "This does not close #310.",
                "base": {"ref": "main"},
            }
        }
        result = self.run_cli(event, "--required-base", "main")
        self.assertEqual(result.returncode, 2)
        self.assertIn("FAIL:", result.stdout)

    def test_null_body_passes(self) -> None:
        event = {"pull_request": {"body": None, "base": {"ref": "main"}}}
        result = self.run_cli(event, "--required-base", "main")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS:", result.stdout)

    def test_other_base_is_explicit_skip(self) -> None:
        event = {
            "pull_request": {
                "body": "This does not close #310.",
                "base": {"ref": "development"},
            }
        }
        result = self.run_cli(event, "--required-base", "main")
        self.assertEqual(result.returncode, 0)
        self.assertIn("SKIP:", result.stdout)

    def test_missing_pull_request_fails_input_validation(self) -> None:
        result = self.run_cli({}, "--required-base", "main")
        self.assertEqual(result.returncode, 3)
        self.assertIn("ERROR:", result.stderr)


if __name__ == "__main__":
    unittest.main()
