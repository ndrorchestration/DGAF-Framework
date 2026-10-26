"""Fail-closed local tests for the non-admitting Python 3.10 resolver experiment."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import py310_test_resolution_feasibility as proof


class ResolutionFeasibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "requirements-ci.txt"
        self.source.write_text(
            "# pinned CI tools\npytest==9.1.1\nblack==26.5.1\n" "setuptools==83.0.0\npip-audit==2.10.1\n",
            encoding="utf-8",
        )
        self.out = self.root / "evidence"
        proof.prepare(self.source, self.out)

    def make_report(self, *, extra=None, interpreter="3.10", skip=None, version="1") -> Path:
        candidate = {"pytest": "9.1.1", "black": "26.10.1", "setuptools": "84.1.0"}
        candidate.update(extra or {})
        if skip:
            candidate.pop(skip)
        data = {
            "version": version,
            "environment": {"python_version": interpreter},
            "install": [{"metadata": {"name": name, "version": ver}} for name, ver in candidate.items()],
        }
        target = self.out / "pip-report.json"
        target.write_text(json.dumps(data), encoding="utf-8")
        return target

    def test_preparation_does_not_rewrite_baseline(self) -> None:
        candidate = (self.out / "py310-test-only-research.in").read_text()
        self.assertIn("black==26.10.1", candidate)
        self.assertIn("setuptools==84.1.0", candidate)
        self.assertIn("pytest==9.1.1", candidate)
        self.assertNotIn("pip-audit==", candidate)
        self.assertIn("pip-audit==2.10.1", self.source.read_text())

    def test_graph_split_provisional_not_security_cleared(self) -> None:
        report = proof.evaluate(self.out, self.make_report())
        self.assertEqual(report["status"], "GRAPH_SPLIT_FEASIBLE_NOT_SECURITY_CLEARED")
        self.assertEqual(report["security_clearance"], "NOT_ESTABLISHED")
        self.assertEqual(report["scanner_chain_packages_still_present"], [])
        self.assertEqual(len(report["pip_report_sha256"]), 64)

    def test_filelock_retention_blocks_split(self) -> None:
        report = proof.evaluate(self.out, self.make_report(extra={"filelock": "4.0.3"}))
        self.assertEqual(report["status"], "SCANNER_CHAIN_STILL_PRESENT")

    def test_missing_direct_requirement_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing or changed"):
            proof.evaluate(self.out, self.make_report(skip="black"))

    def test_wrong_direct_version_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing or changed"):
            proof.evaluate(self.out, self.make_report(extra={"black": "26.5.1"}))

    def test_wrong_interpreter_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Python 3.10"):
            proof.evaluate(self.out, self.make_report(interpreter="3.11"))

    def test_unknown_report_schema_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "schema"):
            proof.evaluate(self.out, self.make_report(version="2"))

    def test_duplicate_resolved_package_rejected(self) -> None:
        report = self.make_report()
        source = json.loads(report.read_text())
        source["install"].append({"metadata": {"name": "Black", "version": "26.10.1"}})
        report.write_text(json.dumps(source))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            proof.evaluate(self.out, report)

    def test_changed_candidate_source_rejected(self) -> None:
        path = self.out / "py310-test-only-research.in"
        path.write_text(path.read_text() + "# injected\n")
        with self.assertRaisesRegex(ValueError, "changed"):
            proof.evaluate(self.out, self.make_report())

    def test_unapproved_baseline_pin_rejected(self) -> None:
        self.source.write_text("pytest==9.1.1\nblack==26.10.1\nsetuptools==83.0.0\npip-audit==2.10.1\n")
        with self.assertRaisesRegex(ValueError, "baseline pins drifted"):
            proof.prepare(self.source, self.root / "other")

    def test_duplicate_direct_requirement_rejected(self) -> None:
        self.source.write_text(self.source.read_text() + "PYTEST==9.1.1\n")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            proof.prepare(self.source, self.root / "other")


if __name__ == "__main__":
    unittest.main()
