from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_locked_analysis_result.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("epoch002_result_admission_test", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def valid_output(validator):
    return {
        "record_type": "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS_OUTPUT",
        "schema_version": 1,
        "protocol_id": validator.PROTOCOL_ID,
        "authorization_event_commit_sha": "a" * 40,
        "authorization_record_id": validator.AUTH_RECORD_ID,
        "materialized_input_sha256": validator.EXPECTED_MATERIALIZED_INPUT_SHA256,
        "analysis_blob_sha": validator.ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": validator.ANALYSIS_CONFIG_SHA256,
        "environment": {"python": validator.EXPECTED_PYTHON, "numpy": validator.EXPECTED_NUMPY},
        "result": {
            "protocol_id": validator.PROTOCOL_ID,
            "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
            "primary_topology": "pdmal",
            "primary_comparator": "random_regular",
            "paired_seed_count": 50,
            "estimate_pdmal_minus_random_regular": 0.1,
            "two_sided_95pct_percentile_ci": [0.02, 0.18],
            "classification": "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
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


def test_local_output_validation_accepts_locked_shape() -> None:
    validator = load_validator()
    validator.validate_local_output_object(valid_output(validator), authorization_event_sha="a" * 40)


def test_local_output_rejects_inconsistent_classification() -> None:
    validator = load_validator()
    output = valid_output(validator)
    output["result"]["classification"] = "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"
    with pytest.raises(SystemExit, match="classification is inconsistent"):
        validator.validate_local_output_object(output, authorization_event_sha="a" * 40)


def test_local_output_rejects_runtime_drift() -> None:
    validator = load_validator()
    output = valid_output(validator)
    output["environment"]["python"] = "3.12.14"
    with pytest.raises(SystemExit, match="runtime identity drift"):
        validator.validate_local_output_object(output, authorization_event_sha="a" * 40)


def test_result_record_preserves_full_nonpromotion_ceiling() -> None:
    validator = load_validator()
    record = validator.expected_result_record(
        authorization_event_sha="a" * 40,
        output_sha256="b" * 64,
        result_parent_sha="c" * 40,
        generated_at_utc="2026-09-18T16:00:00Z",
    )
    validator.validate_schema(record)
    validator.validate_semantics(record)

    assert record["record_type"] == "LOCKED_ANALYSIS_RESULT_RECORD"
    assert record["authorization_effect"] == "NONE"
    assert record["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }
    assert record["non_effects"] == validator.FULL_NON_EFFECTS
    assert set(record["immutable_subject"]) == {"commit_sha", "sha256"}


def test_tooling_mode_is_nonexecuting_and_result_absent() -> None:
    validator = load_validator()
    validator.validate_tooling_only()


def test_result_scope_is_content_address_only() -> None:
    validator = load_validator()
    assert validator.RESULT_SCOPE == "LOCKED_PRIMARY_ANALYSIS_OUTPUT_CONTENT_ADDRESS_ONLY"
    source = VALIDATOR_PATH.read_text(encoding="utf-8")
    assert "estimate_pdmal_minus_random_regular" in source
    assert "subprocess.run" in source
    assert "analyze(" not in source
