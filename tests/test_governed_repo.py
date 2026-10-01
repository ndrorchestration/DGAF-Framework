from components.governed_repo import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    PromotionReason,
    UpstreamDecision,
    assess_promotion,
)


def identity(**overrides):
    values = {
        "repository": "example/repo",
        "change_id": "pr-42",
        "base_sha": "base123",
        "head_sha": "head456",
        "observed_base_sha": "base123",
        "observed_head_sha": "head456",
        "observed_at": "2026-10-01T14:00:00Z",
    }
    values.update(overrides)
    return ChangeIdentity(**values)


def success_gate(gate_id="ci", **overrides):
    values = {
        "gate_id": gate_id,
        "status": "completed",
        "conclusion": "success",
        "observed_at": "2026-10-01T14:01:00Z",
        "head_sha": "head456",
        "base_sha": "base123",
    }
    values.update(overrides)
    return GateReceipt(**values)


def policy(**overrides):
    values = {
        "required_gates": (
            GateRequirement(
                gate_id="ci",
                gate_class="quality",
                require_head_binding=True,
                require_base_binding=True,
            ),
        )
    }
    values.update(overrides)
    return PromotionPolicy(**values)


def test_exact_green_change_is_eligible_but_non_mutating():
    receipt = assess_promotion(identity(), policy(), [success_gate()])

    assert receipt.eligible is True
    assert receipt.reason_code is PromotionReason.ELIGIBLE_FOR_PROMOTION
    assert receipt.merge_executed is False
    assert receipt.mutation_executed is False
    assert receipt.authorization_effect == "NONE"


def test_stale_base_fails_closed_before_gate_evaluation():
    receipt = assess_promotion(
        identity(observed_base_sha="newbase999"),
        policy(),
        [success_gate()],
    )

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.STALE_BASE
    assert receipt.checked_gate_ids == ()


def test_missing_required_check_denies():
    receipt = assess_promotion(identity(), policy(), [])

    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_MISSING
    assert receipt.missing_gate_ids == ("ci",)


def test_nonterminal_required_check_is_not_a_pass():
    receipt = assess_promotion(
        identity(),
        policy(),
        [success_gate(status="in_progress", conclusion=None)],
    )

    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_NOT_TERMINAL
    assert receipt.nonterminal_gate_ids == ("ci",)


def test_failed_required_check_denies():
    receipt = assess_promotion(
        identity(),
        policy(),
        [success_gate(conclusion="failure")],
    )

    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_FAILED
    assert receipt.failed_gate_ids == ("ci",)


def test_gate_bound_to_other_head_denies():
    receipt = assess_promotion(
        identity(),
        policy(),
        [success_gate(head_sha="otherhead")],
    )

    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_FAILED


def test_upstream_evidence_receipt_can_be_required():
    p = policy(require_evidence_acceptance=True)
    evidence = UpstreamDecision(
        decision_class="evidence",
        accepted=False,
        reason_code="DIGEST_MISMATCH",
        receipt_id="evidence-1",
    )

    receipt = assess_promotion(identity(), p, [success_gate()], evidence=evidence)

    assert receipt.reason_code is PromotionReason.EVIDENCE_INSUFFICIENT
    assert receipt.upstream_receipt_ids == ("evidence-1",)


def test_hold_and_lifecycle_blocks_are_explicit():
    hold_receipt = assess_promotion(identity(), policy(hold=True), [success_gate()])
    lifecycle_receipt = assess_promotion(
        identity(),
        policy(lifecycle_blocked=True),
        [success_gate()],
    )

    assert hold_receipt.reason_code is PromotionReason.HOLD
    assert lifecycle_receipt.reason_code is PromotionReason.LIFECYCLE_BLOCKED


def test_receipt_serialization_preserves_non_effects():
    receipt = assess_promotion(identity(), policy(), [success_gate()])
    payload = receipt.to_dict()

    assert payload["reason_code"] == "ELIGIBLE_FOR_PROMOTION"
    assert payload["merge_executed"] is False
    assert payload["mutation_executed"] is False
    assert payload["authorization_effect"] == "NONE"
