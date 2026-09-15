"""Guards for current DGAF Vercel runtime identity metadata."""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PRODUCTION_URL = "https://dgaf-framework.vercel.app"
CANONICAL_PRODUCTION_URL = "https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app"
VERCEL_PROJECT_ID = "prj_euzjAnhqct0wayTWWojizanKN3cX"
COLD_START_WARNING = (
    "Audit counters are in-memory and reset on each serverless cold start. "
    "Wire to Vercel KV for persistence."
)


def test_deployment_verifier_defaults_to_canonical_production_url() -> None:
    script = (REPO_ROOT / "scripts/verify_deployment.sh").read_text(encoding="utf-8")

    assert LEGACY_PRODUCTION_URL not in script
    assert CANONICAL_PRODUCTION_URL in script


def test_deployment_verifier_supports_vercel_protection_bypass_without_embedding_secret() -> None:
    script = (REPO_ROOT / "scripts/verify_deployment.sh").read_text(encoding="utf-8")

    assert "VERCEL_AUTOMATION_BYPASS_SECRET" in script
    assert "x-vercel-protection-bypass" in script
    assert "${VERCEL_AUTOMATION_BYPASS_SECRET}" in script


def test_deployment_verifier_checks_current_orchestrate_response_contract() -> None:
    script = (REPO_ROOT / "scripts/verify_deployment.sh").read_text(encoding="utf-8")

    for legacy_field in ("turn_id", "dgaf_decision", "phi_decision", "seal_hash"):
        assert legacy_field not in script

    assert '"turn": 1' in script
    assert "get('decision'" in script
    assert "get('turn'" in script
    assert "get('effective_confidence'" in script
    assert "get('psi_cubic_check'" in script
    assert "get('trace'" in script
    assert "get('evidence',{})" in script
    assert '"PASS"' in script
    assert '"PARTIAL"' in script


def test_deployment_verifier_fails_closed_on_health_dashboard_and_audit_contract_drift() -> None:
    script = (REPO_ROOT / "scripts/verify_deployment.sh").read_text(encoding="utf-8")

    assert "HEALTH_OK=" in script
    assert "d.get('status') == 'ok'" in script
    assert "d.get('psi_cubic') is True" in script
    assert "d.get('version') == '1.8.0'" in script
    assert '"$HEALTH_OK" = "true"' in script
    assert "health response contract FAIL" in script
    assert "version=$VER (expected 1.8.0)" not in script

    assert '"$HTTP_CODE" = "200"' in script
    assert "dashboard HTTP contract FAIL" in script

    assert "AUDIT=$(curl" in script
    assert "AUDIT_OK=" in script
    assert "d.get('_warning') in (None, expected_warning)" in script
    assert COLD_START_WARNING in script
    assert '"$AUDIT_OK" = "true"' in script
    assert "audit response contract FAIL" in script


def test_ecosystem_registry_binds_current_dgaf_vercel_identity() -> None:
    registry = json.loads((REPO_ROOT / "registry/ecosystem_registry.json").read_text(encoding="utf-8"))
    project = next(project for project in registry["projects"] if project["id"] == "dgaf-framework")
    deployment = next(
        deployment
        for deployment in project["deployments"]
        if deployment["platform"] == "vercel" and deployment["env"] == "prod"
    )

    assert deployment["project_id"] == VERCEL_PROJECT_ID
    assert deployment["url"] == CANONICAL_PRODUCTION_URL
    assert deployment["status"] == "active"
