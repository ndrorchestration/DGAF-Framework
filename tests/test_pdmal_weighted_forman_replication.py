import math
from statistics import pvariance

from experiments.pdmal_weighted_forman_replication import (
    CALIBRATION_REPLICATES,
    EDGES,
    HEALTHY_CURVATURE,
    HELDOUT_REPLICATES,
    TARGET_EDGE_WEIGHTS,
    anomaly_scores,
    detect,
    run_experiment,
    selection_seed,
    validate_result,
    weighted_forman_ricci,
)


def baseline_weights():
    return {edge: 1.0 for edge in EDGES}


def test_weighted_formula_reduces_to_unweighted_minus_two():
    curvature = weighted_forman_ricci(baseline_weights())
    assert len(curvature) == 30
    assert set(curvature.values()) == {HEALTHY_CURVATURE}


def test_known_three_edge_weight_point_three_case_restores_variance():
    weights = baseline_weights()
    perturbed = {(3, 4), (5, 6), (5, 15)}
    for edge in perturbed:
        weights[edge] = 0.3
    curvature = weighted_forman_ricci(weights)
    assert math.isclose(
        pvariance(curvature.values()),
        0.5799847018687604,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_perturbation_targets_span_both_directions_without_invalid_weights():
    assert all(weight > 0 for weight in TARGET_EDGE_WEIGHTS)
    assert any(weight < 1 for weight in TARGET_EDGE_WEIGHTS)
    assert any(weight > 1 for weight in TARGET_EDGE_WEIGHTS)


def test_calibration_and_heldout_replicates_are_disjoint():
    assert set(CALIBRATION_REPLICATES).isdisjoint(HELDOUT_REPLICATES)
    assert len(CALIBRATION_REPLICATES) == len(HELDOUT_REPLICATES) == 10


def test_selection_seed_is_deterministic_and_cell_specific():
    first = selection_seed(3, 0.3, 4)
    assert first == selection_seed(3, 0.3, 4)
    assert first != selection_seed(3, 0.3, 5)
    assert first != selection_seed(5, 0.3, 4)
    assert first != selection_seed(3, 0.5, 4)


def test_rank_top_k_is_an_oracle_size_comparator_only():
    weights = baseline_weights()
    for edge in EDGES[:3]:
        weights[edge] = 0.3
    curvature = weighted_forman_ricci(weights)
    predicted = detect(curvature, 3, "rank_top_k_oracle")
    assert len(predicted) == 3


def test_anomaly_score_is_absolute_deviation_from_healthy_curvature():
    weights = baseline_weights()
    weights[EDGES[0]] = 0.3
    curvature = weighted_forman_ricci(weights)
    scores = anomaly_scores(curvature)
    assert all(score >= 0 for score in scores.values())
    assert any(score > 0 for score in scores.values())


def test_full_preregistered_matrix_is_deterministic_and_fail_closed():
    result_a = run_experiment()
    result_b = run_experiment()
    validate_result(result_a)
    validate_result(result_b)
    assert result_a == result_b
    assert result_a["protocol"]["total_trials"] == 480
    assert result_a["variance_restoration"]["total_trials"] == 480
    assert result_a["epistemic_classification"]["general_reliability"] == "NOT_ESTABLISHED"
    assert result_a["epistemic_classification"]["track_a_state_effect"] == "NONE"
