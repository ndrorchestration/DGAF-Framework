import copy
import json
from pathlib import Path

from scripts.validate_vocabulary_translation_matrix import validate_matrix

MATRIX_PATH = Path("docs/VOCABULARY_TRANSLATION_MATRIX.json")
PUBLIC_LAYER_PATH = Path("docs/PUBLIC_TRANSLATION_LAYER.md")
IDENTITY_MANIFEST_PATH = Path("registry/agent_identity_manifest.v1.json")


def _matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def _manifest() -> dict:
    return json.loads(IDENTITY_MANIFEST_PATH.read_text(encoding="utf-8"))


def test_current_matrix_public_layer_and_manifest_pass() -> None:
    errors = validate_matrix(
        _matrix(),
        PUBLIC_LAYER_PATH.read_text(encoding="utf-8"),
        _manifest(),
    )
    assert errors == []


def test_duplicate_identity_fails_closed() -> None:
    matrix = _matrix()
    matrix["entries"].append(copy.deepcopy(matrix["entries"][0]))
    assert any("duplicate canonical identity" in e for e in validate_matrix(matrix))


def test_sentinel_lineage_cannot_be_collapsed_by_translation() -> None:
    matrix = _matrix()
    sentinel_phi = next(e for e in matrix["entries"] if e["canonical_internal_identity"] == "Sentinel-Phi")
    sentinel_phi["aliases"] = ["Sentinel"]
    errors = validate_matrix(matrix, identity_manifest=_manifest())
    assert any("Sentinel" in e and ("unresolved" in e or "collapse" in e) for e in errors)


def test_demijoule_sentinel_is_role_not_identity() -> None:
    matrix = _matrix()
    demi = next(e for e in matrix["entries"] if e["canonical_internal_identity"] == "DemiJoule")
    demi["abstract_role_classes"] = ["ADVISE"]
    assert any("SENTINEL_ARCHETYPE" in e for e in validate_matrix(matrix))


def test_ionia_remains_state_until_reconciled() -> None:
    matrix = _matrix()
    ionia = next(e for e in matrix["entries"] if e["canonical_internal_identity"] == "Ionia")
    ionia["identity_kind"] = "AGENT"
    assert any("Ionia" in e and "STATE" in e for e in validate_matrix(matrix))


def test_active_manifest_identity_requires_translation_entry() -> None:
    matrix = _matrix()
    matrix["entries"] = [e for e in matrix["entries"] if e["canonical_internal_identity"] != "Reson"]
    errors = validate_matrix(matrix, identity_manifest=_manifest())
    assert any("active identity-manifest" in e and "Reson" in e for e in errors)


def test_apogee_alias_is_preserved() -> None:
    matrix = _matrix()
    apogee = next(e for e in matrix["entries"] if e["canonical_internal_identity"] == "Apogee")
    apogee["aliases"] = []
    assert any("Apogee Lens" in e for e in validate_matrix(matrix))


def test_translation_cannot_change_authority_or_scientific_state() -> None:
    matrix = _matrix()
    matrix["authority"]["authority_effect"] = "PROMOTE"
    matrix["authority"]["scientific_state_effect"] = "PROMOTE"
    errors = validate_matrix(matrix)
    assert "authority_effect must be NONE" in errors
    assert "scientific_state_effect must be NONE" in errors
