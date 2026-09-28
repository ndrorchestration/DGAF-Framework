from pathlib import Path

from scripts.validate_dgaf_profile_bundle_registry import (
    covered_profile_candidates,
    validate_profile_bundles,
)


def test_canonical_profile_bundle_registry_passes():
    assert validate_profile_bundles() == []


def test_profile_candidates_are_covered():
    assert covered_profile_candidates()


def test_unknown_profile_id_fails(tmp_path: Path):
    source = Path("docs/architecture/DGAF_PROFILE_BUNDLE_REGISTRY.v1.json").read_text(
        encoding="utf-8"
    )
    path = tmp_path / "profiles.json"
    path.write_text(source.replace('"id": "P-AOSS"', '"id": "P-UNKNOWN"', 1), encoding="utf-8")
    assert any("unknown profile id" in error for error in validate_profile_bundles(path))
