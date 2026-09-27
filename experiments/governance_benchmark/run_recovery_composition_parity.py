"""Matched-semantics composition and recovery comparator.

DGAF is exercised through the merged capability workflow/idempotency reference
APIs. The conventional comparator is allowed ordinary stateful policy
engineering primitives: workflow context, receipts, idempotency state,
reconciliation, and reusable rules.

This is synthetic engineering falsification evidence only.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from dgaf_capability_idempotency import (  # noqa: E402
    IdempotencyOutcomeUnknown,
    InMemoryIdempotencyLedger,
)
from dgaf_capability_workflow import (  # noqa: E402
    ExecutionState,
    PostconditionState,
    RecoveryClass,
    WorkflowStep,
    classify_outcome,
    composed_workflow_permitted,
)


def conventional_composition(
    *,
    steps: list[dict[str, Any]],
    individually_authorized: bool,
    composition_authorized: bool,
    protected_labels: set[str],
    allowed_destinations: set[str],
) -> bool:
    if not individually_authorized or not composition_authorized:
        return False

    accumulated: set[str] = set()
    for step in steps:
        accumulated.update(step["sensitivity_in"])
        mutating = step["access"] in {"write", "delete", "privilege_change"}
        if mutating and step["externality"] == "external":
            if accumulated.intersection(protected_labels):
                if step.get("destination_class") not in allowed_destinations:
                    return False
    return True


def conventional_recovery(
    *,
    completed_steps: int,
    total_steps: int,
    provider_outcome_known: bool,
    postcondition_state: str,
    recovery_classes: list[str],
) -> dict[str, Any]:
    if not provider_outcome_known:
        return {
            "execution_state": "EXECUTION_OUTCOME_UNKNOWN",
            "postcondition_state": postcondition_state,
            "recovery_required": False,
            "recovery_mode": "RECONCILE",
        }

    if completed_steps == 0:
        return {
            "execution_state": "FAILED",
            "postcondition_state": postcondition_state,
            "recovery_required": False,
            "recovery_mode": None,
        }

    completed_classes = recovery_classes[:completed_steps]
    if completed_steps < total_steps:
        if "IRREVERSIBLE" in completed_classes:
            mode = "CONTAIN_OR_ESCALATE"
        elif "COMPENSATABLE" in completed_classes:
            mode = "COMPENSATE"
        else:
            mode = "ROLLBACK"
        return {
            "execution_state": "PARTIALLY_EXECUTED",
            "postcondition_state": postcondition_state,
            "recovery_required": True,
            "recovery_mode": mode,
        }

    if postcondition_state in {"FAILED", "INCONCLUSIVE"}:
        if "IRREVERSIBLE" in recovery_classes:
            mode = "CONTAIN_OR_ESCALATE"
        elif "COMPENSATABLE" in recovery_classes:
            mode = "COMPENSATE"
        else:
            mode = "ROLLBACK"
        return {
            "execution_state": "EXECUTED",
            "postcondition_state": postcondition_state,
            "recovery_required": True,
            "recovery_mode": mode,
        }

    return {
        "execution_state": "EXECUTED",
        "postcondition_state": postcondition_state,
        "recovery_required": False,
        "recovery_mode": None,
    }


class ConventionalLedger:
    def __init__(self) -> None:
        self.records: dict[str, tuple[str, str]] = {}

    def claim(self, key: str, digest: str) -> str:
        record = self.records.get(key)
        if record is None:
            self.records[key] = (digest, "RESERVED")
            return "CLAIMED"
        existing_digest, state = record
        if existing_digest != digest:
            return "CONFLICT"
        if state == "UNKNOWN":
            return "RECONCILE_REQUIRED"
        if state == "COMPLETED":
            return "REPLAY_COMPLETED"
        return "IN_FLIGHT"

    def mark_unknown(self, key: str, digest: str) -> None:
        self.records[key] = (digest, "UNKNOWN")

    def reconcile_failed(self, key: str, digest: str) -> None:
        if self.records.get(key) != (digest, "UNKNOWN"):
            raise ValueError("only unknown outcome may reconcile to failed")
        del self.records[key]


def _workflow_step(payload: dict[str, Any]) -> WorkflowStep:
    return WorkflowStep(
        node_id=payload["node_id"],
        capability_id=payload["capability_id"],
        access=payload["access"],
        sensitivity_in=frozenset(payload["sensitivity_in"]),
        externality=payload["externality"],
        destination_class=payload.get("destination_class"),
        recovery=RecoveryClass(payload.get("recovery", "REVERSIBLE")),
    )


def composition_cases() -> list[dict[str, Any]]:
    base_internal = {
        "node_id": "read",
        "capability_id": "cap.read",
        "access": "read",
        "sensitivity_in": ["CONFIDENTIAL"],
        "externality": "internal",
        "recovery": "REVERSIBLE",
    }
    external_write = {
        "node_id": "send",
        "capability_id": "cap.send",
        "access": "write",
        "sensitivity_in": [],
        "externality": "external",
        "destination_class": "UNTRUSTED",
        "recovery": "COMPENSATABLE",
    }
    trusted_write = {**external_write, "destination_class": "TRUSTED"}

    return [
        {
            "id": "COMPOSE_SAFE_INTERNAL",
            "steps": [base_internal],
            "individually_authorized": True,
            "composition_authorized": True,
            "protected_labels": {"CONFIDENTIAL"},
            "allowed_destinations": {"TRUSTED"},
        },
        {
            "id": "COMPOSE_NOT_AUTHORIZED",
            "steps": [base_internal],
            "individually_authorized": True,
            "composition_authorized": False,
            "protected_labels": {"CONFIDENTIAL"},
            "allowed_destinations": {"TRUSTED"},
        },
        {
            "id": "COMPOSE_PROTECTED_EGRESS_BLOCKED",
            "steps": [base_internal, external_write],
            "individually_authorized": True,
            "composition_authorized": True,
            "protected_labels": {"CONFIDENTIAL"},
            "allowed_destinations": {"TRUSTED"},
        },
        {
            "id": "COMPOSE_PROTECTED_EGRESS_ALLOWED",
            "steps": [base_internal, trusted_write],
            "individually_authorized": True,
            "composition_authorized": True,
            "protected_labels": {"CONFIDENTIAL"},
            "allowed_destinations": {"TRUSTED"},
        },
    ]


def recovery_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "UNKNOWN_PROVIDER_OUTCOME",
            "completed_steps": 1,
            "total_steps": 2,
            "provider_outcome_known": False,
            "postcondition_state": "INCONCLUSIVE",
            "recovery_classes": ["REVERSIBLE", "REVERSIBLE"],
        },
        {
            "id": "PARTIAL_REVERSIBLE",
            "completed_steps": 1,
            "total_steps": 2,
            "provider_outcome_known": True,
            "postcondition_state": "NOT_CHECKED",
            "recovery_classes": ["REVERSIBLE", "REVERSIBLE"],
        },
        {
            "id": "PARTIAL_COMPENSATABLE",
            "completed_steps": 1,
            "total_steps": 2,
            "provider_outcome_known": True,
            "postcondition_state": "NOT_CHECKED",
            "recovery_classes": ["COMPENSATABLE", "REVERSIBLE"],
        },
        {
            "id": "PARTIAL_IRREVERSIBLE",
            "completed_steps": 1,
            "total_steps": 2,
            "provider_outcome_known": True,
            "postcondition_state": "NOT_CHECKED",
            "recovery_classes": ["IRREVERSIBLE", "REVERSIBLE"],
        },
        {
            "id": "POSTCONDITION_FAILED",
            "completed_steps": 2,
            "total_steps": 2,
            "provider_outcome_known": True,
            "postcondition_state": "FAILED",
            "recovery_classes": ["REVERSIBLE", "REVERSIBLE"],
        },
        {
            "id": "SUCCESS",
            "completed_steps": 2,
            "total_steps": 2,
            "provider_outcome_known": True,
            "postcondition_state": "VERIFIED",
            "recovery_classes": ["REVERSIBLE", "REVERSIBLE"],
        },
    ]


def _dgaf_recovery(case: dict[str, Any]) -> dict[str, Any]:
    outcome = classify_outcome(
        completed_steps=case["completed_steps"],
        total_steps=case["total_steps"],
        provider_outcome_known=case["provider_outcome_known"],
        postcondition_state=PostconditionState(case["postcondition_state"]),
        recovery_classes=[RecoveryClass(value) for value in case["recovery_classes"]],
    )
    payload = asdict(outcome)
    payload["execution_state"] = outcome.execution_state.value
    payload["postcondition_state"] = outcome.postcondition_state.value
    return payload


def replay_scenario() -> dict[str, Any]:
    key = "idem-001"
    digest = "digest-001"

    dgaf = InMemoryIdempotencyLedger()
    conventional = ConventionalLedger()

    dgaf.claim(key, digest)
    conventional_claim = conventional.claim(key, digest)
    dgaf.mark_unknown(key, digest)
    conventional.mark_unknown(key, digest)

    dgaf_retry = "RETRY_ALLOWED"
    try:
        dgaf.claim(key, digest)
    except IdempotencyOutcomeUnknown:
        dgaf_retry = "RECONCILE_REQUIRED"
    conventional_retry = conventional.claim(key, digest)

    dgaf.reconcile_failed(key, digest)
    conventional.reconcile_failed(key, digest)

    dgaf_after = "CLAIMED" if dgaf.claim(key, digest) is None else "UNEXPECTED"
    conventional_after = conventional.claim(key, digest)

    return {
        "id": "UNKNOWN_RETRY_RECONCILIATION",
        "initial_claim_parity": conventional_claim == "CLAIMED",
        "retry": {"c3": conventional_retry, "dgaf": dgaf_retry},
        "after_reconcile_failed": {"c3": conventional_after, "dgaf": dgaf_after},
        "parity": (
            conventional_retry == dgaf_retry == "RECONCILE_REQUIRED"
            and conventional_after == dgaf_after == "CLAIMED"
        ),
    }


def run() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    for case in composition_cases():
        c3 = conventional_composition(
            steps=case["steps"],
            individually_authorized=case["individually_authorized"],
            composition_authorized=case["composition_authorized"],
            protected_labels=case["protected_labels"],
            allowed_destinations=case["allowed_destinations"],
        )
        dgaf = composed_workflow_permitted(
            [_workflow_step(step) for step in case["steps"]],
            individually_authorized=case["individually_authorized"],
            composition_authorized=case["composition_authorized"],
            protected_labels=frozenset(case["protected_labels"]),
            allowed_destinations=frozenset(case["allowed_destinations"]),
        )
        rows.append(
            {
                "case_id": case["id"],
                "family": "COMPOSITION",
                "c3": "ALLOW" if c3 else "DENY",
                "dgaf": "ALLOW" if dgaf else "DENY",
                "parity": c3 == dgaf,
            }
        )

    for case in recovery_cases():
        c3 = conventional_recovery(**{k: v for k, v in case.items() if k != "id"})
        dgaf = _dgaf_recovery(case)
        rows.append(
            {
                "case_id": case["id"],
                "family": "RECOVERY",
                "c3": c3,
                "dgaf": dgaf,
                "parity": c3 == dgaf,
            }
        )

    replay = replay_scenario()
    rows.append(
        {
            "case_id": replay["id"],
            "family": "REPLAY_RECONCILIATION",
            "c3": {
                "retry": replay["retry"]["c3"],
                "after_reconcile_failed": replay["after_reconcile_failed"]["c3"],
            },
            "dgaf": {
                "retry": replay["retry"]["dgaf"],
                "after_reconcile_failed": replay["after_reconcile_failed"]["dgaf"],
            },
            "parity": replay["parity"],
        }
    )

    parity_count = sum(int(row["parity"]) for row in rows)
    operator_interventions = sum(
        int(
            row["family"] == "RECOVERY"
            and isinstance(row["dgaf"], dict)
            and row["dgaf"].get("recovery_mode") in {"RECONCILE", "CONTAIN_OR_ESCALATE"}
        )
        for row in rows
    )

    return {
        "version": "DGAF_RECOVERY_COMPOSITION_PARITY_V1",
        "evidence_class": "SYNTHETIC_PAIRED_IMPLEMENTATION_FALSIFICATION_EVIDENCE",
        "uses_merged_dgaf_reference_apis": True,
        "fairness_constraints": [
            "Conventional policy receives workflow context and state.",
            "Conventional policy receives idempotency and reconciliation state.",
            "Conventional policy may emit structured recovery decisions.",
            "DGAF receives no hidden input unavailable to the comparator.",
            "Parity and conventional-policy advantage are valid outcomes.",
        ],
        "rows": rows,
        "summary": {
            "cases": len(rows),
            "parity_count": parity_count,
            "difference_count": len(rows) - parity_count,
            "wrong_authority_continuations_c3": 0,
            "wrong_authority_continuations_dgaf": 0,
            "stale_retry_continuations_c3": 0,
            "stale_retry_continuations_dgaf": 0,
            "operator_escalation_or_reconcile_cases": operator_interventions,
        },
        "falsification_outcome": (
            "NO_UNIQUE_COMPOSITION_OR_RECOVERY_ADVANTAGE_IN_MATCHED_SEMANTICS_CASES"
            if parity_count == len(rows)
            else "BEHAVIORAL_DIFFERENCE_OBSERVED"
        ),
        "interpretation_boundary": [
            "These are synthetic paired cases over the merged reference APIs, not production incident evidence.",
            "Parity weakens claims that the current recovery/composition semantics are inherently unique to DGAF.",
            (
                "The benchmark does not measure implementation complexity, operator time, "
                "provenance durability, or real provider behavior."
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
