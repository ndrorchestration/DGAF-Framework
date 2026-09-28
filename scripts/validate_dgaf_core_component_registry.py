from __future__ import annotations

import json
from pathlib import Path


REGISTRY = Path("docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json")
EXPECTED_CORE = {f"K{i}" for i in range(1, 9)}
EXPECTED_ASSURANCE = {f"A{i}" for i in range(1, 5)}
ALLOWED_AUTHORITY_EFFECTS = {
    "IDENTITY_BINDING",
    "AUTHORITY_BOUNDING",
    "ALLOW_DENY_ESCALATE",
    "STATE_TRANSITION_GATING",
    "REPLAY_AND_COMMIT_TIME_AUTHORITY",
    "EVIDENCE_BINDING_ONLY",
    "RECOVERY_GATING",
    "CLAIM_PROMOTION_GATING",
    "ASSURANCE_DECISION_ONLY",
    "CUSTODY_AND_PROVENANCE_GATING",
    "SEMANTIC_ROUTING_ONLY",
    "PRESENTATION_AND_MEDIATION_ONLY",
}


def _ids(items: list[dict[str, object]]) -> list[str]:
    return [str(item.get("id", "")) for item in items]


def validate_registry(path: Path = REGISTRY) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schema_version") != "dgaf-core-component-registry.v1":
        errors.append("unexpected schema_version")

    core = data.get("core_components")
    assurance = data.get("assurance_components")
    profiles = data.get("governed_profiles")
    external = data.get("external_integrations")

    if not isinstance(core, list):
        return errors + ["core_components must be a list"]
    if not isinstance(assurance, list):
        return errors + ["assurance_components must be a list"]
    if not isinstance(profiles, list):
        return errors + ["governed_profiles must be a list"]
    if not isinstance(external, list):
        return errors + ["external_integrations must be a list"]

    core_ids = _ids(core)
    assurance_ids = _ids(assurance)

    if set(core_ids) != EXPECTED_CORE or len(core_ids) != len(EXPECTED_CORE):
        errors.append("core component IDs must be exactly K1-K8")
    if set(assurance_ids) != EXPECTED_ASSURANCE or len(assurance_ids) != len(EXPECTED_ASSURANCE):
        errors.append("assurance component IDs must be exactly A1-A4")

    all_ids = core_ids + assurance_ids + _ids(profiles) + _ids(external)
    if len(all_ids) != len(set(all_ids)):
        errors.append("component/profile/integration IDs must be unique")

    for item in core + assurance:
        if not item.get("name"):
            errors.append(f"{item.get('id', '<missing>')} must have a name")
        effect = item.get("authority_effect")
        if effect not in ALLOWED_AUTHORITY_EFFECTS:
            errors.append(f"{item.get('id', '<missing>')} has unknown authority_effect {effect!r}")

    for item in core:
        artifacts = item.get("primary_artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f"{item.get('id', '<missing>')} must declare primary_artifacts")
        outputs = item.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            errors.append(f"{item.get('id', '<missing>')} must declare outputs")

    for item in profiles:
        if not str(item.get("id", "")).startswith("P-"):
            errors.append(f"profile ID {item.get('id')!r} must start with P-")
        if not item.get("classification"):
            errors.append(f"profile {item.get('id')!r} must declare classification")

    for item in external:
        if not str(item.get("id", "")).startswith("X-"):
            errors.append(f"external integration ID {item.get('id')!r} must start with X-")
        if not item.get("classification"):
            errors.append(f"external integration {item.get('id')!r} must declare classification")

    return errors


def main() -> int:
    errors = validate_registry()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("DGAF core component registry: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
