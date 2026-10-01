"""JSON-safe serialization helpers for Evidence Gate v0."""

from __future__ import annotations

from typing import Any

from .evidence_gate import EvidenceAdmissionReceipt


def evidence_admission_receipt_to_dict(receipt: EvidenceAdmissionReceipt) -> dict[str, Any]:
    if not isinstance(receipt, EvidenceAdmissionReceipt):
        raise TypeError("receipt must be EvidenceAdmissionReceipt")
    return {
        "admitted": receipt.admitted,
        "reason_code": receipt.reason_code.value,
        "evidence_id": receipt.evidence_id,
        "target": {
            "type": receipt.target_type,
            "id": receipt.target_id,
            "scope_id": receipt.scope_id,
        },
        "verified_digest": receipt.verified_digest,
        "provenance_class": receipt.provenance_class,
        "claim": {
            "id": receipt.claim_id,
            "class": receipt.claim_class,
            "evidence_class": receipt.evidence_class,
            "ceiling": list(receipt.claim_ceiling),
        },
        "checks": {
            "digest": receipt.digest_checked,
            "target": receipt.target_checked,
            "source": receipt.source_checked,
            "environment": receipt.environment_checked,
            "provenance": receipt.provenance_checked,
            "receipt": receipt.receipt_checked,
            "manifest": receipt.manifest_checked,
            "content_set": receipt.content_set_checked,
            "custody": receipt.custody_checked,
            "claim_scope": receipt.claim_scope_checked,
            "historical_transfer": receipt.historical_transfer_checked,
        },
        "authorization_effect": receipt.authorization_effect,
        "schema_version": receipt.schema_version,
    }
