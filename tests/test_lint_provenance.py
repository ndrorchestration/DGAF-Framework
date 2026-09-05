from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lint_provenance", ROOT / "scripts" / "lint_provenance.py")
assert SPEC and SPEC.loader
lint = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lint
SPEC.loader.exec_module(lint)


def _registry() -> dict:
    return json.loads((ROOT / "docs" / "qa" / "METRICS_PROVENANCE.json").read_text(encoding="utf-8"))


class ProvenanceRegistryTests(unittest.TestCase):
    def test_current_registry_is_fail_closed_and_valid(self) -> None:
        findings = lint.validate_registry(_registry())
        self.assertFalse([finding for finding in findings if finding.level == "ERROR"])

    def test_dependency_block_prevents_verified_promotion(self) -> None:
        data = copy.deepcopy(_registry())
        metric = next(item for item in data["metrics"] if item["metric_id"] == "M-P34-945")
        metric.update(
            {
                "epistemic_status": "VERIFIED",
                "calculation_method": "synthetic test method",
                "dataset_or_corpus": "synthetic test corpus",
                "baseline": "synthetic baseline",
                "configuration_identity": "synthetic-config",
                "source_commit": "0" * 40,
                "execution": {"workflow_run_id": "1", "artifact_id": "2", "timestamp": "2026-09-04T00:00:00Z"},
                "reproduction": {"status": "REPRODUCIBLE", "command": "python synthetic.py"},
            }
        )
        messages = [finding.message for finding in lint.validate_registry(data) if finding.level == "ERROR"]
        self.assertTrue(any("VERIFIED blocked by dependencies" in message for message in messages))

    def test_verified_requires_retained_execution_identity(self) -> None:
        data = copy.deepcopy(_registry())
        for dependency in data["dependency_registry"]:
            if dependency["dependency_id"] == "P-10-INSTRUMENT":
                dependency["epistemic_status"] = "VERIFIED"
        metric = next(item for item in data["metrics"] if item["metric_id"] == "M-P10-SPEED")
        metric.update(
            {
                "epistemic_status": "VERIFIED",
                "calculation_method": "synthetic test method",
                "score_range": "unbounded positive change",
                "dataset_or_corpus": "synthetic test corpus",
                "baseline": "synthetic baseline",
                "configuration_identity": "synthetic-config",
                "source_commit": "0" * 40,
                "reproduction": {"status": "REPRODUCIBLE", "command": "python synthetic.py"},
            }
        )
        messages = [finding.message for finding in lint.validate_registry(data) if finding.level == "ERROR"]
        self.assertTrue(any("requires workflow_run_id, artifact_id, and timestamp" in message for message in messages))

    def test_historical_claims_do_not_require_fabricated_evidence(self) -> None:
        data = _registry()
        metric = next(item for item in data["metrics"] if item["metric_id"] == "M-P36-MTTE")
        self.assertEqual(metric["epistemic_status"], "HISTORICAL_UNVERIFIED")
        self.assertFalse([finding for finding in lint.validate_registry(data) if finding.level == "ERROR"])


if __name__ == "__main__":
    unittest.main()
