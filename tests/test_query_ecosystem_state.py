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


def _reconciliation_evidence(pointer_source, live_commit=None):
    live_commit = live_commit or pointer_source
    return {
        "schema_version": "ECOSYSTEM_LIVE_RECONCILIATION_V1",
        "observed_at": "2026-10-03T19:30:00Z",
        "pointer_source_observation_commit": pointer_source,
        "live_repository_commit": live_commit,
        "container_commit": "e" * 40,
        "evidence_url": "https://example.invalid/reconciliation/1275",
    }


def test_external_reconciliation_can_establish_repository_tip_currentness():
    module = load_module()
    pointer = json.loads((ROOT / "registry/ecosystem_state_pointer.current.json").read_text(encoding="utf-8"))
    source = pointer["snapshot_provenance"]["source_observation_commit"]

    report = module.build_report(ROOT, [], reconciliation_evidence=_reconciliation_evidence(source))

    assert report["pointer"]["live_currentness"] == "DGAF_REPOSITORY_TIP_MATCH_EXTERNAL"
    assert report["reconciliation"]["scope"] == "DGAF_REPOSITORY_TIP_ONLY"
    assert report["reconciliation"]["state"] == "REPOSITORY_TIP_MATCH"
    assert report["reconciliation"]["errors"] == []
    assert report["gaps"]["requires_dgaf_repository_reconciliation"] is False
    assert report["gaps"]["cross_surface_reconciliation_not_established"] is True
    assert report["gaps"]["requires_reconciliation"] is True
    assert report["claim_ceiling"]["independent_validation"] == "NOT_ESTABLISHED"


def test_external_reconciliation_reports_stale_source_advance():
    module = load_module()
    pointer = json.loads((ROOT / "registry/ecosystem_state_pointer.current.json").read_text(encoding="utf-8"))
    source = pointer["snapshot_provenance"]["source_observation_commit"]

    report = module.build_report(
        ROOT,
        [],
        reconciliation_evidence=_reconciliation_evidence(source, live_commit="f" * 40),
    )

    assert report["pointer"]["live_currentness"] == "STALE_SOURCE_ADVANCED"
    assert report["reconciliation"]["state"] == "STALE_SOURCE_ADVANCED"
    assert any("not repository-tip current" in error for error in report["reconciliation"]["errors"])
    assert report["gaps"]["requires_reconciliation"] is True


def test_reconciliation_evidence_must_bind_to_pointer_source():
    module = load_module()

    with pytest.raises(ValueError, match="pointer_source_observation_commit"):
        module.build_report(
            ROOT,
            [],
            reconciliation_evidence=_reconciliation_evidence("f" * 40),
        )


def test_reconciliation_evidence_loader_accepts_utf8_bom(tmp_path):
    module = load_module()
    path = tmp_path / "reconciliation.json"
    path.write_text('{"schema_version":"x"}', encoding="utf-8-sig")

    assert module._load_json(path) == {"schema_version": "x"}


def test_reconciliation_rejects_malformed_git_identity():
    module = load_module()
    pointer = json.loads((ROOT / "registry/ecosystem_state_pointer.current.json").read_text(encoding="utf-8"))
    source = pointer["snapshot_provenance"]["source_observation_commit"]
    evidence = _reconciliation_evidence(source, live_commit="not-a-git-sha")

    with pytest.raises(ValueError, match="live_repository_commit"):
        module.build_report(ROOT, [], reconciliation_evidence=evidence)


def test_reconciliation_rejects_container_source_identity_alias():
    module = load_module()
    pointer = json.loads((ROOT / "registry/ecosystem_state_pointer.current.json").read_text(encoding="utf-8"))
    source = pointer["snapshot_provenance"]["source_observation_commit"]
    evidence = _reconciliation_evidence(source)
    evidence["container_commit"] = source

    with pytest.raises(ValueError, match="container_commit"):
        module.build_report(ROOT, [], reconciliation_evidence=evidence)
