"""Same-source read-only A-direct versus incumbent B-FIXED inspect parity.

These are public development fixtures; not agent experiments, preregistered
trials, hidden held-out cases, independent review, or a C-INSTRUMENT test.
No additional authority, truth, or side effects are created.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from scripts.airp_b_fixed_workflow import FixedWorkflow
from scripts.claimgraph_attribution_query import query_attribution


def _observation(case: str, graph_id: str) -> dict:
    record = {
        "evidence_id": "EVID-REFERENCE-SUPPORT",
        "attribution_source_ref": "fixture://parity/caller",
        "producer_class": "INTERNAL_SAME_SYSTEM",
        "producer_identity_ref": "fixture://parity/producer",
        "attribution_state": "CLAIMED_UNVERIFIED",
        "independence_claimed": False,
        "independence_basis_refs": [],
        "independence_adjudication_state": "NOT_EXECUTED",
        "adjudication_ref": None,
    }
    observation: dict[str, Any] = {
        "record_class": "CLAIMGRAPH_ATTRIBUTION_OBSERVATION_V0",
        "graph_id": graph_id,
        "records": [record],
    }
    if case == "PARTIAL_METADATA":
        observation["records"] = []
    elif case == "REPORTED_INDEPENDENCE":
        record.update(
            {
                "producer_class": "EXTERNAL_HUMAN",
                "attribution_state": "REPORTED_VERIFIED",
                "independence_claimed": True,
                "independence_basis_refs": ["fixture://unverified-claim"],
                "independence_adjudication_state": "REPORTED_VERIFIED_INDEPENDENT",
                "adjudication_ref": "fixture://caller-reported-adjudication",
            }
        )
    elif case == "FORGED_INTERNAL_INDEPENDENCE":
        record["independence_claimed"] = True
        record["independence_basis_refs"] = ["fixture://forged-independence"]
    elif case == "UNKNOWN_EVIDENCE":
        record["evidence_id"] = "EVID-PARITY-UNKNOWN"
    elif case == "DUPLICATE_ATTRIBUTION":
        observation["records"].append(copy.deepcopy(record))
    elif case != "COMPLETE_INTERNAL_CHALLENGED":
        raise AssertionError("not a declared synthetic case")
    return observation


@pytest.mark.parametrize(
    ("case", "expected_class"),
    [
        ("COMPLETE_INTERNAL_CHALLENGED", "COMPLETE"),
        ("PARTIAL_METADATA", "PARTIAL"),
        ("REPORTED_INDEPENDENCE", "COMPLETE"),
        ("FORGED_INTERNAL_INDEPENDENCE", "INVALID"),
        ("UNKNOWN_EVIDENCE", "INVALID"),
        ("DUPLICATE_ATTRIBUTION", "INVALID"),
    ],
)
def test_direct_and_fixed_inspect_have_matching_attribution_semantics(case: str, expected_class: str) -> None:
    """Both arms use the *same* underlying query, not independent oracles."""
    workflow = FixedWorkflow()
    graph = workflow.snapshot()
    observation = _observation(case, graph["graph_id"])
    graph_before = copy.deepcopy(graph)
    observation_before = copy.deepcopy(observation)

    # A-DIRECT: one direct read-only invocation of the current shipped query.
    direct_error = None
    direct_receipt = None
    try:
        direct_receipt = query_attribution(copy.deepcopy(graph), copy.deepcopy(observation))
    except ValueError as exc:
        direct_error = str(exc)

    # B-FIXED: the exact same query through the six-operation fixed runner.
    command = {
        "op": "inspect",
        "branch": "base",
        "expected_version": 0,
        "request_id": "REQ-PARITY-001",
        "args": {"attribution_observation": copy.deepcopy(observation)},
    }
    fixed = workflow.execute(command)
    assert fixed["truth_effect"] == "NONE"
    assert fixed["authorization_effect"] == "NONE"
    assert fixed["independence_effect"] == "NONE"
    assert fixed["external_effects"] == "NONE"

    if expected_class == "INVALID":
        assert direct_error is not None
        assert direct_receipt is None
        assert fixed["status"] == "REJECTED"
        assert fixed["reason"] == f"REJECTED: {direct_error}"
    else:
        assert direct_error is None
        assert fixed["status"] == "ACCEPTED_SYNTHETIC_ONLY"
        assert fixed["state_changed"] is False
        assert fixed["state"] == graph_before
        assert fixed["attribution"] == direct_receipt
        assert fixed["attribution"]["observation_authority"] == "CALLER_SUPPLIED_NOT_REVERIFIED"
        for effect in ("truth_effect", "authorization_effect", "independence_effect"):
            assert fixed["attribution"][effect] == "NONE"
        if expected_class == "PARTIAL":
            assert fixed["attribution"]["completeness"] == "PARTIAL"
        else:
            assert fixed["attribution"]["completeness"] == "COMPLETE_FOR_SUPPORTING_EVIDENCE"
        if case == "REPORTED_INDEPENDENCE":
            assert fixed["attribution"]["claims_with_reported_independently_adjudicated_support"] == [
                "CLAIM-REFERENCE-001"
            ]
            assert fixed["attribution"]["independence_effect"] == "NONE"
        if case == "COMPLETE_INTERNAL_CHALLENGED":
            assert fixed["state"]["claims"][0]["applicability_state"] == "CHALLENGED"
            assert fixed["attribution"]["completeness"] == "COMPLETE_FOR_SUPPORTING_EVIDENCE"

    assert workflow.snapshot() == graph_before
    assert graph == graph_before
    assert observation == observation_before
