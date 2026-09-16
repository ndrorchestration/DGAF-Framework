#!/usr/bin/env python3
"""Evidence-bounded ecosystem registry audit.

Compares the curated ecosystem projection against observable GitHub metadata and
validates current projection semantics. Private repositories that are absent
from the search result are treated as not observable, not as negative evidence.

Usage:
    GITHUB_TOKEN=<your-token> python ecosystem_audit.py
    REGISTRY_PATH=registry/ecosystem_registry.json python ecosystem_audit.py
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from typing import Any

import requests

GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "ndrorchestration")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REGISTRY_PATH = os.environ.get("REGISTRY_PATH", "registry/ecosystem_registry.json")

CURRENT_PERSONAS = frozenset({"Amethyst", "Sentinel", "COLLEEN"})
PROJECTION_STATUSES = frozenset({"CURRENT", "STALE", "HISTORICAL"})
RISKY_CURRENT_CLAIMS = (
    "dgaf-" + "governed",
    "dgaf " + "governed",
    "dgaf-" + "certified",
    "dgaf " + "certified",
    "security " + "compliance",
    "s-tier " + "certification",
    "production-" + "ready",
    "production " + "ready",
)
CLAIM_BOUNDARY_TERMS = (
    "not established",
    "does not establish",
    "does not confer",
    "not certified",
    "historical",
    "legacy",
    "not authorized",
    "no inherited",
)


def load_registry(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("registry root must be one JSON object")
    return value


def fetch_github_repos(owner: str) -> list[dict[str, Any]]:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"https://api.github.com/search/repositories?q=user:{owner}&per_page=50&page={page}"
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        repos.extend(items)
        if len(items) < 50:
            break
        page += 1
    return repos


def _is_historical(project: dict[str, Any]) -> bool:
    projection = project.get("projection")
    return isinstance(projection, dict) and projection.get("projection_status") == "HISTORICAL"


def _project_projection_errors(project: dict[str, Any]) -> list[str]:
    project_id = str(project.get("id", "<unknown>"))
    projection = project.get("projection")
    if not isinstance(projection, dict):
        return [f"{project_id}: project projection metadata is required"]

    errors: list[str] = []
    for field in ("projection_status", "projection_checked_at", "canonical_source", "staleness_class"):
        if field not in projection or projection[field] in (None, ""):
            errors.append(f"{project_id}: projection.{field} is required")

    status = projection.get("projection_status")
    if status not in PROJECTION_STATUSES:
        errors.append(f"{project_id}: invalid project projection_status={status!r}")

    staleness_class = projection.get("staleness_class")
    if not isinstance(staleness_class, list):
        errors.append(f"{project_id}: projection.staleness_class must be an array")

    return errors


def _current_persona_authority_errors(project: dict[str, Any]) -> list[str]:
    if _is_historical(project):
        return []

    errors: list[str] = []
    project_id = str(project.get("id", "<unknown>"))
    documentation = project.get("documentation")
    governance = project.get("governance")

    if isinstance(documentation, dict):
        owner = documentation.get("owner")
        if owner in CURRENT_PERSONAS:
            errors.append(f"{project_id}: current persona authority in documentation.owner={owner}")

    if isinstance(governance, dict):
        owner = governance.get("governance_owner")
        if owner in CURRENT_PERSONAS:
            errors.append(f"{project_id}: current persona authority in governance.governance_owner={owner}")

    return errors


def _claim_scope_errors(project: dict[str, Any]) -> list[str]:
    if _is_historical(project):
        return []

    summary = str(project.get("summary", ""))
    normalized = summary.lower()
    risky = [claim for claim in RISKY_CURRENT_CLAIMS if claim in normalized]
    if not risky:
        return []
    if any(boundary in normalized for boundary in CLAIM_BOUNDARY_TERMS):
        return []

    project_id = str(project.get("id", "<unknown>"))
    return [f"{project_id}: unscoped current claim in summary ({', '.join(sorted(risky))})"]


def _deployment_errors(project: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    project_id = str(project.get("id", "<unknown>"))
    deployments = project.get("deployments", [])
    if not isinstance(deployments, list):
        return [f"{project_id}: deployments must be an array"]

    for index, deployment in enumerate(deployments):
        if not isinstance(deployment, dict):
            errors.append(f"{project_id}: deployment[{index}] must be an object")
            continue
        status = deployment.get("status")
        if status not in {"active", "verified_runtime"}:
            continue
        project_identity = str(deployment.get("project_id", ""))
        observed_at = deployment.get("observed_at")
        evidence_ref = deployment.get("evidence_ref")
        if project_identity.startswith("TODO") or not observed_at or not evidence_ref:
            errors.append(f"{project_id}: deployment[{index}] active runtime claim lacks dated evidence binding")
    return errors


def _github_metadata_errors(project: dict[str, Any], observed_repos: dict[str, dict[str, Any]]) -> list[str]:
    github = project.get("github")
    if not isinstance(github, dict):
        return []

    owner = github.get("owner")
    repo = github.get("repo")
    if not isinstance(owner, str) or not isinstance(repo, str):
        return [f"{project.get('id', '<unknown>')}: malformed GitHub identity"]

    key = f"{owner}/{repo}"
    observed = observed_repos.get(key)
    if observed is None:
        if github.get("private") is True:
            return []
        return [f"{project.get('id', '<unknown>')}: public repository missing from observable GitHub result"]

    errors: list[str] = []
    for field in ("private", "archived", "default_branch"):
        if field in github and field in observed and github[field] != observed[field]:
            errors.append(
                f"{project.get('id', '<unknown>')}: GitHub {field} drift "
                f"registry={github[field]!r} observed={observed[field]!r}"
            )
    return errors


def validate_registry_semantics(
    registry: dict[str, Any], observed_repos: dict[str, dict[str, Any]] | None = None
) -> list[str]:
    """Return deterministic semantic errors without promoting unobservable absence to fact."""

    errors: list[str] = []
    observed = observed_repos or {}
    projection = registry.get("projection")
    if not isinstance(projection, dict):
        errors.append("registry: projection metadata is required")
    else:
        required_projection = (
            "authority_scope",
            "canonical_source",
            "canonical_source_revision",
            "projection_checked_at",
            "projection_status",
            "coverage_scope",
        )
        for field in required_projection:
            if not projection.get(field):
                errors.append(f"registry: projection.{field} is required")
        status = projection.get("projection_status")
        if status not in PROJECTION_STATUSES:
            errors.append(f"registry: invalid projection_status={status!r}")

    projects = registry.get("projects", [])
    if not isinstance(projects, list):
        return errors + ["registry: projects must be an array"]

    for project in projects:
        if not isinstance(project, dict):
            errors.append("registry: project entries must be objects")
            continue
        errors.extend(_project_projection_errors(project))
        errors.extend(_current_persona_authority_errors(project))
        errors.extend(_claim_scope_errors(project))
        errors.extend(_deployment_errors(project))
        errors.extend(_github_metadata_errors(project, observed))

    return errors


def run_audit() -> int:
    registry = load_registry(REGISTRY_PATH)
    projects = registry.get("projects", [])
    reg_keys = {
        f"{project['github']['owner']}/{project['github']['repo']}": project
        for project in projects
        if isinstance(project, dict) and project.get("github")
    }

    print(f"Registry v{registry.get('registry_version')} — {len(projects)} projects loaded.")

    gh_repos = fetch_github_repos(GITHUB_OWNER)
    gh_keys = {repo["full_name"]: repo for repo in gh_repos}
    print(f"GitHub — {len(gh_keys)} observable repos found for {GITHUB_OWNER}.")

    missing_in_registry = sorted(set(gh_keys) - set(reg_keys))
    missing_in_github = sorted(set(reg_keys) - set(gh_keys))

    print("\n=== OBSERVABLE REPOS OUTSIDE CURATED REGISTRY ===")
    if missing_in_registry:
        for key in missing_in_registry:
            repo = gh_keys[key]
            print(
                f"  OUT_OF_SCOPE_OR_UNREGISTERED  {key}  "
                f"(private={repo.get('private')}, archived={repo.get('archived')})"
            )
    else:
        print("  None observed.")

    print("\n=== REGISTRY PROJECT OBSERVABILITY ===")
    if missing_in_github:
        for key in missing_in_github:
            project = reg_keys[key]
            github = project.get("github", {})
            if github.get("private") is True:
                label = "NOT_OBSERVABLE_WITH_TOKEN"
            else:
                label = "MISSING_OR_UNOBSERVED_PUBLIC"
            print(f"  {label}  {key}  (id={project.get('id')}, lifecycle={project.get('lifecycle_state')})")
    else:
        print("  All curated projects are observable.")

    print("\n=== DEPLOYMENT IDENTITY GAPS ===")
    for project in projects:
        if not isinstance(project, dict):
            continue
        for deployment in project.get("deployments", []):
            if not isinstance(deployment, dict):
                continue
            if str(deployment.get("url", "")).startswith("TODO") or str(deployment.get("project_id", "")).startswith(
                "TODO"
            ):
                print(
                    f"  UNVERIFIED_IDENTITY  {project.get('id')}  "
                    f"platform={deployment.get('platform')}  url={deployment.get('url')}"
                )

    print("\n=== LIFECYCLE SUMMARY ===")
    states = Counter(project.get("lifecycle_state") for project in projects if isinstance(project, dict))
    for state, count in sorted(states.items(), key=lambda item: str(item[0])):
        print(f"  {state}: {count}")

    print("\n=== PATTERN COVERAGE ===")
    pattern_map: defaultdict[str, list[str]] = defaultdict(list)
    for project in projects:
        if not isinstance(project, dict):
            continue
        for pattern in project.get("patterns", []):
            pattern_map[str(pattern)].append(str(project.get("id")))
    for pattern, ids in sorted(pattern_map.items()):
        print(f"  {pattern}: {len(ids)} projects")

    semantic_errors = validate_registry_semantics(registry, gh_keys)
    print("\n=== SEMANTIC PROJECTION VALIDATION ===")
    if semantic_errors:
        for error in semantic_errors:
            print(f"  ERROR  {error}")
        return 1

    print("  PASS — no observable semantic contradictions detected.")
    return 0


if __name__ == "__main__":
    sys.exit(run_audit())
