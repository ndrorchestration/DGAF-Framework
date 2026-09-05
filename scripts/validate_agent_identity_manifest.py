#!/usr/bin/env python3
"""Fail-closed validator for registry/agent_identity_manifest.v1.json.

This checker validates structure and conflict preservation only. It does not
resolve contested agent authority or promote conceptual identities to canonical
status.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST = Path("registry/agent_identity_manifest.v1.json")
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "status",
    "authority_policy",
    "source_snapshot",
    "allowed_seat_status",
    "allowed_activation_status",
    "identities",
    "scientific_boundary",
}
REQUIRED_IDENTITY = {
    "identity_id",
    "display_name",
    "seat_status",
    "activation_status",
    "variant_of",
    "directory",
    "rubric_ids",
    "observed_designations",
    "conflicts",
}
EXPECTED_BOUNDARY = "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0"


def _fail(message: str) -> None:
    raise ValueError(message)


def validate_manifest(data: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL - data.keys()
    if missing:
        _fail(f"missing top-level fields: {sorted(missing)}")

    if data["status"] != "conflict-register-not-authority-resolution":
        _fail("manifest status must preserve unresolved authority")
    if data["scientific_boundary"] != EXPECTED_BOUNDARY:
        _fail("scientific boundary changed")

    allowed_seat = set(data["allowed_seat_status"])
    allowed_activation = set(data["allowed_activation_status"])
    identities = data["identities"]
    if not isinstance(identities, list) or not identities:
        _fail("identities must be a non-empty list")

    identity_ids: set[str] = set()
    source_designations: set[tuple[str, str]] = set()
    by_id: dict[str, dict[str, Any]] = {}

    for entry in identities:
        if not isinstance(entry, dict):
            _fail("each identity must be an object")
        missing_fields = REQUIRED_IDENTITY - entry.keys()
        if missing_fields:
            _fail(f"{entry.get('identity_id', '<unknown>')}: missing {sorted(missing_fields)}")

        identity_id = entry["identity_id"]
        if not isinstance(identity_id, str) or not identity_id:
            _fail("identity_id must be a non-empty string")
        if identity_id in identity_ids:
            _fail(f"duplicate stable identity_id: {identity_id}")
        identity_ids.add(identity_id)
        by_id[identity_id] = entry

        if entry["seat_status"] not in allowed_seat:
            _fail(f"{identity_id}: invalid seat_status {entry['seat_status']!r}")
        if entry["activation_status"] not in allowed_activation:
            _fail(f"{identity_id}: invalid activation_status {entry['activation_status']!r}")

        observations = entry["observed_designations"]
        if not isinstance(observations, list) or not observations:
            _fail(f"{identity_id}: observed_designations must be non-empty")
        distinct_ids: set[str] = set()
        for observation in observations:
            source = observation.get("source")
            designation = observation.get("id")
            if not isinstance(source, str) or not source:
                _fail(f"{identity_id}: observation missing source")
            if not isinstance(designation, str) or not designation:
                _fail(f"{identity_id}: observation missing id")
            key = (source, designation)
            if key in source_designations:
                _fail(f"source designation maps to multiple identities: {key}")
            source_designations.add(key)
            distinct_ids.add(designation)

        conflicts = entry["conflicts"]
        if not isinstance(conflicts, list):
            _fail(f"{identity_id}: conflicts must be a list")
        if entry["seat_status"] == "conflicted" and not conflicts:
            _fail(f"{identity_id}: conflicted identity must explain conflict")
        if len(distinct_ids) > 1 and not conflicts:
            _fail(f"{identity_id}: cross-source designation drift must be explicit")

    for identity_id, entry in by_id.items():
        variant_of = entry["variant_of"]
        if variant_of is not None:
            if not isinstance(variant_of, str) or variant_of not in by_id:
                _fail(f"{identity_id}: variant_of must reference an existing stable identity")
            if entry["seat_status"] != "variant":
                _fail(f"{identity_id}: variant_of requires seat_status=variant")

    # Sentinel-Phi must remain a variant lineage and Ionia must remain unresolved,
    # preventing silent collapse or promotion by future edits.
    sentinel_phi = by_id.get("agent.sentinel-phi")
    if not sentinel_phi or sentinel_phi["variant_of"] != "agent.sentinel":
        _fail("Sentinel-Phi variant lineage missing or changed")
    ionia = by_id.get("agent.ionia")
    if not ionia or ionia["seat_status"] != "conflicted":
        _fail("Ionia agent/state conflict must remain explicit until ratified")

    for n in range(20, 28):
        designation = f"A-{n}"
        matches = [
            entry
            for entry in identities
            if any(obs["id"] == designation for obs in entry["observed_designations"])
        ]
        if len(matches) != 1:
            _fail(f"{designation}: expected exactly one observed identity record")
        if matches[0]["seat_status"] == "canonical":
            _fail(f"{designation}: cannot be silently promoted to canonical")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    validate_manifest(data)
    print(f"PASS: {args.manifest} preserves {len(data['identities'])} identity records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
