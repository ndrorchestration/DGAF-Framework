"""Research-only composition baseline over an existing ClaimGraph validator.

These are dictionary edits to *disposable copies*, not implemented Agent
Instrument controls, a version store, or an authorization interface.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads(
    (ROOT / "docs/research/fixtures/AGENT_INSTRUMENT_AB_SMOKE_MANIFEST_V0_1.json").read_text(encoding="utf-8")
)


def _source_graph() -> dict:
    provenance = MANIFEST["provenance"]
    path = ROOT / provenance["graph_fixture_path"]
    raw = path.read_bytes()
    git_blob = hashlib.sha1(f"blob {len(raw)}".encode("ascii") + bytes([0]) + raw).hexdigest()  # noqa: S324
    assert git_blob == provenance["graph_fixture_git_blob_sha1"]
    return json.loads(raw)


def _stable_digest(graph: dict) -> str:
    """Fingerprint a disposable snapshot only; no signature or custody effect."""
    return hashlib.sha256(json.dumps(graph, sort_keys=True).encode("utf-8")).hexdigest()


def test_five_proposed_controls_can_be_represented_as_manual_synthetic_edits() -> None:
    source = _source_graph()
    validate_claim_graph(copy.deepcopy(source))
    original_digest = _stable_digest(source)

    # fork: independent in-memory candidate, NOT a versioned/CAS branch API
    candidate = copy.deepcopy(source)
    assert candidate is not source

    # add_claim: a second proposed, unverified and non-authorizing scoped claim
    new_claim = copy.deepcopy(candidate["claims"][0])
    new_claim["claim_id"] = "CLAIM-AB-PROPOSED-002"
    new_claim["proposition"] = "Synthetic claim added only inside a disposable graph."
    new_claim["epistemic_state"] = "PROPOSED"
    new_claim["verification_status"] = "NOT_VERIFIED"
    new_claim["authorization_relevance"] = "NONE"
    new_claim["supporting_evidence_ids"] = []
    new_claim["contradicting_evidence_ids"] = []
    new_claim["defeaters"] = []
    new_claim["applicability_state"] = "CHALLENGED"
    candidate["claims"].append(new_claim)
    validate_claim_graph(candidate)

    # attach_evidence: create a new synthetic evidence node and matching edge.
    support = copy.deepcopy(candidate["evidence"][0])
    support["evidence_id"] = "EVID-AB-COMPOSITION-SUPPORT"
    support["source_roots"] = ["synthetic-composition-root"]
    support["provenance_ref"] = "fixture://composition-support"
    candidate["evidence"].append(support)
    new_claim["supporting_evidence_ids"].append(support["evidence_id"])
    relation = {
        "relation_id": "REL-AB-COMPOSITION-SUPPORT",
        "relation_type": "SUPPORTS",
        "source_id": support["evidence_id"],
        "target_id": new_claim["claim_id"],
        "scope": "synthetic composition check",
    }
    candidate["relations"].append(relation)
    validate_claim_graph(candidate)
    assert new_claim["epistemic_state"] == "PROPOSED"

    # challenge: introduce explicit counterevidence, state, and triggered defeater.
    counter = copy.deepcopy(candidate["evidence"][1])
    counter["evidence_id"] = "EVID-AB-COMPOSITION-COUNTER"
    counter["source_roots"] = ["synthetic-counter-root"]
    counter["provenance_ref"] = "fixture://composition-counter"
    candidate["evidence"].append(counter)
    new_claim["contradicting_evidence_ids"].append(counter["evidence_id"])
    candidate["relations"].append(
        {
            "relation_id": "REL-AB-COMPOSITION-COUNTER",
            "relation_type": "CONTRADICTS",
            "source_id": counter["evidence_id"],
            "target_id": new_claim["claim_id"],
            "scope": "synthetic challenge only",
        }
    )
    new_claim["defeaters"] = [
        {"defeater_id": "DEF-AB-COMPOSITION", "condition": "synthetic counterexample", "status": "TRIGGERED"}
    ]
    new_claim["applicability_state"] = "CHALLENGED"
    validate_claim_graph(candidate)

    # A prohibited state change is caught by the existing validator.
    invalid = copy.deepcopy(candidate)
    invalid["claims"][-1]["applicability_state"] = "CURRENT"
    with pytest.raises(ValueError, match="triggered defeater but remains CURRENT"):
        validate_claim_graph(invalid)
    assert new_claim["applicability_state"] == "CHALLENGED"

    # compare: source-locked deterministic snapshot DIFFERENCE; not semantic diff.
    assert _stable_digest(source) == original_digest
    assert _stable_digest(candidate) != original_digest
    assert len(candidate["claims"]) == len(source["claims"]) + 1
    assert len(candidate["evidence"]) == len(source["evidence"]) + 2
    assert len(candidate["relations"]) == len(source["relations"]) + 2
    assert new_claim["authorization_relevance"] == "NONE"
    assert new_claim["verification_status"] == "NOT_VERIFIED"
    assert new_claim["epistemic_state"] == "PROPOSED"
    validate_claim_graph(source)
