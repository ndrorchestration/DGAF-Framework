from __future__ import annotations

import json
from pathlib import Path

import components.KAPPA.dynamic_weight_router as router

ROOT = Path(__file__).resolve().parents[1]
CARD = json.loads((ROOT / "components/KAPPA/DGAF_GATE_KAPPA_v3_6_component_card.json").read_text())
CAL = json.loads((ROOT / "components/KAPPA/calibration_v3_6.json").read_text())


def test_v36_thresholds_match_authority_records() -> None:
    assert router.STRONG_THRESH == CARD["thresholds"]["STRONG_THRESH"] == CAL["STRONG_THRESH"] == 0.22
    assert router.BLENDED_THRESH == CARD["thresholds"]["BLENDED_THRESH"] == CAL["BLENDED_THRESH"] == 0.18


def test_v36_threshold_order_is_fail_safe() -> None:
    assert 0.0 < router.BLENDED_THRESH < router.STRONG_THRESH < 1.0


def test_fallback_balanced_remains_valid_safe_policy() -> None:
    result = router.select_weights_with_confidence({"content": "test"})
    assert result["policy"] == "fallback_balanced"
    assert result["config_name"] == "balanced"
    assert result["selected_weights"]["name"] == "Balanced"


def test_policy_boundaries_follow_v36_calibration(monkeypatch) -> None:
    monkeypatch.setattr(router, "detect_input_category", lambda _data: "balanced")
    monkeypatch.setattr(router, "compute_category_confidence", lambda _data, _cat: (0.17, {}))
    assert router.select_weights_with_confidence({"content": "x"})["policy"] == "fallback_balanced"

    monkeypatch.setattr(router, "compute_category_confidence", lambda _data, _cat: (0.20, {}))
    assert router.select_weights_with_confidence({"content": "x"})["policy"] == "apply_blended"

    monkeypatch.setattr(router, "compute_category_confidence", lambda _data, _cat: (0.22, {}))
    assert router.select_weights_with_confidence({"content": "x"})["policy"] == "apply_strong"
