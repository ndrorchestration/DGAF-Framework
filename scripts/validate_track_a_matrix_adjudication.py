#!/usr/bin/env python3
"""Fail-closed validator for the Track A non-empirical matrix adjudication."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/governance/TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_V1.json"
PAYLOAD = ROOT / "test-artifacts/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_PROBE.json"

BOUND_BLOBS = {
    ROOT / "docs/governance/PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1.json": "339d9ada4978ffd0c1eee67c310323f1e7fdc06a",
    ROOT / "docs/qa/APOGEE_11Q_PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1_S078.json": "217028dc03aad6eb6a1a13cb6e32418782c43b08",
    ROOT / "experiments/pdmal_pilot/topology_robustness_profile.py": "5b703273f26bde700fff03269c1734d89b2b347d",
    ROOT / "experiments/pdmal_pilot/test_topology_robustness_profile.py": "e94f8cbb4cef3ebae6bee5e2220f1ff0c7cc4856",
    ROOT / ".github/workflows/track-a-topology-robustness-profile.yml": "fbad06eec3ca6f4c7edc912e3f80f0c3b31e0404",
}
FORBIDDEN = (
    "ffcr", "final_std", "consensus_success", "treatment_effect",
    "confidence_interval", "p_value", "governance_trace", "condition", "dgaf",
)


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def main() -> int:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    payload_raw = PAYLOAD.read_bytes()
    payload = json.loads(payload_raw)

    assert record["record_type"] == "TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION"
    assert record["controller_issue"] == 408
    assert record["adjudication_result"] == "PASS_ADVANCE_TO_PROSPECTIVE_EMPIRICAL_PROTOCOL_PROPOSAL"
    assert record["verification_class"] == "DEVELOPER_ADJUDICATED_NONINDEPENDENT"
    assert record["independent_verification"] is False
    assert record["empirical_evidence"] is False
    assert record["scientific_n_increment"] == 0

    for path, expected in BOUND_BLOBS.items():
        assert git_blob(path) == expected, f"bound source drift: {path}"

    bindings = record["source_bindings"]
    assert bindings["architecture_merge_sha"] == "5e4f00a065c00cefec0b3a79c32b88a5f36a55c2"
    assert bindings["profile_merge_sha"] == "b1e333ee9f9e0a4da78788e5ff019603296888eb"
    assert bindings["qualification_merge_sha"] == "647f612a2412818dca0d632229f352e857e1187e"
    assert bindings["workflow_run_id"] == 34189626294
    assert bindings["retained_artifact_id"] == 10041800252
    assert bindings["retained_archive_digest"] == "sha256:629ee0be7a48606685f2452800ab4e482611fb45f7268d881e934488e1c1c1d5"
    assert hashlib.sha256(payload_raw).hexdigest() == bindings["artifact_payload_sha256"]

    assert payload["profile_id"] == record["profile_id"]
    assert payload["algorithm_id"] == record["algorithm_id"]
    assert payload["scientific_n_increment"] == 0
    assert payload["empirical_authorization"] is False
    assert payload["expected_cells"] == payload["completed_cells"] == 90
    assert len(payload["records"]) == 90

    identities = {
        (item["seed"], item["topology"], item["failure_count"])
        for item in payload["records"]
    }
    assert len(identities) == 90
    assert all(
        item["phase_update_hashes"]["pre_failure"]
        == item["phase_update_hashes"]["recovered"]
        for item in payload["records"]
    )
    assert all(
        item["phase_update_hashes"]["pre_failure"]
        == item["phase_update_hashes"]["during_failure"]
        for item in payload["records"]
        if item["failure_count"] == 0
    )
    assert all(
        item["phase_update_hashes"]["pre_failure"]
        != item["phase_update_hashes"]["during_failure"]
        for item in payload["records"]
        if item["failure_count"] > 0
    )

    raw_lower = payload_raw.decode("utf-8").lower()
    assert not any(token in raw_lower for token in FORBIDDEN)

    inspection = record["structural_inspection"]
    assert inspection["unique_matrix_cells"] == len(identities) == 90
    assert inspection["recovery_hash_mismatches"] == 0
    assert inspection["no_failure_phase_hash_mismatches"] == 0
    assert inspection["positive_failure_cells_with_changed_active_phase_hash"] == 80
    assert inspection["positive_failure_cells_total"] == 80
    assert inspection["forbidden_endpoint_tokens_present"] is False

    next_gate = record["next_gate"]
    assert next_gate["required"] == "TRACK_A_PROSPECTIVE_EMPIRICAL_PROTOCOL_PROPOSAL"
    assert len(next_gate["required_elements"]) == 10
    assert next_gate["empirical_execution"] == "NOT_AUTHORIZED"
    assert next_gate["freeze_status"] == "NOT_ESTABLISHED"
    assert next_gate["high_assurance"] == "NOT_AUTHORIZED"
    assert next_gate["high_assurance_empirical_n"] == 0

    print("TRACK_A_NONEMPIRICAL_MATRIX_ADJUDICATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
