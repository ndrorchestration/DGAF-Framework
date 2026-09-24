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
    assert ".github/workflows/b1-integration-adjudication.yml" in unmapped
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
        ".github/workflows/agent-ontology-adjudication.yml",
    }

    assert expected_mapped.isdisjoint(unmapped)


def test_agent_ontology_adjudication_assurance_family_is_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    audit = next(
        (entry for entry in catalog["audits"] if entry.get("id") == "AUD-CI-AGENT-ONTOLOGY"),
        None,
    )

    assert audit is not None
    assert ".github/workflows/agent-ontology-adjudication.yml" in audit["implementation"]
    assert audit["blocking"] is False
    assert audit["independence"] == "SAME_REPOSITORY_NONINDEPENDENT"
    assert any("scientific" in item.lower() for item in audit["non_effects"])
    assert any("authority matrix" in item.lower() for item in audit["non_effects"])


def test_e2b_verifier_lock_assurance_family_is_catalog_mapped_without_closure():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)
    audit = next(
        (entry for entry in catalog["audits"] if entry.get("id") == "AUD-CI-E2B-VERIFIER-LOCK"),
        None,
    )

    assert audit is not None
    assert ".github/workflows/e2b-verifier-lock.yml" in audit["implementation"]
    assert ".github/workflows/e2b-verifier-lock.yml" not in unmapped
    assert audit["blocking"] is False
    assert audit["independence"] == "SAME_REPOSITORY_NONINDEPENDENT"
    assert any("does not declare e2b closed" in item.lower() for item in audit["non_effects"])
    assert any("independent verification" in item.lower() for item in audit["known_gaps"])


def test_completion_state_reconciler_family_is_catalog_mapped_with_historical_scope():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)
    audit = next(
        (entry for entry in catalog["audits"] if entry.get("id") == "AUD-CI-COMPLETION-STATE-RECONCILER"),
        None,
    )

    assert audit is not None
    assert ".github/workflows/completion-state-reconciler.yml" in audit["implementation"]
    assert ".github/workflows/completion-state-reconciler.yml" not in unmapped
    assert audit["blocking"] is False
    assert audit["independence"] == "SAME_REPOSITORY_NONINDEPENDENT"
    assert any("does not authorize" in item.lower() for item in audit["non_effects"])
    assert any("historical_fixed_scope_track_a_epoch_002_precollection" in item.lower() for item in audit["known_gaps"])
    assert any("current global dgaf state" in item.lower() for item in audit["non_effects"])


def test_track_c_nonempirical_composition_family_is_catalog_mapped_without_authorization():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = _collect_unmapped_workflows(REPO_ROOT, catalog)
    audit = next(
        (
            entry
            for entry in catalog["audits"]
            if entry.get("id") == "AUD-CI-TRACK-C-NONEMPIRICAL-COMPOSITION"
        ),
        None,
    )

    assert audit is not None
    assert ".github/workflows/track-c-nonempirical-composition.yml" in audit["implementation"]
    assert ".github/workflows/track-c-nonempirical-composition.yml" not in unmapped
    assert audit["blocking"] is False
    assert audit["independence"] == "SAME_REPOSITORY_NONINDEPENDENT"
    assert any("does not implement integrated" in item.lower() for item in audit["non_effects"])
    assert any("empirical execution" in item.lower() for item in audit["non_effects"])
    assert any("scientific n" in item.lower() for item in audit["non_effects"])


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


def test_external_runtime_ingress_assurance_family_is_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    implementation_paths = {path for audit in catalog["audits"] for path in audit.get("implementation", [])}

    external_runtime_assurance_paths = {
        "registry/external_runtime_adapter_contract_v1.json",
        "scripts/validate_external_runtime_adapter.py",
        "tests/test_external_runtime_adapter_contract.py",
    }

    assert external_runtime_assurance_paths.issubset(implementation_paths)


def test_semantic_control_field_projection_assurance_family_is_catalog_mapped():
    catalog = load_catalog(CATALOG_PATH)
    audit = next(
        (entry for entry in catalog["audits"] if entry.get("id") == "AUD-UI-SEMANTIC-CONTROL-FIELD"),
        None,
    )

    assert audit is not None

    expected_paths = {
        "app/lib/decision-frontier.ts",
        "app/lib/decision-frontier.test.ts",
        "app/lib/governance-map.ts",
        "app/lib/governance-map.test.ts",
        "app/lib/state-space-projection.ts",
        "app/lib/state-space-projection.test.ts",
    }

    assert expected_paths.issubset(set(audit["implementation"]))
