"""Compatibility surface for Governed Repo.

The canonical implementation lives in the isolated package source at
`packages/governed-repo/src/governed_repo/core.py`.

This module intentionally contains no independent promotion semantics. It
temporarily preserves the historical `components.governed_repo` import path
for DGAF callers while re-exporting the canonical package objects.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PACKAGE_SRC = Path(__file__).resolve().parents[1] / "packages" / "governed-repo" / "src"
_PACKAGE_SRC_STR = str(_PACKAGE_SRC)
_added_path = _PACKAGE_SRC_STR not in sys.path

if _added_path:
    sys.path.insert(0, _PACKAGE_SRC_STR)

try:
    from governed_repo.core import (  # noqa: E402
        ChangeIdentity,
        GateReceipt,
        GateRequirement,
        PromotionPolicy,
        PromotionReason,
        PromotionReceipt,
        UpstreamDecision,
        assess_promotion,
    )
finally:
    if _added_path:
        sys.path.remove(_PACKAGE_SRC_STR)

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
