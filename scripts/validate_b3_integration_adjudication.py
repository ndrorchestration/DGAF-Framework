#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "docs/governance/B3_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json"
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1_S080.json"
PROFILE = ROOT / "docs/governance/DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1.json"
SOURCE = ROOT / "components/ensemble_v17.py"
HARNESS = ROOT / "experiments/pdmal_pilot/b3_p33_convergence_profile.py"
TESTS = ROOT / "experiments/pdmal_pilot/test_b3_p33_convergence_profile.py"
PROFILE_VALIDATOR = ROOT / "scripts/validate_b3_p33_convergence_profile.py"
PROFILE_WORKFLOW = ROOT / ".github/workflows/b3-p33-convergence-profile.yml"

EXPECTED = {
    QUAL: "b4701dfc091b6df3cf36061e5ab154c095a9aeaf",
    PROFILE: "258a490a7e431be9d58e08b88e037ef1d9589ded",
    SOURCE: "686eb9ba339742d9de2767fca18b9907a1c3b70a",
    HARNESS: "3cb8cfd7aa881be241d03a2d3ce08e10e3b2d8f7",
    TESTS: "4c7053dccba13ae0ff420d631701aae875d89694",
    PROFILE_VALIDATOR: "11680dcf0ace99f7abaf94ac83952f25990125fd",
    PROFILE_WORKFLOW: "445fb8765b2c07fb44b960b82f55a95f151f4c31",
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def main() -> int:
    a = json.loads(ADJ.read_text(encoding="utf-8"))
    q = json.loads(QUAL.read_text(encoding="utf-8"))
    p = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert a["record_type"] == "DGAF_B3_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
    assert a["controller_issue"] == 429
    assert a["profile_id"] == p["profile_id"] == q["profile_id"]
    assert a["implementation_merge_sha"] == "114312db125439ae861065e36d3b0d37ffe32d14"
    assert a["qualification_merge_sha"] == "68c94a53718915ae909eb2196373283186a95138"

    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"

    assert q["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert q["scoring_summary"]["total_score"] == 108
    assert q["scoring_summary"]["max_score"] == 110
    assert q["scoring_summary"]["tier"] == "S-TIER"
    assert q["scoring_summary"]["q11_score"] == 9
    assert q["independent_verification"] is False

    assert p["persistence"]["lifetime"] == "ONE_GRAPH_SEQUENCE"
    assert p["persistence"]["reset"] == "ONLY_AT_SEQUENCE_BOUNDARY"
    assert p["registered_sequence"]["expected_statuses"] == [
        "stable", "watch", "warn", "alert", "stable", "stable", "converged"
    ]
    assert p["prohibited"]["consensus_alpha_mapping"] is True
    assert p["prohibited"]["epoch_004_outcome_reuse"] is True

    assert set(a["adjudication"].values()) == {"PASS"}
    assert a["disposition"] == "PASS_B3_STANDALONE_NONEMPIRICAL_LANE_COMPLETE"
    assert a["scientific_n_increment"] == 0
    assert a["b3_empirical_execution_authorized"] is False
    assert a["track_c_empirical_execution_authorized"] is False
    assert a["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert a["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("B3_NONEMPIRICAL_INTEGRATION_ADJUDICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
