"""Public API for the Governed Repo v0 package candidate."""

from .core import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    PromotionReason,
    PromotionReceipt,
    UpstreamDecision,
    assess_promotion,
)
from .github_adapter import (
    GitHubAdapterInputError,
    assess_github_promotion,
    change_identity_from_pull_request,
    gate_receipt_from_check_run,
)

__all__ = [
    "ChangeIdentity",
    "GateReceipt",
    "GateRequirement",
    "PromotionPolicy",
    "PromotionReason",
    "PromotionReceipt",
    "UpstreamDecision",
    "assess_promotion",
    "GitHubAdapterInputError",
    "assess_github_promotion",
    "change_identity_from_pull_request",
    "gate_receipt_from_check_run",
]

__version__ = "0.0.0.dev0"
