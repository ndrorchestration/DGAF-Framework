import copy
import json
from pathlib import Path

from scripts.validate_vocabulary_translation_matrix import validate_matrix

MATRIX_PATH = Path("docs/VOCABULARY_TRANSLATION_MATRIX.json")
PUBLIC_LAYER_PATH = Path("docs/PUBLIC_TRANSLATION_LAYER.md")


def _matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def test_current_matrix_and_public_layer_pass() -> None:
    errors = validate_matrix(_matrix(), PUBLIC_LAYER_PATH.read_text(encoding="utf-8"))
    assert errors == []


def test_duplicate_identity_fails_closed() -> None:
    matrix = _matrix()
    matrix["entries"].append(copy.deepcopy(matrix["entries"][0]))
    errors = validate_matrix(matrix)
    assert any("duplicate canonical identity" in error for error in errors)


def test_sentinel_alias_cannot_point_to_demijoule() -> None:
    matrix = _matrix()
    for entry in matrix["entries"]:
        if entry["canonical_internal_identity"] == "Sentinel-Phi":
            entry["aliases"] = []
        if entry["canonical_internal_identity"] == "DemiJoule":
            entry["aliases"] = ["Sentinel"]
    errors = validate_matrix(matrix)
    assert any("Sentinel" in error and "Sentinel-Phi" in error for error in errors)


def test_apogee_alias_is_canonicalized() -> None:
    matrix = _matrix()
    for entry in matrix["entries"]:
        if entry["canonical_internal_identity"] == "Apogee":
            entry["aliases"] = []
    errors = validate_matrix(matrix)
    assert any("Apogee Lens" in error for error in errors)


def test_external_label_drift_fails() -> None:
    matrix = _matrix()
    for entry in matrix["entries"]:
        if entry["canonical_internal_identity"] == "Amethyst":
            entry["external_label"] = "Supreme Agent"
            entry["first_use_external"] = "Supreme Agent (Amethyst)"
    errors = validate_matrix(matrix)
    assert any("Amethyst" in error and "Governance Orchestrator" in error for error in errors)


def test_authority_effect_must_remain_none() -> None:
    matrix = _matrix()
    matrix["authority"]["authority_effect"] = "PROMOTE"
    errors = validate_matrix(matrix)
    assert "authority_effect must be NONE" in errors
