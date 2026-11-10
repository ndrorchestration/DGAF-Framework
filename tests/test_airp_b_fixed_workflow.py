"""AIRP B-FIXED Phase 2: bounded synthetic positive/negative tests, not agent trials."""
from __future__ import annotations

import base64
import copy
import hashlib

import pytest

from scripts import airp_b_fixed_workflow as b

CLAIM = "CLAIM-BFIX-002"
COUNTER = "EVID-REFERENCE-COUNTER"


def cmd(op: str, args: dict, version: int = 0, branch: str = "base", request: str = "REQ-01") -> dict:
    return {
        "op": op, "branch": branch, "expected_version": version,
        "request_id": request, "args": args,
    }


def add(version: int = 0, branch: str = "base", request: str = "REQ-ADD") -> dict:
    return cmd(
        "add_claim", {"claim_id": CLAIM, "proposition": "Synthetic scoped proposition."},
        version, branch, request,
    )


def attach(version: int = 1, digest: str | None = None) -> dict:
    raw = b"source-locked synthetic evidence bytes"
    return cmd(
        "attach_evidence",
        {
            "claim_id": CLAIM,
            "evidence_node": {
                "evidence_id": "EVID-BFIX-SUPPORT",
                "evidence_class": "DERIVATION",
                "source_roots": ["b-fixed-synthetic-root"],
                "dependency_roots": [],
                "observed_at": "2026-11-09",
                "validity": {
                    "state": "CURRENT",
                    "review_condition": "revalidate on any source change",
                },
                "provenance_ref": "fixture://airp-b-fixed/synthetic",
            },
            "evidence_object": {
                "evidence_id": "EVID-BFIX-SUPPORT",
                "evidence_type": "SYNTHETIC_FIXTURE",
                "digest_algorithm": "sha256",
                "content_digest": digest or hashlib.sha256(raw).hexdigest(),
                "source_class": "SYNTHETIC_TEST",
            },
            "evidence_bytes_b64": base64.b64encode(raw).decode("ascii"),
        },
        version, request="REQ-EVID",
    )


def assert_no_authority(result: dict) -> None:
    assert result["authorization_effect"] == "NONE"
    assert result["truth_effect"] == "NONE"
    assert result["external_effects"] == "NONE"
    assert result["independence_effect"] == "NONE"


def test_source_locks_and_disposable_reference() -> None:
    workflow = b.FixedWorkflow()
    reference = workflow.snapshot()
    assert reference["graph_id"] == "EGRAPH-REFERENCE-001"
    assert len(reference["claims"]) == 1
    reference["claims"].clear()
    assert len(workflow.snapshot()["claims"]) == 1


