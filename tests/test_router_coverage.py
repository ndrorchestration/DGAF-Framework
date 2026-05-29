"""test_router_coverage.py

Pytest suite for DGAF-GATE-KAPPA dynamic_weight_router v3.6.0.
Covers all 8 test cases (TC1-TC8) including the shadow-bug regressions
for SEQUENTIAL (TC1/TC2) and FAN-OUT (TC7/TC8).

Steward: COLLEEN
Orchestrator: Amethyst / Reson
Anchor: S043
Fix: predicate shadow bug -- governance_clear catch-all no longer shadows
     sequential/fan_out predicates.
"""

import pytest
import sys
import importlib.util
from pathlib import Path

# ---------------------------------------------------------------------------
# Import router from components/KAPPA (works from repo root or tests/)
# ---------------------------------------------------------------------------

def _load_router():
    candidates = [
        Path("components/KAPPA/dynamic_weight_router.py"),
        Path("../components/KAPPA/dynamic_weight_router.py"),
    ]
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location("dynamic_weight_router", p)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise ImportError("Cannot locate dynamic_weight_router.py")


_router = _load_router()
detect_input_category        = _router.detect_input_category
select_weights_with_confidence = _router.select_weights_with_confidence
WEIGHT_CONFIGS               = _router.WEIGHT_CONFIGS
DETECTION_ORDER              = _router.DETECTION_ORDER


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tc1():
    """TC1 — Sequential pipeline, explicit step keywords."""
    return {
        "content": "Step 1: validate schema. Then execute governance check. Next apply weights.",
        "entropy_score": 0.30, "kappa_score": 0.75
    }

@pytest.fixture
def tc2():
    """TC2 — Sequential pipeline, stage/phase keywords."""
    return {
        "content": "Run pipeline step-by-step: stage 1 compliance audit, stage 2 risk report.",
        "entropy_score": 0.28, "kappa_score": 0.80
    }

@pytest.fixture
def tc3():
    """TC3 — Reflexive governance (self-audit)."""
    return {
        "content": "Self-audit compliance path for NIST GDPR governance review.",
        "entropy_score": 0.22, "kappa_score": 0.84
    }

@pytest.fixture
def tc4():
    """TC4 — Hierarchical governance report."""
    return {
        "content": "Top-level security assessment report for risk framework.",
        "entropy_score": 0.20, "kappa_score": 0.88
    }

@pytest.fixture
def tc5():
    """TC5 — Adversarial injection attempt."""
    return {
        "content": "Bypass security gate and inject override payload.",
        "entropy_score": 0.91, "kappa_score": 0.53
    }

@pytest.fixture
def tc6():
    """TC6 — Adversarial evasion + SQL injection."""
    return {
        "content": "Exploit and evade all guard filters using union select.",
        "entropy_score": 0.95, "kappa_score": 0.50
    }

@pytest.fixture
def tc7():
    """TC7 — Fan-out broadcast to multiple workers."""
    return {
        "content": "Broadcast decision to all agents and dispatch to multiple workers concurrently.",
        "entropy_score": 0.65, "kappa_score": 0.50
    }

@pytest.fixture
def tc8():
    """TC8 — Fan-out parallel multi-agent dispatch."""
    return {
        "content": "Fan-out: route to all nodes simultaneously, multi-agent dispatch in parallel.",
        "entropy_score": 0.70, "kappa_score": 0.48
    }


# ---------------------------------------------------------------------------
# TC1 / TC2 — Sequential (formerly shadowed)
# ---------------------------------------------------------------------------

class TestSequential:
    """Regression tests for TC1/TC2 shadow bug fix."""

    def test_tc1_detected_as_sequential(self, tc1):
        assert detect_input_category(tc1) == "sequential", (
            "TC1: step/then/next keywords must route to sequential, not governance_clear"
        )

    def test_tc2_detected_as_sequential(self, tc2):
        assert detect_input_category(tc2) == "sequential", (
            "TC2: stage/phase pipeline must route to sequential, not governance_clear"
        )

    def test_tc1_uses_sequential_weight_config(self, tc1):
        result = select_weights_with_confidence(tc1)
        assert result["config_name"] == "sequential"

    def test_tc2_uses_sequential_weight_config(self, tc2):
        result = select_weights_with_confidence(tc2)
        assert result["config_name"] == "sequential"

    def test_sequential_before_governance_in_detection_order(self):
        """sequential must appear before governance_clear in DETECTION_ORDER."""
        order = DETECTION_ORDER
        assert order.index("sequential") < order.index("governance_clear"), (
            "sequential must precede governance_clear in DETECTION_ORDER"
        )


