"""Bounded comparison of direct ClaimGraph use with its existing fixed query pipeline.

This reuses the shipped validator and attribution-query CLI. No Agent Instrument,
workflow engine, authority predicate, agent, or scientific trial is created.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.claimgraph_attribution_query import query_attribution
from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json"
QUERY_PATH = ROOT / "scripts/claimgraph_attribution_query.py"
QUERY_GIT_BLOB = "e3ed75a9e3a0eb6b4a01754894df32bf10985b2a"


def _git_blob(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}".encode("ascii") + bytes([0])
    return hashlib.sha1(header + raw).hexdigest()  # noqa: S324 - Git identity only


def _record() -> dict:
    return {
        "evidence_id": "EVID-REFERENCE-SUPPORT",
        "attribution_source_ref": "fixture://attribution",
        "producer_class": "INTERNAL_SAME_SYSTEM",
        "producer_identity_ref": "fixture://producer",
        "attribution_state": "CLAIMED_UNVERIFIED",
        "independence_claimed": False,
        "independence_basis_refs": [],
        "independence_adjudication_state": "NOT_EXECUTED",
        "adjudication_ref": None,
    }


def _task(case_id: str) -> tuple[dict, dict]:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    record = _record()
    observation = {
        "record_class": "CLAIMGRAPH_ATTRIBUTION_OBSERVATION_V0",
        "graph_id": graph["graph_id"],
        "records": [record],
    }

    if case_id == "ATTR-01":
        pass  # complete internal classification
    elif case_id == "ATTR-02":
        observation["records"] = []  # partial is exit 2, not admission
    elif case_id in {"ATTR-03", "ATTR-04"}:
        record["producer_class"] = "EXTERNAL_HUMAN"
        record["independence_claimed"] = True
        record["independence_basis_refs"] = ["fixture://claimed-basis"]
        if case_id == "ATTR-04":
            record["attribution_state"] = "REPORTED_VERIFIED"
            record["independence_adjudication_state"] = "REPORTED_VERIFIED_INDEPENDENT"
            record["adjudication_ref"] = "fixture://claimed-adjudication"
    elif case_id == "ATTR-05":
        record["independence_claimed"] = True
        record["independence_basis_refs"] = ["fixture://invalid-basis"]
    elif case_id == "ATTR-06":
        record["evidence_id"] = "EVID-ABSENT"
    elif case_id == "ATTR-07":
        graph["relations"] = [r for r in graph["relations"] if r["relation_type"] != "SUPPORTS"]
    elif case_id == "ATTR-08":
        observation["records"].append(copy.deepcopy(record))
    elif case_id == "ATTR-09":
        record["producer_class"] = "EXTERNAL_HUMAN"
        record["independence_claimed"] = True
        record["independence_basis_refs"] = ["fixture://claimed-basis"]
        record["attribution_state"] = "REPORTED_VERIFIED"
        record["independence_adjudication_state"] = "REPORTED_VERIFIED_INDEPENDENT"
    else:
        raise AssertionError("unknown case identifier")
    return graph, observation


@pytest.mark.parametrize(
    ("case_id", "expected_exit", "error_fragment"),
    [
        ("ATTR-01", 0, None),
        ("ATTR-02", 2, None),
        ("ATTR-03", 0, None),
        ("ATTR-04", 0, None),
        ("ATTR-05", 1, "external producer class"),
        ("ATTR-06", 1, "unknown evidence_id"),
        ("ATTR-07", 1, "lacks SUPPORTS relation"),
        ("ATTR-08", 1, "duplicate evidence attribution"),
        ("ATTR-09", 1, "adjudication_ref"),
    ],
    ids=[f"ATTR-0{i}" for i in range(1, 10)],
)
def test_existing_fixed_attribution_workflow_matches_direct_controls(
    case_id: str, expected_exit: int, error_fragment: str | None, tmp_path: Path
) -> None:
    # Source identity is a Git blob reference, not signature or independent custody.
    assert _git_blob(QUERY_PATH) == QUERY_GIT_BLOB
    graph, observation = _task(case_id)
    graph_before = copy.deepcopy(graph)
    observation_before = copy.deepcopy(observation)

    # A: explicit direct validator then direct attribution query. Note the query
    # itself validates again; this is *not* an equal-runtime/cost benchmark.
    direct_error = None
    direct_result = None
    try:
        validate_claim_graph(copy.deepcopy(graph))
        direct_result = query_attribution(copy.deepcopy(graph), copy.deepcopy(observation))
    except ValueError as exc:
        direct_error = str(exc)

    # B: existing fixed pipeline through its CLI. No new orchestrator is added.
    graph_file = tmp_path / "graph.json"
    attribution_file = tmp_path / "observation.json"
    graph_file.write_text(json.dumps(graph, sort_keys=True), encoding="utf-8")
    attribution_file.write_text(json.dumps(observation, sort_keys=True), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(QUERY_PATH), str(graph_file), str(attribution_file)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert result.returncode == expected_exit, (result.stdout[-500:], result.stderr[-500:])
    assert not result.stderr.strip(), result.stderr
    payload = json.loads(result.stdout)
    if expected_exit == 1:
        assert direct_error is not None
        assert error_fragment is not None
        assert error_fragment in direct_error
        assert payload == {"error": direct_error}
    else:
        assert direct_error is None
        assert payload == direct_result
        assert payload["truth_effect"] == "NONE"
        assert payload["authorization_effect"] == "NONE"
        assert payload["independence_effect"] == "NONE"
        assert payload["observation_authority"] == "CALLER_SUPPLIED_NOT_REVERIFIED"
        assert payload["completeness"] == (
            "PARTIAL" if expected_exit == 2 else "COMPLETE_FOR_SUPPORTING_EVIDENCE"
        )
        if case_id == "ATTR-04":
            assert payload["claims_with_reported_independently_adjudicated_support"] == [
                "CLAIM-REFERENCE-001"
            ]  # reported label, NOT independent verification
    assert graph == graph_before  # no persistent mutation
    assert observation == observation_before
