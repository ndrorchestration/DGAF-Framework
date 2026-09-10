#!/usr/bin/env python3
"""Propagation consistency and canonical derivative-claim checker.

The legacy registry remains an advisory provenance/QA control for known wording
recurrences. Entries classified as ``canonical_claim_derivative`` are stricter:
they bind recognition patterns to claim identity/state in ``evidence/claims.json``
and fail closed when a derivative silently strengthens, de-qualifies, or stale-
binds that canonical state.

This checker validates translation consistency only. It does not establish the
truth, efficacy, authorization, or independent verification of any claim.
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
CANONICAL_DERIVATIVE = "canonical_claim_derivative"
CANONICAL_SOURCE = Path("evidence/claims.json")
FAIL_STATUSES = {
    "ERROR_BARE_CURRENT",
    "ERROR_UNKNOWN_CANONICAL_CLAIM",
    "ERROR_STALE_BINDING",
    "ERROR_ATTRIBUTION_TRANSFER",
}
STATUS_QUALIFIERS = {
    "HYPOTHESIS": ["HYPOTHESIS", "NOT ESTABLISHED", "UNVERIFIED"],
    "BLOCKED": ["BLOCKED", "NOT ESTABLISHED", "NOT VERIFIED"],
    "VERIFIED": ["VERIFIED"],
    "ATTESTED": ["ATTESTED"],
}
RUN_TOKEN = re.compile(
    r"\b(?:dpl_[A-Za-z0-9]+|run[_ -]?id\s*[:=]?\s*[A-Za-z0-9._-]+)\b",
    re.IGNORECASE,
)


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError("registry must contain an 'entries' list")
    return data


def load_claims(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("canonical claims file must contain a 'claims' list")
    claims: dict[str, dict[str, Any]] = {}
    for claim in data["claims"]:
        if not isinstance(claim, dict) or not isinstance(claim.get("claim_id"), str) or not claim["claim_id"]:
            raise ValueError("canonical claim entry missing claim_id")
        claim_id = claim["claim_id"]
        if claim_id in claims:
            raise ValueError(f"duplicate canonical claim_id: {claim_id}")
        claims[claim_id] = claim
    return claims


def files_under(root: Path, excluded_paths: set[Path]) -> list[Path]:
    excluded = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    files = []
    excluded_resolved = {p.resolve() for p in excluded_paths}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {
            ".md",
            ".txt",
            ".json",
            ".py",
            ".yaml",
            ".yml",
        }:
            continue
        if any(part in excluded for part in p.parts):
            continue
        if p.resolve() in excluded_resolved:
            continue
        files.append(p)
    return files


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def local_scopes(text: str, start: int, end: int, radius: int) -> list[str]:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    window = text[left:right]
    occurrence_center = start - left

    sentences = list(re.finditer(r"[^.!?\n]*(?:[.!?](?:\s+|$)|\n|$)", window))
    containing = None
    for match in sentences:
        if match.start() <= occurrence_center <= match.end():
            containing = match.group(0)
            break
    scopes = [containing] if containing else []
    para_left = window.rfind("\n\n", 0, occurrence_center)
    para_right = window.find("\n\n", occurrence_center)
    scopes.append(window[(para_left + 2 if para_left >= 0 else 0) : (para_right if para_right >= 0 else len(window))])
    return [scope for scope in scopes if scope is not None]


def nearby_qualifier(
    text: str,
    start: int,
    end: int,
    qualifiers: list[str],
    radius: int,
) -> str | None:
    for scope in local_scopes(text, start, end, radius):
        for qualifier in qualifiers:
            if re.search(re.escape(qualifier), scope, flags=re.IGNORECASE):
                return qualifier
    return None


def explicitly_historical(
    text: str,
    start: int,
    end: int,
    markers: list[str],
    radius: int,
) -> bool:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    window = text[left:right]
    return any(re.search(re.escape(marker), window, flags=re.IGNORECASE) for marker in markers)


def stale_run_binding(
    text: str,
    start: int,
    end: int,
    radius: int,
    canonical_run_id: str | None,
) -> str | None:
    for scope in local_scopes(text, start, end, radius):
        for token in RUN_TOKEN.findall(scope):
            if canonical_run_id is None or canonical_run_id.lower() not in token.lower():
                return token
    return None


def attribution_transfer(
    text: str,
    start: int,
    end: int,
    radius: int,
    claim: dict[str, Any],
) -> bool:
    provenance = claim.get("provenance")
    if not isinstance(provenance, dict):
        return False
    source_owner = provenance.get("source_owner")
    if not isinstance(source_owner, str) or not source_owner or source_owner.upper() in {"DGAF", "PDMAL", "NDR"}:
        return False
    attribution_pattern = re.compile(
        r"\b(?:DGAF|PDMAL|NDR)\s+" r"(?:established|proved|verified|demonstrated|found|showed)\b",
        re.IGNORECASE,
    )
    for scope in local_scopes(text, start, end, radius):
        if attribution_pattern.search(scope) and source_owner.lower() not in scope.lower():
            return True
    return False


def scan_entry(
    entry: dict[str, Any],
    path: Path,
    text: str,
    canonical_claims: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    pattern = entry.get("claim_pattern")
    if not pattern:
        return []
    classification = entry.get("classification", CURRENT)
    historical_allowed = bool(entry.get("historical_allowed", False))
    qualifiers = entry.get("qualifiers_any", [])
    historical_markers = entry.get(
        "historical_markers",
        ["historical", "archived", "at the time", "as of S0"],
    )
    radius = int(entry.get("context_radius", 220))
    results = []

    try:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
    except re.error as exc:
        raise ValueError(f"invalid regex for {entry.get('id')}: {exc}") from exc

    canonical_claim: dict[str, Any] | None = None
    if classification == CANONICAL_DERIVATIVE:
        claim_id = entry.get("canonical_claim_id")
        invalid_claim_id = not isinstance(claim_id, str) or not claim_id
        unavailable_claim = canonical_claims is None or claim_id not in canonical_claims
        if invalid_claim_id or unavailable_claim:
            for match in matches or [None]:
                results.append(
                    {
                        "id": entry.get("id"),
                        "path": str(path),
                        "line": line_number(text, match.start()) if match else 1,
                        "classification": classification,
                        "status": "ERROR_UNKNOWN_CANONICAL_CLAIM",
                        "match": match.group(0) if match else "",
                    }
                )
            return results
        canonical_claim = canonical_claims[claim_id]

    for match in matches:
        line = line_number(text, match.start())
        if classification == HISTORICAL and historical_allowed:
            status = "ALLOWED_HISTORICAL"
        elif classification == MIGRATION:
            status = "REVIEW_MIGRATION"
        elif classification == CANONICAL_DERIVATIVE and canonical_claim is not None:
            is_historical = historical_allowed and explicitly_historical(
                text,
                match.start(),
                match.end(),
                historical_markers,
                radius,
            )
            if is_historical:
                status = "ALLOWED_HISTORICAL"
            elif attribution_transfer(
                text,
                match.start(),
                match.end(),
                radius,
                canonical_claim,
            ):
                status = "ERROR_ATTRIBUTION_TRANSFER"
            else:
                canonical_status = str(canonical_claim.get("status", "")).upper()
                required_qualifiers = STATUS_QUALIFIERS.get(
                    canonical_status,
                    [canonical_status] if canonical_status else [],
                )
                qualifier = nearby_qualifier(
                    text,
                    match.start(),
                    match.end(),
                    required_qualifiers,
                    radius,
                )
                run_id = canonical_claim.get("run_id")
                canonical_run_id = run_id if isinstance(run_id, str) else None
                stale_binding = stale_run_binding(
                    text,
                    match.start(),
                    match.end(),
                    radius,
                    canonical_run_id,
                )
                if stale_binding:
                    status = "ERROR_STALE_BINDING"
                elif canonical_status not in {"VERIFIED", "ATTESTED"} and not qualifier:
                    status = "ERROR_BARE_CURRENT"
                else:
                    status = "PASS_CANONICAL_PARITY"
        else:
            qualifier = nearby_qualifier(
                text,
                match.start(),
                match.end(),
                qualifiers,
                radius,
            )
            if qualifier:
                status = "PASS_QUALIFIED"
            elif historical_allowed and explicitly_historical(
                text,
                match.start(),
                match.end(),
                historical_markers,
                radius,
            ):
                status = "ALLOWED_HISTORICAL"
            else:
                status = "ERROR_BARE_CURRENT"
        results.append(
            {
                "id": entry.get("id"),
                "path": str(path),
                "line": line,
                "classification": classification,
                "status": status,
                "canonical_claim_id": entry.get("canonical_claim_id"),
                "match": match.group(0),
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--claims", type=Path, default=CANONICAL_SOURCE)
    parser.add_argument(
        "--canonical-only",
        action="store_true",
        help="scan only canonically bound derivative entries",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on fail-closed claim translation defects",
    )
    args = parser.parse_args()

    registry = load_registry(args.registry)
    root = args.root.resolve()
    registry_path = args.registry.resolve()
    claims_path = args.claims if args.claims.is_absolute() else root / args.claims
    canonical_claims = load_claims(claims_path)
    entries = [
        entry
        for entry in registry["entries"]
        if not args.canonical_only or entry.get("classification") == CANONICAL_DERIVATIVE
    ]

    findings: list[dict[str, Any]] = []
    for path in files_under(root, {registry_path, claims_path}):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        relative = path.relative_to(root)
        for entry in entries:
            findings.extend(scan_entry(entry, relative, text, canonical_claims))

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding["status"]] = counts.get(finding["status"], 0) + 1

    if args.canonical_only and args.strict:
        mode = "canonical-strict"
    elif args.strict:
        mode = "strict"
    else:
        mode = "advisory"
    report = {
        "mode": mode,
        "canonical_source": str(claims_path.relative_to(root)),
        "counts": counts,
        "findings": findings,
        "evidence_boundary": (
            "translation consistency only; no truth, efficacy, authorization, " "or independent-verification promotion"
        ),
    }
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Propagation consistency: {len(findings)} classified recurrences")
        for status, count in sorted(counts.items()):
            print(f"  {status}: {count}")
        for finding in findings:
            if finding["status"] in FAIL_STATUSES | {"REVIEW_MIGRATION"}:
                print(f"{finding['status']}: {finding['path']}:" f"{finding['line']} [{finding['id']}]")

    failures = sum(counts.get(status, 0) for status in FAIL_STATUSES)
    return 1 if args.strict and failures else 0


if __name__ == "__main__":
    sys.exit(main())
