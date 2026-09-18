#!/usr/bin/env python3
"""Fail-closed validator for Structural Epistemics claim/evidence graphs.

This validates research-record structure and explicit epistemic invariants only.
It does not establish claim truth, empirical efficacy, authorization, or execution.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CLAIM_SCHEMA_PATH = ROOT / "docs/research/STRUCTURAL_EPISTEMICS_CLAIM_RECORD_SCHEMA.json"
GRAPH_SCHEMA_PATH = ROOT / "docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json"

DEPENDENCE_RELATIONS = {
    "SHARES_SOURCE_ROOT",
    "SHARES_MODEL_LINEAGE",
    "SHARES_PROMPT_OR_POLICY",
    "SHARES_TOOL_OUTPUT",
}


def _schema_errors(validator: Draft202012Validator, value: object) -> list[str]:
    return [error.message for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path))]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _relation_exists(relations: list[dict], relation_type: str, source_id: str, target_id: str) -> bool:
    return any(
        relation["relation_type"] == relation_type
        and relation["source_id"] == source_id
        and relation["target_id"] == target_id
        for relation in relations
    )


def _dependency_relation_exists(relations: list[dict], left: str, right: str) -> bool:
    return any(
        relation["relation_type"] in DEPENDENCE_RELATIONS
        and {relation["source_id"], relation["target_id"]} == {left, right}
        for relation in relations
    )


def validate_claim_graph(graph: dict) -> None:
    claim_schema = json.loads(CLAIM_SCHEMA_PATH.read_text(encoding="utf-8"))
    graph_schema = json.loads(GRAPH_SCHEMA_PATH.read_text(encoding="utf-8"))
    claim_validator = Draft202012Validator(claim_schema)
    graph_validator = Draft202012Validator(graph_schema)

    graph_errors = _schema_errors(graph_validator, graph)
    if graph_errors:
        raise ValueError(f"graph schema invalid: {graph_errors[0]}")

    claims = graph["claims"]
    evidence = graph["evidence"]
    relations = graph["relations"]

    for claim in claims:
        errors = _schema_errors(claim_validator, claim)
        if errors:
            raise ValueError(f"claim schema invalid for {claim.get('claim_id', '<unknown>')}: {errors[0]}")

    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    evidence_by_id = {item["evidence_id"]: item for item in evidence}
    relation_ids = [relation["relation_id"] for relation in relations]

    _require(
        len(claim_by_id) == len(claims),
        "duplicate claim_id",
    )
    _require(
        len(evidence_by_id) == len(evidence),
        "duplicate evidence_id",
    )
    _require(
        len(relation_ids) == len(set(relation_ids)),
        "duplicate relation_id",
    )

    node_ids = set(claim_by_id) | set(evidence_by_id)
    _require(
        len(node_ids) == len(claim_by_id) + len(evidence_by_id),
        "claim and evidence identifiers must not collide",
    )

    for relation in relations:
        source = relation["source_id"]
        target = relation["target_id"]
        _require(source in node_ids, f"unknown relation source: {source}")
        _require(target in node_ids, f"unknown relation target: {target}")
        _require(source != target, f"self relation is not allowed: {relation['relation_id']}")

    for claim_id, claim in claim_by_id.items():
        supports = set(claim["supporting_evidence_ids"])
        contradicts = set(claim["contradicting_evidence_ids"])

        _require(
            not supports.intersection(contradicts),
            f"{claim_id} cannot list the same evidence as support and contradiction",
        )

        for evidence_id in supports | contradicts:
            _require(
                evidence_id in evidence_by_id,
                f"{claim_id} references unknown evidence: {evidence_id}",
            )

        for evidence_id in supports:
            _require(
                _relation_exists(relations, "SUPPORTS", evidence_id, claim_id),
                f"{claim_id} support listing lacks SUPPORTS relation for {evidence_id}",
            )

        for evidence_id in contradicts:
            _require(
                _relation_exists(relations, "CONTRADICTS", evidence_id, claim_id),
                f"{claim_id} contradiction listing lacks CONTRADICTS relation for {evidence_id}",
            )

        dependency = claim["dependency_signature"]
        if dependency["status"] == "KNOWN":
            _require(
                bool(dependency["roots"]),
                f"{claim_id} KNOWN dependency signature requires at least one root",
            )
        if dependency["status"] == "UNKNOWN_DEPENDENCE":
            _require(
                not dependency["roots"],
                f"{claim_id} UNKNOWN_DEPENDENCE must not assert known roots",
            )

        retraction = claim["retraction"]
        if claim["applicability_state"] == "RETRACTED":
            _require(
                retraction["state"] == "RETRACTED" and bool(retraction["reason"]),
                f"{claim_id} RETRACTED applicability requires a retraction reason",
            )
        if retraction["state"] == "RETRACTED":
            _require(
                claim["applicability_state"] == "RETRACTED",
                f"{claim_id} retraction record conflicts with applicability_state",
            )

        triggered = [item for item in claim["defeaters"] if item["status"] == "TRIGGERED"]
        _require(
            not triggered or claim["applicability_state"] != "CURRENT",
            f"{claim_id} has a triggered defeater but remains CURRENT",
        )

        if claim["epistemic_state"] in {"VERIFIED", "EMPIRICALLY_SUPPORTED"}:
            _require(
                claim["verification_status"] in {"VERIFIED_IN_SCOPE", "INDEPENDENTLY_VERIFIED"},
                f"{claim_id} epistemic_state requires verified status",
            )

        if claim["epistemic_state"] == "EMPIRICALLY_SUPPORTED":
            _require(
                claim["claim_class"] == "EMPIRICALLY_SUPPORTED",
                f"{claim_id} EMPIRICALLY_SUPPORTED state requires matching claim_class",
            )
            empirical_classes = {"MEASUREMENT", "EXPERIMENT", "CAUSAL_DESIGN"}
            _require(
                any(evidence_by_id[evidence_id]["evidence_class"] in empirical_classes for evidence_id in supports),
                f"{claim_id} EMPIRICALLY_SUPPORTED requires empirical support evidence",
            )

        if claim["causal_level"] == "CAUSAL_IDENTIFIED":
            _require(
                any(
                    evidence_by_id[evidence_id]["evidence_class"] in {"EXPERIMENT", "CAUSAL_DESIGN"}
                    for evidence_id in supports
                ),
                f"{claim_id} CAUSAL_IDENTIFIED requires intervention/causal-design evidence",
            )

        if claim["epistemic_state"] != "PROPOSED" and supports:
            _require(
                any(evidence_by_id[evidence_id]["validity"]["state"] == "CURRENT" for evidence_id in supports),
                f"{claim_id} has no CURRENT supporting evidence",
            )

        for prior_id in claim["supersedes"]:
            _require(prior_id in claim_by_id, f"{claim_id} supersedes unknown claim {prior_id}")
            _require(
                claim_id in claim_by_id[prior_id]["superseded_by"],
                f"{claim_id} supersession is not reciprocally declared by {prior_id}",
            )

        for successor_id in claim["superseded_by"]:
            _require(
                successor_id in claim_by_id,
                f"{claim_id} references unknown superseding claim {successor_id}",
            )
            _require(
                claim_id in claim_by_id[successor_id]["supersedes"],
                f"{claim_id} superseded_by is not reciprocally declared by {successor_id}",
            )

        supporting_nodes = [evidence_by_id[item] for item in supports]
        for left, right in combinations(supporting_nodes, 2):
            shared_sources = set(left["source_roots"]).intersection(right["source_roots"])
            shared_dependencies = set(left["dependency_roots"]).intersection(right["dependency_roots"])
            if shared_sources or shared_dependencies:
                _require(
                    _dependency_relation_exists(relations, left["evidence_id"], right["evidence_id"]),
                    (
                        f"{claim_id} supporting evidence {left['evidence_id']} and "
                        f"{right['evidence_id']} share dependency roots without an "
                        "explicit SHARES_* relation"
                    ),
                )


def load_graph(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("claim/evidence graph must be a JSON object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    validate_claim_graph(load_graph(args.graph))
    print("STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_PASS_STRUCTURAL_ONLY")


if __name__ == "__main__":
    main()
