from pathlib import Path

from registry.audit_catalog import collect_unmapped_workflows, load_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "registry" / "audit_catalog.v1.json"


def test_workflow_coverage_scanner_reports_current_unmapped_definitions():
    catalog = load_catalog(CATALOG_PATH)
    unmapped = collect_unmapped_workflows(REPO_ROOT, catalog)

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

    assert collect_unmapped_workflows(tmp_path, catalog) == [
        ".github/workflows/beta.yaml"
    ]
