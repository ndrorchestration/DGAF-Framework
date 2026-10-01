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

__all__ = [
    "ChangeIdentity",
    "GateReceipt",
    "GateRequirement",
    "PromotionPolicy",
    "PromotionReason",
    "PromotionReceipt",
    "UpstreamDecision",
    "assess_promotion",
]

__version__ = "0.0.0.dev0"
