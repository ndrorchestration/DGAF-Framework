"""Regression tests for Issue #32 Task-4 audit evaluation integrity."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("dgaf_eval_suite.py")
SPEC = importlib.util.spec_from_file_location("dgaf_eval_suite_task4", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

run_audit_hallucination_rate = MODULE.run_audit_hallucination_rate


def audit_event(**overrides):
    event = {
        "role": "Herald",
        "curvature": 0.25,
        "contraction": 0.50,
        "gate_result": "PASS",
        "timestamp": "2026-09-05T00:00:00Z",
        "session_id": "S100",
    }
    event.update(overrides)
    return event


def test_missing_ground_truth_and_outputs_fail_closed():
    result = run_audit_hallucination_rate(precision_mode="BF16", n_samples=1)

    assert result.score == 0.0
    assert result.sample_count == 0
    assert result.preconditions_met is False
    assert result.passed is False
    assert any("ground_truth_fixtures" in item for item in result.precondition_failures)
    assert any("generated_audit_events" in item for item in result.precondition_failures)


def test_exact_six_field_match_is_deterministic_pass():
    expected = [audit_event()]
    observed = [audit_event()]

    result = run_audit_hallucination_rate(
        precision_mode="BF16",
        n_samples=1,
        ground_truth_fixtures=expected,
        generated_audit_events=observed,
    )

    assert result.preconditions_met is True
    assert result.passed is True
    assert result.score == 1.0
    assert result.raw_scores == [1.0]
    assert "DETERMINISTIC FIELD COMPARISON" in result.notes


def test_two_field_mismatches_score_four_of_six_and_fail_target():
    expected = [audit_event()]
    observed = [audit_event(role="Sentinel", gate_result="FAIL")]

    result = run_audit_hallucination_rate(
        precision_mode="BF16",
        n_samples=1,
        ground_truth_fixtures=expected,
        generated_audit_events=observed,
    )

    assert result.preconditions_met is True
    assert result.score == pytest.approx(4 / 6)
    assert result.raw_scores[0] == pytest.approx(4 / 6)
    assert result.passed is False


def test_invalid_ground_truth_fails_closed_without_partial_score():
    expected_event = audit_event()
    del expected_event["session_id"]

    result = run_audit_hallucination_rate(
        precision_mode="BF16",
        n_samples=1,
        ground_truth_fixtures=[expected_event],
        generated_audit_events=[audit_event()],
    )

    assert result.preconditions_met is False
    assert result.passed is False
    assert result.score == 0.0
    assert result.raw_scores == []
    assert any("session_id" in item for item in result.precondition_failures)


def test_insufficient_pair_count_fails_closed():
    event = audit_event()

    result = run_audit_hallucination_rate(
        precision_mode="BF16",
        n_samples=2,
        ground_truth_fixtures=[event],
        generated_audit_events=[event],
    )

    assert result.preconditions_met is False
    assert result.passed is False
    assert result.sample_count == 0
    assert result.raw_scores == []


def test_legacy_herald_client_is_not_given_expected_answers():
    called = False

    def herald_client(_payload):
        nonlocal called
        called = True
        return audit_event()

    result = run_audit_hallucination_rate(
        precision_mode="BF16",
        n_samples=1,
        ground_truth_fixtures=[audit_event()],
        herald_client=herald_client,
    )

    assert called is False
    assert result.preconditions_met is False
    assert result.passed is False
    assert any("not invoked by design" in item for item in result.precondition_failures)


def test_nvfp4_policy_blocks_even_perfect_pairs():
    event = audit_event()

    result = run_audit_hallucination_rate(
        precision_mode="NVFP4",
        n_samples=1,
        ground_truth_fixtures=[event],
        generated_audit_events=[event],
    )

    assert result.preconditions_met is False
    assert result.passed is False
    assert result.score == 0.0
