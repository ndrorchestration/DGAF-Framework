from governed_repo import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    PromotionReason,
    assess_promotion,
)


def _identity(**overrides):
    values = {
        "repository": "example/package-consumer",
        "change_id": "pr-1",
        "base_sha": "base",
        "head_sha": "head",
        "observed_base_sha": "base",
        "observed_head_sha": "head",
        "observed_at": "2026-10-01T16:30:00Z",
    }
    values.update(overrides)
    return ChangeIdentity(**values)


def _policy():
    return PromotionPolicy(
        required_gates=(
            GateRequirement(
                gate_id="ci",
                gate_class="quality",
                require_head_binding=True,
                require_base_binding=True,
            ),
        )
    )


def _gate(**overrides):
    values = {
        "gate_id": "ci",
        "status": "completed",
        "conclusion": "success",
        "observed_at": "2026-10-01T16:31:00Z",
        "head_sha": "head",
        "base_sha": "base",
    }
    values.update(overrides)
    return GateReceipt(**values)


def test_installed_api_positive_and_non_effects():
    receipt = assess_promotion(_identity(), _policy(), [_gate()])
    assert receipt.eligible is True
    assert receipt.reason_code is PromotionReason.ELIGIBLE_FOR_PROMOTION
    assert receipt.merge_executed is False
    assert receipt.mutation_executed is False
    assert receipt.authorization_effect == "NONE"


def test_installed_api_stale_base_denies():
    receipt = assess_promotion(
        _identity(observed_base_sha="new-base"),
        _policy(),
        [_gate()],
    )
    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.STALE_BASE


def test_installed_api_missing_check_denies():
    receipt = assess_promotion(_identity(), _policy(), [])
    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_MISSING


def test_installed_api_nonterminal_check_denies():
    receipt = assess_promotion(
        _identity(),
        _policy(),
        [_gate(status="in_progress", conclusion=None)],
    )
    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_NOT_TERMINAL


def test_installed_api_failed_check_denies():
    receipt = assess_promotion(
        _identity(),
        _policy(),
        [_gate(conclusion="failure")],
    )
    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_FAILED


def test_receipt_is_json_safe():
    receipt = assess_promotion(_identity(), _policy(), [_gate()])
    payload = receipt.to_dict()
    assert payload["reason_code"] == "ELIGIBLE_FOR_PROMOTION"
    assert payload["merge_executed"] is False
    assert payload["mutation_executed"] is False
    assert payload["authorization_effect"] == "NONE"
