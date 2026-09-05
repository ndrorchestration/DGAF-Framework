import copy
import json
from pathlib import Path

import pytest

from scripts.validate_instrument_identity_manifest import validate_manifest

MANIFEST = Path("docs/governance/instrument_identity_manifest_2026-09-04.json")


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def instrument(data, instrument_id):
    return next(x for x in data["instruments"] if x["instrument_id"] == instrument_id)


def test_current_instrument_manifest_validates():
    validate_manifest(load_manifest())


def test_duplicate_instrument_identity_fails_closed():
    data = load_manifest()
    data["instruments"].append(copy.deepcopy(data["instruments"][0]))
    with pytest.raises(ValueError, match="duplicate instrument_id"):
        validate_manifest(data)


def test_11q_silent_normalization_is_rejected():
    data = load_manifest()
    qa11q = instrument(data, "QA-11Q-ARTIFACT-v1")
    qa11q["parameter_set"]["declared_default_weight_sum"] = 11.0
    with pytest.raises(ValueError, match="preserve declared weight sum"):
        validate_manifest(data)


def test_11q_unreachable_threshold_cannot_be_relabelled_reachable():
    data = load_manifest()
    qa11q = instrument(data, "QA-11Q-ARTIFACT-v1")
    qa11q["diagnostics"]["threshold_reachable_under_declared_formula"] = True
    with pytest.raises(ValueError, match="threshold as unreachable"):
        validate_manifest(data)


def test_axis_derivative_cannot_be_silently_promoted():
    data = load_manifest()
    apogee_axis = instrument(data, "APOGEE-AXIS-RUBRIC-v1")
    apogee_axis["binding_strength"] = "CANONICAL"
    with pytest.raises(ValueError, match="contradiction must remain blocked"):
        validate_manifest(data)


def test_reson_threshold_conflict_must_preserve_both_values():
    data = load_manifest()
    reson = instrument(data, "RESON-HARMONIC-v1")
    reson["thresholds_or_predicates"]["observed_thresholds"] = [0.75]
    with pytest.raises(ValueError, match="preserve both observed thresholds"):
        validate_manifest(data)


def test_ahg_divergence_cannot_be_silently_normalized():
    data = load_manifest()
    ahg = instrument(data, "AHG-ANALYSIS-v1")
    ahg["parameter_set"]["explicit_normalization"] = True
    with pytest.raises(ValueError, match="must remain unresolved"):
        validate_manifest(data)


def test_unresolved_upstream_dependency_must_exist():
    data = load_manifest()
    gate = instrument(data, "GATE-11Q-v2")
    gate["upstream_dependencies"] = ["MISSING-INSTRUMENT"]
    with pytest.raises(ValueError, match="missing upstream dependency"):
        validate_manifest(data)


def test_scientific_boundary_cannot_move_in_instrument_reconciliation():
    data = load_manifest()
    data["scientific_boundary"] = "AUTHORIZED"
    with pytest.raises(ValueError, match="scientific boundary changed"):
        validate_manifest(data)
