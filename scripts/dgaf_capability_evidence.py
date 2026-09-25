from __future__ import annotations

from enum import IntEnum

from scripts.dgaf_capability_policy import Authority


class EvidenceStrength(IntEnum):
    UNKNOWN = 0
    ASSERTED = 1
    CORROBORATED = 2
    VERIFIED = 3
    INDEPENDENTLY_VERIFIED = 4


def authority_is_subset(child: Authority, parent: Authority) -> bool:
    if not child.capabilities.issubset(parent.capabilities):
        return False
    if not child.resources.issubset(parent.resources):
        return False
    if parent.max_budget is not None:
        if child.max_budget is None or child.max_budget > parent.max_budget:
            return False
    return True


def evidence_authority_monotonic(
    *,
    prior_strength: EvidenceStrength,
    prior_authority: Authority,
    new_strength: EvidenceStrength,
    new_authority: Authority,
) -> bool:
    """Enforce G16 for the same policy and scope.

    If evidence weakens or stays equal, resulting authority must not grow.
    Stronger evidence may support broader authority only if some separate
    policy rule grants it; this function does not grant authority itself.
    """
    if new_strength <= prior_strength:
        return authority_is_subset(new_authority, prior_authority)
    return True


def verification_implies_authorization(*, verified: bool, authorization_status: str) -> bool:
    """Return True only when authorization independently exists.

    This intentionally prevents verification success from manufacturing
    authorization (G5).
    """
    return verified and authorization_status == "ACTIVE"
