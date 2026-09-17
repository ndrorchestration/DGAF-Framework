from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "pptl" / "experiments"
MANIFEST = EXPERIMENTS / "h4_experiment_manifest.json"
NOTICE = EXPERIMENTS / "EVIDENCE_STATUS.md"
RAW = EXPERIMENTS / "h4_raw_results.csv"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_h4_manifest_is_explicitly_synthetic_historical() -> None:
    manifest = _manifest()

    assert manifest["evidence_status"] == "SYNTHETIC_HISTORICAL"
    assert manifest["empirical_efficacy_evidence"] is False
    assert "runner" not in manifest

    provenance = manifest["provenance"]
    assert isinstance(provenance, dict)
    assert provenance["historical_runner_claim"] == "pptl/experiments/h4_task_stratified.py"
    assert provenance["runner_binding_status"] == "CONTRADICTED"
    assert provenance["verified_runner"] is None
    assert provenance["raw_population_status"] == "INCOMPLETE_NOT_VERIFIED"


def test_h4_manifest_records_retained_raw_population_without_promoting_it() -> None:
    manifest = _manifest()
    provenance = manifest["provenance"]
    assert isinstance(provenance, dict)

    with RAW.open(newline="", encoding="utf-8") as handle:
        retained_rows = sum(1 for _ in csv.DictReader(handle))

    assert retained_rows == 80
    assert provenance["declared_total_runs"] == 2520
    assert provenance["retained_raw_rows"] == retained_rows
    assert provenance["full_raw_population_retained"] is False


def test_h4_evidence_notice_blocks_empirical_promotion() -> None:
    notice = NOTICE.read_text(encoding="utf-8")

    required = (
        "SYNTHETIC / HISTORICAL",
        "not empirical efficacy evidence",
        "runner binding is contradicted",
        "80 retained data rows",
        "2,520",
        "TRIAD-EXP-001",
    )
    for phrase in required:
        assert phrase in notice
