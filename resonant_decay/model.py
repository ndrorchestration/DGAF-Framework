# resonant_decay/model.py
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time


class Tier(Enum):
    AXIOM       = 0  # T0 — non-prunable, hash-anchored
    STRUCTURAL  = 1  # T1 — schemas, protocols, role charts
    OPERATIONAL = 2  # T2 — active tasks, working set
    EXPLORATORY = 3  # T3 — CoT traces, tool logs, speculative


@dataclass
class ContextToken:
    token_id:        str
    content:         str
    tier:            Tier
    inserted_at:     float = field(default_factory=time.time)
    last_touched_at: float = field(default_factory=time.time)
    has_trust_edge:  bool  = False   # PDMAL graph edge → TIF boost
    metadata:        Dict[str, Any] = field(default_factory=dict)
    content_hash:    str  = ""
    locked:          bool = False

    def touch(self) -> None:
        self.last_touched_at = time.time()


@dataclass
class ContextBuffer:
    tokens:     List[ContextToken] = field(default_factory=list)
    max_tokens: int = 8192

    @property
    def utilization(self) -> float:
        est = sum(max(1, len(t.content.split()) * 4 // 3) for t in self.tokens)
        return est / max(1, self.max_tokens)
