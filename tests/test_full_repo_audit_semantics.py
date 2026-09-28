from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "full_repo_audit.py"
SPEC = importlib.util.spec_from_file_location("full_repo_audit", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_historical_commit_binding_only_applies_to_workflows():
    text = "EXPECTED_COMMIT=e1f077fec746acd6066db689ef40db000e027f2f"
    findings = MODULE.semantic_findings(
        Path("docs/experiment/historical.md"), text, "0" * 40
    )
    assert not any(f["type"] == "workflow_historical_commit_binding" for f in findings)


def test_scanner_source_does_not_self_report_semantic_findings():
    text = 'claim_340 = "340%"\nflag_02 = "FLAG-02"\n# verified qualitative'
    findings = MODULE.semantic_findings(
        Path("scripts/full_repo_audit.py"), text, "0" * 40
    )
    assert findings == []


def test_workflow_historical_binding_remains_critical():
    text = "EXPECTED_COMMIT=e1f077fec746acd6066db689ef40db000e027f2f"
    findings = MODULE.semantic_findings(
        Path(".github/workflows/example.yml"), text, "0" * 40
    )
    assert any(
        f["severity"] == "CRITICAL"
        and f["type"] == "workflow_historical_commit_binding"
        for f in findings
    )


def test_immutable_action_pin_is_not_a_literal_review():
    text = "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
    findings = MODULE.semantic_findings(
        Path(".github/workflows/example.yml"), text, "0" * 40
    )
    assert not any(f["type"] == "workflow_literal_40hex_review" for f in findings)


def test_non_action_40hex_in_workflow_is_reviewed_without_stale_claim():
    sha = "1234567890abcdef1234567890abcdef12345678"
    text = f"env:\n  EXPECTED_SOURCE_SHA: {sha}"
    findings = MODULE.semantic_findings(
        Path(".github/workflows/example.yml"), text, "0" * 40
    )
    assert any(
        f["severity"] == "REVIEW"
        and f["type"] == "workflow_literal_40hex_review"
        and f["referenced_commit"] == sha
        for f in findings
    )


def test_qualified_historical_340_language_is_not_flagged():
    text = "FLAG-02 | 340% coordination gain | CLOSED — historical/unverified claim"
    findings = MODULE.semantic_findings(Path("docs/current.md"), text, "0" * 40)
    assert not any(f["type"] == "340_claim_status_language" for f in findings)


def test_unqualified_verified_340_language_is_flagged():
    text = "340% coordination gain VERIFIED"
    findings = MODULE.semantic_findings(Path("docs/current.md"), text, "0" * 40)
    assert any(f["type"] == "340_claim_status_language" for f in findings)


def test_historical_flag02_qualitative_correction_is_not_flagged():
    text = (
        "FLAG-02 is a historical identifier. Current terminology correction: "
        "the evaluation-mode term is qualitative."
    )
    findings = MODULE.semantic_findings(Path("docs/current.md"), text, "0" * 40)
    assert not any(f["type"] == "FLAG02_namespace_migration" for f in findings)


def test_unqualified_flag02_qualitative_collision_is_flagged():
    text = "FLAG-02 is qualitative."
    findings = MODULE.semantic_findings(Path("docs/current.md"), text, "0" * 40)
    assert any(f["type"] == "FLAG02_namespace_migration" for f in findings)
