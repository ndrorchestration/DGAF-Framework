#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "docs/governance/TRACK_C_NONEMPIRICAL_COMPOSITION_PROPOSAL_V1.json"
LANES = {
    "b1": (
        ROOT / "docs/governance/B1_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json",
        "57212ad15da32a51bef8c2ac4847e5522e420d68",
        "PASS_B1_STANDALONE_NONEMPIRICAL_LANE_COMPLETE",
        "07d93d04f26761e39c86b1758831e4e3add857d3",
    ),
    "b2": (
        ROOT / "docs/governance/B2_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json",
        "f585ea2d7cea3d70d6eaf18e4bb216f2a4cdf5bd",
        "PASS_B2_STANDALONE_NONEMPIRICAL_LANE_COMPLETE",
        "bf31e32e9843d6b3ac7d589d71a4140b72f3bcaf",
    ),
    "b3": (
        ROOT / "docs/governance/B3_NONEMPIRICAL_INTEGRATION_ADJUDICATION_V1.json",
        "4dcada0754a07d4211b048f43e8c4617a320ddfe",
        "PASS_B3_STANDALONE_NONEMPIRICAL_LANE_COMPLETE",
        "af66ba53cfdb8af101737d73bc13d1e003bd8856",
    ),
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def main() -> int:
    p = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    assert p["record_type"] == "DGAF_TRACK_C_NONEMPIRICAL_COMPOSITION_PROPOSAL"
    assert p["controller_issue"] == 447
    assert p["status"] == "PROPOSED_NONEMPIRICAL_NOT_AUTHORIZED"

    for lane, (path, expected_blob, disposition, merge_sha) in LANES.items():
        assert blob(path) == expected_blob, f"source drift: {path}"
        data = json.loads(path.read_text(encoding="utf-8"))
        binding = p["source_bindings"][lane]
        assert binding["adjudication_blob_sha"] == expected_blob
        assert binding["adjudication_merge_sha"] == merge_sha
        assert binding["required_disposition"] == disposition
        assert data["disposition"] == disposition
        assert data["verification_class"] == "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
        assert data["scientific_n_increment"] == 0
        assert data["track_c_empirical_execution_authorized"] is False
        assert data["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
        assert data["high_assurance"] == "NOT_AUTHORIZED_N0"

    roles = p["composition_roles"]
    assert roles == {
        "b1": "SEMANTIC_ROUTING_AND_SAFETY_ONLY",
        "b2": "STATEFUL_CONTEXT_AND_CLOSURE_ONLY",
        "b3": "PERSISTENT_GRAPH_CONVERGENCE_MONITORING_ONLY",
    }

    interface = p["proposed_interface_contract"]
    assert interface["role_substitution_allowed"] is False
    assert interface["cross_lane_authority_inference_allowed"] is False
    assert interface["integrated_execution_implemented"] is False

    conflicts = p["proposed_fail_closed_conflict_rules"]
    assert set(conflicts.values()) == {True}

    prohibited = p["prohibited"]
    assert set(prohibited.values()) == {True}
    assert p["scientific_n_increment"] == 0
    assert p["track_c_empirical_execution"] == "NOT_AUTHORIZED"
    assert p["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert p["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("TRACK_C_NONEMPIRICAL_COMPOSITION_PROPOSAL_PASS_NONAUTHORIZING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
