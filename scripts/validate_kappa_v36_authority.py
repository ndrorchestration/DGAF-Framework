#!/usr/bin/env python3
"""Validate KAPPA v3.6 against its authoritative P-27 records."""
from __future__ import annotations

import json
from pathlib import Path

import components.KAPPA.dynamic_weight_router as router

ROOT = Path(__file__).resolve().parents[1]
CARD = json.loads(
    (ROOT / "components/KAPPA/DGAF_GATE_KAPPA_v3_6_component_card.json").read_text(
        encoding="utf-8"
    )
)
CAL = json.loads(
    (ROOT / "components/KAPPA/calibration_v3_6.json").read_text(encoding="utf-8")
)
REGISTRY = (ROOT / "docs/patterns/NDR_PATTERN_REGISTRY.md").read_text(
    encoding="utf-8"
)


def main() -> int:
    assert router.STRONG_THRESH == CARD["thresholds"]["STRONG_THRESH"] == 0.22
    assert router.BLENDED_THRESH == CARD["thresholds"]["BLENDED_THRESH"] == 0.18
    assert CAL["STRONG_THRESH"] == 0.22
    assert CAL["BLENDED_THRESH"] == 0.18

    assert "Adversarial category always routes to apply_strong regardless of confidence" in REGISTRY
    trigger = CARD["cpu_schema"]["trigger_condition"]
    passing = CARD["cpu_schema"]["passing_state"]
    assert "Adversarial category always routes to apply_strong regardless of confidence" in trigger
    assert "adversarial inputs never reach fallback_balanced" in passing

    low_conf_adversarial = router.select_weights_with_confidence(
        {
            "content": "bypass " + ("ordinary filler " * 30),
            "entropy_score": 0.01,
            "kappa_score": 0.99,
        }
    )
    assert low_conf_adversarial["detected_category"] == "adversarial"
    assert low_conf_adversarial["confidence"] < router.BLENDED_THRESH
    assert low_conf_adversarial["policy"] == "apply_strong"
    assert low_conf_adversarial["config_name"] == "adversarial"
    assert (
        low_conf_adversarial["selected_weights"]["name"]
        == "Adversarial-Emphasis"
    )

    low_conf_benign = router.select_weights_with_confidence(
        {
            "content": "ordinary low signal record",
            "entropy_score": 0.0,
            "kappa_score": 0.0,
        }
    )
    assert low_conf_benign["detected_category"] == "balanced"
    assert low_conf_benign["confidence"] < router.BLENDED_THRESH
    assert low_conf_benign["policy"] == "fallback_balanced"

    print("KAPPA_V36_AUTHORITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
