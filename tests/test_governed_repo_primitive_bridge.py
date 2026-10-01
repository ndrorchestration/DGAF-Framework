import pytest

from components.governed_repo import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    PromotionReason,
    assess_promotion,
)
from components.governed_repo_primitive_bridge import (
    ACTION_ADMISSION_SCHEMA_VERSION,
    CLAIMGRAPH_RECEIPT_SCHEMA_VERSION,
    EVIDENCE_GATE_SCHEMA_VERSION,
    PrimitiveReceiptError,
    action_admission_decision,
    claimgraph_decision,
    evidence_gate_decision,
)


def evidence_receipt(*, admitted=True, reason_code="ADMITTED", authorization_effect="NONE"):
    return {
        "schema_version": EVIDENCE_GATE_SCHEMA_VERSION,
        "admitted": admitted,
        "reason_code": reason_code,
        "authorization_effect": authorization_effect,
    }


def claimgraph_receipt(
    *,
    valid=True,
    reason_code="VALID",
    truth_effect="NONE",
    authorization_effect="NONE",
):
    return {
        "receipt_schema_version": CLAIMGRAPH_RECEIPT_SCHEMA_VERSION,
        "valid": valid,
        "reason_code": reason_code,
        "truth_effect": truth_effect,
        "authorization_effect": authorization_effect,
    }


def action_receipt(*, admitted=True, reason_code="ADMITTED", execution_enabled=False):
    return {
        "schema_version": ACTION_ADMISSION_SCHEMA_VERSION,
        "admitted": admitted,
        "reason_code": reason_code,
        "execution_enabled": execution_enabled,
    }


def identity():
    return ChangeIdentity(
        repository="example/repo",
        change_id="pull/42",
        base_sha="base123",
        head_sha="head456",
        observed_base_sha="base123",
        observed_head_sha="head456",
        observed_at="2026-10-01T18:00:00Z",
    )


def gate():
    return GateReceipt(
        gate_id="ci",
        status="completed",
        conclusion="success",
        observed_at="2026-10-01T18:01:00Z",
        head_sha="head456",
        base_sha="base123",
    )


def policy():
    return PromotionPolicy(
        required_gates=(
            GateRequirement(
                gate_id="ci",
                gate_class="quality",
                require_head_binding=True,
                require_base_binding=True,
            ),
        ),
        require_evidence_acceptance=True,
        require_claim_scope_acceptance=True,
        require_authority_resolution=True,
    )


def test_positive_receipts_preserve_primitive_semantics():
    evidence = evidence_gate_decision(evidence_receipt(), receipt_id="ev-1")
    claim_scope = claimgraph_decision(claimgraph_receipt(), receipt_id="cg-1")
    authority = action_admission_decision(action_receipt(), receipt_id="aa-1")

    assert evidence.decision_class == "evidence"
    assert evidence.accepted is True
    assert evidence.reason_code == "ADMITTED"
    assert claim_scope.decision_class == "claim_scope"
    assert claim_scope.accepted is True
    assert claim_scope.reason_code == "VALID"
    assert authority.decision_class == "authority"
    assert authority.accepted is True
    assert authority.reason_code == "ADMITTED"


def test_negative_receipts_preserve_denial_reasons():
    evidence = evidence_gate_decision(
        evidence_receipt(admitted=False, reason_code="DIGEST_MISMATCH")
    )
    claim_scope = claimgraph_decision(
        claimgraph_receipt(valid=False, reason_code="CONTRACT_INVALID")
    )
    authority = action_admission_decision(
        action_receipt(admitted=False, reason_code="OPERATION_MISMATCH")
    )

    assert evidence.accepted is False
    assert evidence.reason_code == "DIGEST_MISMATCH"
    assert claim_scope.accepted is False
    assert claim_scope.reason_code == "CONTRACT_INVALID"
    assert authority.accepted is False
    assert authority.reason_code == "OPERATION_MISMATCH"


def test_effect_laundering_fails_closed():
    with pytest.raises(PrimitiveReceiptError):
        evidence_gate_decision(evidence_receipt(authorization_effect="ALLOW"))

    with pytest.raises(PrimitiveReceiptError):
        claimgraph_decision(claimgraph_receipt(truth_effect="ESTABLISHED"))

    with pytest.raises(PrimitiveReceiptError):
        claimgraph_decision(claimgraph_receipt(authorization_effect="ALLOW"))

    with pytest.raises(PrimitiveReceiptError):
        action_admission_decision(action_receipt(execution_enabled=True))


def test_wrong_schema_and_malformed_receipts_fail_closed():
    bad_evidence = evidence_receipt()
    bad_evidence["schema_version"] = "other"
    with pytest.raises(PrimitiveReceiptError):
        evidence_gate_decision(bad_evidence)

    bad_claim = claimgraph_receipt()
    del bad_claim["valid"]
    with pytest.raises(PrimitiveReceiptError):
        claimgraph_decision(bad_claim)

    with pytest.raises(PrimitiveReceiptError):
        action_admission_decision([])


def test_all_three_primitive_decisions_can_satisfy_non_mutating_policy():
    receipt = assess_promotion(
        identity(),
        policy(),
        [gate()],
        evidence=evidence_gate_decision(evidence_receipt(), receipt_id="ev-1"),
        claim_scope=claimgraph_decision(claimgraph_receipt(), receipt_id="cg-1"),
        authority=action_admission_decision(action_receipt(), receipt_id="aa-1"),
    )

    assert receipt.eligible is True
    assert receipt.reason_code is PromotionReason.ELIGIBLE_FOR_PROMOTION
    assert receipt.upstream_receipt_ids == ("ev-1", "cg-1", "aa-1")
    assert receipt.merge_executed is False
    assert receipt.mutation_executed is False
    assert receipt.authorization_effect == "NONE"


@pytest.mark.parametrize(
    ("evidence", "claim_scope", "authority", "expected"),
    [
        (
            evidence_gate_decision(
                evidence_receipt(admitted=False, reason_code="DIGEST_MISMATCH")
            ),
            claimgraph_decision(claimgraph_receipt()),
            action_admission_decision(action_receipt()),
            PromotionReason.EVIDENCE_INSUFFICIENT,
        ),
        (
            evidence_gate_decision(evidence_receipt()),
            claimgraph_decision(
                claimgraph_receipt(valid=False, reason_code="CONTRACT_INVALID")
            ),
            action_admission_decision(action_receipt()),
            PromotionReason.CLAIM_SCOPE_INVALID,
        ),
        (
            evidence_gate_decision(evidence_receipt()),
            claimgraph_decision(claimgraph_receipt()),
            action_admission_decision(
                action_receipt(admitted=False, reason_code="OPERATION_MISMATCH")
            ),
            PromotionReason.AUTHORITY_UNRESOLVED,
        ),
    ],
)
def test_any_primitive_denial_blocks_existing_governed_repo_policy(
    evidence,
    claim_scope,
    authority,
    expected,
):
    receipt = assess_promotion(
        identity(),
        policy(),
        [gate()],
        evidence=evidence,
        claim_scope=claim_scope,
        authority=authority,
    )

    assert receipt.eligible is False
    assert receipt.reason_code is expected
    assert receipt.merge_executed is False
    assert receipt.mutation_executed is False
    assert receipt.authorization_effect == "NONE"
