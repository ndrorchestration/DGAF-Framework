import copy
import json
from pathlib import Path

from scripts.claimgraph_v0 import (
    AUTHORIZATION_EFFECT_NONE,
    CONTRACT_INVALID,
    TRUTH_EFFECT_NONE,
    VALID,
    validate_claim_graph_receipt,
)
from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "docs/research/fixtures/CLAIMGRAPH_SOFTWARE_INCIDENT_EXAMPLE.json"


def _graph() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_non_dgaf_software_incident_example_passes_existing_validator() -> None:
    graph = _graph()
    validate_claim_graph(graph)


def test_claimgraph_receipt_is_valid_non_truth_non_authorizing() -> None:
    receipt = validate_claim_graph_receipt(_graph())

    assert receipt.valid is True
    assert receipt.reason_code == VALID
    assert receipt.graph_id == "EGRAPH-SOFTWARE-INCIDENT-001"
    assert receipt.graph_schema_version == 1
    assert receipt.claim_count == 1
    assert receipt.evidence_count == 3
    assert receipt.relation_count == 4
    assert receipt.truth_effect == TRUTH_EFFECT_NONE
    assert receipt.authorization_effect == AUTHORIZATION_EFFECT_NONE
    assert receipt.error_detail is None
    payload = receipt.to_dict()
    assert payload["checks_performed"] == ["SCHEMA_AND_DECLARED_INVARIANTS"]


def test_invalid_graph_returns_stable_contract_invalid_receipt() -> None:
    graph = copy.deepcopy(_graph())
    graph["claims"][0]["supporting_evidence_ids"].append("EVID-MISSING")

    receipt = validate_claim_graph_receipt(graph)

    assert receipt.valid is False
    assert receipt.reason_code == CONTRACT_INVALID
    assert receipt.truth_effect == TRUTH_EFFECT_NONE
    assert receipt.authorization_effect == AUTHORIZATION_EFFECT_NONE
    assert receipt.error_detail is not None
    assert "references unknown evidence" in receipt.error_detail


def test_contradiction_and_shared_dependency_remain_explicit() -> None:
    graph = _graph()
    relation_types = {relation["relation_type"] for relation in graph["relations"]}

    assert "SUPPORTS" in relation_types
    assert "CONTRADICTS" in relation_types
    assert "SHARES_SOURCE_ROOT" in relation_types
    assert graph["claims"][0]["applicability_state"] == "CHALLENGED"
    assert graph["claims"][0]["causal_level"] == "ASSOCIATION"
