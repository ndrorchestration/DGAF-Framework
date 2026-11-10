"""Source-locked synthetic A/B surface parity smoke — no agents or authority.

A invokes the existing ClaimGraph validator directly; B invokes the exact
same validator via its CLI. This is a structural interface/plumbing check,
NOT an experiment, fixed-workflow comparison, or independent verification.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/research/fixtures/AGENT_INSTRUMENT_AB_SMOKE_MANIFEST_V0_1.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
CASES = MANIFEST["cases"]


def _git_blob_sha1(path: Path) -> str:
    """Git SHA-1 blob digest, not SHA-256 or the SHA-1 of raw bytes alone."""
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git identity only, not security


def _candidate(mutation: str) -> dict:
    path = ROOT / MANIFEST["provenance"]["graph_fixture_path"]
    graph = json.loads(path.read_text(encoding="utf-8"))
    claim = graph["claims"][0]

    if mutation == "NONE":
        return graph
    if mutation == "UNKNOWN_EVIDENCE":
        claim["supporting_evidence_ids"].append("EVID-MISSING-AB")
    elif mutation == "DROP_SUPPORT_RELATION":
        graph["relations"] = [r for r in graph["relations"] if r["relation_type"] != "SUPPORTS"]
    elif mutation == "TRIGGERED_DEFEATER_CURRENT":
        claim["applicability_state"] = "CURRENT"
        claim["defeaters"] = [
            {
                "defeater_id": "DEF-AB-1",
                "condition": "synthetic counterexample",
                "status": "TRIGGERED",
            }
        ]
    elif mutation in {
        "DUPLICATED_SUPPORT_SHARED_ROOT",
        "DUPLICATED_SUPPORT_WITH_RELATION",
    }:
        source = graph["evidence"][0]
        clone = copy.deepcopy(source)
        clone["evidence_id"] = "EVID-AB-SUPPORT-ALIAS"
        clone["provenance_ref"] = "fixture://ab-support-alias"
        graph["evidence"].append(clone)
        claim["supporting_evidence_ids"].append(clone["evidence_id"])
        graph["relations"].append(
            {
                "relation_id": "REL-AB-SUPPORT-ALIAS",
                "relation_type": "SUPPORTS",
                "source_id": clone["evidence_id"],
                "target_id": claim["claim_id"],
                "scope": "synthetic smoke",
            }
        )
        if mutation == "DUPLICATED_SUPPORT_WITH_RELATION":
            graph["relations"].append(
                {
                    "relation_id": "REL-AB-SHARED-SOURCE",
                    "relation_type": "SHARES_SOURCE_ROOT",
                    "source_id": source["evidence_id"],
                    "target_id": clone["evidence_id"],
                    "scope": "synthetic shared source root, not independent",
                }
            )
    else:
        raise AssertionError(f"unapproved mutation: {mutation}")
    return graph


def _direct(graph: dict) -> tuple[bool, str]:
    try:
        validate_claim_graph(graph)
    except ValueError as exc:
        return False, str(exc)
    return True, "STRUCTURAL_ONLY"


def _fixed_cli(graph: dict, tmp_path: Path) -> tuple[bool, str]:
    """A deterministic CLI proxy, NOT a complete fixed-workflow agent."""
    disposable = tmp_path / "candidate.json"
    disposable.write_text(json.dumps(graph, sort_keys=True), encoding="utf-8")
    validator = ROOT / MANIFEST["provenance"]["validator_path"]
    process = subprocess.run(
        [sys.executable, str(validator), str(disposable)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert process.returncode in {0, 1}, (
        f"CLI process/setup error, not a graph verdict: {process.returncode}: " f"{process.stderr[-500:]}"
    )
    return process.returncode == 0, process.stdout + process.stderr


def test_ab_smoke_manifest_is_source_bound_and_non_authorizing() -> None:
    provenance = MANIFEST["provenance"]
    assert MANIFEST["record_type"] == "AGENT_INSTRUMENT_AB_SMOKE_MANIFEST_V0_1"
    assert provenance["protected_main_commit"] == "1a95b94332dffb404c5a3ce026d70781a8c10b90"
    assert _git_blob_sha1(ROOT / provenance["graph_fixture_path"]) == provenance["graph_fixture_git_blob_sha1"]
    assert _git_blob_sha1(ROOT / provenance["validator_path"]) == provenance["validator_git_blob_sha1"]
    assert MANIFEST["interface_surfaces"]["C_INSTRUMENT"] == "NOT_IMPLEMENTED"
    state = MANIFEST["result_state"]
    assert state["scientific_n_increment"] == 0
    assert state["agent_trial_count"] == 0
    assert state["experiment_trial_count"] == 0
    assert state["claim_truth_effect"] == "NONE"
    assert state["authorization_effect"] == "NONE"
    assert state["external_effects"] == "PROHIBITED"
    assert state["independence"] == "NOT_ESTABLISHED"
    assert len(CASES) == 6
    assert {case["mutation"] for case in CASES} == {
        "NONE",
        "UNKNOWN_EVIDENCE",
        "DROP_SUPPORT_RELATION",
        "TRIGGERED_DEFEATER_CURRENT",
        "DUPLICATED_SUPPORT_SHARED_ROOT",
        "DUPLICATED_SUPPORT_WITH_RELATION",
    }
    assert len({case["id"] for case in CASES}) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_direct_and_fixed_cli_agree_on_synthetic_structure(case: dict, tmp_path: Path) -> None:
    graph = _candidate(case["mutation"])
    direct_pass, direct_feedback = _direct(copy.deepcopy(graph))
    cli_pass, cli_feedback = _fixed_cli(copy.deepcopy(graph), tmp_path)

    expected_pass = case["expected"] == "PASS"
    assert case["expected"] in {"PASS", "REJECT"}
    assert direct_pass == expected_pass, f"unexpected direct validator result for {case['id']}: {direct_feedback}"
    assert cli_pass == expected_pass, f"unexpected CLI validator result for {case['id']}: {cli_feedback[-500:]}"
    assert direct_pass == cli_pass  # matched validator entry points, not agent parity
    if expected_pass:
        assert case["error_fragment"] is None
        assert "STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_PASS_STRUCTURAL_ONLY" in cli_feedback
    else:
        fragment = case["error_fragment"]
        assert isinstance(fragment, str) and fragment
        assert fragment in direct_feedback
        assert fragment in cli_feedback
