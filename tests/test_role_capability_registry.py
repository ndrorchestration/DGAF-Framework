import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "role_capability_registry.v1.json"
LINEAGE = ROOT / "governance" / "persona_role_lineage.v1.json"

REFERENCE_CLASSES = {"FD", "PP", "FX", "HP", "UN"}
AUTHORITY_STATUSES = {"equivalent", "none", "unresolved"}


def _load(path: Path) -> dict:
    assert path.is_file(), f"required architecture artifact missing: {path}"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_registry_has_versioned_unique_functional_ids():
    registry = _load(REGISTRY)
    assert registry["schema_version"] == 1
    assert registry["architecture"] == "persona-to-role"

    role_ids = [role["id"] for role in registry["roles"]]
    capability_ids = [capability["id"] for capability in registry["capabilities"]]

    assert role_ids
    assert capability_ids
    assert len(role_ids) == len(set(role_ids))
    assert len(capability_ids) == len(set(capability_ids))
    assert all(role_id.startswith("role.") for role_id in role_ids)
    assert all(capability_id.startswith("cap.") for capability_id in capability_ids)


def test_every_role_resolves_capabilities_and_authority_classes():
    registry = _load(REGISTRY)
    capability_ids = {capability["id"] for capability in registry["capabilities"]}
    allowed_authority = set(registry["authority_classes"])

    for role in registry["roles"]:
        assert role["capabilities"], f"role has no capabilities: {role['id']}"
        assert set(role["capabilities"]) <= capability_ids
        assert set(role["authority_classes"]) <= allowed_authority
        assert role["boundary"].strip()


def test_lineage_maps_identity_without_granting_new_authority():
    registry = _load(REGISTRY)
    lineage = _load(LINEAGE)
    role_ids = {role["id"] for role in registry["roles"]}

    assert lineage["schema_version"] == 1
    assert lineage["registry_schema_version"] == registry["schema_version"]

    legacy_ids = []
    for entry in lineage["entries"]:
        legacy_ids.append(entry["legacy_identity"])
        assert entry["reference_class"] in REFERENCE_CLASSES
        assert entry["authority_equivalence"]["status"] in AUTHORITY_STATUSES
        assert entry["authority_equivalence"]["authority_change"] is False

        role_id = entry.get("role_id")
        if entry["reference_class"] == "FD":
            assert role_id in role_ids
            assert entry["authority_equivalence"]["status"] == "equivalent"
        elif role_id is not None:
            assert role_id in role_ids

    assert len(legacy_ids) == len(set(legacy_ids))


def test_state_and_historical_aliases_cannot_become_authority_seats():
    registry = _load(REGISTRY)
    lineage = _load(LINEAGE)
    roles = {role["id"]: role for role in registry["roles"]}
    entries = {entry["legacy_identity"]: entry for entry in lineage["entries"]}

    ionia = entries["Ionia"]
    assert ionia["role_id"] == "role.convergence-state-observer"
    assert roles[ionia["role_id"]]["authority_classes"] == ["STATE", "ADVISORY"]
    assert "no independent governance authority" in roles[ionia["role_id"]]["boundary"].lower()

    sentinel = entries["Sentinel"]
    sentience = entries["Sentience"]
    assert sentinel["reference_class"] == "HP"
    assert sentience["reference_class"] == "HP"
    assert sentinel["role_id"] is None
    assert sentience["role_id"] is None
    assert sentinel["authority_equivalence"]["status"] == "none"
    assert sentience["authority_equivalence"]["status"] == "none"
