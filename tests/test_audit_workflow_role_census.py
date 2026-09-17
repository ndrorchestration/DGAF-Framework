from pathlib import Path

from registry import audit_catalog
from registry.audit_catalog import load_catalog

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "registry" / "audit_catalog.v1.json"


def _build_workflow_role_census(repo_root, catalog):
    helper = getattr(audit_catalog, "build_workflow_role_census")
    return helper(repo_root, catalog)


def test_role_census_marks_only_catalog_bound_workflows_as_recurring_assurance():
    catalog = load_catalog(CATALOG_PATH)
    census = _build_workflow_role_census(REPO_ROOT, catalog)

    assert census[".github/workflows/governance-ci.yml"] == "RECURRING_ASSURANCE"
    assert census[".github/workflows/agent-ontology-adjudication.yml"] == "UNCLASSIFIED"
    assert set(census.values()) <= {"RECURRING_ASSURANCE", "UNCLASSIFIED"}
    assert list(census) == sorted(census)


def test_role_census_does_not_infer_unmapped_workflow_roles_from_filenames(tmp_path):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "obvious-audit.yml").write_text("name: Audit\n", encoding="utf-8")
    (workflows / "mapped.yml").write_text("name: Mapped\n", encoding="utf-8")

    catalog = {
        "audits": [
            {
                "id": "AUD-MAPPED",
                "implementation": [".github/workflows/mapped.yml"],
            }
        ]
    }

    assert _build_workflow_role_census(tmp_path, catalog) == {
        ".github/workflows/mapped.yml": "RECURRING_ASSURANCE",
        ".github/workflows/obvious-audit.yml": "UNCLASSIFIED",
    }
