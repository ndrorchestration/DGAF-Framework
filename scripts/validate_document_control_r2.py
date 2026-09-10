#!/usr/bin/env python3
"""Validate registered DGAF document-control R2 temporal routing.

This validator is deliberately dependency-free and non-authorizing. It validates
projection/routing metadata only; it cannot establish scientific truth, freeze,
collection authorization, efficacy, or empirical N.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "docs/governance/document-control-r2.json"
ALLOWED_CLASSES = {
    "CURRENT_AUTHORITY",
    "CURRENT_SUPPORTING",
    "HISTORICAL",
    "SUPERSEDED",
    "AUDIT",
    "PROVENANCE",
    "EXPLORATORY",
}
ALLOWED_PROJECTION_STATES = {"VERIFIED", "NOT_VERIFIED", "STALE", "INVALID"}
REQUIRED = {
    "record_id",
    "title",
    "record_class",
    "domain",
    "owner",
    "scope",
    "lifecycle_state",
    "current_state_ref",
    "projection_state",
}


def fail(message: str) -> None:
    raise ValueError(message)


def repo_path(value: str) -> Path:
    if not isinstance(value, str) or not value or value.startswith(("/", "\\")):
        fail(f"invalid repository path: {value!r}")
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"path escapes repository: {value!r}")
    return candidate


def validate(data: dict) -> None:
    if data.get("schema_version") != "0.1":
        fail("schema_version must be 0.1")
    authority_ref = data.get("current_authority_ref")
    if not authority_ref or not repo_path(authority_ref).is_file():
        fail("current_authority_ref must point to an existing repository file")
    records = data.get("records")
    if not isinstance(records, list) or not records:
        fail("records must be a non-empty list")

    ids: set[str] = set()
    current_by_scope: dict[str, str] = {}
    for record in records:
        if not isinstance(record, dict):
            fail("each record must be an object")
        missing = REQUIRED - record.keys()
        if missing:
            fail(f"record missing required fields: {sorted(missing)}")
        rid = record["record_id"]
        if not isinstance(rid, str) or not rid or rid in ids:
            fail(f"invalid or duplicate record_id: {rid!r}")
        ids.add(rid)
        record_class = record["record_class"]
        if record_class not in ALLOWED_CLASSES:
            fail(f"{rid}: invalid record_class {record_class!r}")
        if record["projection_state"] not in ALLOWED_PROJECTION_STATES:
            fail(f"{rid}: invalid projection_state")
        owner = record["owner"]
        if not isinstance(owner, dict) or not owner.get("authority_ref"):
            fail(f"{rid}: owner.authority_ref is required")
        if not repo_path(owner["authority_ref"]).is_file():
            fail(f"{rid}: owner source is missing")
        current_ref = record["current_state_ref"]
        if not repo_path(current_ref).is_file():
            fail(f"{rid}: current_state_ref is missing")

        if record_class in {"HISTORICAL", "SUPERSEDED"}:
            if current_ref == owner["authority_ref"]:
                fail(f"{rid}: historical/superseded record routes to itself as current")
            if record.get("last_verified_at") is not None and record["projection_state"] != "VERIFIED":
                fail(f"{rid}: non-VERIFIED projection carries last_verified_at")
            if record_class == "SUPERSEDED" and not record.get("superseded_by") and not record.get("terminal_reason"):
                fail(f"{rid}: SUPERSEDED requires superseded_by or terminal_reason")

        if (
            record["projection_state"] in {"NOT_VERIFIED", "STALE", "INVALID"}
            and record.get("last_verified_at") is not None
        ):
            fail(f"{rid}: {record['projection_state']} must not present a verification timestamp")
        if record["projection_state"] == "VERIFIED" and not record.get("last_verified_at"):
            fail(f"{rid}: VERIFIED requires last_verified_at")

        if record_class == "CURRENT_AUTHORITY":
            scope = record["scope"]
            prior = current_by_scope.get(scope)
            if prior:
                fail(f"conflicting CURRENT_AUTHORITY projections for scope {scope!r}: {prior}, {rid}")
            current_by_scope[scope] = rid


def main() -> int:
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_REGISTRY
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"DOCUMENT_CONTROL_R2=FAIL: {exc}", file=sys.stderr)
        return 1
    print("DOCUMENT_CONTROL_R2=PASS " f"records={len(data['records'])} authority={data['current_authority_ref']}")
    print("SCIENTIFIC_STATE_EFFECT=NONE")
    print("AUTHORIZATION_EFFECT=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
