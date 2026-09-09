#!/usr/bin/env python3
"""Fail-closed validation for DGAF's internal/external vocabulary registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MATRIX_PATH = Path("docs/VOCABULARY_TRANSLATION_MATRIX.json")
PUBLIC_LAYER_PATH = Path("docs/PUBLIC_TRANSLATION_LAYER.md")

REQUIRED_IDENTITIES = {
    "Amethyst",
    "COLLEEN",
    "Apogee",
    "Sentinel-Phi",
    "DemiJoule",
    "Herald",
    "Professor Prodigy",
    "Nova",
    "Perigee",
    "Reciprocity",
    "The Librarian",
    "The Auditor",
    "The Actualizer",
    "Zenith",
}

REQUIRED_ALIAS_BINDINGS = {
    "Apogee Lens": "Apogee",
    "Sentinel": "Sentinel-Phi",
    "Prodigy": "Professor Prodigy",
}

REQUIRED_EXTERNAL_LABELS = {
    "Amethyst": "Governance Orchestrator",
    "Apogee": "Evidence & Verification Reviewer",
    "DemiJoule": "Runtime Safety & Constraint Adviser",
    "Sentinel-Phi": "Security & Policy Boundary Enforcer",
    "Herald": "Publication & External Communication Gatekeeper",
    "COLLEEN": "Continuity & Provenance Coordinator",
}


def load_matrix(path: Path = MATRIX_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_matrix(matrix: dict, public_text: str | None = None) -> list[str]:
    errors: list[str] = []
    if matrix.get("record_type") != "DGAF_VOCABULARY_TRANSLATION_MATRIX":
        errors.append("record_type mismatch")
    if matrix.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    authority = matrix.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    else:
        if authority.get("translation_not_renaming") is not True:
            errors.append("translation_not_renaming must be true")
        if authority.get("scientific_state_effect") != "NONE":
            errors.append("scientific_state_effect must be NONE")
        if authority.get("authority_effect") != "NONE":
            errors.append("authority_effect must be NONE")

    entries = matrix.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["entries must be a non-empty list"]

    identities: dict[str, dict] = {}
    alias_to_identity: dict[str, str] = {}
    external_labels: set[str] = set()

    required_fields = {
        "canonical_internal_identity",
        "aliases",
        "external_label",
        "internal_function",
        "abstract_role_classes",
        "authority_class",
        "authority_ceiling",
        "first_use_external",
    }

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry[{index}] must be an object")
            continue
        missing = required_fields - set(entry)
        if missing:
            errors.append(f"entry[{index}] missing fields: {sorted(missing)}")
            continue

        identity = entry["canonical_internal_identity"]
        if not isinstance(identity, str) or not identity.strip():
            errors.append(f"entry[{index}] has invalid canonical_internal_identity")
            continue
        if identity in identities:
            errors.append(f"duplicate canonical identity: {identity}")
        identities[identity] = entry

        aliases = entry["aliases"]
        if not isinstance(aliases, list) or any(not isinstance(a, str) or not a.strip() for a in aliases):
            errors.append(f"{identity}: aliases must be non-empty strings")
            aliases = []
        for alias in aliases:
            if alias in identities or alias in alias_to_identity:
                errors.append(f"duplicate/ambiguous alias: {alias}")
            alias_to_identity[alias] = identity

        label = entry["external_label"]
        if not isinstance(label, str) or not label.strip():
            errors.append(f"{identity}: external_label must be non-empty")
        elif label in external_labels:
            errors.append(f"duplicate external_label: {label}")
        external_labels.add(label)

        if not isinstance(entry["abstract_role_classes"], list) or not entry["abstract_role_classes"]:
            errors.append(f"{identity}: abstract_role_classes must be non-empty")
        if not isinstance(entry["authority_ceiling"], str) or not entry["authority_ceiling"].strip():
            errors.append(f"{identity}: authority_ceiling must be non-empty")
        expected_first_use = f"{label} ({identity})"
        if entry["first_use_external"] != expected_first_use:
            errors.append(f"{identity}: first_use_external must equal {expected_first_use!r}")

    missing_identities = REQUIRED_IDENTITIES - set(identities)
    if missing_identities:
        errors.append(f"missing required identities: {sorted(missing_identities)}")

    for alias, canonical in REQUIRED_ALIAS_BINDINGS.items():
        if alias_to_identity.get(alias) != canonical:
            errors.append(f"alias {alias!r} must resolve to {canonical!r}")

    for identity, label in REQUIRED_EXTERNAL_LABELS.items():
        if identities.get(identity, {}).get("external_label") != label:
            errors.append(f"{identity}: expected external label {label!r}")

    demi_roles = set(identities.get("DemiJoule", {}).get("abstract_role_classes", []))
    if "SENTINEL_ARCHETYPE" not in demi_roles:
        errors.append("DemiJoule must distinguish SENTINEL_ARCHETYPE from Sentinel-Phi identity")
    if alias_to_identity.get("Sentinel") != "Sentinel-Phi":
        errors.append("Sentinel alias must resolve only to Sentinel-Phi")

    if public_text is not None:
        for identity, entry in identities.items():
            label = entry["external_label"]
            first_use = entry["first_use_external"]
            if identity in REQUIRED_IDENTITIES and label not in public_text:
                errors.append(f"public translation layer missing external label for {identity}: {label}")
            if identity in REQUIRED_EXTERNAL_LABELS and first_use not in public_text:
                errors.append(f"public translation layer missing first-use form: {first_use}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=MATRIX_PATH)
    parser.add_argument("--public-layer", type=Path, default=PUBLIC_LAYER_PATH)
    args = parser.parse_args()

    matrix = load_matrix(args.matrix)
    public_text = args.public_layer.read_text(encoding="utf-8")
    errors = validate_matrix(matrix, public_text)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: vocabulary translation matrix ({len(matrix['entries'])} canonical identities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
