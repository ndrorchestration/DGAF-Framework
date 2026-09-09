#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "docs/governance/B1_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json"
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1_S081.json"
PROFILE = ROOT / "docs/governance/DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1.json"
EXPECTED = {
    QUAL: "820b23e1b620d61228f73143533a755b845e8728",
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
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def main() -> int:
    a = json.loads(ADJ.read_text(encoding="utf-8"))
    q = json.loads(QUAL.read_text(encoding="utf-8"))
    p = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert a["record_type"] == "DGAF_B1_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
    assert a["controller_issue"] == 445
    assert a["profile_id"] == p["profile_id"] == q["profile_id"]
    assert a["implementation_merge_sha"] == "002f6c7037c7e72c31c39499cba97681da76a962"
    assert a["qualification_merge_sha"] == "f94be1b096565a7909ed79a298fe380f56a09b1b"
    assert a["qualification_blob_sha"] == EXPECTED[QUAL]

    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"

    assert q["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert q["scoring_summary"]["total_score"] == 107
    assert q["scoring_summary"]["max_score"] == 110
    assert q["scoring_summary"]["tier"] == "S-TIER"
    assert q["scoring_summary"]["q11_score"] == 9
    assert q["scoring_summary"]["attestation_result"] == "GRANTED_WITH_EXPLICIT_SOURCE_LIMITATIONS"
    assert q["independent_verification"] is False
    assert q["scoring"]["Q07"]["score"] == 8

    assert p["known_source_limitation"]["silent_redesign_allowed"] is False
    assert p["known_source_limitation"]["interpretation"] == "PRESERVE_AND_REPORT_LIMITATION"
    assert p["excluded_components"] == {"P-31": "B2_ONLY", "P-32": "B2_ONLY", "P-33": "B3_ONLY"}
    assert p["prohibited"]["efficacy_estimation"] is True
    assert p["prohibited"]["historical_epoch_pooling"] is True
    assert p["prohibited"]["empirical_execution"] is True

    limitations = " ".join(q["limitations"])
    assert "reprompt remains unreachable" in limitations
    assert "narrow KAPPA-derived confidence region" in limitations

    assert set(a["adjudication"].values()) == {"PASS"}
    assert a["disposition"] == "PASS_B1_STANDALONE_NONEMPIRICAL_LANE_COMPLETE"
    assert a["scientific_n_increment"] == 0
    assert a["b1_empirical_execution_authorized"] is False
    assert a["track_c_empirical_execution_authorized"] is False
    assert a["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert a["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("B1_NONEMPIRICAL_INTEGRATION_ADJUDICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
