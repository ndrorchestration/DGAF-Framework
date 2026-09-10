#!/usr/bin/env python3
"""Propagation and canonical claim-surface consistency checker.

The canonical claim identity/status authority is ``evidence/claims.json``.
Evidence Cards are richer detail projections and may not silently promote or
rewrite canonical claim state. Registered derivative recurrence checking remains
advisory unless ``--strict`` is supplied.

This checker establishes repository consistency only. It does not establish
scientific truth, empirical efficacy, freeze, or authorization.
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

STATUS_TO_CARD_CLASS = {
    "VERIFIED": {"VERIFIED"},
    "ATTESTED": {"ATTESTED"},
    "HYPOTHESIS": {"HYPOTHESIS"},
    "BLOCKED": {"HYPOTHESIS", "UNSUPPORTED"},
}
NONVERIFIED_STATUSES = {"HYPOTHESIS", "BLOCKED"}
CARD_REQUIRED = {
    "id",
    "canonical_claim_id",
    "claim",
    "claim_class",
    "context",
    "measurement",
    "provenance",
    "evidence_maturity",
    "validation_status",
}


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError("registry must contain an 'entries' list")
    return data


def load_claim_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("claim registry must contain a top-level 'claims' list")
    return data


def _parse_index_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    lowered = value.lower()
    if lowered == "null":
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def load_card_index(path: Path) -> dict[str, Any]:
    """Parse the intentionally flat CLAIM_CARD_INDEX YAML without dependencies.

    Supported shape is top-level scalar keys plus flat list entries under
    ``cards`` and ``supplemental_cards``. Nested structures fail closed.
    """
    result: dict[str, Any] = {"cards": [], "supplemental_cards": []}
    section: str | None = None
    item: dict[str, Any] | None = None

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 0:
            item = None
            if stripped.endswith(":") and stripped[:-1] in {"cards", "supplemental_cards"}:
                section = stripped[:-1]
                continue
            section = None
            if ":" not in stripped:
                raise ValueError(f"{path}:{lineno}: unsupported top-level YAML syntax")
            key, value = stripped.split(":", 1)
            result[key.strip()] = _parse_index_scalar(value)
            continue

        if section not in {"cards", "supplemental_cards"}:
            raise ValueError(f"{path}:{lineno}: nested content outside registered list section")

        if indent == 2 and stripped.startswith("- "):
            if ":" not in stripped[2:]:
                raise ValueError(f"{path}:{lineno}: list item must start with key: value")
            key, value = stripped[2:].split(":", 1)
            item = {key.strip(): _parse_index_scalar(value)}
            result[section].append(item)
            continue

        if indent == 4 and item is not None:
            if ":" not in stripped:
                raise ValueError(f"{path}:{lineno}: list property must be key: value")
            key, value = stripped.split(":", 1)
            item[key.strip()] = _parse_index_scalar(value)
            continue

        raise ValueError(f"{path}:{lineno}: unsupported YAML nesting; index must remain flat")

    return result


def _relative_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _check_card_shape(card: dict[str, Any], card_path: str, errors: list[str]) -> None:
    missing = sorted(CARD_REQUIRED - set(card))
    if missing:
        errors.append(f"{card_path}: canonical Evidence Card missing required fields: {', '.join(missing)}")
        return
    if not isinstance(card.get("context"), dict) or not card["context"].get("intended_use"):
        errors.append(f"{card_path}: context.intended_use is required")
    if not isinstance(card.get("measurement"), dict):
        errors.append(f"{card_path}: measurement must be an object")
    else:
        if not card["measurement"].get("metric") or not card["measurement"].get("method"):
            errors.append(f"{card_path}: measurement.metric and measurement.method are required")
    if not isinstance(card.get("provenance"), dict):
        errors.append(f"{card_path}: provenance must be an object")
    else:
        if not card["provenance"].get("source") or not card["provenance"].get("recorded_at"):
            errors.append(f"{card_path}: provenance.source and provenance.recorded_at are required")


def reconcile_claim_surfaces(
    root: Path, claims_path: Path, card_index_path: Path
) -> tuple[list[str], set[str], dict[str, int]]:
    """Return fail-closed mapping errors, canonical card paths, and statistics."""
    root = root.resolve()
    claims_path = claims_path.resolve()
    card_index_path = card_index_path.resolve()
    errors: list[str] = []
    canonical_card_paths: set[str] = set()

    claims_doc = load_claim_registry(claims_path)
    index = load_card_index(card_index_path)
    claims_rel = _relative_to_root(claims_path, root)

    if index.get("version") != 2:
        errors.append("CLAIM_CARD_INDEX version must be 2")
    if index.get("canonical_claim_source") != claims_rel:
        errors.append(f"CLAIM_CARD_INDEX canonical_claim_source must be {claims_rel!r}")
    if index.get("state_authority") != claims_rel:
        errors.append(f"CLAIM_CARD_INDEX state_authority must be {claims_rel!r}")

    claims_by_id: dict[str, dict[str, Any]] = {}
    for claim in claims_doc["claims"]:
        if not isinstance(claim, dict):
            errors.append("canonical claim entry must be an object")
            continue
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id:
            errors.append("canonical claim missing claim_id")
            continue
        if claim_id in claims_by_id:
            errors.append(f"duplicate canonical claim_id: {claim_id}")
            continue
        claims_by_id[claim_id] = claim
        if claim.get("status") not in STATUS_TO_CARD_CLASS:
            errors.append(f"{claim_id}: unsupported canonical status {claim.get('status')!r}")
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"{claim_id}: canonical statement must be non-empty")
        if claim.get("status") in NONVERIFIED_STATUSES and claim.get("run_id") is not None:
            errors.append(f"{claim_id}: {claim.get('status')} claim may not carry a current run_id")

    seen_card_ids: set[str] = set()
    mapped_claim_ids: set[str] = set()
    seen_targets: set[str] = set()

    for entry in index.get("cards", []):
        if not isinstance(entry, dict):
            errors.append("canonical card index entry must be an object")
            continue
        card_id = entry.get("id")
        claim_id = entry.get("canonical_claim_id")
        card_ref = entry.get("card")
        if not isinstance(card_id, str) or not card_id:
            errors.append("canonical card index entry missing id")
            continue
        if card_id in seen_card_ids:
            errors.append(f"duplicate Evidence Card id in index: {card_id}")
        seen_card_ids.add(card_id)

        if not isinstance(claim_id, str) or not claim_id:
            errors.append(f"{card_id}: canonical_claim_id is required")
            continue
        if claim_id in mapped_claim_ids:
            errors.append(f"{claim_id}: canonical claim mapped more than once")
        mapped_claim_ids.add(claim_id)
        claim = claims_by_id.get(claim_id)
        if claim is None:
            errors.append(f"{card_id}: unknown canonical_claim_id {claim_id!r}")
            continue

        if card_ref == "pending" or not isinstance(card_ref, str) or not card_ref:
            errors.append(f"{claim_id}: canonical Evidence Card may not be pending")
            continue
        if card_ref in seen_targets:
            errors.append(f"{claim_id}: Evidence Card target reused: {card_ref}")
        seen_targets.add(card_ref)
        canonical_card_paths.add(card_ref)

        card_path = root / card_ref
        if card_path.suffix.lower() != ".json":
            errors.append(f"{claim_id}: canonical Evidence Card must be dependency-free JSON: {card_ref}")
            continue
        if not card_path.is_file():
            errors.append(f"{claim_id}: missing canonical Evidence Card: {card_ref}")
            continue
        try:
            card = json.loads(card_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{claim_id}: invalid canonical Evidence Card {card_ref}: {exc}")
            continue
        if not isinstance(card, dict):
            errors.append(f"{card_ref}: canonical Evidence Card must be an object")
            continue
        _check_card_shape(card, card_ref, errors)

        if card.get("id") != card_id:
            errors.append(f"{claim_id}: index/card id mismatch: {card_id!r} != {card.get('id')!r}")
        if card.get("canonical_claim_id") != claim_id:
            errors.append(f"{claim_id}: card canonical_claim_id mismatch")
        if card.get("claim") != claim.get("statement"):
            errors.append(f"{claim_id}: Evidence Card proposition differs from canonical statement")

        allowed_classes = STATUS_TO_CARD_CLASS.get(claim.get("status"), set())
        if card.get("claim_class") not in allowed_classes:
            errors.append(
                f"{claim_id}: card claim_class {card.get('claim_class')!r} "
                f"is incompatible with canonical status {claim.get('status')!r}"
            )

        if claim.get("status") in NONVERIFIED_STATUSES:
            if card.get("validation_status") != "NOT_VALIDATED":
                errors.append(f"{claim_id}: non-verified claim card must be NOT_VALIDATED")
            if card.get("evidence_maturity") != "SPECIFIED":
                errors.append(f"{claim_id}: non-verified claim card must remain SPECIFIED")
            if card.get("last_verified") is not None:
                errors.append(f"{claim_id}: non-verified claim card may not carry last_verified")
        else:
            if card.get("validation_status") not in {
                "VALIDATED_FOR_CONTEXT",
                "INDEPENDENTLY_REPLICATED",
            }:
                errors.append(f"{claim_id}: verified/attested card requires contextual validation status")

        provenance = card.get("provenance")
        expected_source = f"{claims_rel}#{claim_id}"
        if not isinstance(provenance, dict) or provenance.get("source") != expected_source:
            errors.append(f"{claim_id}: provenance.source must be {expected_source!r}")
        context = card.get("context")
        if not isinstance(context, dict) or not context.get("scope"):
            errors.append(f"{claim_id}: canonical Evidence Card requires explicit context.scope")

    missing_mappings = sorted(set(claims_by_id) - mapped_claim_ids)
    for claim_id in missing_mappings:
        errors.append(f"{claim_id}: canonical claim has no Evidence Card mapping")
    extra_mappings = sorted(mapped_claim_ids - set(claims_by_id))
    for claim_id in extra_mappings:
        errors.append(f"{claim_id}: Evidence Card maps unknown canonical claim")

    for entry in index.get("supplemental_cards", []):
        if not isinstance(entry, dict):
            errors.append("supplemental card index entry must be an object")
            continue
        card_id = entry.get("id")
        if not isinstance(card_id, str) or not card_id:
            errors.append("supplemental card entry missing id")
            continue
        if card_id in seen_card_ids:
            errors.append(f"duplicate Evidence Card id across canonical/supplemental sets: {card_id}")
        seen_card_ids.add(card_id)
        if entry.get("relationship") != "supplemental_noncanonical":
            errors.append(f"{card_id}: supplemental card must declare relationship=supplemental_noncanonical")
        if entry.get("canonical_claim_id") not in {None, ""}:
            errors.append(f"{card_id}: supplemental card may not claim canonical_claim_id")
        card_ref = entry.get("card")
        if card_ref not in {None, "", "pending"}:
            if not isinstance(card_ref, str) or not (root / card_ref).is_file():
                errors.append(f"{card_id}: supplemental card target missing: {card_ref}")

    stats = {
        "canonical_claims": len(claims_by_id),
        "canonical_cards": len(index.get("cards", [])),
        "supplemental_cards": len(index.get("supplemental_cards", [])),
    }
    return errors, canonical_card_paths, stats


def validate_registry_claim_bindings(
    registry: dict[str, Any], claims: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    claim_ids = {
        c.get("claim_id")
        for c in claims.get("claims", [])
        if isinstance(c, dict) and isinstance(c.get("claim_id"), str)
    }
    for entry in registry.get("entries", []):
        if not isinstance(entry, dict):
            errors.append("propagation registry entry must be an object")
            continue
        classification = entry.get("classification", CURRENT)
        bound = entry.get("canonical_claim_id")
        if classification == CURRENT:
            if not isinstance(bound, str) or not bound:
                errors.append(f"{entry.get('id')}: current_claim entry must bind canonical_claim_id")
            elif bound not in claim_ids:
                errors.append(f"{entry.get('id')}: unknown canonical_claim_id {bound!r}")
        elif bound is not None and bound not in claim_ids:
            errors.append(f"{entry.get('id')}: unknown optional canonical_claim_id {bound!r}")
    return errors


def files_under(root: Path, excluded_paths: set[str]) -> list[Path]:
    excluded_parts = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    files = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt", ".json", ".py", ".yaml", ".yml"}:
            continue
        if any(part in excluded_parts for part in p.parts):
            continue
        rel = p.relative_to(root).as_posix()
        if rel in excluded_paths:
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
            "canonical_claim_id": entry.get("canonical_claim_id"),
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
    parser.add_argument("--claims", type=Path)
    parser.add_argument("--card-index", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true", help="exit 1 on current bare derivative claims")
    args = parser.parse_args()

    root = args.root.resolve()
    registry_path = args.registry.resolve()
    registry = load_registry(registry_path)

    claim_surface_errors: list[str] = []
    canonical_card_paths: set[str] = set()
    claim_surface_stats = {"canonical_claims": 0, "canonical_cards": 0, "supplemental_cards": 0}
    claims_doc: dict[str, Any] | None = None

    if bool(args.claims) != bool(args.card_index):
        claim_surface_errors.append("--claims and --card-index must be supplied together")
    elif args.claims and args.card_index:
        try:
            claims_doc = load_claim_registry(args.claims)
            claim_surface_errors, canonical_card_paths, claim_surface_stats = reconcile_claim_surfaces(
                root, args.claims, args.card_index
            )
            claim_surface_errors.extend(validate_registry_claim_bindings(registry, claims_doc))
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            claim_surface_errors.append(str(exc))

    excluded_paths = {_relative_to_root(registry_path, root)}
    if args.claims:
        excluded_paths.add(_relative_to_root(args.claims, root))
    if args.card_index:
        excluded_paths.add(_relative_to_root(args.card_index, root))
    excluded_paths.update(canonical_card_paths)

    findings: list[dict[str, Any]] = []
    for path in files_under(root, excluded_paths):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for entry in registry["entries"]:
            findings.extend(scan_entry(entry, path.relative_to(root), text))

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding["status"]] = counts.get(finding["status"], 0) + 1

    report = {
        "mode": "strict" if args.strict else "advisory",
        "claim_surface": {
            "status": "FAIL_CLOSED" if claim_surface_errors else "PASS_STRUCTURAL_MAPPING_ONLY",
            "authority": _relative_to_root(args.claims, root) if args.claims else None,
            "stats": claim_surface_stats,
            "errors": claim_surface_errors,
            "scientific_effect": "NONE",
            "authorization_effect": "NONE",
        },
        "counts": counts,
        "findings": findings,
    }

    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Canonical claim surface: {report['claim_surface']['status']}")
        for error in claim_surface_errors:
            print(f"CLAIM_SURFACE_ERROR: {error}")
        print(f"Propagation consistency: {len(findings)} classified recurrences")
        for status, count in sorted(counts.items()):
            print(f"  {status}: {count}")
        for finding in findings:
            if finding["status"] in {"ERROR_BARE_CURRENT", "REVIEW_MIGRATION"}:
                print(
                    f"{finding['status']}: {finding['path']}:{finding['line']} "
                    f"[{finding['id']}; canonical={finding.get('canonical_claim_id')}]"
                )

    if claim_surface_errors:
        return 1
    return 1 if args.strict and counts.get("ERROR_BARE_CURRENT", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
