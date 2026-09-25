from __future__ import annotations

from datetime import datetime, timedelta, timezone

from scripts.dgaf_capability_policy import (
    Authority,
    all_links_non_widening,
    approval_matches_commit,
    authorization_is_active,
    commit_guards_pass,
    delegation_is_non_widening,
    intersect_authority,
    permitted_by_effective_authority,
)


def auth(capabilities, resources, budget=None):
    return Authority(
        capabilities=frozenset(capabilities),
        resources=frozenset(resources),
        max_budget=budget,
    )


def test_g11_child_delegation_cannot_add_capability():
    parent = auth({"repo.read"}, {"repo:a"}, 100)
    child = auth({"repo.read", "repo.write"}, {"repo:a"}, 100)
    assert delegation_is_non_widening(parent, child) is False


def test_g11_child_delegation_cannot_expand_resource_scope():
    parent = auth({"repo.read"}, {"repo:a"}, 100)
    child = auth({"repo.read"}, {"repo:a", "repo:b"}, 100)
    assert delegation_is_non_widening(parent, child) is False


def test_g11_child_delegation_cannot_expand_budget():
    parent = auth({"repo.read"}, {"repo:a"}, 100)
    child = auth({"repo.read"}, {"repo:a"}, 101)
    assert delegation_is_non_widening(parent, child) is False


def test_g11_chain_requires_every_link_to_attenuate():
    root = auth({"read", "write"}, {"a", "b"}, 10)
    middle = auth({"read"}, {"a"}, 5)
    child = auth({"read"}, {"a"}, 4)
    assert all_links_non_widening([(root, middle), (middle, child)]) is True


def test_confused_deputy_intersection_blocks_executor_only_power():
    requester = auth({"repo.read"}, {"repo:a"})
    delegation = auth({"repo.read"}, {"repo:a"})
    executor = auth({"repo.read", "repo.delete"}, {"repo:a"})
    policy = auth({"repo.read", "repo.delete"}, {"repo:a"})
    assert (
        permitted_by_effective_authority(
            "repo.delete",
            "repo:a",
            requester=requester,
            delegation=delegation,
            executor=executor,
            policy=policy,
        )
        is False
    )


def test_effective_authority_is_intersection():
    a = auth({"read", "write"}, {"a", "b"}, 100)
    b = auth({"read"}, {"a", "b"}, 50)
    c = auth({"read", "delete"}, {"a"}, 25)
    result = intersect_authority(a, b, c)
    assert result.capabilities == frozenset({"read"})
    assert result.resources == frozenset({"a"})
    assert result.max_budget == 25


def test_g12_consumed_approval_cannot_replay():
    digest = "sha256:" + "a" * 64
    assert (
        approval_matches_commit(
            approved_digest=digest,
            commit_digest=digest,
            authorization_status="ACTIVE",
            consumed=True,
        )
        is False
    )


def test_g12_digest_substitution_is_blocked():
    assert (
        approval_matches_commit(
            approved_digest="sha256:" + "a" * 64,
            commit_digest="sha256:" + "b" * 64,
            authorization_status="ACTIVE",
            consumed=False,
        )
        is False
    )


def test_g9_revoked_authorization_is_inactive():
    now = datetime(2026, 9, 25, 12, tzinfo=timezone.utc)
    assert (
        authorization_is_active(
            "REVOKED",
            not_before=now - timedelta(minutes=5),
            expires_at=now + timedelta(minutes=5),
            now=now,
        )
        is False
    )


def test_expired_authorization_is_inactive():
    now = datetime(2026, 9, 25, 12, tzinfo=timezone.utc)
    assert (
        authorization_is_active(
            "ACTIVE",
            not_before=now - timedelta(minutes=10),
            expires_at=now,
            now=now,
        )
        is False
    )


def test_g13_missing_commit_guard_fails_closed():
    required = {"branch_sha": "abc", "allowlist_version": "42"}
    observed = {"branch_sha": "abc"}
    assert commit_guards_pass(required, observed) is False


def test_g13_changed_commit_guard_fails_closed():
    required = {"branch_sha": "abc"}
    observed = {"branch_sha": "def"}
    assert commit_guards_pass(required, observed) is False


def test_matching_commit_guards_pass():
    required = {"branch_sha": "abc", "allowlist_version": "42"}
    observed = {"branch_sha": "abc", "allowlist_version": "42"}
    assert commit_guards_pass(required, observed) is True
