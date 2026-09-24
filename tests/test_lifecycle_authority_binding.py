import json
from datetime import datetime, timezone
from pathlib import Path

from registry import ecosystem_audit


def test_account_lifecycle_authority_is_bound_to_profile_registry():
    binding_path = Path(__file__).resolve().parents[1] / "registry" / "lifecycle_authority.json"
    assert binding_path.exists(), "DGAF projection must bind account lifecycle classification externally"

    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    assert binding["authority_scope"] == "ACCOUNT_LEVEL_LIFECYCLE_ONLY"
    assert binding["canonical_repository"] == "ndrorchestration/ndrorchestration"
    assert binding["canonical_path"] == "ecosystem/repository-lifecycle.json"
    assert binding["projection_semantics"] == "DGAF_LOCAL_FIELDS_NON_AUTHORITATIVE"


def test_audit_labels_local_lifecycle_state_as_non_authoritative(capsys, monkeypatch, tmp_path):
    projection_checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "registry_version": "0.5.0",
                "projection": {
                    "authority_scope": "projection_only",
                    "canonical_source": "project-local repository governance/evidence",
                    "canonical_source_revision": "test",
                    "projection_checked_at": projection_checked_at,
                    "projection_status": "CURRENT",
                    "staleness_class": None,
                },
                "projects": [
                    {
                        "id": "example",
                        "github": {
                            "owner": "ndrorchestration",
                            "repo": "example",
                            "private": False,
                            "archived": False,
                            "default_branch": "main",
                        },
                        "lifecycle_state": "active",
                        "summary": "Example project.",
                        "authority": {"current_owner": None},
                        "deployments": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(ecosystem_audit, "REGISTRY_PATH", str(registry_path))
    monkeypatch.setattr(
        ecosystem_audit,
        "fetch_github_repos",
        lambda owner: [
            {
                "full_name": "ndrorchestration/example",
                "private": False,
                "archived": False,
                "default_branch": "main",
            }
        ],
    )

    assert ecosystem_audit.run_audit() == 0
    output = capsys.readouterr().out
    assert "NON-AUTHORITATIVE LOCAL ACTIVITY STATUS" in output
    assert "=== LIFECYCLE SUMMARY ===" not in output
