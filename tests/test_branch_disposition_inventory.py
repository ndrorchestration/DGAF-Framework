from scripts.inventory_branch_disposition import (
    ACTIVE,
    MERGED,
    REVIEW,
    CompareFacts,
    classify_branch,
)


def facts(status: str, ahead: int, behind: int) -> CompareFacts:
    return CompareFacts(status=status, ahead_by=ahead, behind_by=behind, branch_sha="a" * 40)


def test_open_pr_head_is_always_active():
    assert classify_branch(is_open_pr_head=True, facts=facts("behind", 0, 3)) == ACTIVE


def test_fully_merged_behind_branch_is_safe_candidate():
    assert classify_branch(is_open_pr_head=False, facts=facts("behind", 0, 8)) == MERGED


def test_identical_branch_is_safe_candidate():
    assert classify_branch(is_open_pr_head=False, facts=facts("identical", 0, 0)) == MERGED


def test_ahead_branch_requires_review():
    assert classify_branch(is_open_pr_head=False, facts=facts("ahead", 2, 0)) == REVIEW


def test_diverged_branch_requires_review_even_if_some_history_is_merged():
    assert classify_branch(is_open_pr_head=False, facts=facts("diverged", 3, 9)) == REVIEW


def test_ambiguous_status_requires_review():
    assert classify_branch(is_open_pr_head=False, facts=facts("unknown", 0, 0)) == REVIEW


def test_lookup_error_requires_review():
    assert classify_branch(is_open_pr_head=False, facts=None, error="HTTPError") == REVIEW
