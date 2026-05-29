# resonant_decay/governance.py
# SHA-256 hash anchoring, lock/validate for Topological Invariant Factors.
import hashlib
from .model import ContextToken


def compute_hash(content: str, metadata: dict) -> str:
    h = hashlib.sha256()
    h.update(content.encode())
    h.update(str(sorted(metadata.items())).encode())
    return h.hexdigest()


def lock_token(token: ContextToken) -> ContextToken:
    token.content_hash = compute_hash(token.content, token.metadata)
    token.locked = True
    return token


def validate_token(token: ContextToken) -> bool:
    if not token.locked:
        return True
    return compute_hash(token.content, token.metadata) == token.content_hash
