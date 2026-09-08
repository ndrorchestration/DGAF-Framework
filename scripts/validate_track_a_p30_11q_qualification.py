#!/usr/bin/env python3
"""Validate Track A source-bound P-30/11Q profile qualification."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUAL = ROOT / "docs/qa/APOGEE_11Q_PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_S078.json"
PROFILE = ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json"
PROFILE_MD = ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.md"
PROBE = ROOT / "experiments/pdmal_pilot/topology_robustness_profile.py"
TESTS = ROOT / "experiments/pdmal_pilot/test_topology_robustness_profile.py"
WORKFLOW = ROOT / ".github/workflows/track-a-topology-robustness-profile.yml"

EXPECTED = {
    PROFILE: "339d9ada4978ffd0c1eee67c310323f1e7fdc06a",
    PROFILE_MD: "d0e2e48ea670404cced48c5d20c3829faba52279",
    PROBE: "5b703273f26bde700fff03269c1734d89b2b347d",
    TESTS: "e94f8cbb4cef3ebae6bee5e2220f1ff0c7cc4856",
    WORKFLOW: "fbad06eec3ca6f4c7edc912e3f80f0c3b31e0404",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def main() -> int:
    q = json.loads(QUAL.read_text(encoding="utf-8"))
    p = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert q["record_type"] == "DGAF_P30_11Q_PROFILE_QUALIFICATION"
    assert q["attestation_gate"] == "P-30"
    assert q["profile_id"] == p["profile_id"] == "PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1"
    assert q["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert q["independent_verification"] is False
    assert q["empirical_evidence"] is False
    assert q["scientific_n_increment"] == 0

    for path, expected in EXPECTED.items():
        actual = git_blob(path)
        assert actual == expected, f"source blob drift: {path}: {actual} != {expected}"

    b = q["source_bindings"]
    assert b["architecture_merge_sha"] == "5e4f00a065c00cefec0b3a79c32b88a5f36a55c2"
    assert b["profile_merge_sha"] == "b1e333ee9f9e0a4da78788e5ff019603296888eb"
    assert b["profile_blob_sha"] == EXPECTED[PROFILE]
    assert b["profile_doc_blob_sha"] == EXPECTED[PROFILE_MD]
    assert b["probe_blob_sha"] == EXPECTED[PROBE]
    assert b["probe_test_blob_sha"] == EXPECTED[TESTS]
    assert b["workflow_blob_sha"] == EXPECTED[WORKFLOW]
    assert b["retained_artifact_id"] == 10041800252
    assert b["retained_artifact_digest"] == "sha256:629ee0be7a48606685f2452800ab4e482611fb45f7268d881e934488e1c1c1d5"
    assert b["exact_head_workflows_passed"] == "20/20"

    scores = q["scoring"]
    assert set(scores) == {f"Q{i:02d}" for i in range(1, 12)}
    total = sum(item["score"] for item in scores.values())
    assert total == q["scoring_summary"]["total_score"] == 108
    assert q["scoring_summary"]["max_score"] == 110
    assert q["scoring_summary"]["tier"] == "S-TIER"
    assert q["scoring_summary"]["q11_score"] == scores["Q11"]["score"] == 9
    assert q["scoring_summary"]["q11_threshold_met"] is True
    assert q["scoring_summary"]["attestation_result"] == "GRANTED"

    assert p["scientific_n_increment"] == 0
    assert p["empirical_authorization"] is False
    assert q["next_gate"]["required"] == "TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION"
    assert q["next_gate"]["empirical_execution"] == "NOT_AUTHORIZED"
    assert q["next_gate"]["high_assurance_changed"] is False

    print("TRACK_A_P30_11Q_QUALIFICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
