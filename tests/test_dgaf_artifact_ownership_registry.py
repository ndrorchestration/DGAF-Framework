from pathlib import Path

from scripts.validate_dgaf_artifact_ownership_registry import validate_registry


def test_canonical_artifact_registry_passes():
    assert validate_registry() == []


def test_duplicate_path_fails(tmp_path: Path):
    source = Path("docs/architecture/DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json").read_text(encoding="utf-8")
    marker = '"path": "scripts/dgaf_capability_canonicalize.py"'
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"path": "schemas/capability_manifest.schema.json"', marker, 1), encoding="utf-8")
    assert any("duplicate registry path" in e for e in validate_registry(path))


def test_unknown_owner_fails(tmp_path: Path):
    source = Path("docs/architecture/DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json").read_text(encoding="utf-8")
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"primary_owner": "K1"', '"primary_owner": "K99"', 1), encoding="utf-8")
    assert any("unknown primary_owner" in e for e in validate_registry(path))


def test_profile_must_be_profile_namespace(tmp_path: Path):
    source = Path("docs/architecture/DGAF_ARTIFACT_OWNERSHIP_REGISTRY.v1.json").read_text(encoding="utf-8")
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"profile": null', '"profile": "K1"', 1), encoding="utf-8")
    assert any("invalid profile" in e for e in validate_registry(path))
