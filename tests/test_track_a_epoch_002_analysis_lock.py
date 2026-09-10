from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

from scripts import validate_track_a_epoch_002_analysis_lock as validator

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
PROTOCOL_PATH = ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
ANALYSIS_PATH = ROOT / "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"


def load_analysis():
    name = "track_a_epoch_002_analysis_test"
    spec = importlib.util.spec_from_file_location(name, ANALYSIS_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def records():
    return [
        {
            "seed_id": seed,
            "topology": topology,
            "failure_count": failure_count,
            "ffcr_success": topology == "pdmal",
            "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
        }
        for seed in range(20270201, 20270251)
        for topology in ("ring", "pdmal", "random_regular", "small_world", "complete")
        for failure_count in (0, 1, 2, 3, 4, 5, 6, 8, 10)
    ]


def load_records():
    return (
        json.loads(LOCK_PATH.read_text(encoding="utf-8")),
        json.loads(PROTOCOL_PATH.read_text(encoding="utf-8")),
        load_analysis(),
    )


def test_validator_accepts_exact_successor_lock():
    lock, protocol, analysis = load_records()
    validator.validate_records(lock, protocol, analysis)


def test_analysis_uses_exact_successor_identity_and_method():
    analysis = load_analysis()
    result = analysis.analyze(records())
    assert result["protocol_id"] == "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
    assert result["paired_seed_count"] == 50
    assert result["bootstrap_resamples"] == 10_000
    assert result["bootstrap_seed"] == 20270251
    assert result["classification"] == "SUPPORTS_DIRECTIONAL_TRACK_A_HYPOTHESIS"
    assert result["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert result["high_assurance"] == "NOT_AUTHORIZED_N0"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("successor_custody_recovery_receipt_established", True),
        ("exact_candidate_freeze_established", True),
        ("collection_authorized", True),
        ("unblinding_authorized", True),
        ("primary_analysis_authorized", True),
        ("empirical_execution_authorized", True),
        ("scientific_n_increment", 1),
        ("canonical_dgaf_efficacy", "ESTABLISHED"),
        ("high_assurance", "AUTHORIZED"),
    ],
)
def test_lock_fails_closed_on_scientific_state_promotion(field, value):
    lock, protocol, analysis = load_records()
    mutated = copy.deepcopy(lock)
    mutated["boundaries"][field] = value
    with pytest.raises(AssertionError):
        validator.validate_records(mutated, protocol, analysis)


def test_lock_fails_closed_on_wrong_protocol_identity():
    lock, protocol, analysis = load_records()
    mutated = copy.deepcopy(lock)
    mutated["protocol_id"] = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
    with pytest.raises(AssertionError):
        validator.validate_records(mutated, protocol, analysis)


def test_lock_fails_closed_on_bootstrap_seed_drift():
    lock, protocol, analysis = load_records()
    mutated = copy.deepcopy(lock)
    mutated["primary_contract"]["bootstrap_seed"] = 20270151
    with pytest.raises(AssertionError):
        validator.validate_records(mutated, protocol, analysis)


def test_protocol_fails_closed_on_epoch_001_outcome_use():
    lock, protocol, analysis = load_records()
    mutated = copy.deepcopy(protocol)
    mutated["epoch_001_outcomes_used_for_successor_design"] = True
    with pytest.raises(AssertionError):
        validator.validate_records(lock, mutated, analysis)


def test_protocol_fails_closed_if_custody_gate_is_relaxed():
    lock, protocol, analysis = load_records()
    mutated = copy.deepcopy(protocol)
    mutated["next_gates"]["successor_solo_custody_recovery_receipt"] = "OPTIONAL"
    with pytest.raises(AssertionError):
        validator.validate_records(lock, mutated, analysis)


def test_analysis_rejects_epoch_001_seed_panel():
    analysis = load_analysis()
    bad = records()
    bad[0] = dict(bad[0], seed_id=20270101)
    with pytest.raises(ValueError, match="unexpected matrix cell"):
        analysis.analyze(bad)


def test_analysis_rejects_outcome_exclusion():
    analysis = load_analysis()
    bad = records()
    bad[0] = dict(bad[0], excluded=True)
    with pytest.raises(ValueError, match="outcome exclusions are prohibited"):
        analysis.analyze(bad)
