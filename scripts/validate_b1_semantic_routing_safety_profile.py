#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "docs/governance/DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1.json"

EXPECTED = {
    ROOT / "components/KAPPA/dynamic_weight_router.py": "8a2193a810c22bf6732f1a7f08650e06b8fbff08",
    ROOT / "components/evaluate_router.py": "8c141231bae3fcb0321f0c306ada068e5d369546",
    ROOT / "components/evaluate_router_v1_1.py": "3ece02b81e0b8bf331eb1e769a8225ab87af322a",
    ROOT / "components/ensemble_v17.py": "686eb9ba339742d9de2767fca18b9907a1c3b70a",
    ROOT / "experiments/pdmal_pilot/b1_semantic_routing_safety_profile.py": "14c81690e0caa33635565018a3746bec3820b718",
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def main() -> None:
    d = json.loads(PROFILE.read_text(encoding="utf-8"))
    assert d["profile_id"] == "DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1"
    assert d["controller_issue"] == 400
    assert d["status"] == "NONEMPIRICAL_PROFILE_CANDIDATE"

    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"

    b = d["source_bindings"]
    assert b["kappa_blob_sha"] == EXPECTED[ROOT / "components/KAPPA/dynamic_weight_router.py"]
    assert b["evaluate_router_blob_sha"] == EXPECTED[ROOT / "components/evaluate_router.py"]
    assert b["sentinel_blob_sha"] == EXPECTED[ROOT / "components/evaluate_router_v1_1.py"]
    assert b["demijoule_blob_sha"] == EXPECTED[ROOT / "components/ensemble_v17.py"]
    assert b["harness_blob_sha"] == EXPECTED[ROOT / "experiments/pdmal_pilot/b1_semantic_routing_safety_profile.py"]

    assert d["registered_fixtures"] == [
        "clean-governance",
        "ambiguous-mixed",
        "adversarial",
        "low-confidence-balanced",
        "deontic-forbidden",
    ]
    assert d["required_behavior"]["adversarial_kappa_policy"] == "apply_strong"
    assert d["required_behavior"]["deontic_forbidden_sentinel_risk"] == "risk_block"
    assert d["required_behavior"]["low_confidence_nonforbidden_sentinel_risk"] == "risk_warn"
    assert d["known_source_limitation"]["silent_redesign_allowed"] is False
    assert d["p30_disposition"] == "EXTERNAL_PROFILE_QUALIFICATION_REQUIRED_AFTER_IMPLEMENTATION"

    assert d["prohibited"]["efficacy_estimation"] is True
    assert d["prohibited"]["historical_epoch_pooling"] is True
    assert d["prohibited"]["numeric_proxy_for_semantic_input"] is True
    assert d["prohibited"]["empirical_execution"] is True
    assert d["scientific_n_increment"] == 0
    assert d["empirical_execution_authorized"] is False
    assert d["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert d["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("B1_SEMANTIC_ROUTING_SAFETY_PROFILE_SOURCE_BINDING_PASS_NONEMPIRICAL")


if __name__ == "__main__":
    main()
