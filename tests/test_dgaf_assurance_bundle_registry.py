from pathlib import Path

from scripts.validate_dgaf_assurance_bundle_registry import (
    covered_assurance_candidates,
    validate_assurance_bundles,
)


def test_canonical_assurance_bundle_registry_passes():
    assert validate_assurance_bundles() == []


def test_assurance_candidates_are_covered():
    assert covered_assurance_candidates()


def test_unknown_assurance_owner_fails(tmp_path: Path):
    source = Path(
        "docs/architecture/DGAF_ASSURANCE_BUNDLE_REGISTRY.v1.json"
    ).read_text(encoding="utf-8")
    path = tmp_path / "assurance.json"
    path.write_text(
        source.replace('"primary_owner": "A1"', '"primary_owner": "K1"', 1),
        encoding="utf-8",
    )
    assert any(
        "invalid assurance primary owner" in error
        for error in validate_assurance_bundles(path)
    )
