"""Fixture-key authenticated message boundary; no DGAF or production authority.

HMAC-SHA256 authenticates bytes only relative to pre-shared in-memory test keys.
This prototype has no secure key provisioning, transport, persistent ledger,
trusted clock, proof of agent independence, or external execution permissions.
"""

from dataclasses import dataclass, replace
from hashlib import sha256
from hmac import compare_digest, new
from json import dumps
from re import fullmatch
from threading import Lock

ROLE_KINDS = {
    "Generator": frozenset({"CANDIDATE"}),
    "Critic": frozenset({"ASSESSMENT", "OBJECTION"}),
    "Governor": frozenset({"RESOLUTION"}),
}
VERSION = "triad-mac-v0.1"


@dataclass(frozen=True)
class SignedMessage:
    version: str
    run_id: str
    message_id: str
    sender_id: str
    sender_role: str
    recipient_id: str
    kind: str
    epoch: int
    predecessor: int
    deadline: int
    candidate_digest: str
    evidence_digest: str
    policy_digest: str
    content: str
    content_digest: str
    mac: str = ""


@dataclass(frozen=True)
class MessageReceipt:
    outcome: str
    reason: str
    accepted_sequence: int


def digest_text(content: str) -> str:
    """Digest UTF-8 fixture content; hashes never authenticate a sender."""
    return sha256(content.encode("utf-8")).hexdigest()


def signed_bytes(message: SignedMessage) -> bytes:
    """Exact signed fields in deterministic JSON; MAC is deliberately excluded."""
    fields = (
        "version", "run_id", "message_id", "sender_id", "sender_role",
        "recipient_id", "kind", "epoch", "predecessor", "deadline",
        "candidate_digest", "evidence_digest", "policy_digest", "content",
        "content_digest",
    )
    return dumps(
        {field: getattr(message, field) for field in fields},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def sign_fixture(message: SignedMessage, key: bytes) -> SignedMessage:
    """Test helper. Caller-held key is not a credential issuer or validation."""
    return replace(message, mac=new(key, signed_bytes(message), "sha256").hexdigest())


class SyntheticMessageBoundary:
    """Single-run authenticated-message admission, with in-process replay lock.

    Only messages, not controller commits or external actions, are admitted.
    Replays return historical receipts even after revocation without new effects.
    """

    def __init__(
        self,
        run_id: str,
        identities: dict[str, str],
        fixture_keys: dict[str, bytes],
        candidate_digest: str,
        evidence_digest: str,
        policy_digest: str,
    ):
        if type(run_id) is not str or not run_id or type(identities) is not dict or type(fixture_keys) is not dict:
            raise ValueError("BAD_MANIFEST")
        if (
            len(identities) != 3
            or set(identities.values()) != set(ROLE_KINDS)
            or set(identities) != set(fixture_keys)
            or any(type(identity) is not str or not identity for identity in identities)
            or any(type(key) is not bytes or len(key) < 32 for key in fixture_keys.values())
        ):
            raise ValueError("BAD_MANIFEST")
        if any(not self._is_digest(value) for value in (candidate_digest, evidence_digest, policy_digest)):
            raise ValueError("BAD_MANIFEST")
        self._run_id = run_id
        self._identities = dict(identities)
        self._keys = dict(fixture_keys)
        self._candidate_digest = candidate_digest
        self._evidence_digest = evidence_digest
        self._policy_digest = policy_digest
        self._lock = Lock()
        self._epoch = 0
        self._predecessor = 0
        self._revoked: set[str] = set()
        self._receipts: dict[str, tuple[SignedMessage, MessageReceipt]] = {}
        self._admitted_ids: list[str] = []

    @staticmethod
    def _is_digest(value: object) -> bool:
        return type(value) is str and fullmatch("[0-9a-f]{64}", value) is not None

    @classmethod
    def _well_formed(cls, message: SignedMessage, now: int) -> bool:
        strings = (
            message.version, message.run_id, message.message_id, message.sender_id,
            message.sender_role, message.recipient_id, message.kind, message.content,
        )
        digests = (
            message.candidate_digest, message.evidence_digest, message.policy_digest,
            message.content_digest, message.mac,
        )
        return (
            all(type(value) is str and bool(value) for value in strings)
            and all(type(value) is int and value >= 0 for value in (message.epoch, message.predecessor, message.deadline, now))
            and all(cls._is_digest(value) for value in digests)
        )

    def revoke_identity(self, sender_id: str) -> None:
        """Trusted fixture fault injection, not a governed revocation issuer."""
        with self._lock:
            if sender_id not in self._identities:
                raise ValueError("UNKNOWN_IDENTITY")
            self._revoked.add(sender_id)

    def invalidate_epoch(self) -> None:
        """Fault injection only: not an adaptive switch or authorized epoch."""
        with self._lock:
            self._epoch += 1

    def snapshot(self) -> tuple[int, int, tuple[str, ...]]:
        with self._lock:
            return self._epoch, len(self._admitted_ids), tuple(self._admitted_ids)

    def admit(self, message: SignedMessage, now: int) -> MessageReceipt:
        with self._lock:
            def hold(reason: str) -> MessageReceipt:
                return MessageReceipt("HOLD", reason, len(self._admitted_ids))

            if type(message) is not SignedMessage or not self._well_formed(message, now):
                return hold("MALFORMED")
            key = self._keys.get(message.sender_id)
            if key is None:
                return hold("UNKNOWN_IDENTITY")
            expected_mac = new(key, signed_bytes(message), "sha256").hexdigest()
            if not compare_digest(message.mac, expected_mac):
                return hold("INVALID_MAC")
            if message.sender_role != self._identities[message.sender_id]:
                return hold("ROLE_SPOOF")
            if message.content_digest != digest_text(message.content):
                return hold("CONTENT_DIGEST_MISMATCH")

            previous = self._receipts.get(message.message_id)
            if previous is not None:
                prior_message, receipt = previous
                return receipt if prior_message == message else hold("ID_CONFLICT")

            if message.sender_id in self._revoked:
                reason = "REVOKED"
            elif message.version != VERSION or message.run_id != self._run_id:
                reason = "WRONG_RUN_OR_VERSION"
            elif message.recipient_id != "controller":
                reason = "UNAUTHORIZED_EDGE"
            elif message.kind not in ROLE_KINDS[message.sender_role]:
                reason = "UNAUTHORIZED_KIND"
            elif message.epoch != self._epoch:
                reason = "STALE_EPOCH"
            elif message.predecessor != self._predecessor:
                reason = "STALE_PREDECESSOR"
            elif (
                message.candidate_digest != self._candidate_digest
                or message.evidence_digest != self._evidence_digest
                or message.policy_digest != self._policy_digest
            ):
                reason = "IDENTITY_MISMATCH"
            elif now >= message.deadline:
                reason = "EXPIRED"
            else:
                reason = None

            if reason is None:
                self._admitted_ids.append(message.message_id)
                receipt = MessageReceipt("ADMITTED_SYNTHETIC", "VALID_MESSAGE", len(self._admitted_ids))
            else:
                receipt = hold(reason)
            self._receipts[message.message_id] = (message, receipt)
            return receipt
