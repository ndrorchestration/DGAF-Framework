"""Regression guard for the DGAF live-runtime production endpoint binding."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PRODUCTION_URL = "https://dgaf-framework.vercel.app"
CANONICAL_PRODUCTION_URL = "https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app"
CANONICAL_COLD_START_WARNING = (
    "Audit counters are in-memory and reset on each serverless cold start. "
    "Configure an admitted durable store before relying on persistent audit state."
)


@pytest.mark.parametrize(
    "relative_path",
    [
        ".github/workflows/regression.yml",
        "scripts/live_regression_v17.py",
    ],
)
def test_live_regression_defaults_bind_to_canonical_production_url(relative_path: str) -> None:
    text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    assert LEGACY_PRODUCTION_URL not in text
    assert CANONICAL_PRODUCTION_URL in text


def test_scheduled_live_regression_cannot_be_redirected_by_repository_variable() -> None:
    workflow = (REPO_ROOT / ".github/workflows/regression.yml").read_text(encoding="utf-8")

    assert "vars.DGAF_URL" not in workflow
    assert "inputs.dgaf_url" in workflow


def test_live_audit_check_does_not_require_cross_request_serverless_counter_persistence() -> None:
    workflow = (REPO_ROOT / ".github/workflows/regression.yml").read_text(encoding="utf-8")
    audit_block = workflow.split("- name: Audit log check", 1)[1].split("- name: Notify on live-regression failure", 1)[
        0
    ]

    assert "turn_count" not in audit_block
    assert "d.get('status') == 'ok'" in audit_block
    assert "d.get('version') == '1.8.0'" in audit_block
    assert "d.get('_warning') in (None, expected_warning)" in audit_block
    assert CANONICAL_COLD_START_WARNING in audit_block
    assert "audit response contract FAIL" in audit_block


def test_live_audit_contract_matches_runtime_warning_and_fails_job_closed() -> None:
    workflow = (REPO_ROOT / ".github/workflows/regression.yml").read_text(encoding="utf-8")
    verifier = (REPO_ROOT / "scripts/verify_deployment.sh").read_text(encoding="utf-8")
    runtime = (REPO_ROOT / "pages/api/audit.ts").read_text(encoding="utf-8")
    live_job = workflow.split("  live-regression:", 1)[1]

    assert "Configure an admitted durable store" in runtime
    assert CANONICAL_COLD_START_WARNING in workflow
    assert CANONICAL_COLD_START_WARNING in verifier
    assert "continue-on-error: true" not in live_job
    assert "Vercel unavailable" not in live_job
