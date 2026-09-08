#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json"
PROTOCOL = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/track_a_epoch_001_analysis.py"

EXPECTED_PROTOCOL_BLOB = "52148950ff054a407c2e6b5cf36103695cf96474"
EXPECTED_ANALYSIS_BLOB = "1ae463614de770314315527156916a5b5229cfdd"
EXPECTED_CONFIG_SHA256 = "355b164f69e91405819f092d0721b7597b87b06de79394a0c451169410a5ab6d"


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def load_analysis():
    spec = importlib.util.spec_from_file_location("track_a_epoch_001_analysis", ANALYSIS)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    analysis = load_analysis()

    assert lock["record_type"] == "TRACK_A_EPOCH_001_ANALYSIS_LOCK"
    assert lock["controller_issue"] == 415
    assert lock["preregistration_merge_sha"] == "26077b27ca336454148006e6daf4cd087005b421"
    assert git_blob(PROTOCOL) == EXPECTED_PROTOCOL_BLOB
    assert git_blob(ANALYSIS) == EXPECTED_ANALYSIS_BLOB
    assert lock["preregistration_blob_sha"] == EXPECTED_PROTOCOL_BLOB
    assert lock["analysis_blob_sha"] == EXPECTED_ANALYSIS_BLOB
    assert analysis.analysis_config_sha256() == EXPECTED_CONFIG_SHA256
    assert lock["analysis_config_sha256"] == EXPECTED_CONFIG_SHA256

    p = protocol["primary_analysis"]
    c = lock["primary_contract"]
    assert c["seed_count"] == protocol["matrix"]["seed_count"] == 50
    assert c["expected_total_records"] == protocol["matrix"]["expected_total_observations"] == 2250
    assert c["endpoint"] == protocol["endpoint"]["field"] == "ffcr_success"
    assert c["primary_topology"] == p["primary_topology"] == "pdmal"
    assert c["primary_comparator"] == p["primary_comparator"] == "random_regular"
    assert c["bootstrap_resamples"] == p["bootstrap_resamples"] == 10000
    assert c["bootstrap_seed"] == p["bootstrap_seed"] == 20270151
    assert c["alpha"] == p["alpha"] == 0.05
    assert c["confirmatory_test_count"] == protocol["multiplicity_policy"]["confirmatory_test_count"] == 1

    b = lock["boundaries"]
    assert b["runner_implemented_by_this_lock"] is False
    assert b["collection_authorized"] is False
    assert b["unblinding_authorized"] is False
    assert b["scientific_n_increment"] == 0
    assert b["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert b["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("TRACK_A_EPOCH_001_ANALYSIS_LOCK_PASS_NONEMPIRICAL")


if __name__ == "__main__":
    main()
