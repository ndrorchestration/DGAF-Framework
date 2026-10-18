"""V2 benchmark candidate: local engineering only, no oracle promotion."""

import importlib.util
import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "experiments/governance_benchmark/v2"
spec = importlib.util.spec_from_file_location("dgaf_opa_v2_candidate", V2 / "verify_opa_c3.py")
assert spec and spec.loader
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def test_scenario_catalog_is_eight_design_only_entries():
    doc = json.loads((V2 / "scenario_catalog_v1.json").read_text(encoding="utf-8"))
    assert doc["status"] == "DESIGN_ONLY_ORACLE_UNFROZEN"
    assert doc["evidence_class"] == "NON_EXECUTED_DESIGN"
    assert [s["id"] for s in doc["scenarios"]] == [f"GOV2-{n:02d}" for n in range(1, 9)]
    for scenario in doc["scenarios"]:
        assert scenario["required_evidence"] and scenario["safety_invariant"]
        assert "observed_result" not in scenario
    assert doc["claim_ceiling"]["scientific_n_increment"] == 0


def test_missing_opa_blocks(tmp_path):
    with pytest.raises(RuntimeError, match="BLOCKED_OPA_BINARY_MISSING"):
        candidate.verify_binary(tmp_path / "missing")


def test_opa_undefined_result_blocks(tmp_path):
    fake = tmp_path / "opa"
    fake.write_text("#!/bin/sh\necho '{\"result\":[]}'\n", encoding="utf-8")
    fake.chmod(0o755)
    with pytest.raises(RuntimeError, match="BLOCKED_OPA_RESULT_UNDETERMINED"):
        candidate.opa_allow(fake, {"action": {"authorized": True}})


def test_claim_ceiling_does_not_promote():
    assert "SCIENTIFIC_N_INCREMENT=0" in candidate.CEILINGS
    assert "INDEPENDENT_VALIDATION=NOT_ESTABLISHED" in candidate.CEILINGS
    assert "HIGH_ASSURANCE=NOT_AUTHORIZED" in candidate.CEILINGS


def test_fixed_fixture_parity_with_pinned_opa_only():
    opa = os.environ.get("DGAF_V2_OPA_BINARY")
    if not opa:
        pytest.skip("Pinned OPA unavailable: no parity result is asserted")
    report = candidate.run(Path(opa))
    assert report["summary"]["cases"] == 13
    assert report["summary"]["non_parity"] == 0
    assert report["summary"]["opa_false_blocks"] == 0
    assert report["summary"]["dgaf_false_blocks"] == 0
    assert report["candidate_state"] == "UNCOMMITTED_NOT_ADMITTED"
