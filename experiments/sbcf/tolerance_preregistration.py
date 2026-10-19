"""Prospective one-sided distribution-free calibration sample-size contract.

Mathematics is conditional on independent, identically distributed positive-control
observations from a stable target population. No such assumptions are established
merely by constructing or validating this candidate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction

from scripts.dgaf_capability_canonicalize import sha256_digest

_EFFECT_DIGEST = "sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff"
_CUSTODY_DIGEST = "sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5"
_OBSERVATION_DIGEST = "sha256:d01d33de9f14d9bdace222528325d5766f5422088c8a4fa4c109adc1465e55cf"
_RECEIVER_DIGEST = "sha256:3d05f5c94a0aca51fd8b80fe20e4acb84330e649b5e7a1251064fd9721aa0cd5"
_MAX_SAMPLES = 100_000
_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "parent_digests",
        "target",
        "method",
        "sampling_assumptions",
        "sample_plan",
        "separation",
    }
)
_REQUIRED_PARENTS = frozenset({"effect_contract", "receiver_custody", "negative_observation", "calibration_receiver"})
_REQUIRED_TARGET = frozenset({"status", "coverage_p", "confidence_gamma", "scientific_rationale"})
_REQUIRED_METHOD = frozenset({"family", "statistic", "sample_size_rule", "source", "outcomes_used_to_select_targets"})
_REQUIRED_ASSUMPTIONS = frozenset(
    {
        "status",
        "sampling_design_id",
        "independent_samples_required",
        "identically_distributed_required",
        "stable_runtime_and_receiver_required",
        "censoring_and_timeouts_accounted_for",
        "receiver_monotonic_clock_required",
        "same_predeclared_protocol_required",
    }
)
_REQUIRED_PLAN = frozenset(
    {
        "samples_per_system",
        "equal_counts_across_systems",
        "maximum_allowed_samples",
        "preregister_before_positive_controls",
    }
)
_REQUIRED_SEPARATION = frozenset(
    {
        "no_empirical_samples_collected",
        "external_custody_not_implied",
        "statistical_result_not_efficacy",
        "structural_ready_not_run_authorization",
        "analysis_authorization_separate",
    }
)


@dataclass(frozen=True)
class TolerancePreregReadiness:
    ready: bool
    blockers: tuple[str, ...]


def _probability(value: object, label: str) -> Fraction:
    # Strings retain exact decimal intent; floats and bools are prohibited.
    if type(value) is not str or re.fullmatch(r"0\.[0-9]{1,6}", value) is None:
        raise ValueError(f"{label} must be an exact decimal string in (0, 1)")
    probability = Fraction(Decimal(value))
    if not 0 < probability < 1:
        raise ValueError(f"{label} must be strictly between 0 and 1")
    return probability


def _positive_integer(value: object, label: str) -> int:
    if type(value) is not int or not 1 <= value <= _MAX_SAMPLES:
        raise ValueError(f"{label} must be integer between 1 and {_MAX_SAMPLES}")
    return value


def minimum_positive_control_samples(coverage_p: str, confidence_gamma: str) -> int:
    """Minimum n such that 1 - p**n >= gamma, compared with exact rationals.

    Conditional distribution-free one-sided maximum tolerance-limit relation
    under IID sampling. It is not a false-negative guarantee and does not prove
    independence, stationarity, or representative sampling.
    """
    coverage = _probability(coverage_p, "coverage")
    confidence = _probability(confidence_gamma, "confidence")
    miss_probability = 1 - confidence
    if coverage**_MAX_SAMPLES > miss_probability:
        raise ValueError("required calibration samples exceed bounded implementation cap")
    lo, hi = 1, _MAX_SAMPLES
    while lo < hi:
        middle = (lo + hi) // 2
        if coverage**middle <= miss_probability:
            hi = middle
        else:
            lo = middle + 1
    return lo


def validate_tolerance_preregistration(contract: dict) -> None:
    if type(contract) is not dict or set(contract) != _REQUIRED_TOP:
        raise ValueError("invalid tolerance preregistration schema")
    if contract["schema_version"] != "sbcf-tolerance-prereg-v0":
        raise ValueError("unsupported tolerance preregistration version")
    if contract["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid tolerance preregistration status")
    parents = contract["parent_digests"]
    if type(parents) is not dict or set(parents) != _REQUIRED_PARENTS:
        raise ValueError("invalid parent digest schema")
    for name, digest in (
        ("effect_contract", _EFFECT_DIGEST),
        ("receiver_custody", _CUSTODY_DIGEST),
        ("negative_observation", _OBSERVATION_DIGEST),
        ("calibration_receiver", _RECEIVER_DIGEST),
    ):
        if parents[name] != digest:
            raise ValueError(f"wrong exact parent digest: {name}")

    target = contract["target"]
    if type(target) is not dict or set(target) != _REQUIRED_TARGET:
        raise ValueError("invalid tolerance target schema")
    if target["status"] not in {"UNSELECTED", "PROSPECTIVELY_SELECTED"}:
        raise ValueError("invalid target selection status")
    if target["status"] == "UNSELECTED":
        if any(target[name] is not None for name in ("coverage_p", "confidence_gamma", "scientific_rationale")):
            raise ValueError("unselected targets cannot contain values")
    else:
        _probability(target["coverage_p"], "coverage")
        _probability(target["confidence_gamma"], "confidence")
        rationale = target["scientific_rationale"]
        if type(rationale) is not str or not rationale.strip():
            raise ValueError("selected targets require a prospective scientific rationale")

    method = contract["method"]
    if type(method) is not dict or set(method) != _REQUIRED_METHOD:
        raise ValueError("invalid tolerance method schema")
    expected = {
        "family": "DISTRIBUTION_FREE_ONE_SIDED_UPPER_TOLERANCE",
        "statistic": "SAMPLE_MAXIMUM",
        "sample_size_rule": "1-p^n>=gamma",
        "source": "POSITIVE_CONTROLS_ONLY",
        "outcomes_used_to_select_targets": False,
    }
    if method != expected or method["outcomes_used_to_select_targets"] is not False:
        raise ValueError("tolerance method or outcome firewall changed")

    assumptions = contract["sampling_assumptions"]
    if type(assumptions) is not dict or set(assumptions) != _REQUIRED_ASSUMPTIONS:
        raise ValueError("invalid sampling assumptions schema")
    if assumptions["status"] not in {"UNASSESSED", "DOCUMENTED_UNVERIFIED"}:
        raise ValueError("invalid sampling assumption status")
    sampling_design = assumptions["sampling_design_id"]
    if assumptions["status"] == "UNASSESSED" and sampling_design is not None:
        raise ValueError("unassessed sampling design cannot contain an id")
    if assumptions["status"] == "DOCUMENTED_UNVERIFIED" and (
        type(sampling_design) is not str or not sampling_design.strip()
    ):
        raise ValueError("documented sampling assumptions require design identity")
    for field in (
        "independent_samples_required",
        "identically_distributed_required",
        "stable_runtime_and_receiver_required",
        "censoring_and_timeouts_accounted_for",
        "receiver_monotonic_clock_required",
        "same_predeclared_protocol_required",
    ):
        if assumptions[field] is not True:
            raise ValueError(f"sampling safeguard weakened: {field}")

    plan = contract["sample_plan"]
    if type(plan) is not dict or set(plan) != _REQUIRED_PLAN:
        raise ValueError("invalid sample plan schema")
    for field in ("samples_per_system", "maximum_allowed_samples"):
        if plan[field] is not None:
            _positive_integer(plan[field], field)
    if plan["equal_counts_across_systems"] is not True:
        raise ValueError("equal calibration counts required")
    if plan["preregister_before_positive_controls"] is not True:
        raise ValueError("calibration must be preregistered")

    separation = contract["separation"]
    if type(separation) is not dict or set(separation) != _REQUIRED_SEPARATION:
        raise ValueError("invalid tolerance separation schema")
    if any(value is not True for value in separation.values()):
        raise ValueError("tolerance separation cannot be weakened")

    if contract["status"] == "FROZEN":
        if target["status"] != "PROSPECTIVELY_SELECTED":
            raise ValueError("frozen tolerance preregistration requires selected targets")
        if assumptions["status"] != "DOCUMENTED_UNVERIFIED":
            raise ValueError("frozen tolerance preregistration requires documented sampling design")
        count = plan["samples_per_system"]
        limit = plan["maximum_allowed_samples"]
        if count is None or limit is None:
            raise ValueError("frozen tolerance preregistration requires sample count and budget")
        required = minimum_positive_control_samples(target["coverage_p"], target["confidence_gamma"])
        if count < required:
            raise ValueError("planned sample count below exact tolerance requirement")
        if limit < count:
            raise ValueError("sample budget below preregistered count")


def evaluate_tolerance_preregistration(contract: dict) -> TolerancePreregReadiness:
    validate_tolerance_preregistration(contract)
    blockers: list[str] = []
    if contract["status"] != "FROZEN":
        blockers.append("tolerance_preregistration_not_frozen")
    if contract["target"]["status"] != "PROSPECTIVELY_SELECTED":
        blockers.append("coverage_confidence_target_unselected")
    if contract["sampling_assumptions"]["status"] != "DOCUMENTED_UNVERIFIED":
        blockers.append("sampling_design_unassessed")
    if contract["sample_plan"]["samples_per_system"] is None:
        blockers.append("sample_count_unset")
    if contract["sample_plan"]["maximum_allowed_samples"] is None:
        blockers.append("sample_budget_unset")
    return TolerancePreregReadiness(not blockers, tuple(sorted(blockers)))


def tolerance_preregistration_digest(contract: dict) -> str:
    validate_tolerance_preregistration(contract)
    return sha256_digest(contract)
