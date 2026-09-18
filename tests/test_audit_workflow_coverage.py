from pathlib import Path

from registry import audit_catalog
from registry.audit_catalog import load_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "registry" / "audit_catalog.v1.json"


def _collect_unmapped_workflows(repo_root, catalog):
    helper = getattr(audit_catalog, "collect_unmapped_workflows")
    return helper(repo_root, catalog)


def test_workflow_coverage_scanner_reports_current_unmapped_definitions():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)

    assert unmapped
    assert ".github/workflows/agent-ontology-adjudication.yml" in unmapped
    assert ".github/workflows/governance-ci.yml" not in unmapped
    assert all(path.startswith(".github/workflows/") for path in unmapped)
    assert unmapped == sorted(unmapped)


def test_workflow_coverage_scanner_accepts_catalog_mapping_by_exact_implementation_path(tmp_path):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "alpha.yml").write_text("name: Alpha\n", encoding="utf-8")
    (workflows / "beta.yaml").write_text("name: Beta\n", encoding="utf-8")

    catalog = {
        "version": "AUDIT_CATALOG_V1",
        "coverage": {"status": "PARTIAL", "known_gaps": ["beta unclassified"]},
        "audits": [
            {
                "id": "AUD-ALPHA",
                "implementation": [".github/workflows/alpha.yml"],
            }
        ],
    }

    assert _collect_unmapped_workflows(tmp_path, catalog) == [".github/workflows/beta.yaml"]


def test_verified_recurring_assurance_workflows_are_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)

    expected_mapped = {
        ".github/workflows/claim-hygiene.yml",
        ".github/workflows/control-state-consistency.yml",
        ".github/workflows/critical-pr-lane-custody.yml",
        ".github/workflows/epistemic-evidence-validation.yml",
        ".github/workflows/external-acceptance-readiness-validation.yml",
        ".github/workflows/full-repo-audit.yml",
        ".github/workflows/ip-hygiene.yml",
    }

    assert expected_mapped.isdisjoint(unmapped)
    assert ".github/workflows/agent-ontology-adjudication.yml" in unmapped


def test_protected_main_required_context_workflows_are_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)

    required_context_workflows = {
        ".github/workflows/governance-ci.yml",
        ".github/workflows/pptl-ci.yml",
        ".github/workflows/pr-issue-closure-keyword-guard.yml",
    }

    assert required_context_workflows.isdisjoint(unmapped)


def test_core_exact_head_verification_workflows_are_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)

    core_verification_workflows = {
        ".github/workflows/python-tests.yml",
        ".github/workflows/ui-command-center-validation.yml",
        ".github/workflows/doc-lint-pr-scope.yml",
        ".github/workflows/validate-control-state-head.yml",
    }

    assert core_verification_workflows.isdisjoint(unmapped)
