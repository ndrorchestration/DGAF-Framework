#!/usr/bin/env python3
"""Propagation consistency checker.

Advisory provenance/QA control: detects recurrences of known corrected claims
that are still presented as current, unqualified claims. Historical references
and terminology-migration records are explicitly classified rather than treated
as defects.

This checker is intentionally NOT an epistemic verification gate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CURRENT = "current_claim"
MIGRATION = "terminology_migration"
HISTORICAL = "historical_reference"


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError("registry must contain an 'entries' list")
    return data


def files_under(root: Path, registry_path: Path) -> list[Path]:
    excluded = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    files = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt", ".json", ".py", ".yaml", ".yml"}:
            continue
        if any(part in excluded for part in p.parts):
            continue
        if p.resolve() == registry_path.resolve():
            continue
        files.append(p)
    return files


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def nearby_qualifier(text: str, start: int, end: int, qualifiers: list[str], radius: int) -> str | None:
    # Prefer the same sentence/paragraph. A qualifier elsewhere in a broad
    # character window must not silently qualify an unrelated occurrence.
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    window = text[left:right]
    occurrence_center = start - left

    sentences = list(re.finditer(r"[^.!?\n]*(?:[.!?](?:\s+|$)|\n|$)", window))
    containing = None
    for m in sentences:
        if m.start() <= occurrence_center <= m.end():
            containing = m.group(0)
            break
    scopes = [containing] if containing else []
    # Paragraph is the fallback, still much narrower than the old ±220 chars.
    para_left = window.rfind("\n\n", 0, occurrence_center)
    para_right = window.find("\n\n", occurrence_center)
    scopes.append(window[(para_left + 2 if para_left >= 0 else 0):(para_right if para_right >= 0 else len(window))])

    for scope in scopes:
        if scope is None:
            continue
        for q in qualifiers:
            if re.search(re.escape(q), scope, flags=re.IGNORECASE):
                return q
    return None


def explicitly_historical(text: str, start: int, end: int, markers: list[str], radius: int) -> bool:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    window = text[left:right]
    return any(re.search(re.escape(m), window, flags=re.IGNORECASE) for m in markers)


def scan_entry(entry: dict[str, Any], path: Path, text: str) -> list[dict[str, Any]]:
    pattern = entry.get("claim_pattern")
    if not pattern:
        return []
    classification = entry.get("classification", CURRENT)
    historical_allowed = bool(entry.get("historical_allowed", False))
    qualifiers = entry.get("qualifiers_any", [])
    historical_markers = entry.get("historical_markers", ["historical", "archived", "at the time", "as of S0"])
    radius = int(entry.get("context_radius", 220))
    results = []

    try:
        matches = re.finditer(pattern, text, flags=re.IGNORECASE)
    except re.error as exc:
        raise ValueError(f"invalid regex for {entry.get('id')}: {exc}") from exc

    for m in matches:
        line = line_number(text, m.start())
        if classification == HISTORICAL and historical_allowed:
            status = "ALLOWED_HISTORICAL"
        elif classification == MIGRATION:
            status = "REVIEW_MIGRATION"
        else:
            qualifier = nearby_qualifier(text, m.start(), m.end(), qualifiers, radius)
            if qualifier:
                status = "PASS_QUALIFIED"
            elif historical_allowed and explicitly_historical(text, m.start(), m.end(), historical_markers, radius):
                status = "ALLOWED_HISTORICAL"
            else:
                status = "ERROR_BARE_CURRENT"
        results.append({
            "id": entry.get("id"),
            "path": str(path),
            "line": line,
            "classification": classification,
            "status": status,
            "match": m.group(0),
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true", help="exit 1 on current bare claims only")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    root = args.root.resolve()
    registry_path = args.registry.resolve()
    findings: list[dict[str, Any]] = []
    for path in files_under(root, registry_path):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for entry in registry["entries"]:
            findings.extend(scan_entry(entry, path.relative_to(root), text))

    counts: dict[str, int] = {}
    for f in findings:
        counts[f["status"]] = counts.get(f["status"], 0) + 1

    report = {"mode": "strict" if args.strict else "advisory", "counts": counts, "findings": findings}
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Propagation consistency: {len(findings)} classified recurrences")
        for status, count in sorted(counts.items()):
            print(f"  {status}: {count}")
        for f in findings:
            if f["status"] in {"ERROR_BARE_CURRENT", "REVIEW_MIGRATION"}:
                print(f"{f['status']}: {f['path']}:{f['line']} [{f['id']}]")

    return 1 if args.strict and counts.get("ERROR_BARE_CURRENT", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
