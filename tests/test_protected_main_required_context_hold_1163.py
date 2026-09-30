import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOLD_RECORD = REPO_ROOT / "docs" / "governance" / "PROTECTED_MAIN_REQUIRED_CONTEXT_HOLD_1163_2026-09-30.json"
POLICY_RECORD = REPO_ROOT / "docs" / "governance" / "PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_1163_required_context_hold_record_is_bounded_non_mutating_evidence():
    record = _load(HOLD_RECORD)

    assert record["record_type"] == "DGAF_PROTECTED_MAIN_REQUIRED_CONTEXT_HOLD"
    assert record["schema_version"] == 1
    assert record["related_pr"] == 1163
    assert record["related_issue"] == 277
    assert record["classification"] == "BRANCH_PROTECTION_CHECK_CONTEXT_VISIBILITY_HOLD"
    assert record["settings_mutation_performed"] is False
    assert record["scientific_n_increment"] == 0


def test_1163_hold_records_exact_heads_and_merge_rejection():
    record = _load(HOLD_RECORD)
    observed = record["observed_state"]

    assert observed["protected_main_sha"] == "01773b5dff37f8ded1df0ac2eb76148bd57ffaa8"
    assert observed["pr_head_sha"] == "ab56c766bc3637b6583be13ffba08221b940cd7f"
    assert observed["pr_state"] == "OPEN_READY_NON_DRAFT_MERGEABLE"
    assert observed["fresh_post_ready_guard"] == "SUCCESS"
    assert observed["visible_required_checks_green"] is True
    assert observed["pinned_head_squash_merge_attempt"] == "REJECTED_BY_BRANCH_PROTECTION"
    assert observed["merge_rejection_message"] == "3 of 3 required status checks are expected."
    assert "no evidenced repository test failure" in observed["failure_interpretation"]


def test_1163_hold_does_not_authorize_bypass_or_admin_mutation():
    record = _load(HOLD_RECORD)
    action = record["safe_next_action"]

    assert "Retry pinned-head merge only" in action["retry_condition"]
    assert action["bypass_authorized"] is False
    assert action["admin_settings_mutation_authorized"] is False
    assert action["routine_code_or_workflow_mutation_authorized_by_this_record"] is False


def test_1163_hold_is_consistent_with_required_context_policy():
    record = _load(HOLD_RECORD)
    policy = _load(POLICY_RECORD)

    assert record["policy_context"]["source_policy_record"] == "docs/governance/PROTECTED_MAIN_REQUIRED_CONTEXT_POLICY_V1.json"
    assert record["policy_context"]["global_required_context_hygiene"] == policy["observed_state"]["global_required_context_hygiene"]
    assert record["policy_context"]["literal_global_context_list_authorized_for_application"] is False
    assert policy["application_protocol"]["literal_global_context_list_authorized_for_application"] is False
    assert policy["application_protocol"]["specialized_gate_strategy"] == record["policy_context"]["specialized_gate_strategy"]


def test_1163_hold_preserves_claim_boundary():
    record = _load(HOLD_RECORD)
    boundary = record["claim_boundary"]

    assert boundary["repository_admin_configuration_changed"] is False
    assert boundary["literal_admin_context_list_ready"] is False
    assert boundary["freeze_established"] is False
    assert boundary["empirical_execution_authorized"] is False
    assert boundary["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert boundary["independent_validation"] == "NOT_ESTABLISHED"
    assert boundary["high_assurance"] == "PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0"
