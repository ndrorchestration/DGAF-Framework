#!/usr/bin/env python3
"""Fail-closed ecosystem registry projection audit.

The registry is a bounded machine-readable projection, not an authority source.
The audit reports structural inventory facts and exits nonzero when material
semantic projection drift is detected.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import os
import re
import sys
from typing import Any

import requests

GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "ndrorchestration")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REGISTRY_PATH = os.environ.get("REGISTRY_PATH", "registry/ecosystem_registry.json")
PROJECTION_MAX_AGE_DAYS = int(os.environ.get("PROJECTION_MAX_AGE_DAYS", "7"))

_ALLOWED_PROJECTION_STATUS = {"CURRENT", "STALE", "HISTORICAL"}
_ALLOWED_STALENESS = {
    None,
    "METADATA",
    "SOURCE_SEMANTIC",
    "RUNTIME_IDENTITY",
    "HISTORICAL_SCOPE",
    "GENERATOR",
}
_PERSONA_OWNERS = {"amethyst", "sentinel", "colleen"}
_HIGH_RISK_PHRASES = (
    "dgaf-governed",
    "dgaf governed",
    "dgaf-certified",
    "dgaf certified",
    "security compliance",
    "certified compliant",
    "guaranteed compliance",
)
_NEGATING_SCOPE_PHRASES = (
    "not established",
    "not certified",
    "not governed",
    "historical",
    "superseded",
    "does not establish",
)


def load_registry(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_github_repos(owner: str) -> list[dict]:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    repos, page = [], 1
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


def _violation(code: str, *, project_id: str | None = None, detail: str) -> dict:
    record = {"code": code, "detail": detail}
    if project_id is not None:
        record["project_id"] = project_id
    return record


def _parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _valid_current_owner(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(("role.", "capability."))


def _is_persona_owner(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() in _PERSONA_OWNERS


def _has_unscoped_current_claim(text: Any) -> bool:
    if not isinstance(text, str):
        return False
    for clause in re.split(r"[.;\n]+", text.lower()):
        if not any(phrase in clause for phrase in _HIGH_RISK_PHRASES):
            continue
        if not any(scope in clause for scope in _NEGATING_SCOPE_PHRASES):
            return True
    return False


def collect_semantic_violations(
    registry: dict,
    github_repos: list[dict],
    *,
    now: datetime | None = None,
) -> list[dict]:
    """Return deterministic fail-closed semantic projection violations."""

    if now is None:
        now = datetime.now(timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    else:
        now = now.astimezone(timezone.utc)

    violations: list[dict] = []
    projection = registry.get("projection")
    required_projection_fields = (
        "authority_scope",
        "canonical_source",
        "canonical_source_revision",
        "projection_checked_at",
        "projection_status",
        "staleness_class",
    )
    if not isinstance(projection, dict):
        violations.append(
            _violation(
                "PROJECTION_METADATA_MISSING",
                detail="registry.projection is required and must be an object",
            )
        )
        projection = {}
    else:
        missing = [field for field in required_projection_fields if field not in projection]
        if missing:
            violations.append(
                _violation(
                    "PROJECTION_METADATA_MISSING",
                    detail=f"projection missing required fields: {', '.join(missing)}",
                )
            )

    if projection:
        if projection.get("authority_scope") != "projection_only":
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail="projection.authority_scope must equal projection_only",
                )
            )
        if not str(projection.get("canonical_source", "")).strip():
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail="projection.canonical_source must be non-empty",
                )
            )
        if not str(projection.get("canonical_source_revision", "")).strip():
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail="projection.canonical_source_revision must be non-empty",
                )
            )
        status = projection.get("projection_status")
        if status not in _ALLOWED_PROJECTION_STATUS:
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail=f"invalid projection_status: {status!r}",
                )
            )
        staleness = projection.get("staleness_class")
        if staleness not in _ALLOWED_STALENESS:
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail=f"invalid staleness_class: {staleness!r}",
                )
            )
        checked_at = _parse_datetime(projection.get("projection_checked_at"))
        if checked_at is None:
            violations.append(
                _violation(
                    "PROJECTION_METADATA_INVALID",
                    detail="projection_checked_at must be a parseable ISO-8601 timestamp",
                )
            )
        elif (
            status == "CURRENT"
            and (now - checked_at).total_seconds() > PROJECTION_MAX_AGE_DAYS * 86400
        ):
            violations.append(
                _violation(
                    "PROJECTION_METADATA_STALE",
                    detail=(
                        f"CURRENT projection is older than {PROJECTION_MAX_AGE_DAYS} days: "
                        f"{projection.get('projection_checked_at')}"
                    ),
                )
            )

    gh_by_name = {
        repo.get("full_name"): repo
        for repo in github_repos
        if repo.get("full_name")
    }

    for project in registry.get("projects", []):
        project_id = str(project.get("id", "<missing-id>"))
        github = project.get("github") or {}
        full_name = None
        if github.get("owner") and github.get("repo"):
            full_name = f"{github['owner']}/{github['repo']}"
        observed = gh_by_name.get(full_name)
        if observed:
            for field in ("private", "archived", "default_branch"):
                if field in github and github.get(field) != observed.get(field):
                    violations.append(
                        _violation(
                            "GITHUB_METADATA_MISMATCH",
                            project_id=project_id,
                            detail=(
                                f"{field} registry={github.get(field)!r} "
                                f"observed={observed.get(field)!r}"
                            ),
                        )
                    )

        authority = project.get("authority")
        if isinstance(authority, dict):
            current_owner = authority.get("current_owner")
            if current_owner is not None and not _valid_current_owner(current_owner):
                code = (
                    "CURRENT_PERSONA_AUTHORITY"
                    if _is_persona_owner(current_owner)
                    else "CURRENT_AUTHORITY_INVALID"
                )
                violations.append(
                    _violation(
                        code,
                        project_id=project_id,
                        detail=(
                            "current authority owner must be a functional "
                            f"role/capability id: {current_owner!r}"
                        ),
                    )
                )

        for container_name, field in (
            ("documentation", "owner"),
            ("governance", "governance_owner"),
        ):
            container = project.get(container_name)
            if isinstance(container, dict) and _is_persona_owner(container.get(field)):
                violations.append(
                    _violation(
                        "CURRENT_PERSONA_AUTHORITY",
                        project_id=project_id,
                        detail=f"legacy current persona authority at {container_name}.{field}",
                    )
                )

        if _has_unscoped_current_claim(project.get("summary")):
            violations.append(
                _violation(
                    "UNSCOPED_CURRENT_CLAIM",
                    project_id=project_id,
                    detail=(
                        "summary contains an unscoped current "
                        "authority/certification/compliance claim"
                    ),
                )
            )

        for deployment in project.get("deployments", []):
            if deployment.get("status") != "active":
                continue
            project_id_value = str(deployment.get("project_id", ""))
            observed_at = _parse_datetime(deployment.get("observed_at"))
            evidence = deployment.get("evidence")
            if (
                project_id_value.startswith("TODO")
                or not project_id_value
                or observed_at is None
                or not evidence
            ):
                violations.append(
                    _violation(
                        "ACTIVE_DEPLOYMENT_UNVERIFIED",
                        project_id=project_id,
                        detail=(
                            "active deployment requires non-TODO identity, "
                            "observed_at, and evidence binding"
                        ),
                    )
                )

    return violations


def audit_exit_code(violations: list[dict]) -> int:
    return 1 if violations else 0


def run_audit() -> int:
    registry = load_registry(REGISTRY_PATH)
    projects = registry.get("projects", [])
    reg_keys = {
        f"{p['github']['owner']}/{p['github']['repo']}": p
        for p in projects
        if p.get("github")
    }

    print(f"Registry v{registry.get('registry_version')} — {len(projects)} projects loaded.")

    gh_repos = fetch_github_repos(GITHUB_OWNER)
    gh_keys = {r["full_name"]: r for r in gh_repos}
    print(f"GitHub — {len(gh_keys)} repos found for {GITHUB_OWNER}.")

    missing_in_registry = sorted(set(gh_keys) - set(reg_keys))
    missing_in_github = sorted(set(reg_keys) - set(gh_keys))

    print("\n=== REPOS IN GITHUB BUT NOT IN REGISTRY ===")
    if missing_in_registry:
        for key in missing_in_registry:
            r = gh_keys[key]
            print(
                f"  UNREGISTERED  {key}  "
                f"(private={r.get('private')}, archived={r.get('archived')})"
            )
    else:
        print("  None — registry is complete.")

    print("\n=== PROJECTS IN REGISTRY BUT MISSING FROM GITHUB ===")
    if missing_in_github:
        for key in missing_in_github:
            p = reg_keys[key]
            print(
                f"  MISSING  {key}  "
                f"(id={p.get('id')}, lifecycle={p.get('lifecycle_state')})"
            )
    else:
        print("  None — all registry projects have corresponding GitHub repos.")

    print("\n=== DEPLOYMENT TODO STUBS ===")
    for project in projects:
        for deployment in project.get("deployments", []):
            if str(deployment.get("url", "")).startswith("TODO") or str(
                deployment.get("project_id", "")
            ).startswith("TODO"):
                print(
                    f"  FILL_IN  {project['id']}  platform={deployment['platform']}  "
                    f"url={deployment.get('url')}"
                )

    print("\n=== SEMANTIC PROJECTION VIOLATIONS ===")
    violations = collect_semantic_violations(registry, gh_repos)
    if violations:
        for violation in violations:
            project_suffix = (
                f" project={violation['project_id']}"
                if violation.get("project_id")
                else ""
            )
            print(f"  {violation['code']}{project_suffix}  {violation['detail']}")
    else:
        print(
            "  None — bounded projection semantics are internally consistent "
            "with observed GitHub metadata."
        )

    print("\n=== LIFECYCLE SUMMARY ===")
    states = Counter(p.get("lifecycle_state") for p in projects)
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")

    print("\n=== PATTERN COVERAGE ===")
    pattern_map: dict[str, list[str]] = defaultdict(list)
    for project in projects:
        for pattern in project.get("patterns", []):
            pattern_map[pattern].append(project["id"])
    for pattern, ids in sorted(pattern_map.items()):
        print(f"  {pattern}: {len(ids)} projects")

    return audit_exit_code(violations)


if __name__ == "__main__":
    sys.exit(run_audit())
