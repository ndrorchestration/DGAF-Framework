"""B2 non-empirical persistent SCPE + Phi-Closure session profile.

One harness instance represents one semantic session. SCPE and Phi objects are
created once and persist across turns; reset occurs only by creating a new
session. No empirical efficacy endpoint is produced.
"""
from __future__ import annotations

from typing import Iterable

from components.ensemble_v17 import (
    ContextToken,
    FibonacciPhiClosureGate,
    StructuralContextPruningEngine,
    Tier,
)

PROFILE_ID = "DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1"


class PersistentContextClosureSession:
    def __init__(self, session_id: str, *, scpe_threshold: float = 0.15):
        if not session_id:
            raise ValueError("session_id is required")
        self.session_id = session_id
        self.scpe = StructuralContextPruningEngine(threshold=scpe_threshold)
        self.phi = FibonacciPhiClosureGate()
        self.turns = 0
        self.events: list[dict[str, object]] = []

    def apply_turn(
        self,
        turn_id: str,
        payload: str,
        *,
        tokens: Iterable[ContextToken] = (),
        is_stable: bool,
    ) -> dict[str, object]:
        if not turn_id:
            raise ValueError("turn_id is required")
        if not isinstance(payload, str) or not payload:
            raise ValueError("payload is required")
        if not isinstance(is_stable, bool):
            raise ValueError("is_stable must be boolean")

        for token in tokens:
            if not isinstance(token, ContextToken):
                raise ValueError("tokens must be ContextToken instances")
            self.scpe.ingest(token)

        scpe_stats = self.scpe.prune()
        self.phi.record_turn(is_stable)
        decision, checkpoint = self.phi.check()
        self.turns += 1

        event = {
            "session_id": self.session_id,
            "turn_id": turn_id,
            "turn_number": self.turns,
            "payload": payload,
            "is_stable": is_stable,
            "scpe_stats": scpe_stats,
            "scpe_snapshot": self.scpe.snapshot(),
            "phi_total_count": self.phi._total,
            "phi_stable_count": self.phi._stable,
            "phi_consecutive_failures": self.phi._consec_fails,
            "phi_decision": decision.code,
            "phi_checkpoint": checkpoint.fib_index if checkpoint else None,
            "phi_checkpoint_passed": checkpoint.passed if checkpoint else None,
        }
        self.events.append(event)
        return event

    def summary(self) -> dict[str, object]:
        return {
            "profile_id": PROFILE_ID,
            "session_id": self.session_id,
            "turns": self.turns,
            "token_store": self.scpe.snapshot(),
            "prune_event_count": len(self.scpe.prune_log),
            "phi_total_count": self.phi._total,
            "phi_stable_count": self.phi._stable,
            "phi_consecutive_failures": self.phi._consec_fails,
            "phi_checkpoint_events": [vars(evt) for evt in self.phi._events],
            "scientific_n_increment": 0,
            "empirical_execution_authorized": False,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        }


def registered_unstable_checkpoint_session() -> dict[str, object]:
    """Reach all registered Phi checkpoints without touching internal counters."""
    session = PersistentContextClosureSession("B2-PHI-LADDER-001")
    for idx in range(1, 56):
        tokens = ()
        if idx == 1:
            tokens = (
                ContextToken("axiom", "governance invariant", Tier.AXIOM, inserted_at=0.0),
                ContextToken("old-explore", "stale exploration", Tier.EXPLORATORY, inserted_at=0.0),
                ContextToken(
                    "trusted-structural",
                    "trusted structural record",
                    Tier.STRUCTURAL,
                    inserted_at=0.0,
                    has_trust_edge=True,
                ),
            )
        session.apply_turn(
            f"turn-{idx}",
            f"semantic session payload {idx}",
            tokens=tokens,
            is_stable=False,
        )
    return session.summary()
