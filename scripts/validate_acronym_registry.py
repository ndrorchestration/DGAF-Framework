#!/usr/bin/env python3
"""Fail-closed acronym/identifier completeness validation for current-facing docs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "taxonomy" / "ACRONYM_REGISTRY.v1.json"
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*|SSoT)(?![A-Za-z0-9])")
REQUIRED = {"DGAF","PDMAL","AOSS","ACP","MDAR","AOGA","AAR","PDP","PEP","ASIS"}

def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def validate_registry(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("record_type") != "NDR_ACRONYM_REGISTRY":
        errors.append("record_type mismatch")
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    authority = data.get("authority", {})
    if authority.get("undefined_current_acronyms_prohibited") is not True:
        errors.append("undefined_current_acronyms_prohibited must be true")
    if authority.get("backronyms_prohibited") is not True:
        errors.append("backronyms_prohibited must be true")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["entries must be a non-empty list"]
    seen: set[str] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry[{i}] must be an object")
            continue
        for key in ("token","expansion","classification","status"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                errors.append(f"entry[{i}] missing non-empty {key}")
        token = entry.get("token")
        if isinstance(token, str):
            if token in seen:
                errors.append(f"duplicate token: {token}")
            seen.add(token)
        if entry.get("status") == "current" and entry.get("classification") == "opaque_historical_identifier":
            errors.append(f"{token}: opaque historical identifier cannot be current")
    missing = REQUIRED - seen
    if missing:
        errors.append(f"missing required canonical tokens: {sorted(missing)}")
    return errors

def lint_surfaces(data: dict) -> list[str]:
    errors: list[str] = []
    registered = {e["token"] for e in data["entries"]}
    allow = set(data.get("literal_allowlist", []))
    patterns = [re.compile(p) for p in data.get("ignored_patterns", [])]
    for rel in data.get("scan_paths", []):
        path = ROOT / rel
        if not path.exists():
            errors.append(f"scan path missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        unknown: set[str] = set()
        for token in TOKEN_RE.findall(text):
            if token in registered or token in allow:
                continue
            if any(p.fullmatch(token) for p in patterns):
                continue
            unknown.add(token)
        if unknown:
            errors.append(f"{rel}: undefined uppercase/shorthand tokens: {sorted(unknown)}")
    return errors

def main() -> int:
    data = load()
    errors = validate_registry(data) + lint_surfaces(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: acronym registry v1 (schema + current-surface completeness)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
