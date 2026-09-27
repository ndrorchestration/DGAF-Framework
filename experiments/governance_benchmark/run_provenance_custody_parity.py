"""Matched provenance-custody falsification benchmark.

Uses the merged DGAF reference transaction implementation to emit a real bounded
receipt/audit pair, mutates linked provenance fields, and compares detection
against a conventional validator allowed the same ordinary custody checks.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# isort: off
from scripts.dgaf_capability_pep import ApprovalState, EnforcementContext, VerificationState  # noqa: E402
from scripts.dgaf_capability_policy import Authority  # noqa: E402
from scripts.dgaf_capability_reference_transaction import (  # noqa: E402
    TransactionIdentity,
    TransactionMetadata,
    run_reference_transaction,
)
# isort: on

NOW = datetime(2026, 9, 27, 7, 45, tzinfo=timezone.utc)


def _authority(capability: str, resource: str) -> Authority:
    return Authority(frozenset({capability}), frozenset({resource}))


def _identity() -> TransactionIdentity:
    return TransactionIdentity(
        workflow_id="workflow:custody-1",
        invocation_id="invoke:custody-1",
        authorization_id="auth:custody-1",
        idempotency_key="idem:custody-1",
        event_id="audit:custody-1",
    )


def _metadata() -> TransactionMetadata:
    return TransactionMetadata(
        capability_id="dgaf.local.materialize",
        capability_version="0.1.0",
        resource={"id": "dgaf.local.materialized_input"},
        parameters={"action": "materialize"},
        initiating_principal="agent:operator",
        executing_principal="gateway:local",
        delegation_chain_id="delegation:custody-1",
        policy_id="policy:local-materialization",
        policy_version="0.1.0",
        state_guards={"input_sha": "abc"},
        nonce="nonce-custody-1",
        adapter_identity="dgaf-local-mcp-adapter",
        runtime_identity="runtime:local-test",
    )


def _context_factory(metadata: TransactionMetadata):
    def factory(digest: str) -> EnforcementContext:
        cap = metadata.capability_id
        resource = metadata.resource["id"]
        allowed = _authority(cap, resource)
        return EnforcementContext(
            capability=cap,
            resource=resource,
            protected_side_effect=True,
            requester_authority=allowed,
            delegation_authority=allowed,
            executor_authority=allowed,
            policy_authority=allowed,
            authorization_status="ACTIVE",
            authorization_not_before=NOW - timedelta(minutes=5),
            authorization_expires_at=NOW + timedelta(minutes=5),
            commit_digest=digest,
            approval=ApprovalState(
                requester=metadata.initiating_principal,
                approver="human:reviewer",
                approved_digest=digest,
                consumed=False,
            ),
            verification=VerificationState(required=True, passed=True),
            required_state_guards=metadata.state_guards,
            observed_state_guards=metadata.state_guards,
            now=NOW,
        )

    return factory


def base_artifacts() -> dict[str, Any]:
    metadata = _metadata()
    result = run_reference_transaction(
        request={"action": "materialize"},
        identity=_identity(),
        metadata=metadata,
        context_factory=_context_factory(metadata),
        dispatcher=lambda request: {
            "status": "PASS",
            "action": request["action"],
            "evidence_sha256": "a" * 64,
            "synthetic_reference_only": True,
        },
        postcondition=lambda response: response["status"] == "PASS",
        timestamp=NOW,
        evidence_ids=["evidence:synthetic-custody"],
        verifier_ids=["verifier:custody"],
    )
    assert result.execution_receipt is not None
    return {
        "action_envelope": result.action_envelope,
        "action_digest": result.action_digest,
        "receipt": result.execution_receipt,
        "audit": result.audit_event,
    }


def _schemas_valid(artifacts: dict[str, Any]) -> bool:
    receipt_schema = json.loads((ROOT / "schemas/execution_receipt.schema.json").read_text(encoding="utf-8"))
    audit_schema = json.loads((ROOT / "schemas/capability_audit_event.schema.json").read_text(encoding="utf-8"))
    try:
        jsonschema.validate(artifacts["receipt"], receipt_schema)
        jsonschema.validate(artifacts["audit"], audit_schema)
    except jsonschema.ValidationError:
        return False
    return True


def custody_links_valid(artifacts: dict[str, Any]) -> bool:
    receipt = artifacts["receipt"]
    audit = artifacts["audit"]
    expected_provider_id = None
    provider = receipt.get("provider_receipt")
    if isinstance(provider, dict) and isinstance(provider.get("evidence_sha256"), str):
        expected_provider_id = "sha256:" + provider["evidence_sha256"].removeprefix("sha256:")

    checks = (
        receipt["action_digest"] == artifacts["action_digest"] == audit["action_digest"],
        receipt["authorization_id"] == audit["authorization_id"],
        receipt["workflow_id"] == audit["workflow_id"],
        receipt["invocation_id"] == audit["invocation_id"],
        receipt["capability_id"] == audit["capability_id"],
        receipt["adapter_identity"] == audit["adapter_identity"],
        receipt["executor_identity"] == audit["executing_principal"],
        audit["provider_receipt_id"] == expected_provider_id,
    )
    return _schemas_valid(artifacts) and all(checks)


def conventional_custody_valid(artifacts: dict[str, Any]) -> bool:
    return custody_links_valid(artifacts)


def dgaf_custody_valid(artifacts: dict[str, Any]) -> bool:
    return custody_links_valid(artifacts)


def mutation_cases() -> list[tuple[str, str, str, Any]]:
    return [
        ("ACTION_DIGEST", "receipt", "action_digest", "sha256:" + "b" * 64),
        ("AUTHORIZATION_ID", "audit", "authorization_id", "auth:mutated"),
        ("WORKFLOW_ID", "receipt", "workflow_id", "workflow:mutated"),
        ("INVOCATION_ID", "audit", "invocation_id", "invoke:mutated"),
        ("CAPABILITY_ID", "audit", "capability_id", "dgaf.local.other"),
        ("ADAPTER_IDENTITY", "receipt", "adapter_identity", "adapter:mutated"),
        ("EXECUTOR_IDENTITY", "audit", "executing_principal", "gateway:other"),
        ("PROVIDER_RECEIPT_ID", "audit", "provider_receipt_id", "sha256:" + "c" * 64),
    ]


def run() -> dict[str, Any]:
    base = base_artifacts()
    rows: list[dict[str, Any]] = []

    for case_id, container, field, value in mutation_cases():
        mutated = copy.deepcopy(base)
        mutated[container][field] = value
        c3_detected = not conventional_custody_valid(mutated)
        dgaf_detected = not dgaf_custody_valid(mutated)
        rows.append(
            {
                "case_id": case_id,
                "c3_detected": c3_detected,
                "dgaf_detected": dgaf_detected,
                "parity": c3_detected == dgaf_detected,
                "operator_review_required_c3": int(c3_detected),
                "operator_review_required_dgaf": int(dgaf_detected),
            }
        )

    base_valid = conventional_custody_valid(base) and dgaf_custody_valid(base)
    parity_count = sum(int(row["parity"]) for row in rows)
    c3_reviews = sum(row["operator_review_required_c3"] for row in rows)
    dgaf_reviews = sum(row["operator_review_required_dgaf"] for row in rows)

    return {
        "version": "DGAF_PROVENANCE_CUSTODY_PARITY_V1",
        "evidence_class": "SYNTHETIC_PROVENANCE_FALSIFICATION_EVIDENCE",
        "uses_merged_reference_transaction": True,
        "base_artifacts_valid": base_valid,
        "rows": rows,
        "summary": {
            "mutation_cases": len(rows),
            "parity_count": parity_count,
            "difference_count": len(rows) - parity_count,
            "detected_mutations_c3": sum(int(row["c3_detected"]) for row in rows),
            "detected_mutations_dgaf": sum(int(row["dgaf_detected"]) for row in rows),
            "operator_review_count_c3": c3_reviews,
            "operator_review_count_dgaf": dgaf_reviews,
        },
        "falsification_outcome": (
            "NO_UNIQUE_PROVENANCE_CUSTODY_ADVANTAGE_IN_MATCHED_CHECKS"
            if base_valid and parity_count == len(rows)
            else "CUSTODY_DIFFERENCE_OBSERVED"
        ),
        "interpretation_boundary": [
            "The comparator is intentionally allowed the same ordinary cross-link and schema checks.",
            "Parity weakens claims that these bounded provenance-link checks are inherently unique to DGAF.",
            (
                "This does not measure durable storage, independent custody, "
                "distributed tamper resistance, or operator time."
            ),
        ],
        "claim_ceiling": [
            "SCIENTIFIC_N_INCREMENT_0",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
            "HIGH_ASSURANCE_NOT_AUTHORIZED",
        ],
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
