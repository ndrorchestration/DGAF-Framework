from pathlib import Path

from scripts.validate_dgaf_core_component_registry import validate_registry


def test_canonical_registry_passes():
    assert validate_registry() == []


def test_duplicate_id_fails(tmp_path: Path):
    source = Path("docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json").read_text(encoding="utf-8")
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"id": "A1"', '"id": "K1"', 1), encoding="utf-8")
    assert any("unique" in error or "A1-A4" in error for error in validate_registry(path))


def test_missing_core_component_fails(tmp_path: Path):
    source = Path("docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json").read_text(encoding="utf-8")
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"id": "K8"', '"id": "K9"', 1), encoding="utf-8")
    assert any("K1-K8" in error for error in validate_registry(path))


def test_profile_cannot_masquerade_as_core(tmp_path: Path):
    source = Path("docs/architecture/DGAF_CORE_COMPONENT_REGISTRY.v1.json").read_text(encoding="utf-8")
    path = tmp_path / "registry.json"
    path.write_text(source.replace('"id": "P-AOSS"', '"id": "AOSS"', 1), encoding="utf-8")
    assert any("must start with P-" in error for error in validate_registry(path))
