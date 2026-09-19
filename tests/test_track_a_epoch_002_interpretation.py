from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_interpretation.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("epoch002_interpretation_test", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def valid_analysis_output(validator, *, estimate=0.10, ci=None):
    if ci is None:
        ci = [0.02, 0.18]
    result_validator = validator.result_validator()
    classification = result_validator.expected_classification(float(estimate), float(ci[0]), float(ci[1]))
    return {
        "record_type": "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS_OUTPUT",
        "schema_version": 1,
        "protocol_id": validator.PROTOCOL_ID,
        "authorization_event_commit_sha": "a" * 40,
        "authorization_record_id": "E002-ANALYSIS-AUTH-0001",
        "materialized_input_sha256": result_validator.EXPECTED_MATERIALIZED_INPUT_SHA256,
        "analysis_blob_sha": result_validator.ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": result_validator.ANALYSIS_CONFIG_SHA256,
        "environment": {
            "python": result_validator.EXPECTED_PYTHON,
            "numpy": result_validator.EXPECTED_NUMPY,
        },
        "result": {
            "protocol_id": validator.PROTOCOL_ID,
            "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
            "primary_topology": "pdmal",
            "primary_comparator": "random_regular",
            "paired_seed_count": 50,
            "estimate_pdmal_minus_random_regular": estimate,
            "two_sided_95pct_percentile_ci": ci,
            "classification": classification,
            "bootstrap_resamples": 10000,
            "bootstrap_seed": 20270251,
            "alpha": 0.05,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED_N0",
        },
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }


@pytest.mark.parametrize(
    ("estimate", "ci", "classification"),
    [
        (0.10, [0.02, 0.18], "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"),
        (-0.10, [-0.18, -0.02], "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"),
        (0.01, [-0.04, 0.06], "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"),
    ],
)
def test_local_interpretation_packet_obeys_frozen_classification(
    estimate, ci, classification
) -> None:
    validator = load_validator()
    output = valid_analysis_output(validator, estimate=estimate, ci=ci)
    packet = validator.expected_local_interpretation_packet(
        output,
        result_event_sha="b" * 40,
        output_sha256="c" * 64,
    )
    validator.validate_local_interpretation_packet_object(
        packet,
        expected_result_event_sha="b" * 40,
        expected_output_sha256="c" * 64,
    )
    assert packet["result"]["classification"] == classification
    assert packet["interpretation"]["classification"] == classification


def test_local_packet_rejects_claim_scope_inflation() -> None:
    validator = load_validator()
    packet = validator.expected_local_interpretation_packet(
        valid_analysis_output(validator),
        result_event_sha="b" * 40,
        output_sha256="c" * 64,
    )
    packet["interpretation"]["claim_scope"] = "CANONICAL_DGAF_EFFICACY"
    with pytest.raises(SystemExit, match="claim ceiling or statement drift"):
        validator.validate_local_interpretation_packet_object(
            packet,
            expected_result_event_sha="b" * 40,
            expected_output_sha256="c" * 64,
        )


def test_local_packet_rejects_historical_pooling() -> None:
    validator = load_validator()
    packet = validator.expected_local_interpretation_packet(
        valid_analysis_output(validator),
        result_event_sha="b" * 40,
        output_sha256="c" * 64,
    )
    packet["separation_constraints"]["track_a_epoch_001_pooled"] = True
    with pytest.raises(SystemExit, match="binding drift: separation_constraints"):
        validator.validate_local_interpretation_packet_object(
            packet,
            expected_result_event_sha="b" * 40,
            expected_output_sha256="c" * 64,
        )


def test_local_packet_rejects_digest_substitution() -> None:
    validator = load_validator()
    packet = validator.expected_local_interpretation_packet(
        valid_analysis_output(validator),
        result_event_sha="b" * 40,
        output_sha256="c" * 64,
    )
    with pytest.raises(SystemExit, match="binding drift: locked_analysis_output_sha256"):
        validator.validate_local_interpretation_packet_object(
            packet,
            expected_result_event_sha="b" * 40,
            expected_output_sha256="d" * 64,
        )


def test_note_is_content_address_only_and_nonpromotional() -> None:
    validator = load_validator()
    note = validator.expected_note_record(
        result_event_sha="b" * 40,
        packet_sha256="c" * 64,
        interpretation_parent_sha="d" * 40,
        generated_at_utc="2026-09-19T10:00:00Z",
    )
    validator.validate_note_record(
        note,
        result_event_sha="b" * 40,
        interpretation_parent_sha="d" * 40,
    )
    assert note["record_type"] == "INTERPRETATION_NOTE"
    assert note["authorization_effect"] == "NONE"
    assert note["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    assert note["predecessor_record_ids"] == [validator.RESULT_RECORD_ID]
    serialized = validator.canonical_json_bytes(note).decode("utf-8")
    assert "estimate_pdmal_minus_random_regular" not in serialized
    assert "two_sided_95pct_percentile_ci" not in serialized
    assert "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS" not in serialized


def test_tooling_mode_preserves_accepted_result_and_absent_note(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    monkeypatch.setattr(
        validator,
        "NOTE_REL",
        "docs/experiment/track_a_runs/__TOOLING_ONLY_INTERPRETATION_ABSENT__.json",
    )
    validator.validate_tooling_only()


def test_interpretation_tooling_has_no_analysis_execution_surface() -> None:
    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    assert "run_track_a_epoch_002_locked_primary_analysis.py" not in source
    assert "analyze(" not in source
