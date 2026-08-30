"""Canonical orchestration-state identity and exact cycle detection."""
from __future__ import annotations
import hashlib, json
from typing import Any, Iterable

def canonical_state(state: dict[str, Any]) -> str:
    return json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def state_id(state: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_state(state).encode("utf-8")).hexdigest()

class StateRegistry:
    def __init__(self) -> None:
        self._seen: set[str] = set()
    def observe(self, state: dict[str, Any]) -> str:
        sid = state_id(state); self._seen.add(sid); return sid
    def contains(self, state: dict[str, Any]) -> bool:
        return state_id(state) in self._seen
    @property
    def count(self) -> int: return len(self._seen)
    def ids(self) -> Iterable[str]: return tuple(sorted(self._seen))
