#!/usr/bin/env python3
"""Validate the source-bound Epoch 004 post-fidelity claim ceiling."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AMENDMENT = ROOT / "docs/experiment/EPOCH_004_POST_FIDELITY_CLAIM_CEILING_2026-09-08.json"
PRIMARY = ROOT / "docs/experiment/CANONICAL_SOLO_EPOCH_004_PRIMARY_RESULT.json"
PRIMARY_MD = ROOT / "docs/experiment/CANONICAL_SOLO_EPOCH_004_PRIMARY_ADJUDICATION.md"
AUDIT_JSON = ROOT / "docs/experiment/SEVEN_GATE_TREATMENT_FIDELITY_AUDIT_2026-09-08.json"
AUDIT_MD = ROOT / "docs/experiment/SEVEN_GATE_TREATMENT_FIDELITY_AUDIT_2026-09-08.md"

EXPECTED_BLOBS = {
    PRIMARY: "4a17f9e6a656721fcef9cfce04bb78ed34ce673a",
    PRIMARY_MD: "8f436f0d68b65f19866ae31f9784d2fceee668a5",
    AUDIT_JSON: "15a2867f5fe9a9b139c07f632dcbc3d18e0c86ad",
    AUDIT_MD: "991e0e34973fc829dd0b4049aa0b644af8212999",
}


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def main() -> int:
    amendment = json.loads(AMENDMENT.read_text(encoding="utf-8"))
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))

    assert amendment["record_type"] == "DGAF_EPOCH_004_POST_FIDELITY_CLAIM_CEILING"
    assert amendment["scientific_n_increment"] == 0
    assert amendment["empirical_execution_authorized"] is False
    assert amendment["historical_result_rewritten"] is False
    assert amendment["historical_analysis_recalculated"] is False
    assert amendment["historical_pooling_allowed"] is False

    for path, expected in EXPECTED_BLOBS.items():
        actual = git_blob(path)
        assert actual == expected, f"historical source drift: {path}: {actual} != {expected}"

    bindings = amendment["source_bindings"]
    assert bindings["primary_result_blob_sha"] == EXPECTED_BLOBS[PRIMARY]
    assert bindings["primary_adjudication_blob_sha"] == EXPECTED_BLOBS[PRIMARY_MD]
    assert bindings["seven_gate_audit_json_blob_sha"] == EXPECTED_BLOBS[AUDIT_JSON]
    assert bindings["seven_gate_audit_md_blob_sha"] == EXPECTED_BLOBS[AUDIT_MD]
    assert bindings["seven_gate_audit_merge_sha"] == "f5644417c9183b4d1db38f9624ea01ba46b8197e"
    assert bindings["mechanism_diagnostic_artifact_id"] == 10040466222
    assert (
        bindings["mechanism_diagnostic_artifact_digest"]
        == "sha256:d150323e9cdd9ba641cf9aa7a2deb1a8cc5f29871fdff1821a50cf3a1a8e1b07"
    )

    locked = amendment["locked_primary_result"]
    result = primary["result"]
    assert locked["dgaf_ffcr"] == result["dgaf_ffcr"] == 0.7337777777777778
    assert locked["null_ffcr"] == result["null_ffcr"] == 0.8275555555555555
    assert (
        locked["paired_effect_dgaf_minus_null"]
        == result["paired_effect_dgaf_minus_null"]
        == -0.0937777777777778
    )
    assert locked["two_sided_95pct_ci"] == result["two_sided_95pct_ci"]
    assert locked["two_sided_95pct_ci"] == [
        -0.11822222222222223,
        -0.07066666666666668,
    ]
    assert (
        locked["classification"]
        == result["classification"]
        == "EVIDENCE_AGAINST_DIRECTIONAL_DGAF"
    )
    assert locked["estimator_recalculated_in_amendment"] is False

    assert audit["canonical_seven_gate_treatment_fidelity"] == "NOT_ESTABLISHED"
    assert audit["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"

    interpretation = amendment["post_fidelity_interpretation"]
    assert interpretation["supported_scope"] == "EXACT_EPOCH_004_EXECUTED_RESTORED_BINDING_TREATMENT"
    assert interpretation["seven_gate_canonical_treatment_fidelity"] == "NOT_ESTABLISHED"
    assert interpretation["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert interpretation["independent_validation"] is False
    assert interpretation["high_assurance_acceptance"] is False
    assert interpretation["production_readiness"] is False

    supersession = amendment["supersession_policy"]
    assert supersession["supersedes_primary_result"] is False
    assert supersession["supersedes_primary_analysis"] is False
    assert supersession["supersedes_historical_adjudication_text"] is False
    assert supersession["narrows_future_interpretation_only"] is True

    print("EPOCH_004_POST_FIDELITY_CLAIM_CEILING_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
