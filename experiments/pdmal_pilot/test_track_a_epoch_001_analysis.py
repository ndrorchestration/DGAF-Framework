from copy import deepcopy

import pytest

from experiments.pdmal_pilot.track_a_epoch_001_analysis import (
    ALGORITHM_ID,
    FAILURE_COUNTS,
    SEEDS,
    TOPOLOGIES,
    analyze,
    paired_seed_effects,
    primary_estimate,
)


def _records(pdmal=True, random_regular=False, other=False):
    out = []
    for seed in SEEDS:
        for topology in TOPOLOGIES:
            for failure_count in FAILURE_COUNTS:
                if topology == "pdmal":
                    success = pdmal
                elif topology == "random_regular":
                    success = random_regular
                else:
                    success = other
                out.append(
                    {
                        "seed_id": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "ffcr_success": success,
                        "excluded": False,
                        "algorithm_id": ALGORITHM_ID,
                    }
                )
    return out


def test_positive_primary_contract_is_exact() -> None:
    result = analyze(_records(pdmal=True, random_regular=False))
    assert result["paired_seed_count"] == 50
    assert result["estimate_pdmal_minus_random_regular"] == 1.0
    assert result["two_sided_95pct_percentile_ci"] == [1.0, 1.0]
    assert result["classification"] == "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"


def test_negative_primary_contract_is_exact() -> None:
    result = analyze(_records(pdmal=False, random_regular=True))
    assert result["estimate_pdmal_minus_random_regular"] == -1.0
    assert result["two_sided_95pct_percentile_ci"] == [-1.0, -1.0]
    assert result["classification"] == "EVIDENCE_AGAINST_DIRECTIONAL_TRACK_A_HYPOTHESIS"


def test_other_topologies_cannot_change_primary_estimate() -> None:
    baseline = primary_estimate(paired_seed_effects(_records(pdmal=True, random_regular=False, other=False)))
    changed = primary_estimate(paired_seed_effects(_records(pdmal=True, random_regular=False, other=True)))
    assert baseline == changed == 1.0


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "malformed", "excluded", "wrong_algorithm", "extra"])
def test_matrix_or_endpoint_drift_fails_closed(mutation: str) -> None:
    records = _records()
    if mutation == "missing":
        records.pop()
    elif mutation == "duplicate":
        records[-1] = deepcopy(records[0])
    elif mutation == "malformed":
        records[0]["ffcr_success"] = "true"
    elif mutation == "excluded":
        records[0]["excluded"] = True
    elif mutation == "wrong_algorithm":
        records[0]["algorithm_id"] = "OTHER"
    elif mutation == "extra":
        records.append(
            {
                "seed_id": 999,
                "topology": "pdmal",
                "failure_count": 0,
                "ffcr_success": True,
                "excluded": False,
                "algorithm_id": ALGORITHM_ID,
            }
        )
    with pytest.raises(ValueError):
        paired_seed_effects(records)
