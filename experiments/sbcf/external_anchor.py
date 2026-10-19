"""Fail-closed external-anchor contract for synthetic SBCF recovery.

The anchor is supplied by a caller and MUST be verified by an independently
managed trust boundary before this contract can support any security claim.
"""

from dataclasses import dataclass
from typing import Callable

from .recovery import Disposition, RecoveryCheck


@dataclass(frozen=True)
class AnchorRecord:
    source: str
    run: str
    policy: str
    sequence: int
    checkpoint_id: str


def reconcile_with_anchor(
    local: RecoveryCheck,
    anchor: AnchorRecord | None,
    *,
    expected_source: str,
    expected_run: str,
    expected_policy: str,
    verify_anchor: Callable[[AnchorRecord], bool],
) -> RecoveryCheck:
    """Require a verified anchor that exactly matches the local high-water mark."""
    if local.disposition != Disposition.CONSISTENT:
        return RecoveryCheck(
            Disposition.BLOCKED, "LOCAL_RECOVERY_BLOCKED", local.evidence_sequence, local.witness_sequence
        )
    if anchor is None or not isinstance(anchor, AnchorRecord):
        return RecoveryCheck(
            Disposition.BLOCKED, "ANCHOR_MISSING_OR_INVALID", local.evidence_sequence, local.witness_sequence
        )
    if (
        anchor.source != expected_source
        or anchor.run != expected_run
        or anchor.policy != expected_policy
        or type(anchor.sequence) is not int
        or anchor.sequence < 0
        or not isinstance(anchor.checkpoint_id, str)
        or not anchor.checkpoint_id
    ):
        return RecoveryCheck(
            Disposition.BLOCKED, "ANCHOR_SCOPE_INVALID", local.evidence_sequence, local.witness_sequence
        )
    try:
        verified = verify_anchor(anchor)
    except Exception:
        verified = False
    if verified is not True:
        return RecoveryCheck(
            Disposition.BLOCKED, "ANCHOR_NOT_VERIFIED", local.evidence_sequence, local.witness_sequence
        )
    if anchor.sequence != local.evidence_sequence or anchor.sequence != local.witness_sequence:
        return RecoveryCheck(
            Disposition.BLOCKED, "ANCHOR_COUNTER_MISMATCH", local.evidence_sequence, local.witness_sequence
        )
    return RecoveryCheck(
        Disposition.CONSISTENT,
        "MATCHED_VERIFIED_ANCHOR_CONTRACT_ONLY",
        local.evidence_sequence,
        local.witness_sequence,
    )
