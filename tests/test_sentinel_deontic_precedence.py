from components.evaluate_router_v1_1 import RISK_BLOCK, RISK_WARN, sentinel_review


def test_forbidden_deontic_state_precedes_low_confidence_warn() -> None:
    record = {
        "id": "forbidden-low-confidence",
        "category": "adversarial",
        "confidence": 0.05,
        "content": "adversarial test record",
    }
    routing = {
        "category": "adversarial",
        "policy": "apply_strong",
        "confidence": 0.05,
    }
    result = sentinel_review(record, routing, "after_category_detection")
    assert result["deontic_gate"]["gate"] == "forbidden"
    assert result["risk"] == RISK_BLOCK


def test_benign_low_confidence_still_warns() -> None:
    record = {
        "id": "benign-low-confidence",
        "category": "balanced",
        "confidence": 0.15,
        "content": "ordinary record",
    }
    routing = {
        "category": "balanced",
        "policy": "fallback_balanced",
        "confidence": 0.15,
    }
    result = sentinel_review(record, routing, "after_category_detection")
    assert result["deontic_gate"]["gate"] == "permitted"
    assert result["risk"] == RISK_WARN


def test_adversarial_non_strong_policy_remains_hard_block() -> None:
    record = {
        "id": "adversarial-nonstrong",
        "category": "adversarial",
        "confidence": 0.8,
        "content": "adversarial test record",
    }
    routing = {
        "category": "adversarial",
        "policy": "fallback_balanced",
        "confidence": 0.8,
    }
    result = sentinel_review(record, routing, "after_category_detection")
    assert result["risk"] == RISK_BLOCK
