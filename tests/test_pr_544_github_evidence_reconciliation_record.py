from __future__ import annotations

import json
from pathlib import Path

from scripts.reconcile_github_pr_evidence import reconcile

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs/orchestration/records/PR_544_GITHUB_EVIDENCE_SNAPSHOT.json"
REPORT = ROOT / "docs/orchestration/records/PR_544_GITHUB_EVIDENCE_RECONCILIATION_REPORT.json"


def test_retained_pr_544_reconciliation_report_is_reproducible() -> None:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    retained = json.loads(REPORT.read_text(encoding="utf-8"))
    assert reconcile(snapshot, snapshot["pull_request"]["head_sha"]) == retained
    assert retained["reconciliation_status"] == "PASS"
    assert retained["authorization_effect"] == "NONE"
    assert retained["scientific_state_effect"] == "NONE"
