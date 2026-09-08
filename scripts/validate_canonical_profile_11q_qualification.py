#!/usr/bin/env python3
"""Validate the source-bound developer P-30/P-11 11Q qualification."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "experiments/pdmal_pilot"
sys.path.insert(0, str(PILOT))

from canonical_p30_qualification import verify_qualification_artifact  # noqa: E402

QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.json"
BINDING = ROOT / "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.binding.json"
PROFILE = ROOT / "docs/governance/CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE_V1.json"
EXPECTED_PROFILE_BLOB = "133d7b71c9e829d5461e7c911527c6b2b10ba9ae"
EXPECTED_SOURCE = "c8a07306d212e23cc5a4c1e0d98b7e8f47f45e21"
EXPECTED_REVIEWED_HEAD = "01c86153026c3864134d0ffa1af1c118cd32bfea"
PROFILE_ID = "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"


def main() -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    raw = QUAL.read_bytes()
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    assert binding["qualification_sha256"] == actual_sha256
    assert binding["profile_id"] == PROFILE_ID
    assert binding["profile_source_sha"] == EXPECTED_SOURCE
    assert binding["profile_reviewed_head_sha"] == EXPECTED_REVIEWED_HEAD
    assert binding["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert binding["independent_verification"] is False
    assert binding["empirical_authorization"] is False
    assert binding["scientific_n_increment"] == 0

    actual_profile_blob = subprocess.check_output(
        ["git", "hash-object", str(PROFILE.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()
    assert actual_profile_blob == EXPECTED_PROFILE_BLOB

    assert verify_qualification_artifact(
        raw,
        expected_sha256=actual_sha256,
        expected_profile_id=PROFILE_ID,
        expected_profile_source_sha=EXPECTED_SOURCE,
    )

    data = json.loads(raw.decode("utf-8"))
    scores = [data["scoring"][f"Q{i:02d}"]["score"] for i in range(1, 12)]
    assert sum(scores) == data["scoring_summary"]["total_score"] == 107
    assert data["scoring_summary"]["max_score"] == 110
    assert data["scoring_summary"]["tier"] == "S-TIER"
    assert data["scoring_summary"]["q11_score"] == 9
    assert data["scoring_summary"]["attestation_result"] == "GRANTED"
    assert data["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
    assert data["independent_verification"] is False
    assert data["empirical_evidence"] is False
    assert data["scientific_n_increment"] == 0
    print("Canonical profile 11Q qualification: PASS_SELF_ATTESTED_NONINDEPENDENT")


if __name__ == "__main__":
    main()
