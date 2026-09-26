#!/usr/bin/env python3
"""Fail-closed acronym/identifier completeness validation for current-facing docs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "taxonomy" / "ACRONYM_REGISTRY.v1.json"
HUMAN_REGISTRY = ROOT / "docs" / "taxonomy" / "NDR_ACRONYM_REGISTRY.md"
PROJECTION_START = "<!-- ACRONYM_JSON_PROJECTION_START -->"
PROJECTION_END = "<!-- ACRONYM_JSON_PROJECTION_END -->"
PROJECT_CLASSIFICATIONS = {
    "acronym",
    "historical_acronym",
    "opaque_historical_identifier",
    "conflicted_historical_identifier",
    "brand_or_scoped_token",
    "brand_token",
    "name_token",
}

# We intentionally do not treat every uppercase word as an acronym. Current-state
# docs legitimately contain uppercase status vocabulary (PASS, CURRENT,
# FAIL-CLOSED, etc.). Lint only strong acronym/identifier contexts:
# 1) parenthetical first-use forms, e.g. "Policy Enforcement Point (PEP)";
# 2) explicit "TOKEN =" or "TOKEN —" definition-like forms.
PAREN_TOKEN_RE = re.compile(r"\(([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*|SSoT)\)")
DEFINITION_TOKEN_RE = re.compile(
    r"(?m)^(?:[-*]\s+)?(?:\*\*)?([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*|SSoT)(?:\*\*)?\s*(?:=|—|:)\s+"
)

REQUIRED = {
    "DGAF",
    "PDMAL",
    "AOSS",
    "ACP",
    "MDAR",
    "AOGA",
    "AAR",
    "PDP",
    "PEP",
    "ASIS",
}


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
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry[{index}] must be an object")
            continue
        for key in ("token", "expansion", "classification", "status"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                errors.append(f"entry[{index}] missing non-empty {key}")
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


def _project_projection_entries(data: dict) -> list[dict]:
    return sorted(
        (
            entry
            for entry in data["entries"]
            if entry["classification"] in PROJECT_CLASSIFICATIONS
        ),
        key=lambda entry: entry["token"].casefold(),
    )


def render_markdown_projection(data: dict) -> str:
    lines = [
        PROJECTION_START,
        "| Token | JSON expansion / classification | Status |",
        "|---|---|---|",
    ]
    for entry in _project_projection_entries(data):
        token = entry["token"].replace("|", "\\|")
        expansion = entry["expansion"].replace("|", "\\|")
        classification = entry["classification"].replace("|", "\\|")
        status = entry["status"].replace("|", "\\|")
        lines.append(
            f"| **{token}** | {expansion} _(classification: {classification})_ | {status} |"
        )
    lines.append(PROJECTION_END)
    return "\n".join(lines)


def validate_markdown_projection(data: dict) -> list[str]:
    if not HUMAN_REGISTRY.exists():
        return ["human-readable acronym registry missing"]

    text = HUMAN_REGISTRY.read_text(encoding="utf-8")
    if text.count(PROJECTION_START) != 1 or text.count(PROJECTION_END) != 1:
        return ["human-readable registry must contain exactly one JSON projection marker pair"]

    start = text.index(PROJECTION_START)
    end = text.index(PROJECTION_END) + len(PROJECTION_END)
    actual = text[start:end]
    expected = render_markdown_projection(data)
    if actual != expected:
        return [
            "human-readable acronym registry JSON projection drifted; "
            "regenerate the marked projection from ACRONYM_REGISTRY.v1.json"
        ]
    return []


def _candidate_tokens(text: str) -> set[str]:
    tokens = set(PAREN_TOKEN_RE.findall(text))
    tokens.update(DEFINITION_TOKEN_RE.findall(text))
    return tokens


def lint_surfaces(data: dict) -> list[str]:
    errors: list[str] = []
    registered = {entry["token"] for entry in data["entries"]}
    ignored = set(data.get("literal_allowlist", []))
    patterns = [re.compile(pattern) for pattern in data.get("ignored_patterns", [])]

    for rel in data.get("scan_paths", []):
        path = ROOT / rel
        if not path.exists():
            errors.append(f"scan path missing: {rel}")
            continue

        unknown: set[str] = set()
        for token in _candidate_tokens(path.read_text(encoding="utf-8")):
            if token in registered or token in ignored:
                continue
            if any(pattern.fullmatch(token) for pattern in patterns):
                continue
            unknown.add(token)

        if unknown:
            errors.append(f"{rel}: undefined acronym/identifier candidates: {sorted(unknown)}")

    return errors


def main() -> int:
    data = load()
    errors = validate_registry(data) + lint_surfaces(data) + validate_markdown_projection(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: acronym registry v1 (schema + current-surface completeness + Markdown projection)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
