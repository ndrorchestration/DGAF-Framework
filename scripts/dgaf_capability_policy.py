from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


@dataclass(frozen=True)
class Authority:
    capabilities: frozenset[str]
    resources: frozenset[str]
    max_budget: int | None = None


def intersect_authority(*authorities: Authority) -> Authority:
    if not authorities:
        raise ValueError("at least one authority is required")
    capabilities = set(authorities[0].capabilities)
    resources = set(authorities[0].resources)
    budgets = []
    for authority in authorities:
        capabilities.intersection_update(authority.capabilities)
        resources.intersection_update(authority.resources)
        if authority.max_budget is not None:
            budgets.append(authority.max_budget)
    return Authority(
        capabilities=frozenset(capabilities),
        resources=frozenset(resources),
        max_budget=min(budgets) if budgets else None,
    )


def delegation_is_non_widening(parent: Authority, child: Authority) -> bool:
    if not child.capabilities.issubset(parent.capabilities):
        return False
    if not child.resources.issubset(parent.resources):
        return False
    if parent.max_budget is not None:
        if child.max_budget is None or child.max_budget > parent.max_budget:
            return False
    return True


def authorization_is_active(
    status: str,
    *,
    not_before: datetime,
    expires_at: datetime,
    now: datetime | None = None,
) -> bool:
    now = now or datetime.now(timezone.utc)
    if status != "ACTIVE":
        return False
    return not_before <= now < expires_at


def approval_matches_commit(
    *,
    approved_digest: str,
    commit_digest: str,
    authorization_status: str,
    consumed: bool,
) -> bool:
    if consumed:
        return False
    if authorization_status != "ACTIVE":
        return False
    return approved_digest == commit_digest


def commit_guards_pass(
    required: dict[str, Any],
    observed: dict[str, Any],
) -> bool:
    for key, expected in required.items():
        if key not in observed:
            return False
        if observed[key] != expected:
            return False
    return True


def permitted_by_effective_authority(
    capability: str,
    resource: str,
    *,
    requester: Authority,
    delegation: Authority,
    executor: Authority,
    policy: Authority,
) -> bool:
    effective = intersect_authority(requester, delegation, executor, policy)
    return capability in effective.capabilities and resource in effective.resources


def all_links_non_widening(chain: Iterable[tuple[Authority, Authority]]) -> bool:
    return all(delegation_is_non_widening(parent, child) for parent, child in chain)
