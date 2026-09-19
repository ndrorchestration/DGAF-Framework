from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
INTERPRETATION_VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_interpretation.py"
RESULT_VALIDATOR_PATH = ROOT / "scripts/validate_track_a_epoch_002_locked_analysis_result.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def valid_result(
    *,
    estimate: float = 0.1,
    ci: list[float] | None = None,
    classification: str = "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS",
) -> dict:
    if ci is None:
        ci = [0.02, 0.18]
    return {
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
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
    }


def test_local_interpretation_is_exact_and_same_system_nonindependent() -> None:
    validator = load_module(INTERPRETATION_VALIDATOR_PATH, "epoch002_interpretation_local_test")
    result = valid_result()
    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    validator.validate_local_interpretation(
        artifact,
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    assert artifact["evidence_class"] == "SAME_SYSTEM_NONINDEPENDENT"
    assert artifact["confirmatory_contract"]["confirmatory_test_count"] == 1
    assert artifact["interpretation"]["exploratory_claims"] == []
    assert len(artifact["interpretation"]["competing_interpretations"]) >= 2
    assert len(artifact["interpretation"]["scope_limitations"]) >= 5


def test_preregistered_contract_and_claim_ceiling_are_bound() -> None:
    validator = load_module(INTERPRETATION_VALIDATOR_PATH, "epoch002_interpretation_prereg_test")
    prereg = validator.validate_preregistered_contract()
    assert prereg["primary_analysis"]["estimand"] == "mean of 50 paired_seed_effect values"
    assert prereg["multiplicity_policy"]["confirmatory_test_count"] == 1
    assert prereg["claim_ceiling"]["allowed_if_executed"] == validator.EXACT_CLAIM_SCOPE


@pytest.mark.parametrize(
    ("estimate", "ci", "classification"),
    [
        (0.10, [0.02, 0.18], "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"),
        (-0.10, [-0.18, -0.02], "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"),
        (0.01, [-0.04, 0.06], "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"),
    ],
)
def test_all_frozen_interpretation_branches_preserve_competing_views(
    estimate: float,
    ci: list[float],
    classification: str,
) -> None:
    validator = load_module(
        INTERPRETATION_VALIDATOR_PATH,
        f"epoch002_interpretation_branch_{classification}",
    )
    result = valid_result(estimate=estimate, ci=ci, classification=classification)
    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    assert artifact["interpretation"]["confirmatory_statement"] == validator.interpretation_statement(classification)
    assert artifact["interpretation"]["competing_interpretations"] == (
        validator.COMPETING_INTERPRETATIONS[classification]
    )
    assert artifact["interpretation"]["claim_scope"] == validator.EXACT_CLAIM_SCOPE


def test_local_interpretation_rejects_historical_pooling_or_claim_scope_drift() -> None:
    validator = load_module(
        INTERPRETATION_VALIDATOR_PATH,
        "epoch002_interpretation_scope_guard_test",
    )
    result = valid_result()
    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    artifact["separation_constraints"]["track_a_epoch_001_pooled"] = True
    with pytest.raises(SystemExit, match="does not match the frozen interpretation contract"):
        validator.validate_local_interpretation(
            artifact,
            result_event_sha="a" * 40,
            locked_output_sha256="b" * 64,
            result=result,
        )

    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    artifact["interpretation"]["claim_scope"] = "CANONICAL_DGAF_EFFICACY"
    with pytest.raises(SystemExit, match="does not match the frozen interpretation contract"):
        validator.validate_local_interpretation(
            artifact,
            result_event_sha="a" * 40,
            locked_output_sha256="b" * 64,
            result=result,
        )


def test_local_interpretation_rejects_claim_inflation() -> None:
    validator = load_module(INTERPRETATION_VALIDATOR_PATH, "epoch002_interpretation_claim_test")
    result = valid_result()
    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    artifact["scientific_state_effect"]["canonical_dgaf_efficacy"] = "ESTABLISHED"
    with pytest.raises(SystemExit, match="does not match the frozen interpretation contract"):
        validator.validate_local_interpretation(
            artifact,
            result_event_sha="a" * 40,
            locked_output_sha256="b" * 64,
            result=result,
        )


def test_local_interpretation_rejects_exploratory_relabeling() -> None:
    validator = load_module(INTERPRETATION_VALIDATOR_PATH, "epoch002_interpretation_exploratory_test")
    result = valid_result()
    artifact = validator.expected_local_interpretation(
        result_event_sha="a" * 40,
        locked_output_sha256="b" * 64,
        result=result,
    )
    artifact["interpretation"]["exploratory_claims"] = ["post-hoc stronger claim"]
    with pytest.raises(SystemExit, match="does not match the frozen interpretation contract"):
        validator.validate_local_interpretation(
            artifact,
            result_event_sha="a" * 40,
            locked_output_sha256="b" * 64,
            result=result,
        )


def test_repository_note_contains_content_address_not_numerical_result() -> None:
    validator = load_module(INTERPRETATION_VALIDATOR_PATH, "epoch002_interpretation_note_test")
    note = validator.expected_repository_note(
        result_event_sha="a" * 40,
        interpretation_sha256="b" * 64,
        parent_sha="c" * 40,
        generated_at_utc="2026-09-19T09:00:00Z",
    )
    validator.validate_schema(note)
    validator.validate_semantics(note)

    rendered = str(note)
    assert note["record_type"] == "INTERPRETATION_NOTE"
    assert note["evidence_scope"] == "INTERPRETATION_CONTENT_ADDRESS_ONLY_SAME_SYSTEM_NONINDEPENDENT"
    assert note["predecessor_record_ids"] == ["E002-ANALYSIS-RESULT-0001"]
    assert "estimate_pdmal_minus_random_regular" not in rendered
    assert "two_sided_95pct_percentile_ci" not in rendered
    assert "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS" not in rendered
    assert note["authorization_effect"] == "NONE"
    assert note["scientific_state_effect"]["empirical_n_increment"] == 0


def test_result_validator_still_rejects_inconsistent_classification() -> None:
    result_validator = load_module(RESULT_VALIDATOR_PATH, "epoch002_interpretation_result_guard_test")
    output = {
        "record_type": "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS_OUTPUT",
        "schema_version": 1,
        "protocol_id": result_validator.PROTOCOL_ID,
        "authorization_event_commit_sha": "a" * 40,
        "authorization_record_id": result_validator.AUTH_RECORD_ID,
        "materialized_input_sha256": result_validator.EXPECTED_MATERIALIZED_INPUT_SHA256,
        "analysis_blob_sha": result_validator.ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": result_validator.ANALYSIS_CONFIG_SHA256,
        "environment": {"python": result_validator.EXPECTED_PYTHON, "numpy": result_validator.EXPECTED_NUMPY},
        "result": valid_result(),
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "independent_validation": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED_N0",
    }
    output["result"]["classification"] = "INCONCLUSIVE_OR_NOT_DIRECTIONALLY_SUPPORTED"
    with pytest.raises(SystemExit, match="classification is inconsistent"):
        result_validator.validate_local_output_object(output, authorization_event_sha="a" * 40)


def test_interpretation_tooling_does_not_run_primary_analysis() -> None:
    source = INTERPRETATION_VALIDATOR_PATH.read_text(encoding="utf-8")
    preparer = (ROOT / "scripts/prepare_track_a_epoch_002_interpretation_note.py").read_text(encoding="utf-8")
    combined = source + preparer
    assert "run_track_a_epoch_002_locked_primary_analysis.py" not in combined
    assert "subprocess.run" not in source
    assert "SCIENTIFIC_N_INCREMENT=0" in source
