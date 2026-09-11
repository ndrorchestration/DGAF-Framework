import copy
import json
from pathlib import Path

from scripts.validate_vocabulary_translation_matrix import validate_matrix

MATRIX_PATH = Path("docs/VOCABULARY_TRANSLATION_MATRIX.json")
PUBLIC_LAYER_PATH = Path("docs/PUBLIC_TRANSLATION_LAYER.md")
IDENTITY_MANIFEST_PATH = Path("registry/agent_identity_manifest.v1.json")
ONTOLOGY_PATH = Path("registry/agent_ontology_adjudication.v1.json")


def _matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def _manifest() -> dict:
    return json.loads(IDENTITY_MANIFEST_PATH.read_text(encoding="utf-8"))


def _ontology() -> dict:
    return json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))


def test_current_matrix_public_layer_manifest_and_ontology_pass() -> None:
    errors = validate_matrix(
        _matrix(),
        PUBLIC_LAYER_PATH.read_text(encoding="utf-8"),
        _manifest(),
        _ontology(),
    )
    assert errors == []


def test_duplicate_identity_fails_closed() -> None:
    matrix = _matrix()
    matrix["entries"].append(copy.deepcopy(matrix["entries"][0]))
    assert any("duplicate canonical identity" in error for error in validate_matrix(matrix))


def test_sentinel_lineage_cannot_be_collapsed_by_translation() -> None:
    matrix = _matrix()
    sentinel_phi = next(entry for entry in matrix["entries"] if entry["canonical_internal_identity"] == "Sentinel-Phi")
    sentinel_phi["aliases"] = ["Sentinel"]
    errors = validate_matrix(
        matrix,
        identity_manifest=_manifest(),
        ontology_adjudication=_ontology(),
    )
    assert any("Sentinel" in error and "alias" in error for error in errors)


def test_demijoule_sentinel_is_role_not_identity() -> None:
    matrix = _matrix()
    demi = next(entry for entry in matrix["entries"] if entry["canonical_internal_identity"] == "DemiJoule")
    demi["abstract_role_classes"] = ["ADVISE"]
    assert any("SENTINEL_ARCHETYPE" in error for error in validate_matrix(matrix))


def test_ionia_agent_and_state_remain_distinct_after_adjudication() -> None:
    matrix = _matrix()
    ionia = next(entry for entry in matrix["entries"] if entry["canonical_internal_identity"] == "Ionia")
    ionia_state = next(entry for entry in matrix["entries"] if entry["canonical_internal_identity"] == "IONIA_STATE")
    ionia["identity_kind"] = "STATE"
    ionia_state["identity_kind"] = "AGENT"
    errors = validate_matrix(matrix, ontology_adjudication=_ontology())
    assert any("Ionia" in error and "AGENT" in error for error in errors)
    assert any("IONIA_STATE" in error and "STATE" in error for error in errors)


def test_ionia_state_translation_entry_is_required() -> None:
    matrix = _matrix()
    matrix["entries"] = [entry for entry in matrix["entries"] if entry["canonical_internal_identity"] != "IONIA_STATE"]
    errors = validate_matrix(matrix, ontology_adjudication=_ontology())
    assert any("missing required identities" in error and "IONIA_STATE" in error for error in errors)


def test_active_manifest_identity_requires_translation_entry() -> None:
    matrix = _matrix()
    matrix["entries"] = [entry for entry in matrix["entries"] if entry["canonical_internal_identity"] != "Reson"]
    errors = validate_matrix(matrix, identity_manifest=_manifest())
    assert any("active identity-manifest" in error and "Reson" in error for error in errors)


def test_apogee_alias_is_preserved() -> None:
    matrix = _matrix()
    apogee = next(entry for entry in matrix["entries"] if entry["canonical_internal_identity"] == "Apogee")
    apogee["aliases"] = []
    assert any("Apogee Lens" in error for error in validate_matrix(matrix))


def test_translation_cannot_change_authority_or_scientific_state() -> None:
    matrix = _matrix()
    matrix["authority"]["authority_effect"] = "PROMOTE"
    matrix["authority"]["scientific_state_effect"] = "PROMOTE"
    errors = validate_matrix(matrix)
    assert "authority_effect must be NONE" in errors
    assert "scientific_state_effect must be NONE" in errors


def test_accepted_ontology_cannot_reclassify_ionia_state_as_seat() -> None:
    ontology = _ontology()
    ontology["distinct_objects"]["ionia"]["state.ionia-0hz"]["canonical_seat"] = "A-13"
    errors = validate_matrix(_matrix(), ontology_adjudication=ontology)
    assert any("IONIA_STATE must not consume" in error for error in errors)
