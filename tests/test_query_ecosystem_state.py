import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "query_ecosystem_state.py"


def load_module():
    spec = importlib.util.spec_from_file_location("query_ecosystem_state", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_report_preserves_historical_snapshot_and_claim_ceiling():
    module = load_module()
    report = module.build_report(ROOT, ["AOSS_STAGE_A_READINESS", "TEKTITE_PUBLIC_STATUS"])

    assert report["schema_version"] == "ECOSYSTEM_QUERY_REPORT_V1"
    assert report["pointer"]["embedded_scope"] == "HISTORICAL_SNAPSHOT"
    assert report["pointer"]["live_currentness"] == "UNVERIFIED_NO_EXTERNAL_RECONCILIATION"
    assert report["claim_ceiling"] == {
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
        "live_repository_mutation": "NOT_AUTHORIZED",
        "production_executor": "NOT_ESTABLISHED",
    }
    assert report["gaps"]["missing_required_consumers"] == []


def test_report_exposes_receipt_non_authority_semantics():
    module = load_module()
    report = module.build_report(ROOT, [])

    assert report["receipt_authority"] == {
        "authority_effect": "NONE",
        "follow_on_authority": "FRESH_ADJUDICATION_REQUIRED",
    }


def test_missing_consumer_is_reported_not_inferred():
    module = load_module()
    report = module.build_report(ROOT, ["UNKNOWN_CONSUMER"])

    assert report["gaps"]["missing_required_consumers"] == ["UNKNOWN_CONSUMER"]
    assert report["gaps"]["requires_reconciliation"] is True


def test_invalid_pointer_refuses_to_build_report(tmp_path):
    module = load_module()

    for relative in [
        "docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json",
        "schemas/execution_receipt.schema.json",
    ]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")

    pointer = json.loads((ROOT / "registry/ecosystem_state_pointer.current.json").read_text(encoding="utf-8"))
    pointer["claim_ceiling"]["independent_validation"] = "ESTABLISHED"
    target = tmp_path / "registry/ecosystem_state_pointer.current.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(pointer), encoding="utf-8")

    with pytest.raises(ValueError, match="claim_ceiling"):
        module.build_report(tmp_path, [])
