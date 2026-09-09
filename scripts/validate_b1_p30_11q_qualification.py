#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1_S081.json"
PROFILE = ROOT / "docs/governance/DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1.json"
EXPECTED = {
    PROFILE: "692f5d1acaa68725e65b0e835fc96d9979253dd8",
    ROOT / "components/KAPPA/dynamic_weight_router.py": "8a2193a810c22bf6732f1a7f08650e06b8fbff08",
    ROOT / "components/evaluate_router.py": "8c141231bae3fcb0321f0c306ada068e5d369546",
    ROOT / "components/evaluate_router_v1_1.py": "3ece02b81e0b8bf331eb1e769a8225ab87af322a",
    ROOT / "components/ensemble_v17.py": "686eb9ba339742d9de2767fca18b9907a1c3b70a",
    ROOT / "experiments/pdmal_pilot/b1_semantic_routing_safety_profile.py": "0ac0841259fad8d333e620ad54f1f81e238c4074",
    ROOT / "experiments/pdmal_pilot/test_b1_semantic_routing_safety_profile.py": "0ca9d200018e2aa1855d876ad3f7e3f5464bb1af",
    ROOT / "scripts/validate_b1_semantic_routing_safety_profile.py": "33c8bbe39e709126439e69eed492e7137450efbc",
    ROOT / ".github/workflows/b1-semantic-routing-safety-profile.yml": "7a711fc3e7779e7056c88a6efe877fcb1cead5ec",
}


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


def main() -> int:
    q = json.loads(QUAL.read_text(encoding="utf-8"))
    p = json.loads(PROFILE.read_text(encoding="utf-8"))
    assert q["record_type"] == "DGAF_P30_11Q_PROFILE_QUALIFICATION"
    assert q["profile_id"] == p["profile_id"] == "DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1"
    assert q["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert q["independent_verification"] is False
    assert q["empirical_evidence"] is False
    assert q["scientific_n_increment"] == 0
    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"
    b = q["source_bindings"]
    assert b["profile_merge_sha"] == "002f6c7037c7e72c31c39499cba97681da76a962"
    assert b["profile_blob_sha"] == EXPECTED[PROFILE]
    assert b["harness_blob_sha"] == EXPECTED[ROOT / "experiments/pdmal_pilot/b1_semantic_routing_safety_profile.py"]
    scores = q["scoring"]
    assert set(scores) == {f"Q{i:02d}" for i in range(1, 12)}
    assert sum(item["score"] for item in scores.values()) == q["scoring_summary"]["total_score"] == 107
    assert q["scoring_summary"]["max_score"] == 110
    assert q["scoring_summary"]["tier"] == "S-TIER"
    assert q["scoring_summary"]["q11_score"] == 9
    assert q["scoring_summary"]["attestation_result"] == "GRANTED_WITH_EXPLICIT_SOURCE_LIMITATIONS"
    assert scores["Q07"]["score"] == 8
    assert p["known_source_limitation"]["silent_redesign_allowed"] is False
    assert p["prohibited"]["efficacy_estimation"] is True
    assert p["prohibited"]["empirical_execution"] is True
    assert q["next_gate"]["required"] == "B1_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
    assert q["next_gate"]["empirical_execution"] == "NOT_AUTHORIZED"
    assert q["next_gate"]["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert q["next_gate"]["high_assurance_changed"] is False
    print("B1_P30_11Q_QUALIFICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
