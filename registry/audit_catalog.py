"""Validation helpers for the repository-local audit/assurance catalog.

This module validates catalog structure and explicit assurance boundaries. It does
not execute the audits it describes and does not promote repository, runtime,
scientific, or authorization state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REQUIRED_TEXT_FIELDS = (
    "id",
    "name",
    "class",
    "assertion",
    "owner",
    "decision_effect",
    "fail_behavior",
    "independence",
    "lifecycle",
)
_REQUIRED_LIST_FIELDS = (
    "target_layers",
    "implementation",
    "trigger",
    "evidence",
    "verdicts",
    "non_effects",
)


def load_catalog(path: Path | str) -> dict[str, Any]:
    """Load a UTF-8 JSON audit catalog.

    Missing files and malformed JSON intentionally propagate as hard failures.
    """

    catalog_path = Path(path)
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def _violation(code: str, audit_id: str | None = None, field: str | None = None) -> dict[str, str]:
    result = {"code": code}
    if audit_id:
        result["audit_id"] = audit_id
    if field:
        result["field"] = field
    return result


def collect_catalog_violations(catalog: dict[str, Any]) -> list[dict[str, str]]:
    """Return deterministic structural/semantic violations for a catalog."""

    violations: list[dict[str, str]] = []

    if catalog.get("version") != "AUDIT_CATALOG_V1":
        violations.append(_violation("CATALOG_VERSION_INVALID"))

    audits = catalog.get("audits")
    if not isinstance(audits, list) or not audits:
        violations.append(_violation("AUDIT_LIST_MISSING"))
        return violations

    seen_ids: set[str] = set()
    for entry in audits:
        if not isinstance(entry, dict):
            violations.append(_violation("AUDIT_ENTRY_INVALID"))
            continue

        audit_id = entry.get("id") if isinstance(entry.get("id"), str) else None
        if audit_id:
            if audit_id in seen_ids:
                violations.append(_violation("DUPLICATE_AUDIT_ID", audit_id))
            seen_ids.add(audit_id)

        for field in _REQUIRED_TEXT_FIELDS:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                code = {
                    "decision_effect": "DECISION_EFFECT_MISSING",
                    "fail_behavior": "FAIL_BEHAVIOR_MISSING",
                    "owner": "OWNER_MISSING",
                    "assertion": "ASSERTION_MISSING",
                }.get(field, "REQUIRED_FIELD_MISSING")
                violations.append(_violation(code, audit_id, field))

        for field in _REQUIRED_LIST_FIELDS:
            value = entry.get(field)
            invalid_items = isinstance(value, list) and any(
                not isinstance(item, str) or not item.strip() for item in value
            )
            if not isinstance(value, list) or not value or invalid_items:
                code = {
                    "non_effects": "NON_EFFECTS_MISSING",
                    "target_layers": "TARGET_LAYER_MISSING",
                    "implementation": "IMPLEMENTATION_BINDING_MISSING",
                    "evidence": "EVIDENCE_BINDING_MISSING",
                }.get(field, "REQUIRED_LIST_FIELD_MISSING")
                violations.append(_violation(code, audit_id, field))

        if not isinstance(entry.get("blocking"), bool):
            violations.append(_violation("BLOCKING_SEMANTICS_MISSING", audit_id, "blocking"))

        known_gaps = entry.get("known_gaps")
        if not isinstance(known_gaps, list) or any(not isinstance(item, str) for item in known_gaps):
            violations.append(_violation("KNOWN_GAPS_INVALID", audit_id, "known_gaps"))

    coverage = catalog.get("coverage")
    if not isinstance(coverage, dict):
        violations.append(_violation("COVERAGE_METADATA_MISSING"))
    else:
        if not isinstance(coverage.get("status"), str) or not coverage["status"].strip():
            violations.append(_violation("COVERAGE_STATUS_MISSING"))
        gaps = coverage.get("known_gaps")
        if not isinstance(gaps, list) or not gaps:
            violations.append(_violation("COVERAGE_GAPS_MISSING"))

    return violations


def collect_unmapped_workflows(repo_root: Path | str, catalog: dict[str, Any]) -> list[str]:
    """Return workflow definitions not exactly bound by catalog implementation paths.

    Unmapped workflow definitions are coverage gaps only. Their presence does not
    classify them as audits or change catalog coverage state.
    """

    root = Path(repo_root)
    workflows_dir = root / ".github" / "workflows"
    discovered = {
        path.relative_to(root).as_posix()
        for pattern in ("*.yml", "*.yaml")
        for path in workflows_dir.glob(pattern)
        if path.is_file()
    }

    mapped: set[str] = set()
    audits = catalog.get("audits")
    if isinstance(audits, list):
        for entry in audits:
            if not isinstance(entry, dict):
                continue
            implementation = entry.get("implementation")
            if not isinstance(implementation, list):
                continue
            mapped.update(value for value in implementation if isinstance(value, str) and value)

    return sorted(discovered - mapped)


def collect_missing_implementation_paths(repo_root: Path | str, catalog: dict[str, Any]) -> list[dict[str, str]]:
    """Return catalog implementation bindings that do not resolve in the repository.

    Only repository-relative implementation bindings are accepted by this catalog.
    Missing bindings are assurance defects; this helper does not infer whether an
    unmapped repository path is itself an audit.
    """

    root = Path(repo_root)
    missing: list[dict[str, str]] = []
    audits = catalog.get("audits")
    if not isinstance(audits, list):
        return missing

    for entry in audits:
        if not isinstance(entry, dict):
            continue
        audit_id = entry.get("id")
        implementation = entry.get("implementation")
        if not isinstance(implementation, list):
            continue
        for value in implementation:
            if not isinstance(value, str) or not value:
                continue
            if not (root / value).exists():
                missing.append({"audit_id": str(audit_id or ""), "path": value})

    return sorted(missing, key=lambda item: (item["audit_id"], item["path"]))


_ALLOWED_WORKFLOW_CLASSIFICATIONS = {"CLASSIFIED_NON_AUDIT"}
_ALLOWED_WORKFLOW_LIFECYCLES = {
    "CURRENT",
    "HISTORICAL_EXACT_SCOPE",
    "CLOSED_BOUNDED_EXACT_SCOPE",
}


def load_workflow_classification(path: Path | str) -> dict[str, Any]:
    """Load the machine-readable workflow classification registry."""

    classification_path = Path(path)
    return json.loads(classification_path.read_text(encoding="utf-8"))


def collect_workflow_classification_violations(
    classification: dict[str, Any],
) -> list[dict[str, str]]:
    """Return deterministic structural violations for workflow classifications."""

    violations: list[dict[str, str]] = []
    if classification.get("version") != "WORKFLOW_CLASSIFICATION_V1":
        violations.append(_violation("WORKFLOW_CLASSIFICATION_VERSION_INVALID"))
        return violations

    entries = classification.get("classifications")
    if not isinstance(entries, list):
        violations.append(_violation("WORKFLOW_CLASSIFICATION_LIST_MISSING"))
        return violations

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            violations.append(_violation("WORKFLOW_CLASSIFICATION_ENTRY_INVALID"))
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path.startswith(".github/workflows/"):
            violations.append(_violation("WORKFLOW_CLASSIFICATION_PATH_INVALID"))
            continue
        if path in seen:
            violations.append(_violation("WORKFLOW_CLASSIFICATION_DUPLICATE_PATH"))
        seen.add(path)

        if entry.get("classification") not in _ALLOWED_WORKFLOW_CLASSIFICATIONS:
            violations.append(_violation("WORKFLOW_CLASSIFICATION_KIND_INVALID"))
        if entry.get("lifecycle") not in _ALLOWED_WORKFLOW_LIFECYCLES:
            violations.append(_violation("WORKFLOW_CLASSIFICATION_LIFECYCLE_INVALID"))
        for field in ("kind", "controller", "decision_effect", "reason"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                violations.append(_violation("WORKFLOW_CLASSIFICATION_FIELD_MISSING", field=field))

    return violations


def collect_unclassified_workflows(
    repo_root: Path | str,
    catalog: dict[str, Any],
    classification: dict[str, Any],
) -> list[str]:
    """Return workflow definitions neither audit-mapped nor explicitly classified."""

    root = Path(repo_root)
    workflows_dir = root / ".github" / "workflows"
    discovered = {
        path.relative_to(root).as_posix()
        for pattern in ("*.yml", "*.yaml")
        for path in workflows_dir.glob(pattern)
        if path.is_file()
    }

    audit_paths: set[str] = set()
    audits = catalog.get("audits")
    if isinstance(audits, list):
        for entry in audits:
            if isinstance(entry, dict) and isinstance(entry.get("implementation"), list):
                audit_paths.update(
                    value
                    for value in entry["implementation"]
                    if isinstance(value, str) and value.startswith(".github/workflows/")
                )

    classified_paths = {
        entry["path"]
        for entry in classification.get("classifications", [])
        if isinstance(entry, dict)
        and isinstance(entry.get("path"), str)
        and entry.get("classification") == "CLASSIFIED_NON_AUDIT"
    }

    return sorted(discovered - audit_paths - classified_paths)


def collect_missing_classified_workflow_paths(repo_root: Path | str, classification: dict[str, Any]) -> list[str]:
    """Return classified workflow paths that do not exist in the repository."""

    root = Path(repo_root)
    missing = []
    for entry in classification.get("classifications", []):
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if isinstance(path, str) and path and not (root / path).exists():
            missing.append(path)
    return sorted(missing)
