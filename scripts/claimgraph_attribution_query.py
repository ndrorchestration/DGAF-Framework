#!/usr/bin/env python3
"""Bounded ClaimGraph attribution query.

This adapter joins an accepted schema-v1 ClaimGraph with a caller-supplied
attribution observation and emits a non-truth, non-authorizing receipt.
It does not verify producer identity or independence and does not mutate the
ClaimGraph record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if __package__ in {None, ""} and str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_structural_epistemics_claim_graph import (  # noqa: E402
    validate_claim_graph,
)

RECEIPT_SCHEMA_VERSION = "claimgraph.attribution-query.v0-candidate"
OBSERVATION_RECORD_CLASS = "CLAIMGRAPH_ATTRIBUTION_OBSERVATION_V0"

PRODUCER_CLASSES = {
    "INTERNAL_SAME_SYSTEM",
    "EXTERNAL_HUMAN",
    "EXTERNAL_SYSTEM",
    "MIXED",
    "UNKNOWN",
}
EXTERNAL_PRODUCER_CLASSES = {"EXTERNAL_HUMAN", "EXTERNAL_SYSTEM"}
ATTRIBUTION_STATES = {"UNKNOWN", "CLAIMED_UNVERIFIED", "REPORTED_VERIFIED"}
INDEPENDENCE_STATES = {
    "NOT_EXECUTED",
    "INCONCLUSIVE",
    "REPORTED_VERIFIED_INDEPENDENT",
    "REPORTED_VERIFIED_NOT_INDEPENDENT",
}
REPORTED_ADJUDICATION_STATES = {
    "REPORTED_VERIFIED_INDEPENDENT",
    "REPORTED_VERIFIED_NOT_INDEPENDENT",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_observation(graph: dict, observation: dict) -> dict[str, dict]:
    required = {"record_class", "graph_id", "records"}
    if set(observation) != required:
        missing = sorted(required - set(observation))
        extra = sorted(set(observation) - required)
        raise ValueError(f"attribution observation fields mismatch: missing={missing} extra={extra}")
    if observation["record_class"] != OBSERVATION_RECORD_CLASS:
        raise ValueError(f"record_class must be {OBSERVATION_RECORD_CLASS}")
    if observation["graph_id"] != graph.get("graph_id"):
        raise ValueError("attribution observation graph_id must match ClaimGraph")
    if not isinstance(observation["records"], list):
        raise ValueError("attribution observation records must be an array")

    evidence_ids = {
        item["evidence_id"]
        for item in graph.get("evidence", [])
        if isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
    }
    record_required = {
        "evidence_id",
        "attribution_source_ref",
        "producer_class",
        "producer_identity_ref",
        "attribution_state",
        "independence_claimed",
        "independence_basis_refs",
        "independence_adjudication_state",
        "adjudication_ref",
    }
    by_evidence: dict[str, dict] = {}

    for record in observation["records"]:
        if not isinstance(record, dict) or set(record) != record_required:
            raise ValueError("attribution record fields must match the closed candidate contract")

        evidence_id = record["evidence_id"]
        if not _nonempty_string(evidence_id) or evidence_id not in evidence_ids:
            raise ValueError(f"unknown evidence_id: {evidence_id!r}")
        if evidence_id in by_evidence:
            raise ValueError(f"duplicate evidence attribution: {evidence_id}")

        if not _nonempty_string(record["attribution_source_ref"]):
            raise ValueError("attribution_source_ref must be a non-empty string")
        if record["producer_class"] not in PRODUCER_CLASSES:
            raise ValueError("unsupported producer_class")
        producer_identity_ref = record["producer_identity_ref"]
        if producer_identity_ref is not None and not _nonempty_string(producer_identity_ref):
            raise ValueError("producer_identity_ref must be null or a non-empty string")
        if record["producer_class"] != "UNKNOWN" and not producer_identity_ref:
            raise ValueError("non-UNKNOWN producer_class requires producer_identity_ref")
        if record["attribution_state"] not in ATTRIBUTION_STATES:
            raise ValueError("unsupported attribution_state")
        if not isinstance(record["independence_claimed"], bool):
            raise ValueError("independence_claimed must be boolean")
        independence_basis_refs = record["independence_basis_refs"]
        if not isinstance(independence_basis_refs, list) or any(
            not _nonempty_string(item) for item in independence_basis_refs
        ):
            raise ValueError("independence_basis_refs must be an array of non-empty strings")
        if record["independence_claimed"] and record["producer_class"] not in EXTERNAL_PRODUCER_CLASSES:
            raise ValueError("independence_claimed=true requires an external producer class")
        if record["independence_claimed"] and not independence_basis_refs:
            raise ValueError("claimed independence requires independence_basis_refs")
        if record["independence_adjudication_state"] not in INDEPENDENCE_STATES:
            raise ValueError("unsupported independence_adjudication_state")

        adjudication_ref = record["adjudication_ref"]
        if adjudication_ref is not None and not _nonempty_string(adjudication_ref):
            raise ValueError("adjudication_ref must be null or a non-empty string")

        independence_state = record["independence_adjudication_state"]
        if independence_state in REPORTED_ADJUDICATION_STATES and not adjudication_ref:
            raise ValueError("reported adjudication requires adjudication_ref")
        if independence_state == "REPORTED_VERIFIED_INDEPENDENT":
            if not record["independence_claimed"]:
                raise ValueError("reported independent adjudication requires independence_claimed=true")
            if record["producer_class"] == "INTERNAL_SAME_SYSTEM":
                raise ValueError("INTERNAL_SAME_SYSTEM cannot be reported verified independent")
            if record["producer_class"] not in EXTERNAL_PRODUCER_CLASSES:
                raise ValueError("reported verified independence requires an external producer class")

        by_evidence[evidence_id] = dict(record)

    return by_evidence


def query_attribution(graph: dict, observation: dict) -> dict:
    """Classify caller-supplied attribution metadata without promoting it."""

    validate_claim_graph(graph)
    by_evidence = _validate_observation(graph, observation)

    supporting_ids = sorted(
        {evidence_id for claim in graph["claims"] for evidence_id in claim.get("supporting_evidence_ids", [])}
    )
    mapped_supporting = sorted(set(supporting_ids).intersection(by_evidence))
    completeness = "COMPLETE_FOR_SUPPORTING_EVIDENCE" if len(mapped_supporting) == len(supporting_ids) else "PARTIAL"

    internal_only: list[str] = []
    unmapped: list[str] = []
    external_observed: list[str] = []
    external_unverified: list[str] = []
    reported_independent: list[str] = []
    unknown_or_mixed: list[str] = []

    for claim in graph["claims"]:
        claim_id = claim["claim_id"]
        support_ids = claim.get("supporting_evidence_ids", [])
        missing = [evidence_id for evidence_id in support_ids if evidence_id not in by_evidence]
        records = [by_evidence[evidence_id] for evidence_id in support_ids if evidence_id in by_evidence]

        if missing:
            unmapped.append(claim_id)
        if (
            support_ids
            and not missing
            and all(record["producer_class"] == "INTERNAL_SAME_SYSTEM" for record in records)
        ):
            internal_only.append(claim_id)
        if any(record["producer_class"] in EXTERNAL_PRODUCER_CLASSES for record in records):
            external_observed.append(claim_id)
        if any(
            record["producer_class"] in EXTERNAL_PRODUCER_CLASSES and record["attribution_state"] != "REPORTED_VERIFIED"
            for record in records
        ):
            external_unverified.append(claim_id)
        if any(record["independence_adjudication_state"] == "REPORTED_VERIFIED_INDEPENDENT" for record in records):
            reported_independent.append(claim_id)
        if any(record["producer_class"] in {"UNKNOWN", "MIXED"} for record in records):
            unknown_or_mixed.append(claim_id)

    return {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "graph_id": graph["graph_id"],
        "graph_schema_version": graph["schema_version"],
        "observation_record_class": observation["record_class"],
        "observation_authority": "CALLER_SUPPLIED_NOT_REVERIFIED",
        "supporting_evidence_count": len(supporting_ids),
        "mapped_supporting_evidence_count": len(mapped_supporting),
        "completeness": completeness,
        "evidence_attribution": [by_evidence[key] for key in sorted(by_evidence)],
        "claims_declared_supported_only_by_internal_evidence": sorted(internal_only),
        "claims_with_unmapped_support": sorted(unmapped),
        "claims_with_external_support_observed": sorted(external_observed),
        "claims_with_external_attribution_claimed_unverified": sorted(external_unverified),
        "claims_with_reported_independently_adjudicated_support": sorted(reported_independent),
        "claims_with_unknown_or_mixed_support": sorted(unknown_or_mixed),
        "truth_effect": "NONE",
        "authorization_effect": "NONE",
        "independence_effect": "NONE",
    }


def _load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("attribution_observation", type=Path)
    args = parser.parse_args()

    try:
        receipt = query_attribution(
            _load_object(args.graph),
            _load_object(args.attribution_observation),
        )
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 2 if receipt["completeness"] == "PARTIAL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
