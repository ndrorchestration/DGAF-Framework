import copy
import json
from pathlib import Path

import pytest

from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json"


def _graph() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _support_relation(evidence_id: str, claim_id: str, suffix: str) -> dict:
    return {
        "relation_id": f"REL-SUPPORT-{suffix}",
        "relation_type": "SUPPORTS",
        "source_id": evidence_id,
        "target_id": claim_id,
        "scope": "test",
    }


def test_reference_fixture_passes() -> None:
    validate_claim_graph(_graph())


def test_unknown_evidence_reference_fails_closed() -> None:
    graph = _graph()
    graph["claims"][0]["supporting_evidence_ids"].append("EVID-MISSING")
    with pytest.raises(ValueError, match="references unknown evidence"):
        validate_claim_graph(graph)


def test_support_listing_requires_matching_relation() -> None:
    graph = _graph()
    graph["relations"] = [
        relation
        for relation in graph["relations"]
        if relation["relation_type"] != "SUPPORTS"
    ]
    with pytest.raises(ValueError, match="lacks SUPPORTS relation"):
        validate_claim_graph(graph)


def test_contradiction_listing_requires_matching_relation() -> None:
    graph = _graph()
    graph["relations"] = [
        relation
        for relation in graph["relations"]
        if relation["relation_type"] != "CONTRADICTS"
    ]
    with pytest.raises(ValueError, match="lacks CONTRADICTS relation"):
        validate_claim_graph(graph)


def test_repeated_support_root_requires_explicit_dependency_relation() -> None:
    graph = _graph()
    claim = graph["claims"][0]
    claim["supporting_evidence_ids"].append("EVID-REFERENCE-SUPPORT-2")
    graph["evidence"].append(
        {
            "evidence_id": "EVID-REFERENCE-SUPPORT-2",
            "evidence_class": "DERIVATION",
            "source_roots": ["support-root"],
            "dependency_roots": [],
            "observed_at": "2026-09-18",
            "validity": {
                "state": "CURRENT",
                "review_condition": "review on fixture change",
            },
            "provenance_ref": "fixture://support-2",
        }
    )
    graph["relations"].append(
        _support_relation(
            "EVID-REFERENCE-SUPPORT-2",
            "CLAIM-REFERENCE-001",
            "REFERENCE-2",
        )
    )

    with pytest.raises(ValueError, match="share dependency roots without"):
        validate_claim_graph(graph)

    graph["relations"].append(
        {
            "relation_id": "REL-SHARED-ROOT",
            "relation_type": "SHARES_SOURCE_ROOT",
            "source_id": "EVID-REFERENCE-SUPPORT",
            "target_id": "EVID-REFERENCE-SUPPORT-2",
            "scope": "shared support-root",
        }
    )
    validate_claim_graph(graph)


def test_triggered_defeater_cannot_remain_current() -> None:
    graph = _graph()
    claim = graph["claims"][0]
    claim["applicability_state"] = "CURRENT"
    claim["defeaters"] = [
        {
            "defeater_id": "DEF-1",
            "condition": "counterexample observed",
            "status": "TRIGGERED",
        }
    ]
    with pytest.raises(ValueError, match="triggered defeater but remains CURRENT"):
        validate_claim_graph(graph)


def test_retraction_state_must_be_consistent() -> None:
    graph = _graph()
    claim = graph["claims"][0]
    claim["applicability_state"] = "RETRACTED"
    claim["retraction"] = {"state": "NOT_RETRACTED", "reason": None}
    with pytest.raises(ValueError, match="requires a retraction reason"):
        validate_claim_graph(graph)


def test_causal_identified_requires_intervention_or_causal_design_evidence() -> None:
    graph = _graph()
    graph["claims"][0]["causal_level"] = "CAUSAL_IDENTIFIED"
    with pytest.raises(ValueError, match="requires intervention/causal-design evidence"):
        validate_claim_graph(graph)


def test_empirically_supported_requires_empirical_evidence() -> None:
    graph = _graph()
    claim = graph["claims"][0]
    claim["claim_class"] = "EMPIRICALLY_SUPPORTED"
    claim["epistemic_state"] = "EMPIRICALLY_SUPPORTED"
    claim["verification_status"] = "VERIFIED_IN_SCOPE"
    with pytest.raises(ValueError, match="requires empirical support evidence"):
        validate_claim_graph(graph)


def test_non_proposed_claim_requires_current_support() -> None:
    graph = _graph()
    graph["evidence"][0]["validity"]["state"] = "STALE"
    with pytest.raises(ValueError, match="has no CURRENT supporting evidence"):
        validate_claim_graph(graph)


def test_unknown_dependence_cannot_assert_known_roots() -> None:
    graph = _graph()
    graph["claims"][0]["dependency_signature"] = {
        "status": "UNKNOWN_DEPENDENCE",
        "roots": ["known-root"],
    }
    with pytest.raises(ValueError, match="must not assert known roots"):
        validate_claim_graph(graph)


def test_supersession_must_be_reciprocal() -> None:
    graph = _graph()
    successor = copy.deepcopy(graph["claims"][0])
    successor["claim_id"] = "CLAIM-REFERENCE-002"
    successor["proposition"] = "Successor claim"
    successor["supersedes"] = ["CLAIM-REFERENCE-001"]
    successor["superseded_by"] = []
    successor["supporting_evidence_ids"] = []
    successor["contradicting_evidence_ids"] = []
    successor["epistemic_state"] = "PROPOSED"
    graph["claims"].append(successor)

    with pytest.raises(ValueError, match="not reciprocally declared"):
        validate_claim_graph(graph)


def test_same_evidence_cannot_support_and_contradict_claim() -> None:
    graph = _graph()
    graph["claims"][0]["contradicting_evidence_ids"].append(
        "EVID-REFERENCE-SUPPORT"
    )
    with pytest.raises(ValueError, match="same evidence as support and contradiction"):
        validate_claim_graph(graph)
