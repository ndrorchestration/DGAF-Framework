from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "registry/ecosystem_audit.py"

spec = importlib.util.spec_from_file_location("ecosystem_audit", MODULE_PATH)
assert spec is not None and spec.loader is not None
MODULE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MODULE)


def _validator():
    validator = getattr(MODULE, "validate_registry_semantics", None)
    assert callable(validator), "ecosystem audit must expose validate_registry_semantics"
    return validator


def _registry(project: dict) -> dict:
    return {
        "registry_version": "0.5.0",
        "generated_at": "2026-09-15T06:51:14Z",
        "projection": {
            "authority_scope": "NON_AUTHORITATIVE_ECOSYSTEM_PROJECTION",
            "canonical_source": "PROJECT_LOCAL_EVIDENCE_AND_OBSERVABLE_GITHUB_METADATA",
            "canonical_source_revision": "1fb2c665587d5a0e7b213aef1cc5c870097cdc9b",
            "projection_checked_at": "2026-09-15T06:51:14Z",
            "projection_status": "CURRENT",
            "coverage_scope": "CURATED_PROJECT_REGISTRY_NOT_EXHAUSTIVE_REPOSITORY_INVENTORY",
        },
        "projects": [project],
    }


def _project(*, private: bool = False) -> dict:
    return {
        "id": "example",
        "name": "Example",
        "summary": "Bounded project-local example.",
        "github": {
            "owner": "ndrorchestration",
            "repo": "example",
            "default_branch": "main",
            "private": private,
            "archived": False,
        },
        "documentation": {
            "status": "current",
            "steward_role": "role.provenance-archivist",
        },
        "governance": {
            "authority_scope": "PROJECT_LOCAL_NO_INHERITED_DGAF_AUTHORITY",
            "governance_owner_role": None,
        },
        "projection": {
            "projection_status": "CURRENT",
            "projection_checked_at": "2026-09-15T06:51:14Z",
            "canonical_source": "repository-local evidence",
            "staleness_class": [],
        },
        "deployments": [],
        "lifecycle_state": "active",
    }


def test_validator_rejects_current_persona_authority() -> None:
    project = _project()
    project["documentation"] = {"owner": "Amethyst"}
    project["governance"] = {"governance_owner": "Sentinel"}

    errors = _validator()(_registry(project), {})

    assert any("persona authority" in error.lower() for error in errors)


def test_validator_rejects_active_deployment_without_observation_binding() -> None:
    project = _project()
    project["deployments"] = [
        {
            "platform": "vercel",
            "project_id": "TODO:vercel-project-id",
            "url": "https://example.vercel.app",
            "status": "active",
            "observed_at": None,
        }
    ]

    errors = _validator()(_registry(project), {})

    assert any("deployment" in error.lower() and "evidence" in error.lower() for error in errors)


def test_validator_detects_observable_github_metadata_drift() -> None:
    project = _project(private=False)
    observed = {
        "ndrorchestration/example": {
            "private": True,
            "archived": False,
            "default_branch": "main",
        }
    }

    errors = _validator()(_registry(project), observed)

    assert any("private" in error.lower() for error in errors)


def test_private_repo_absence_is_not_promoted_to_missing_evidence() -> None:
    project = _project(private=True)

    errors = _validator()(_registry(project), {})

    assert not any("missing from github" in error.lower() for error in errors)


def test_historical_lineage_can_preserve_persona_and_certification_terms() -> None:
    project = _project(private=True)
    project["summary"] = "Historical S-Tier certification and Amethyst lineage record."
    project["lifecycle_state"] = "archived"
    project["projection"] = {
        "projection_status": "HISTORICAL",
        "projection_checked_at": "2026-09-15T06:51:14Z",
        "canonical_source": "historical repository record",
        "staleness_class": ["HISTORICAL_SCOPE"],
    }
    project["historical_lineage"] = {
        "personas": ["Amethyst"],
        "labels": ["S-Tier certification"],
    }

    errors = _validator()(_registry(project), {})

    assert errors == []


def test_validator_rejects_unscoped_current_governance_or_compliance_claim() -> None:
    project = _project()
    project["summary"] = "DGAF-governed service providing security compliance."

    errors = _validator()(_registry(project), {})

    assert any("unscoped current claim" in error.lower() for error in errors)


def test_checked_in_registry_has_no_internal_projection_drift() -> None:
    registry = json.loads((ROOT / "registry/ecosystem_registry.json").read_text(encoding="utf-8"))
    observed: dict[str, dict] = {}
    for project in registry.get("projects", []):
        github = project.get("github")
        if isinstance(github, dict) and github.get("private") is False:
            key = f"{github['owner']}/{github['repo']}"
            observed[key] = {
                "private": github.get("private"),
                "archived": github.get("archived"),
                "default_branch": github.get("default_branch"),
            }

    errors = _validator()(registry, observed)

    assert errors == []