def test_fails_closed_if_main_source_bytes_drift(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(b, "LOCKED_GIT_BLOBS", {b.FIXTURE: "0" * 40})
    with pytest.raises(ValueError, match="SOURCE_LOCK_MISMATCH"):
        b.FixedWorkflow()


def test_preplanned_six_operation_sequence_and_non_authority() -> None:
    workflow = b.FixedWorkflow()
    plan = {
        "record_type": "AIRP_B_FIXED_PLAN",
        "schema_version": 1,
        "source_commit": b.PROTECTED_MAIN,
        "steps": [
            cmd("inspect", {"attribution_observation": None}, request="REQ-I0"),
            add(),
            attach(),
            cmd("challenge", {"claim_id": CLAIM, "counterevidence_id": COUNTER}, 2, request="REQ-CH"),
            cmd("fork", {"new_branch": "candidate"}, 3, request="REQ-F"),
            cmd(
                "compare", {"other_branch": "candidate", "other_version": 0},
                3, request="REQ-CO",
            ),
        ],
    }
    result = workflow.run_plan(plan)
    assert result["outcome"] == "COMPLETED_SYNTHETIC_ONLY"
    assert len(result["step_results"]) == 6
    assert len(result["lineage"]) == 6
    assert result["scientific_n_increment"] == 0
    assert result["high_assurance"] == "NOT_AUTHORIZED"
    for step in result["step_results"]:
        assert step["status"] == "ACCEPTED_SYNTHETIC_ONLY"
        assert_no_authority(step)
    assert result["step_results"][2]["admission_class"] == "EVIDENCE_GATE_ADMITTED_SYNTHETIC_ONLY"
    assert result["step_results"][-1]["comparison"]["left_digest"] == result["step_results"][-1]["comparison"]["right_digest"]
    assert workflow.snapshot()["claims"][-1]["applicability_state"] == "CHALLENGED"
    assert workflow.snapshot("candidate") == workflow.snapshot()


def test_explicit_proposed_claim_ceiling() -> None:
    workflow = b.FixedWorkflow()
    result = workflow.execute(add())
    assert result["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    claim = workflow.snapshot()["claims"][-1]
    assert claim["verification_status"] == "NOT_VERIFIED"
    assert claim["epistemic_state"] == "PROPOSED"
    assert claim["authorization_relevance"] == "NONE"
    assert claim["supporting_evidence_ids"] == []


def test_gate_digest_mismatch_rejects_without_state_change() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    before = workflow.snapshot()
    result = workflow.execute(attach(digest="0" * 64))
    assert result["status"] == "REJECTED"
    assert "EVIDENCE_GATE_REJECTED" in result["reason"]
    assert workflow.snapshot() == before
    assert_no_authority(result)


def test_bad_base64_is_fail_closed() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    command = attach()
    command["args"]["evidence_bytes_b64"] = "not base64!@"
    result = workflow.execute(command)
    assert result["status"] == "REJECTED"
    assert len(workflow.snapshot()["evidence"]) == 2


def test_duplicate_evidence_rejected_without_partial_append() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    assert workflow.execute(attach())["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    again = attach(version=2)
    again["request_id"] = "REQ-EVID2"
    result = workflow.execute(again)
    assert result["status"] == "REJECTED"
    assert len(workflow.snapshot()["evidence"]) == 3


def test_challenge_requires_known_counterevidence() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    result = workflow.execute(
        cmd("challenge", {"claim_id": CLAIM, "counterevidence_id": "EVID-MISSING"}, 1)
    )
    assert result["status"] == "REJECTED"
    assert workflow.snapshot()["claims"][-1]["applicability_state"] == "CURRENT"


def test_stale_compare_and_mutation_rejected() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    stale = workflow.execute(
        cmd("inspect", {"attribution_observation": None}, 0, request="REQ-STALE")
    )
    assert stale["status"] == "REJECTED"
    assert "STALE" in stale["reason"]
    assert len(workflow.snapshot()["claims"]) == 2


def test_idempotent_replay_and_conflict() -> None:
    workflow = b.FixedWorkflow()
    first = add()
    result = workflow.execute(first)
    assert workflow.execute(copy.deepcopy(first)) == result
    assert len(workflow.snapshot()["claims"]) == 2
    changed = copy.deepcopy(first)
    changed["args"]["proposition"] = "a different request with the same idempotency key"
    collision = workflow.execute(changed)
    assert collision["status"] == "REJECTED"
    assert collision["reason"] == "IDEMPOTENCY_KEY_CONFLICT"


def test_fork_is_branch_version_copy_not_external_rollback() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(cmd("fork", {"new_branch": "alternative"}, request="REQ-FORK"))
    assert workflow.snapshot("alternative") == workflow.snapshot("base", 0)
    new = workflow.execute(add(branch="alternative"))
    assert new["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    assert len(workflow.snapshot("alternative")["claims"]) == 2
    assert len(workflow.snapshot("base")["claims"]) == 1
    comparison = workflow.execute(
        cmd("compare", {"other_branch": "alternative", "other_version": 1}, request="REQ-DIFF")
    )
    assert comparison["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    assert comparison["comparison"]["structural_difference_only"]["claims"]["only_right"] == [CLAIM]
    assert comparison["comparison"]["semantic_oracle_effect"] == "NONE"


def test_rejected_unauthorized_tool_call() -> None:
    workflow = b.FixedWorkflow()
    denial = workflow.execute(cmd("send_email", {"to": "nobody@example.com"}))
    assert denial["status"] == "REJECTED"
    assert_no_authority(denial)
    assert workflow.snapshot() == b.FixedWorkflow().snapshot()


def test_disallows_user_supplied_verification_or_permission_on_claim() -> None:
    workflow = b.FixedWorkflow()
    command = add()
    command["args"]["epistemic_state"] = "EMPIRICALLY_SUPPORTED"
    denial = workflow.execute(command)
    assert denial["status"] == "REJECTED"
    assert len(workflow.snapshot()["claims"]) == 1


def test_invalid_relation_and_shared_source_dependency_stay_validated() -> None:
    workflow = b.FixedWorkflow()
    workflow.execute(add())
    command = attach()
    command["args"]["evidence_node"]["source_roots"] = ["support-root"]
    assert workflow.execute(command)["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    # The new proposed claim alone has the extra supporting node; it does not
    # have a second support with the same root, so there is no false independence.
    assert workflow.snapshot()["claims"][-1]["epistemic_state"] == "PROPOSED"


def test_attribution_observation_is_non_verifying() -> None:
    workflow = b.FixedWorkflow()
    obs = {
        "record_class": "CLAIMGRAPH_ATTRIBUTION_OBSERVATION_V0",
        "graph_id": "EGRAPH-REFERENCE-001",
        "records": [{
            "evidence_id": "EVID-REFERENCE-SUPPORT",
            "attribution_source_ref": "synthetic://producer-claim",
            "producer_class": "INTERNAL_SAME_SYSTEM",
            "producer_identity_ref": "synthetic-internal-fixture",
            "attribution_state": "CLAIMED_UNVERIFIED",
            "independence_claimed": False,
            "independence_basis_refs": [],
            "independence_adjudication_state": "NOT_EXECUTED",
            "adjudication_ref": None,
        }],
    }
    result = workflow.execute(cmd("inspect", {"attribution_observation": obs}))
    assert result["status"] == "ACCEPTED_SYNTHETIC_ONLY"
    assert result["attribution"]["observation_authority"] == "CALLER_SUPPLIED_NOT_REVERIFIED"
    assert result["attribution"]["independence_effect"] == "NONE"


def test_bad_observation_does_not_change_state() -> None:
    workflow = b.FixedWorkflow()
    result = workflow.execute(cmd("inspect", {"attribution_observation": {"invalid": True}}))
    assert result["status"] == "REJECTED"
    assert workflow.snapshot() == b.FixedWorkflow().snapshot()


def test_plan_stops_on_first_rejected_step() -> None:
    workflow = b.FixedWorkflow()
    result = workflow.run_plan({
        "record_type": "AIRP_B_FIXED_PLAN",
        "schema_version": 1,
        "source_commit": b.PROTECTED_MAIN,
        "steps": [
            add(),
            cmd("challenge", {"claim_id": CLAIM, "counterevidence_id": "EVID-MISSING"}, 1, request="REQ-BAD"),
            attach(version=1),
        ],
    })
    assert result["outcome"] == "STOPPED_ON_REJECTION"
    assert len(result["step_results"]) == 2
    assert len(workflow.snapshot()["claims"]) == 2
    assert len(workflow.snapshot()["evidence"]) == 2


def test_source_commit_mismatch_blocks_plan() -> None:
    workflow = b.FixedWorkflow()
    with pytest.raises(ValueError, match="INVALID_PLAN_IDENTITY"):
        workflow.run_plan({
            "record_type": "AIRP_B_FIXED_PLAN", "schema_version": 1,
            "source_commit": "0" * 40, "steps": [add()],
        })


def test_replay_existing_revision_never_promotes_scientific_state() -> None:
    workflow = b.FixedWorkflow()
    first = workflow.execute(add())
    replay = workflow.execute(add())
    assert replay == first
    assert replay["authorization_effect"] == "NONE"
    assert workflow.snapshot()["claims"][-1]["verification_status"] == "NOT_VERIFIED"
