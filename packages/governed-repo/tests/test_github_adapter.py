import pytest

from governed_repo import (
    assess_github_promotion,
    GateRequirement,
    gate_receipt_from_check_run,
    GitHubAdapterInputError,
    PromotionPolicy,
    PromotionReason,
)


def pull_request(**overrides):
    value = {
        "number": 42,
        "base": {"sha": "base123"},
        "head": {"sha": "head456"},
        "merge_commit_sha": "merge789",
    }
    value.update(overrides)
    return value


def check_run(**overrides):
    value = {
        "name": "ci",
        "status": "completed",
        "conclusion": "success",
        "head_sha": "head456",
        "completed_at": "2026-10-01T17:00:00Z",
        "app": {"slug": "github-actions", "id": 15368},
    }
    value.update(overrides)
    return value


def policy(*, require_base_binding=False):
    return PromotionPolicy(
        required_gates=(
            GateRequirement(
                gate_id="ci",
                gate_class="quality",
                require_head_binding=True,
                require_base_binding=require_base_binding,
            ),
        )
    )


def assess(pr=None, checks=None, **kwargs):
    values = {
        "repository": "example/repo",
        "pull_request": pull_request() if pr is None else pr,
        "check_runs": [check_run()] if checks is None else checks,
        "expected_base_sha": "base123",
        "expected_head_sha": "head456",
        "observed_at": "2026-10-01T17:01:00Z",
        "policy": policy(),
    }
    values.update(kwargs)
    return assess_github_promotion(**values)


def test_exact_pr_and_check_are_eligible_without_effects():
    receipt = assess()

    assert receipt.eligible is True
    assert receipt.reason_code is PromotionReason.ELIGIBLE_FOR_PROMOTION
    assert receipt.merge_executed is False
    assert receipt.mutation_executed is False
    assert receipt.authorization_effect == "NONE"


def test_stale_pr_base_denies():
    receipt = assess(pr=pull_request(base={"sha": "older-base"}))

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.STALE_BASE


def test_head_identity_mismatch_denies():
    receipt = assess(pr=pull_request(head={"sha": "other-head"}))

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.HEAD_IDENTITY_MISMATCH


def test_missing_required_check_denies():
    receipt = assess(checks=[])

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_MISSING


def test_nonterminal_check_denies():
    receipt = assess(checks=[check_run(status="in_progress", conclusion=None)])

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_NOT_TERMINAL


def test_failed_check_denies():
    receipt = assess(checks=[check_run(conclusion="failure")])

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_FAILED


def test_duplicate_check_name_fails_closed_as_missing_unique_receipt():
    receipt = assess(checks=[check_run(), check_run()])

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_MISSING


def test_check_run_preserves_source_identity_as_observation_only():
    receipt = gate_receipt_from_check_run(check_run())

    assert receipt.source_identity == "github-app:github-actions:15368"
    assert receipt.head_sha == "head456"
    assert receipt.base_sha is None


def test_raw_check_run_does_not_claim_base_binding():
    receipt = assess(policy=policy(require_base_binding=True))

    assert receipt.eligible is False
    assert receipt.reason_code is PromotionReason.REQUIRED_CHECK_FAILED


def test_malformed_pull_request_fails_without_guessing():
    with pytest.raises(GitHubAdapterInputError):
        assess(pr={"number": 42, "base": {}, "head": {"sha": "head456"}})


def test_malformed_check_run_fails_without_guessing():
    with pytest.raises(GitHubAdapterInputError):
        assess(checks=[{"name": "ci", "status": "completed"}])
