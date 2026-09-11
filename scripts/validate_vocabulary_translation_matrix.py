#!/usr/bin/env python3
"""Fail-closed validation for DGAF's internal/external vocabulary registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MATRIX_PATH = Path("docs/VOCABULARY_TRANSLATION_MATRIX.json")
PUBLIC_LAYER_PATH = Path("docs/PUBLIC_TRANSLATION_LAYER.md")
IDENTITY_MANIFEST_PATH = Path("registry/agent_identity_manifest.v1.json")
ONTOLOGY_ADJUDICATION_PATH = Path("registry/agent_ontology_adjudication.v1.json")

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
    "Reson",
    "Lyra",
    "Echolette",
    "Ionia",
    "IONIA_STATE",
}
REQUIRED_ALIAS_BINDINGS = {
    "Apogee Lens": "Apogee",
    "Prodigy": "Professor Prodigy",
    "Ionia 0Hz": "IONIA_STATE",
}
REQUIRED_EXTERNAL_LABELS = {
    "Amethyst": "Governance Orchestrator",
    "Apogee": "Evidence & Verification Reviewer",
    "DemiJoule": "Runtime Safety & Constraint Adviser",
    "Sentinel-Phi": "Security & Policy Boundary Enforcer",
    "Herald": "Publication & External Communication Gatekeeper",
    "COLLEEN": "Continuity & Provenance Coordinator",
    "Reson": "Coherence & Drift Reviewer",
    "Lyra": "Synthesis & Narrative Adviser",
    "Echolette": "Pattern & Temporal-Coherence Reviewer",
    "Ionia": "Convergence & Modal-Lock Agent",
    "IONIA_STATE": "Convergence & Modal-Lock State",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_matrix(
    matrix: dict,
    public_text: str | None = None,
    identity_manifest: dict | None = None,
    ontology_adjudication: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    if matrix.get("record_type") != "DGAF_VOCABULARY_TRANSLATION_MATRIX":
        errors.append("record_type mismatch")
    if matrix.get("schema_version") != 2:
        errors.append("schema_version must be 2")

    authority = matrix.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    else:
        for key in (
            "scientific_state_effect",
            "authority_effect",
            "identity_resolution_effect",
        ):
            if authority.get(key) != "NONE":
                errors.append(f"{key} must be NONE")
        if authority.get("translation_not_renaming") is not True:
            errors.append("translation_not_renaming must be true")

    coverage = matrix.get("coverage_policy")
    if not isinstance(coverage, dict):
        errors.append("coverage_policy must be an object")
    else:
        if coverage.get("ontology_adjudication") != str(ONTOLOGY_ADJUDICATION_PATH):
            errors.append("coverage_policy must bind accepted ontology adjudication")
    change_control = matrix.get("change_control")
    if not isinstance(change_control, dict) or "MOVING_STATE_PROHIBITED" not in change_control:
        errors.append("change_control must prohibit moving state")

    unresolved = matrix.get("unresolved_relations")
    if not isinstance(unresolved, list) or not unresolved:
        errors.append("unresolved_relations must be a non-empty list")
    else:
        sentinel_records = [
            record
            for record in unresolved
            if isinstance(record, dict)
            and set(record.get("terms", [])) == {"Sentinel", "Sentinel-Phi"}
        ]
        if (
            not sentinel_records
            or sentinel_records[0].get("status") != "UNRESOLVED_IDENTITY_LINEAGE"
        ):
            errors.append("Sentinel/Sentinel-Phi lineage must retain bounded unresolved status")
        ionia_records = [
            record
            for record in unresolved
            if isinstance(record, dict) and "Ionia" in set(record.get("terms", []))
        ]
        if ionia_records:
            errors.append("Ionia agent-vs-state conflict is adjudicated and must not remain unresolved")

    entries = matrix.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["entries must be a non-empty list"]

    identities: dict[str, dict] = {}
    alias_to_identity: dict[str, str] = {}
    labels: set[str] = set()
    required_fields = {
        "canonical_internal_identity",
        "identity_kind",
        "resolution_status",
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

        if entry["identity_kind"] not in {"AGENT", "STATE"}:
            errors.append(f"{identity}: identity_kind must be AGENT or STATE")
        if not isinstance(entry["resolution_status"], str) or not entry[
            "resolution_status"
        ].strip():
            errors.append(f"{identity}: resolution_status must be non-empty")

        aliases = entry["aliases"]
        if not isinstance(aliases, list) or any(
            not isinstance(alias, str) or not alias.strip() for alias in aliases
        ):
            errors.append(f"{identity}: aliases must be strings")
            aliases = []
        for alias in aliases:
            if alias == identity or alias in alias_to_identity or alias in identities:
                errors.append(f"duplicate/ambiguous alias: {alias}")
            alias_to_identity[alias] = identity

        label = entry["external_label"]
        if not isinstance(label, str) or not label.strip():
            errors.append(f"{identity}: external_label must be non-empty")
        elif label in labels:
            errors.append(f"duplicate external_label: {label}")
        labels.add(label)

        roles = entry["abstract_role_classes"]
        if not isinstance(roles, list) or not roles:
            errors.append(f"{identity}: abstract_role_classes must be non-empty")
        if not isinstance(entry["authority_ceiling"], str) or not entry[
            "authority_ceiling"
        ].strip():
            errors.append(f"{identity}: authority_ceiling must be non-empty")
        expected_first_use = f"{label} ({identity})"
        if entry["first_use_external"] != expected_first_use:
            errors.append(
                f"{identity}: first_use_external must equal {expected_first_use!r}"
            )

    missing = REQUIRED_IDENTITIES - set(identities)
    if missing:
        errors.append(f"missing required identities: {sorted(missing)}")

    for alias, canonical in REQUIRED_ALIAS_BINDINGS.items():
        if alias_to_identity.get(alias) != canonical:
            errors.append(f"alias {alias!r} must resolve to {canonical!r}")
    if "Sentinel" in alias_to_identity:
        errors.append("Sentinel must not be encoded as an alias of Sentinel-Phi")

    for identity, label in REQUIRED_EXTERNAL_LABELS.items():
        if identities.get(identity, {}).get("external_label") != label:
            errors.append(f"{identity}: expected external label {label!r}")

    if identities.get("Ionia", {}).get("identity_kind") != "AGENT":
        errors.append("Ionia must remain the adjudicated sovereign AGENT identity")
    if identities.get("IONIA_STATE", {}).get("identity_kind") != "STATE":
        errors.append("IONIA_STATE must remain a distinct STATE")
    if "SENTINEL_ARCHETYPE" not in set(
        identities.get("DemiJoule", {}).get("abstract_role_classes", [])
    ):
        errors.append("DemiJoule must retain SENTINEL_ARCHETYPE as a role class")

    if ontology_adjudication is not None:
        if ontology_adjudication.get("status") != "accepted-ontology-adjudication":
            errors.append("ontology adjudication status is not accepted")
        seats = ontology_adjudication.get("canonical_seats", {})
        if seats.get("agent.ionia") != "A-13":
            errors.append("accepted ontology must retain Agent Ionia at A-13")
        distinct = ontology_adjudication.get("distinct_objects", {})
        ionia = distinct.get("ionia", {}) if isinstance(distinct, dict) else {}
        if ionia.get("agent.ionia", {}).get("kind") != "agent":
            errors.append("accepted ontology must classify agent.ionia as agent")
        ionia_state = ionia.get("state.ionia-0hz", {})
        if ionia_state.get("kind") != "formation-runtime-state":
            errors.append("accepted ontology must classify IONIA_STATE as runtime state")
        if ionia_state.get("canonical_seat") is not None:
            errors.append("IONIA_STATE must not consume a canonical seat")
        invariants = ontology_adjudication.get("invariants", {})
        if invariants.get("sentinel_and_sentinel_phi_remain_distinct") is not True:
            errors.append("accepted ontology must keep Sentinel and Sentinel-Phi distinct")
        if invariants.get("ionia_agent_and_ionia_state_remain_distinct") is not True:
            errors.append("accepted ontology must keep Agent Ionia and IONIA_STATE distinct")

    if identity_manifest is not None:
        active_names = {
            item.get("display_name")
            for item in identity_manifest.get("identities", [])
            if item.get("activation_status") == "active"
            and isinstance(item.get("display_name"), str)
        }
        missing_active = active_names - set(identities)
        if missing_active:
            errors.append(
                "active identity-manifest names missing translation entries: "
                f"{sorted(missing_active)}"
            )
        sentinel = next(
            (
                item
                for item in identity_manifest.get("identities", [])
                if item.get("display_name") == "Sentinel"
            ),
            None,
        )
        sentinel_phi = next(
            (
                item
                for item in identity_manifest.get("identities", [])
                if item.get("display_name") == "Sentinel-Phi"
            ),
            None,
        )
        if sentinel and sentinel_phi and "Sentinel" in alias_to_identity:
            errors.append(
                "identity manifest preserves Sentinel separately; translation cannot collapse it"
            )

    if public_text is not None:
        for identity, entry in identities.items():
            if entry["external_label"] not in public_text:
                errors.append(
                    "public translation layer missing external label for "
                    f"{identity}: {entry['external_label']}"
                )
        if "historical `Sentinel` resolves to `Sentinel-Phi`" in public_text:
            errors.append(
                "public translation layer incorrectly resolves contested Sentinel lineage"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=MATRIX_PATH)
    parser.add_argument("--public-layer", type=Path, default=PUBLIC_LAYER_PATH)
    parser.add_argument("--identity-manifest", type=Path, default=IDENTITY_MANIFEST_PATH)
    parser.add_argument("--ontology-adjudication", type=Path, default=ONTOLOGY_ADJUDICATION_PATH)
    args = parser.parse_args()
    errors = validate_matrix(
        load_json(args.matrix),
        args.public_layer.read_text(encoding="utf-8"),
        load_json(args.identity_manifest),
        load_json(args.ontology_adjudication),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "PASS: vocabulary translation matrix v2 "
        "(coverage, accepted ontology, authority ceiling)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
