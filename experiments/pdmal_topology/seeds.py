from __future__ import annotations

import hashlib


def derive_seed(master_seed: int, stream: str) -> int:
    """Derive deterministic, independent integer seeds for named RNG streams."""
    payload = f"pdmal-v1|{master_seed}|{stream}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big")
