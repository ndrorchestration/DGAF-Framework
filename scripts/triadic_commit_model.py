"""Disposable, trusted-input commit model; not a DGAF authority or executor.

Models only atomic in-process admission and replay. No authenticated transport,
durable recovery, LLM evaluation, adaptive policy or external effects exist.
"""

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class Proposal:
    operation: str
    candidate: str
    evidence: str
    policy: str
    predecessor: int
    epoch: int
    checks_pass: bool
    objection: bool
    deadline: int


@dataclass(frozen=True)
class Receipt:
    outcome: str
    reason: str
    version: int
    epoch: int


class SyntheticController:
    """Single-process model with trusted fixture clock and authority inputs.

    Tests control authority and time explicitly; this is not authentication.
    All mutations share one lock. Replays return the original receipt even
    after revocation, without performing another transition.
    """

    def __init__(self, evidence: str, policy: str):
        self._lock = Lock()
        self._evidence = evidence
        self._policy = policy
        self._version = 0
        self._epoch = 0
        self._authorized = True
        self._accepted: str | None = None
        self._receipts: dict[str, tuple[Proposal, Receipt]] = {}

    def revoke(self):
        with self._lock:
            self._authorized = False

    def invalidate_epoch(self):
        """Fault injection only; does not implement an authorized mode switch."""
        with self._lock:
            self._epoch += 1

    def snapshot(self):
        with self._lock:
            return self._version, self._epoch, self._accepted

    def commit(self, proposal: Proposal, now: int) -> Receipt:
        with self._lock:

            def deny(reason):
                return Receipt("HOLD", reason, self._version, self._epoch)

            if type(proposal) is not Proposal:
                return deny("MALFORMED")
            if any(
                type(x) is not str or not x
                for x in (
                    proposal.operation,
                    proposal.candidate,
                    proposal.evidence,
                    proposal.policy,
                )
            ):
                return deny("MALFORMED")
            if (
                any(
                    type(x) is not int or x < 0
                    for x in (
                        proposal.predecessor,
                        proposal.epoch,
                        proposal.deadline,
                        now,
                    )
                )
                or type(proposal.checks_pass) is not bool
                or type(proposal.objection) is not bool
            ):
                return deny("MALFORMED")
            previous = self._receipts.get(proposal.operation)
            if previous is not None:
                original, receipt = previous
                return receipt if original == proposal else deny("ID_CONFLICT")
            if not self._authorized:
                reason = "REVOKED"
            elif proposal.epoch != self._epoch:
                reason = "STALE_EPOCH"
            elif proposal.predecessor != self._version:
                reason = "STALE_PREDECESSOR"
            elif proposal.evidence != self._evidence or proposal.policy != self._policy:
                reason = "IDENTITY_MISMATCH"
            elif now >= proposal.deadline:
                reason = "EXPIRED"
            elif not proposal.checks_pass or proposal.objection:
                reason = "INCOMPLETE_OR_OBJECTED"
            else:
                reason = None
            if reason is not None:
                receipt = deny(reason)
            else:
                self._version += 1
                self._accepted = proposal.candidate
                receipt = Receipt("COMMITTED_SYNTHETIC", "ELIGIBLE", self._version, self._epoch)
            self._receipts[proposal.operation] = (proposal, receipt)
            return receipt