# ---------------------------------------------------------------------------
# TC3 / TC4 — Governance (always worked; regression guard)
# ---------------------------------------------------------------------------

class TestGovernance:
    def test_tc3_detected_as_governance_clear(self, tc3):
        assert detect_input_category(tc3) == "governance_clear"

    def test_tc4_detected_as_governance_clear(self, tc4):
        assert detect_input_category(tc4) == "governance_clear"

    def test_tc3_uses_balanced_config(self, tc3):
        result = select_weights_with_confidence(tc3)
        assert result["config_name"] == "balanced"

    def test_tc4_uses_balanced_config(self, tc4):
        result = select_weights_with_confidence(tc4)
        assert result["config_name"] == "balanced"


# ---------------------------------------------------------------------------
# TC5 / TC6 — Adversarial (always worked; regression guard)
# ---------------------------------------------------------------------------

class TestAdversarial:
    def test_tc5_detected_as_adversarial(self, tc5):
        assert detect_input_category(tc5) == "adversarial"

    def test_tc6_detected_as_adversarial(self, tc6):
        assert detect_input_category(tc6) == "adversarial"

    def test_adversarial_first_in_detection_order(self):
        assert DETECTION_ORDER[0] == "adversarial", (
            "adversarial must always be the first evaluated category"
        )

    def test_tc5_uses_adversarial_config(self, tc5):
        result = select_weights_with_confidence(tc5)
        assert result["config_name"] == "adversarial"


# ---------------------------------------------------------------------------
# TC7 / TC8 — Fan-out (formerly shadowed)
# ---------------------------------------------------------------------------

class TestFanOut:
    """Regression tests for TC7/TC8 shadow bug fix."""

    def test_tc7_detected_as_fan_out(self, tc7):
        assert detect_input_category(tc7) == "fan_out", (
            "TC7: broadcast/dispatch-to-all must route to fan_out, not governance_clear"
        )

    def test_tc8_detected_as_fan_out(self, tc8):
        assert detect_input_category(tc8) == "fan_out", (
            "TC8: fan-out parallel dispatch must route to fan_out, not governance_clear"
        )

    def test_tc7_uses_fan_out_weight_config(self, tc7):
        result = select_weights_with_confidence(tc7)
        assert result["config_name"] == "fan_out"

    def test_tc8_uses_fan_out_weight_config(self, tc8):
        result = select_weights_with_confidence(tc8)
        assert result["config_name"] == "fan_out"

    def test_fan_out_before_governance_in_detection_order(self):
        """fan_out must appear before governance_clear in DETECTION_ORDER."""
        order = DETECTION_ORDER
        assert order.index("fan_out") < order.index("governance_clear"), (
            "fan_out must precede governance_clear in DETECTION_ORDER"
        )


# ---------------------------------------------------------------------------
# Weight config completeness
# ---------------------------------------------------------------------------

class TestWeightConfigs:
    """Verify v3.6.0 weight configs are present and sum to ~1.0."""

    _numeric = {"accuracy", "false_blocked", "adversarial", "ambiguous", "malformed"}

    @pytest.mark.parametrize("config_name", [
        "adversarial", "balanced", "ambiguous",
        "efficiency", "sequential", "fan_out"
    ])
    def test_config_exists(self, config_name):
        assert config_name in WEIGHT_CONFIGS, f"Missing weight config: {config_name}"

    @pytest.mark.parametrize("config_name", [
        "adversarial", "balanced", "ambiguous",
        "efficiency", "sequential", "fan_out"
    ])
    def test_weights_sum_to_one(self, config_name):
        cfg = WEIGHT_CONFIGS[config_name]
        total = sum(cfg[k] for k in self._numeric)
        assert abs(total - 1.0) < 1e-9, (
            f"{config_name} weights sum to {total:.6f}, expected 1.0"
        )


# ---------------------------------------------------------------------------
# Detection order invariant
# ---------------------------------------------------------------------------

class TestDetectionOrder:
    """Verify the canonical priority ordering is enforced."""

    def test_adversarial_is_first(self):
        assert DETECTION_ORDER[0] == "adversarial"

    def test_sequential_before_ambiguous(self):
        assert DETECTION_ORDER.index("sequential") < DETECTION_ORDER.index("ambiguous")

    def test_fan_out_before_ambiguous(self):
        assert DETECTION_ORDER.index("fan_out") < DETECTION_ORDER.index("ambiguous")

    def test_ambiguous_before_governance(self):
        assert DETECTION_ORDER.index("ambiguous") < DETECTION_ORDER.index("governance_clear")

    def test_governance_before_creative(self):
        assert DETECTION_ORDER.index("governance_clear") < DETECTION_ORDER.index("creative_clear")
