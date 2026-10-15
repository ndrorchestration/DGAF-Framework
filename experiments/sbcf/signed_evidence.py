"""Prototype HMAC evidence envelope with replay defense; shared-key simulation, not independent attestation."""
from dataclasses import dataclass, field
import hashlib
import hmac
import json

def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def sign(value: dict, secret: bytes) -> str:
    return hmac.new(secret, canonical(value), hashlib.sha256).hexdigest()

@dataclass
class EvidenceVerifier:
    keys: dict[str, bytes]
    seen: set[tuple[str, str, int]] = field(default_factory=set)

    def admit(self, record: dict, *, expected_run: str, expected_policy: str, expected_nonce: str) -> bool:
        required = {"source", "run", "policy", "nonce", "sequence", "state", "signature"}
        if not isinstance(record, dict) or set(record) != required:
            return False
        source = record["source"]
        if not isinstance(source, str) or source not in self.keys:
            return False
        if any(type(record[k]) is not str or not record[k] for k in ("run", "policy", "nonce")):
            return False
        if (record["run"], record["policy"], record["nonce"]) != (expected_run, expected_policy, expected_nonce):
            return False
        seq = record["sequence"]
        if type(seq) is not int or seq < 0 or type(record["state"]) is not dict:
            return False
        identity = (source, expected_run, seq)
        if identity in self.seen:
            return False
        fields = {k: record[k] for k in required if k != "signature"}
        signature = record["signature"]
        if not isinstance(signature, str) or len(signature) != 64:
            return False
        if not hmac.compare_digest(sign(fields, self.keys[source]), signature):
            return False
        self.seen.add(identity)
        return True
