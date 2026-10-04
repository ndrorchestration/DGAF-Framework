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


def test_report_enumerates_tektite_public_claim_evidence_seed_without_claiming_completeness():
    module = load_module()
    report = module.build_report(ROOT, [])

    public_claims = report["public_claim_evidence"]
    assert public_claims["scope"] == "TEKTITE_V0_1_EVIDENCE_LEDGER_SEED_ONLY"
    assert public_claims["completeness"] == "NOT_ESTABLISHED"
    assert len(public_claims["entries"]) == 3
    assert public_claims["missing_public_link_artifacts"] == ["AI Evidence Audit positioning"]
    assert all("claim_supported" in entry for entry in public_claims["entries"])
    assert all("claim_not_supported" in entry for entry in public_claims["entries"])


def test_report_exposes_control_test_reference_scan_as_heuristic_only():
    module = load_module()
    report = module.build_report(ROOT, [])

    scan = report["control_test_reference_scan"]
    assert scan["scope"] == "DIRECT_TEST_REFERENCE_HEURISTIC_ONLY"
    assert scan["coverage"] == "NOT_ESTABLISHED"

    rows = {(row["component_id"], row["artifact"]): row["direct_test_mentions"] for row in scan["rows"]}
    assert "tests/test_capability_governance_contracts.py" in rows[("K1", "scripts/dgaf_capability_canonicalize.py")]
    assert rows[("K8", "docs/EPISTEMIC_EVIDENCE_STANDARD.md")] == []


def _acp_reconciliation_observation(embedded, live=None):
    return {
        "schema_version": "ACP_LIVE_RECONCILIATION_V0_CANDIDATE",
        "observed_at": "2026-10-04T18:30:00Z",
        "tektite_embedded_acp_commit": embedded,
        "live_acp_repository_commit": live or embedded,
        "evidence_url": "https://github.com/ndrorchestration/agent-control-plane",
    }


def test_acp_reconciliation_reports_source_advance_without_semantic_promotion():
    module = load_module()
    embedded = "4d3cdd21a445b765753cb5d36360f643210fe0b5"
    live = "e7135323663ebbe025b18b74a13f2d99c14e2b57"

    report = module.build_report(
        ROOT,
        [],
        acp_reconciliation_observation=_acp_reconciliation_observation(embedded, live),
    )

    reconciliation = report["acp_reconciliation"]
    assert reconciliation["scope"] == "ACP_REPOSITORY_TIP_ONLY"
    assert reconciliation["state"] == "ACP_SOURCE_ADVANCED"
    assert reconciliation["semantic_reconciliation"] == "NOT_ESTABLISHED"
    assert reconciliation["authority_effect"] == "NONE"
    assert reconciliation["cross_surface_reconciliation"] == "NOT_ESTABLISHED"
    assert report["gaps"]["requires_acp_repository_reconciliation"] is True


def test_acp_reconciliation_tip_match_still_does_not_establish_semantic_currentness():
    module = load_module()
    embedded = "4d3cdd21a445b765753cb5d36360f643210fe0b5"

    report = module.build_report(
        ROOT,
        [],
        acp_reconciliation_observation=_acp_reconciliation_observation(embedded),
    )

    reconciliation = report["acp_reconciliation"]
    assert reconciliation["state"] == "ACP_REPOSITORY_TIP_MATCH"
    assert reconciliation["semantic_reconciliation"] == "NOT_ESTABLISHED"
    assert report["gaps"]["requires_acp_repository_reconciliation"] is False
    assert report["gaps"]["cross_surface_reconciliation_not_established"] is True


def test_acp_reconciliation_must_bind_to_tektite_manifest_identity():
    module = load_module()

    with pytest.raises(ValueError, match="tektite_embedded_acp_commit"):
        module.build_report(
            ROOT,
            [],
            acp_reconciliation_observation=_acp_reconciliation_observation("f" * 40),
        )


def test_acp_reconciliation_rejects_malformed_live_sha():
    module = load_module()
    embedded = "4d3cdd21a445b765753cb5d36360f643210fe0b5"

    with pytest.raises(ValueError, match="live_acp_repository_commit"):
        module.build_report(
            ROOT,
            [],
            acp_reconciliation_observation=_acp_reconciliation_observation(
                embedded,
                "not-a-sha",
            ),
        )


def test_cli_accepts_acp_reconciliation_observation(tmp_path):
    import subprocess
    import sys

    embedded = "4d3cdd21a445b765753cb5d36360f643210fe0b5"
    live = "e7135323663ebbe025b18b74a13f2d99c14e2b57"
    path = tmp_path / "acp-reconciliation.json"
    path.write_text(
        json.dumps(_acp_reconciliation_observation(embedded, live)),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--acp-reconciliation-observation",
            str(path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    report = json.loads(result.stdout)
    assert report["acp_reconciliation"]["state"] == "ACP_SOURCE_ADVANCED"
    assert report["acp_reconciliation"]["semantic_reconciliation"] == "NOT_ESTABLISHED"
