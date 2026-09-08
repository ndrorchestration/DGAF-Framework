#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "docs/governance/B2_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json"
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1_S079.json"
PROFILE = ROOT / "docs/governance/DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1.json"
SOURCE = ROOT / "components/ensemble_v17.py"
HARNESS = ROOT / "experiments/pdmal_pilot/b2_stateful_context_closure_profile.py"
TESTS = ROOT / "experiments/pdmal_pilot/test_b2_stateful_context_closure_profile.py"
PROFILE_VALIDATOR = ROOT / "scripts/validate_b2_stateful_context_closure_profile.py"
PROFILE_WORKFLOW = ROOT / ".github/workflows/b2-stateful-context-closure-profile.yml"

EXPECTED = {
    QUAL: "035c690354be7acd5fbbfa2bcd95967d9c0a65c8",
    PROFILE: "306cd38952b979276908789bd042a3e3323c5ac3",
    SOURCE: "686eb9ba339742d9de2767fca18b9907a1c3b70a",
    HARNESS: "765dd5dd50f0590c6ee3c2c805c7e6144c4e86eb",
    TESTS: "a205b878bf17f2160d323aa6e79b31ffa242d6b0",
    PROFILE_VALIDATOR: "294af500f20aec2a40d443fbfb299792a0f61172",
    PROFILE_WORKFLOW: "a239ff486816d1e7b5414334b7342b7a2873c4ee",
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def main() -> int:
    a = json.loads(ADJ.read_text(encoding="utf-8"))
    q = json.loads(QUAL.read_text(encoding="utf-8"))
    p = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert a["record_type"] == "DGAF_B2_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
    assert a["controller_issue"] == 427
    assert a["profile_id"] == p["profile_id"] == q["profile_id"]
    assert a["implementation_merge_sha"] == "9e6971d5c8fc39e46acfe743e6588bbdc127abe8"
    assert a["qualification_merge_sha"] == "a82c56894f1334279dd62adc2b858c924d5ba05f"

    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"

    assert q["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert q["scoring_summary"]["total_score"] == 108
    assert q["scoring_summary"]["max_score"] == 110
    assert q["scoring_summary"]["tier"] == "S-TIER"
    assert q["scoring_summary"]["q11_score"] == 9
    assert q["independent_verification"] is False

    assert p["persistence"]["lifetime"] == "ONE_COMPLETE_SESSION"
    assert p["persistence"]["reset"] == "ONLY_AT_SESSION_BOUNDARY"
    assert p["registered_phi_checkpoints"] == [13, 21, 34, 55]
    assert p["known_source_limitation"]["silent_redesign_allowed"] is False

    assert set(a["adjudication"].values()) == {"PASS"}
    assert a["disposition"] == "PASS_B2_STANDALONE_NONEMPIRICAL_LANE_COMPLETE"
    assert a["scientific_n_increment"] == 0
    assert a["b2_empirical_execution_authorized"] is False
    assert a["track_c_empirical_execution_authorized"] is False
    assert a["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert a["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("B2_NONEMPIRICAL_INTEGRATION_ADJUDICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
