from __future__ import annotations

import pytest

from analysis import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    SeedEffect,
    analysis_config_sha256,
    condition_ffcr,
    decision,
    paired_bootstrap_ci,
    primary_estimate,
)

TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURES = (0, 1, 2, 3, 4, 5, 6, 8, 10)
BLIND_DGAF = "blind_dgaf"
BLIND_NULL = "blind_null"


def _records(blind_id: str, success: bool = True) -> list[dict]:
    return [
        {
            "blinded_condition_id": blind_id,
            "topology": topology,
            "failure_count": failure_count,
            "ffcr_success": success,
        }
        for topology in TOPOLOGIES
        for failure_count in FAILURES
    ]


def _map() -> dict[str, str]:
    return {
        "blind_dgaf": "dgaf",
        "blind_null": "null",
        "blind_simple": "simple",
        "blind_static": "static",
    }


def test_condition_ffcr_requires_complete_matrix() -> None:
    records = _records(BLIND_DGAF)
    records.extend(_records("blind_simple"))
    records.extend(_records("blind_null"))
    records.extend(_records("blind_static"))
    assert condition_ffcr(records, "dgaf", condition_map=_map()) == 1.0
    with pytest.raises(ValueError, match="incomplete condition matrix"):
        condition_ffcr(records[:-1], "static", condition_map=_map())


def test_condition_ffcr_rejects_duplicate_or_malformed_cells() -> None:
    records = _records(BLIND_NULL)
    records.append(records[0])
    records.extend(_records("blind_dgaf"))
    records.extend(_records("blind_simple"))
    records.extend(_records("blind_static"))
    with pytest.raises(ValueError, match="invalid or duplicate"):
        condition_ffcr(records, "null", condition_map=_map())

    malformed = _records(BLIND_NULL)
    malformed.extend(_records("blind_dgaf"))
    malformed.extend(_records("blind_simple"))
    malformed.extend(_records("blind_static"))
    malformed[0]["ffcr_success"] = "true"
    with pytest.raises(ValueError, match="boolean ffcr_success"):
        condition_ffcr(malformed, "null", condition_map=_map())


def test_condition_ffcr_requires_bijective_unblinding_map() -> None:
    records = _records(BLIND_DGAF)
    with pytest.raises(ValueError, match="bijectively"):
        condition_ffcr(records, "dgaf", condition_map={"blind_dgaf": "dgaf"})


def test_condition_ffcr_requires_explicit_unblinding_map() -> None:
    records = _records(BLIND_DGAF)
    with pytest.raises(ValueError, match="four canonical conditions"):
        condition_ffcr(records, "dgaf", condition_map={})


def test_primary_estimate_is_equal_weighted_over_seeds() -> None:
    effects = [SeedEffect(1, 1.0, 0.0), SeedEffect(2, 0.5, 0.0)]
    assert primary_estimate(effects) == pytest.approx(0.75)


def test_primary_estimate_rejects_duplicate_or_nonfinite_seeds() -> None:
    with pytest.raises(ValueError, match="unique seed identifiers"):
        primary_estimate([SeedEffect(1, 1.0, 0.0), SeedEffect(1, 0.5, 0.0)])
    with pytest.raises(ValueError, match="finite"):
        primary_estimate([SeedEffect(1, float("nan"), 0.0)])


def test_paired_bootstrap_is_deterministic() -> None:
    effects = [SeedEffect(i, 0.5 + i / 100, 0.25) for i in range(1, 11)]
    ci_a = paired_bootstrap_ci(effects, resamples=1000, seed=BOOTSTRAP_SEED)
    ci_b = paired_bootstrap_ci(effects, resamples=1000, seed=BOOTSTRAP_SEED)
    assert ci_a == ci_b


def test_paired_bootstrap_rejects_invalid_parameters() -> None:
    effects = [SeedEffect(1, 0.5, 0.25)]
    with pytest.raises(ValueError):
        paired_bootstrap_ci(effects, resamples=True)
    with pytest.raises(ValueError):
        paired_bootstrap_ci(effects, seed=True)
    with pytest.raises(ValueError):
        paired_bootstrap_ci(effects, alpha=float("nan"))


def test_decision_requires_positive_estimate_and_positive_ci() -> None:
    effects = [SeedEffect(1, 0.8, 0.2), SeedEffect(2, 0.7, 0.1)]
    assert decision(effects, (0.3, 0.6)) == "SUPPORTS_DIRECTIONAL_DGAF"
    assert decision(effects, (-0.1, 0.6)) == "NOT_SUPPORTED_OR_INCONCLUSIVE"


def test_decision_rejects_invalid_ci():
    effects = [SeedEffect(1, 0.8, 0.2)]
    with pytest.raises(ValueError):
        decision(effects, (0.6, 0.3))
    with pytest.raises(ValueError):
        decision(effects, [0.1, 0.2])  # type: ignore[arg-type]


def test_analysis_configuration_is_hashed() -> None:
    assert BOOTSTRAP_RESAMPLES == 10_000
    assert len(analysis_config_sha256()) == 64
