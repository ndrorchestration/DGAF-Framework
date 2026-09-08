#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "docs/experiment/CANONICAL_SOLO_EPOCH_004_PRIMARY_RESULT.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/analysis.py"
EXPECTED_ANALYSIS_BLOB = "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
EXPECTED_CONFIG_SHA256 = "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


def main() -> int:
    d = json.loads(RESULT.read_text(encoding="utf-8"))
    assert d["record_type"] == "DGAF_CANONICAL_SOLO_EPOCH_PRIMARY_RESULT"
    assert d["epoch_id"] == "PDMAL-SOLO-CANONICAL-EPOCH-004"
    assert d["validation_track"] == "SOLO_DEVELOPER"
    assert d["independent_verification"] is False
    assert d["frozen_collection_sha"] == "9725ffd80d5386826d61b7f824524f7f8d89fce8"
    assert d["runner_parent_sha"] == "647de0607dbcef1f2bcc77e009264527f2fda9d6"
    assert d["execution_run_id"] == 34181212217
    assert d["dataset_artifact"]["id"] == 10039138297
    assert d["dataset_artifact"]["digest"] == "sha256:6a11f4748eb40e10fa2c0476f759fb800bb43181a266ec3e0b4a457c7b7d1876"
    assert d["dataset_artifact"]["seed_count"] == 50
    assert d["dataset_artifact"]["observations"] == 9000
    assert d["dataset_artifact"]["outcomes_inspected_by_collection_workflow"] is False
    assert d["key_artifact"]["id"] == 10039138610
    assert d["key_artifact"]["digest"] == "sha256:dc4c0aada6baaed556eabd4ad179b945228600959a78b48b8620b144e28d1a68"
    assert d["key_artifact"]["key_value_published"] is False
    assert d["historical_pooling_allowed"] is False
    locked = d["locked_primary_analysis"]
    assert git_blob(ANALYSIS) == EXPECTED_ANALYSIS_BLOB
    assert locked["statistical_source_blob_sha"] == EXPECTED_ANALYSIS_BLOB
    assert locked["analysis_config_sha256"] == EXPECTED_CONFIG_SHA256
    assert locked["primary_contrast"] == "dgaf-vs-null"
    assert locked["estimand"] == "mean_seed_paired_ffcr_difference"
    assert locked["paired_seeds"] == 50
    assert locked["bootstrap_resamples"] == 10000
    assert locked["bootstrap_seed"] == 20260823
    assert locked["alpha"] == 0.05
    r = d["result"]
    assert r["dgaf_ffcr"] == 0.7337777777777778
    assert r["null_ffcr"] == 0.8275555555555555
    assert r["paired_effect_dgaf_minus_null"] == -0.0937777777777778
    assert r["two_sided_95pct_ci"] == [-0.11822222222222223, -0.07066666666666668]
    assert r["classification"] == "EVIDENCE_AGAINST_DIRECTIONAL_DGAF"
    assert r["paired_effect_dgaf_minus_null"] <= 0
    assert r["two_sided_95pct_ci"][1] < 0
    assert d["claim_ceiling"]["independent_validation"] == "NOT_ESTABLISHED"
    assert d["claim_ceiling"]["high_assurance"] == "NOT_AUTHORIZED_N0"
    assert d["claim_ceiling"]["universal_dgaf_inferiority"] == "NOT_ESTABLISHED"
    print("CANONICAL_EPOCH_004_PRIMARY_RESULT_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
