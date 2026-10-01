#!/usr/bin/env python3
"""ClaimGraph v0 validation receipt wrapper.

This module deliberately reuses the accepted Structural Epistemics validator.
It adds a JSON-safe developer receipt without changing schema-v1 validation
semantics. A valid receipt establishes contract conformance only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

from scripts.validate_structural_epistemics_claim_graph import (
    load_graph,
    validate_claim_graph,
)

CLAIMGRAPH_RECEIPT_SCHEMA_VERSION = "claimgraph.validation-receipt.v0-candidate"
TRUTH_EFFECT_NONE = "NONE"
AUTHORIZATION_EFFECT_NONE = "NONE"

VALID = "VALID"
CONTRACT_INVALID = "CONTRACT_INVALID"
INPUT_INVALID = "INPUT_INVALID"


@dataclass(frozen=True)
class ClaimGraphValidationReceipt:
    valid: bool
    reason_code: str
    graph_id: Optional[str]
    graph_schema_version: Optional[int]
    claim_count: int
    evidence_count: int
    relation_count: int
    checks_performed: tuple[str, ...]
    error_detail: Optional[str]
    truth_effect: str = TRUTH_EFFECT_NONE
    authorization_effect: str = AUTHORIZATION_EFFECT_NONE
    receipt_schema_version: str = CLAIMGRAPH_RECEIPT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.truth_effect != TRUTH_EFFECT_NONE:
            raise ValueError("ClaimGraph validation never establishes truth")
        if self.authorization_effect != AUTHORIZATION_EFFECT_NONE:
            raise ValueError("ClaimGraph validation never grants authorization")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["checks_performed"] = list(self.checks_performed)
        return value


def _safe_count(graph: dict[str, Any], key: str) -> int:
    value = graph.get(key)
    return len(value) if isinstance(value, list) else 0


def validate_claim_graph_receipt(graph: object) -> ClaimGraphValidationReceipt:
    """Return a non-truth, non-authorizing receipt for one claim graph."""

    if not isinstance(graph, dict):
        return ClaimGraphValidationReceipt(
            valid=False,
            reason_code=INPUT_INVALID,
            graph_id=None,
            graph_schema_version=None,
            claim_count=0,
            evidence_count=0,
            relation_count=0,
            checks_performed=(),
            error_detail="claim/evidence graph must be a JSON object",
        )

    graph_id = graph.get("graph_id") if isinstance(graph.get("graph_id"), str) else None
    schema_version = graph.get("schema_version") if isinstance(graph.get("schema_version"), int) else None
    claim_count = _safe_count(graph, "claims")
    evidence_count = _safe_count(graph, "evidence")
    relation_count = _safe_count(graph, "relations")

    try:
        validate_claim_graph(graph)
    except (ValueError, TypeError, KeyError) as exc:
        return ClaimGraphValidationReceipt(
            valid=False,
            reason_code=CONTRACT_INVALID,
            graph_id=graph_id,
            graph_schema_version=schema_version,
            checks_performed=("SCHEMA_AND_DECLARED_INVARIANTS",),
            error_detail=str(exc),
            claim_count=claim_count,
            evidence_count=evidence_count,
            relation_count=relation_count,
        )

    return ClaimGraphValidationReceipt(
        valid=True,
        reason_code=VALID,
        graph_id=graph_id,
        graph_schema_version=schema_version,
        checks_performed=("SCHEMA_AND_DECLARED_INVARIANTS",),
        error_detail=None,
        claim_count=claim_count,
        evidence_count=evidence_count,
        relation_count=relation_count,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()

    try:
        graph = load_graph(args.graph)
        receipt = validate_claim_graph_receipt(graph)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        receipt = ClaimGraphValidationReceipt(
            valid=False,
            reason_code=INPUT_INVALID,
            graph_id=None,
            graph_schema_version=None,
            claim_count=0,
            evidence_count=0,
            relation_count=0,
            checks_performed=(),
            error_detail=str(exc),
        )

    print(json.dumps(receipt.to_dict(), sort_keys=True))
    raise SystemExit(0 if receipt.valid else 1)


if __name__ == "__main__":
    main()
