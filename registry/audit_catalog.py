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
