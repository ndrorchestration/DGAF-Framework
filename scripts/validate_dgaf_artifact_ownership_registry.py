from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (
    ROOT
    / "docs"
    / "architecture"
    / "DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json"
)
COMPONENTS = (
    ROOT
    / "docs"
    / "architecture"
    / "DGAF_CORE_COMPONENT_REGISTRY.v1.json"
)

ALLOWED_TYPES = {
    "code",
    "schema",
    "policy",
    "evidence",
    "test",
    "workflow",
    "ui",
    "record",
    "documentation",
    "validator",
    "registry",
}
ALLOWED_LIFECYCLES = {
    "ACTIVE",
    "HISTORICAL",
    "SUPERSEDED",
    "RETIRED",
    "CANDIDATE",
}
ALLOWED_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
ALLOWED_EFFECTS = {
    "NONE",
    "IDENTITY_BINDING",
    "AUTHORITY_BOUNDING",
    "ALLOW_DENY_ESCALATE",
    "STATE_TRANSITION_GATING",
    "REPLAY_OR_COMMIT_GATING",
    "EVIDENCE_BINDING",
    "RECOVERY_GATING",
    "CLAIM_PROMOTION_GATING",
    "CUSTODY_GATING",
    "ASSURANCE_ONLY",
    "PRESENTATION_ONLY",
}


def canonical_ids() -> set[str]:
    data = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    ids: set[str] = set()
    keys = (
        "core_components",
        "assurance_components",
        "governed_profiles",
        "external_integrations",
    )
    for key in keys:
        ids.update(str(item["id"]) for item in data[key])
    return ids


def validate_registry(path: Path = REGISTRY) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "dgaf-artifact-ownership-registry.v1":
        errors.append("unexpected schema_version")
    records = data.get("records")
    if not isinstance(records, list):
        return errors + ["records must be a list"]

    ids = canonical_ids()
    seen: set[str] = set()
    for idx, rec in enumerate(records):
        label = f"record[{idx}]"
        path_value = rec.get("path")
        if not isinstance(path_value, str) or not path_value:
            errors.append(f"{label}: path missing")
            continue
        if path_value in seen:
            errors.append(f"{path_value}: duplicate registry path")
        seen.add(path_value)

        if not (ROOT / path_value).exists():
            errors.append(f"{path_value}: registered path does not exist")

        owner = rec.get("primary_owner")
        if owner not in ids:
            errors.append(f"{path_value}: unknown primary_owner {owner!r}")

        deps = rec.get("secondary_dependencies")
        if not isinstance(deps, list):
            errors.append(
                f"{path_value}: secondary_dependencies must be a list"
            )
        else:
            unknown = sorted(set(map(str, deps)) - ids)
            if unknown:
                errors.append(
                    f"{path_value}: unknown secondary_dependencies {unknown}"
                )
            if owner in deps:
                errors.append(
                    f"{path_value}: primary owner duplicated as secondary dependency"
                )

        profile = rec.get("profile")
        if profile is not None and (
            profile not in ids or not str(profile).startswith("P-")
        ):
            errors.append(f"{path_value}: invalid profile {profile!r}")

        if rec.get("artifact_type") not in ALLOWED_TYPES:
            errors.append(f"{path_value}: invalid artifact_type")
        if rec.get("lifecycle") not in ALLOWED_LIFECYCLES:
            errors.append(f"{path_value}: invalid lifecycle")
        if rec.get("classification_confidence") not in ALLOWED_CONFIDENCE:
            errors.append(f"{path_value}: invalid classification_confidence")

        effect = rec.get("authority_effect")
        if effect not in ALLOWED_EFFECTS:
            errors.append(
                f"{path_value}: invalid authority_effect {effect!r}"
            )

        if (
            rec.get("lifecycle") == "ACTIVE"
            and (
                str(owner).startswith("K")
                or str(owner).startswith("P-")
            )
            and effect == "NONE"
        ):
            errors.append(
                f"{path_value}: active kernel/profile artifact cannot have "
                "NONE authority effect"
            )

        if not rec.get("role"):
            errors.append(f"{path_value}: role missing")
        if not rec.get("evidence_scope"):
            errors.append(f"{path_value}: evidence_scope missing")
        if not rec.get("source_binding"):
            errors.append(f"{path_value}: source_binding missing")

        tests = rec.get("tests_or_validators")
        if not isinstance(tests, list):
            errors.append(
                f"{path_value}: tests_or_validators must be a list"
            )
        else:
            for test_path in tests:
                if not (ROOT / str(test_path)).exists():
                    errors.append(
                        f"{path_value}: linked test/validator absent: "
                        f"{test_path}"
                    )

    return errors


def main() -> int:
    errors = validate_registry()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    record_count = len(
        json.loads(REGISTRY.read_text(encoding="utf-8"))["records"]
    )
    print(f"DGAF artifact ownership registry: PASS ({record_count} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
