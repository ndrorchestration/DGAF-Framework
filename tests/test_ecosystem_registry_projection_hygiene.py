import json
from datetime import datetime, timezone
from pathlib import Path

from registry import ecosystem_audit
from registry.ecosystem_audit import audit_exit_code, collect_semantic_violations


def _repo(full_name="ndrorchestration/example", **overrides):
    base = {
        "full_name": full_name,
        "private": False,
        "archived": False,
        "default_branch": "main",
    }
    base.update(overrides)
    return base


def _project(**overrides):
    base = {
        "id": "example",
        "summary": "Example project.",
        "github": {
            "owner": "ndrorchestration",
            "repo": "example",
            "private": False,
            "archived": False,
            "default_branch": "main",
        },
        "authority": {"current_owner": "role.project-maintainer"},
        "deployments": [],
    }
    base.update(overrides)
    return base


def _registry(project=None, projection=None):
    if projection is None:
        projection = {
            "authority_scope": "projection_only",
            "canonical_source": "project-local repository governance/evidence",
            "canonical_source_revision": "0083d64aa5f9395a9aa38ff0ca01ccd9e528fd44",
            "projection_checked_at": "2026-09-16T12:00:00Z",
            "projection_status": "CURRENT",
            "staleness_class": None,
        }
    return {
        "registry_version": "0.5.0",
        "projection": projection,
        "projects": [project or _project()],
    }


def _violations(registry, repos=None):
    return collect_semantic_violations(
        registry,
        repos or [_repo()],
        now=datetime(2026, 9, 16, 12, tzinfo=timezone.utc),
    )


def _codes(violations):
    return {v["code"] for v in violations}


def test_rejects_current_persona_authority_without_functional_role():
    registry = _registry(_project(authority={"current_owner": "Amethyst"}))
    assert "CURRENT_PERSONA_AUTHORITY" in _codes(_violations(registry))


def test_rejects_live_github_metadata_mismatch():
    assert "GITHUB_METADATA_MISMATCH" in _codes(_violations(_registry(), [_repo(private=True)]))


def test_rejects_active_deployment_without_bound_observation():
    deployment = {
        "platform": "vercel",
        "project_id": "TODO:vercel-project-id",
        "status": "active",
        "observed_at": None,
    }
    registry = _registry(_project(deployments=[deployment]))
    assert "ACTIVE_DEPLOYMENT_UNVERIFIED" in _codes(_violations(registry))


def test_rejects_unscoped_current_positive_claim_but_allows_negative_statement():
    bad = _registry(_project(summary="Example is DGAF-governed with security compliance."))
    assert "UNSCOPED_CURRENT_CLAIM" in _codes(_violations(bad))

    good = _registry(
        _project(summary="Security compliance is NOT established; " "DGAF-governed is historical lineage only.")
    )
    assert "UNSCOPED_CURRENT_CLAIM" not in _codes(_violations(good))


def test_requires_projection_metadata_and_rejects_stale_current_projection():
    missing = _registry(projection={})
    assert "PROJECTION_METADATA_MISSING" in _codes(_violations(missing))

    stale_projection = {
        "authority_scope": "projection_only",
        "canonical_source": "project-local repository governance/evidence",
        "canonical_source_revision": "old",
        "projection_checked_at": "2026-08-01T00:00:00Z",
        "projection_status": "CURRENT",
        "staleness_class": None,
    }
    stale = _registry(projection=stale_projection)
    assert "PROJECTION_METADATA_STALE" in _codes(_violations(stale))


def test_historical_persona_lineage_does_not_reactivate_current_authority():
    project = _project(historical_lineage={"former_persona_owners": ["Amethyst", "Sentinel", "COLLEEN"]})
    assert "CURRENT_PERSONA_AUTHORITY" not in _codes(_violations(_registry(project)))


def test_audit_exit_code_fails_closed_on_semantic_violations():
    assert audit_exit_code([]) == 0
    assert audit_exit_code([{"code": "PROJECTION_METADATA_MISSING"}]) == 1


def test_run_audit_returns_nonzero_when_semantic_violations(tmp_path, monkeypatch):
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps({"registry_version": "0.4.0", "projects": []}),
        encoding="utf-8",
    )
    monkeypatch.setattr(ecosystem_audit, "REGISTRY_PATH", str(registry_path))
    monkeypatch.setattr(ecosystem_audit, "fetch_github_repos", lambda owner: [])

    assert ecosystem_audit.run_audit() == 1


def test_mixed_summary_does_not_let_negative_clause_mask_positive_claim():
    mixed = _registry(_project(summary="Example is DGAF-governed. Security compliance is NOT established."))
    assert "UNSCOPED_CURRENT_CLAIM" in _codes(_violations(mixed))


def test_real_registry_has_no_semantic_projection_violations():
    registry_path = Path(__file__).resolve().parents[1] / "registry" / "ecosystem_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    visibility = {
        "DGAF-Framework": (False, False, "main"),
        "Driftwatch": (False, False, "main"),
        "aoga-dashboard": (True, False, "main"),
        "pptl-governance-dashboard": (True, False, "main"),
        "sentinel-governance": (False, False, "main"),
        "Amethyst-Governance-Eval-Stack": (True, False, "main"),
        "junior-apogee-app": (False, False, "main"),
        "phi-calculus-app": (False, False, "main"),
        "Acoustic-mesh": (False, False, "main"),
        "3d-visualization-hub": (False, False, "main"),
        "ai-governance-frameworks": (False, False, "main"),
        "gold-star-qa-framework": (True, True, "main"),
    }
    repos = [
        _repo(
            f"ndrorchestration/{name}",
            private=private,
            archived=archived,
            default_branch=branch,
        )
        for name, (private, archived, branch) in visibility.items()
    ]
    assert (
        collect_semantic_violations(
            registry,
            repos,
            now=datetime(2026, 9, 16, 12, tzinfo=timezone.utc),
        )
        == []
    )
