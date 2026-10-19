"""Guard production-deployment workflow mapping without certifying the runtime."""

from pathlib import Path

from registry.audit_catalog import collect_unmapped_workflows, load_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_production_deploy_is_mapped_to_existing_runtime_audit_family():
    catalog = load_catalog(REPO_ROOT / "registry" / "audit_catalog.v1.json")
    family = next(entry for entry in catalog["audits"] if entry["id"] == "AUD-RUNTIME-LIVE")

    assert ".github/workflows/deploy.yml" in family["implementation"]
    assert ".github/workflows/regression.yml" in family["implementation"]
    assert "RUNTIME" in family["target_layers"]
    assert ".github/workflows/deploy.yml" not in collect_unmapped_workflows(REPO_ROOT, catalog)
    assert any("scientific" in limitation.lower() for limitation in family["non_effects"])
