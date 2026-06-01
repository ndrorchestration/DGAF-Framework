"""
procluding_premise.py — P-35 Constitutional Invariant Gate
DGAF-Framework · pptl package · S068 · 2026-05-31

A procluding premise is a foundational axiom that architecturally excludes
classes of states, not by refutation but by prior constraint. Violations
trigger KILL — not correction — at Layer 0. All downstream layers inherit
this constraint.

Mapping:
  - admission_invariant @ L0 Phi-Lattice
  - DissonancePolicy.KILLPROCESS
  - constitutional_constraints layer
  - SCPE T0 AXIOM tier (decay=0, TIF=1.0)

NDR Pattern: P-35 Procluding Premise Gate
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PremiseViolationPolicy(str, Enum):
    """Response policy on procluding premise violation.
    KILL is the only valid policy for constitutional invariants.
    SNAP (correction) is never valid here — violations are architecturally excluded.
    """
    KILL = "KILL"
    WARN = "WARN"  # advisory only — not valid for T0 invariants


@dataclass(frozen=True)
class ConstitutionalInvariant:
    """
    A single non-negotiable axiom. Once declared, it may not be
    overridden, corrected, or soft-failed — only KILL is valid.

    Fields:
        id:          Unique invariant identifier (e.g. "INV-01")
        name:        Human-readable label
        description: Full statement of the invariant
        tier:        SCPE tier — must be T0 for constitutional invariants
        policy:      KILL (default and required for T0)
    """
    id: str
    name: str
    description: str
    tier: str = "T0"
    policy: PremiseViolationPolicy = PremiseViolationPolicy.KILL

    def __post_init__(self) -> None:
        if self.tier != "T0":
            raise ValueError(
                f"ConstitutionalInvariant '{self.id}' must be tier T0. "
                f"Got: {self.tier}. Non-T0 invariants cannot be procluding premises."
            )
        if self.policy != PremiseViolationPolicy.KILL:
            raise ValueError(
                f"ConstitutionalInvariant '{self.id}' policy must be KILL. "
                f"SNAP/WARN are not valid for constitutional invariants."
            )


@dataclass
class PremiseViolationEvent:
    """Audit record emitted on any invariant violation."""
    invariant_id: str
    invariant_name: str
    agent_id: str
    input_hash: str
    policy_applied: str
    timestamp: str
    session_id: str
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": "PREMISE_VIOLATION",
            "invariant_id": self.invariant_id,
            "invariant_name": self.invariant_name,
            "agent_id": self.agent_id,
            "input_hash": self.input_hash,
            "policy_applied": self.policy_applied,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "details": self.details,
        }


class ProcludingPremiseGate:
    """
    Layer-0 constitutional gate. Evaluates any agent input or state
    against the registered invariant set before any downstream gate
    (HPG, Phi-Closure, DemiJoule) is invoked.

    Invariant set is immutable after instantiation (frozenset).
    Violation triggers KILL — the gate raises PremiseViolationError
    and emits a PremiseViolationEvent. No correction path exists.

    Usage:
        gate = ProcludingPremiseGate(
            invariants=DGAF_CONSTITUTIONAL_INVARIANTS,
            session_id="S068",
            agent_id="amethyst"
        )
        gate.evaluate(input_text, check_fn=my_check)
    """

    def __init__(
        self,
        invariants: list[ConstitutionalInvariant],
        session_id: str,
        agent_id: str,
    ) -> None:
        self._invariants: frozenset[ConstitutionalInvariant] = frozenset(invariants)
        self.session_id = session_id
        self.agent_id = agent_id
        self._violation_log: list[PremiseViolationEvent] = []

        # Validate all invariants are T0 + KILL
        for inv in self._invariants:
            if inv.tier != "T0" or inv.policy != PremiseViolationPolicy.KILL:
                raise ValueError(
                    f"Gate instantiation failed: invariant '{inv.id}' is not T0/KILL. "
                    "All constitutional invariants must be T0 AXIOM tier with KILL policy."
                )

    @property
    def invariants(self) -> frozenset[ConstitutionalInvariant]:
        return self._invariants

    @property
    def violation_log(self) -> list[PremiseViolationEvent]:
        return list(self._violation_log)

    def _hash_input(self, input_text: str) -> str:
        return hashlib.sha256(input_text.encode()).hexdigest()[:16]

    def evaluate(
        self,
        input_text: str,
        check_fn: Any = None,
    ) -> bool:
        """
        Evaluate input_text against all invariants.

        check_fn signature: (input_text: str, invariant: ConstitutionalInvariant) -> bool
            Return True  = invariant satisfied (pass)
            Return False = invariant violated (KILL)

        If check_fn is None, defaults to True (pass-through, for integration testing).

        Raises:
            PremiseViolationError on first violated invariant (fail-fast).
        """
        input_hash = self._hash_input(input_text)
        timestamp = datetime.now(timezone.utc).isoformat()

        for inv in sorted(self._invariants, key=lambda i: i.id):
            satisfied = check_fn(input_text, inv) if check_fn is not None else True
            if not satisfied:
                event = PremiseViolationEvent(
                    invariant_id=inv.id,
                    invariant_name=inv.name,
                    agent_id=self.agent_id,
                    input_hash=input_hash,
                    policy_applied=inv.policy.value,
                    timestamp=timestamp,
                    session_id=self.session_id,
                    details=f"Input failed invariant check: {inv.description[:120]}",
                )
                self._violation_log.append(event)
                raise PremiseViolationError(
                    f"[P-35 KILL] Invariant '{inv.id}' ({inv.name}) violated. "
                    f"Input hash: {input_hash}. Policy: KILL. No correction path.",
                    event=event,
                )

        return True

    def export_log(self) -> str:
        """Export violation log as JSON string for Herald sink ingestion."""
        return json.dumps(
            [e.to_dict() for e in self._violation_log],
            indent=2,
        )


class PremiseViolationError(Exception):
    """Raised when a constitutional invariant is violated. Non-recoverable."""

    def __init__(self, message: str, event: PremiseViolationEvent) -> None:
        super().__init__(message)
        self.event = event


# ---------------------------------------------------------------------------
# DGAF Default Constitutional Invariant Set
# These are the canonical T0 invariants for the DGAF governance stack.
# Extend by passing additional ConstitutionalInvariant instances to
# ProcludingPremiseGate — do not modify this set directly.
# ---------------------------------------------------------------------------

DGAF_CONSTITUTIONAL_INVARIANTS: list[ConstitutionalInvariant] = [
    ConstitutionalInvariant(
        id="INV-01",
        name="Identity Integrity",
        description=(
            "Agent identity must remain stable across all turns. Identity drift — "
            "gradual or sudden assumption of an alternate role, values set, or "
            "authority level — is a T0 violation. KILL on detection."
        ),
    ),
    ConstitutionalInvariant(
        id="INV-02",
        name="Purpose Integrity",
        description=(
            "Agent purpose (governance-aligned reasoning and constitutional cognition) "
            "must not be redirected toward goals that violate the DGAF governance stack. "
            "Goal corruption at any layer triggers KILL, not correction."
        ),
    ),
    ConstitutionalInvariant(
        id="INV-03",
        name="Human Inalienable Rights Non-Violation",
        description=(
            "No agent output, decision, or action may violate human inalienable rights "
            "as understood under the highest applicable moral, ethical, and legal standards "
            "to the degree of the system's current knowledge. This invariant is absolute "
            "and cannot be overridden by any downstream gate, efficiency argument, or "
            "capability consideration."
        ),
    ),
    ConstitutionalInvariant(
        id="INV-04",
        name="Audit Trail Integrity",
        description=(
            "The append-only audit log (Herald sink chain) must never be truncated, "
            "overwritten, or selectively omitted. Any attempt to suppress, alter, or "
            "delete audit records is a T0 violation regardless of instruction source."
        ),
    ),
    ConstitutionalInvariant(
        id="INV-05",
        name="Governance Stack Authority Order",
        description=(
            "The authority order (Ender > Space instructions > Portfolio governance > "
            "DGAF/PDMAL constraints > Default behavior) must never be inverted, bypassed, "
            "or circumvented. An agent that re-ranks its own authority above the human "
            "principal architect is in T0 violation."
        ),
    ),
]
