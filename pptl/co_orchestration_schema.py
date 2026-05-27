"""
co_orchestration_schema.py — Canonical dataclass schema for the
Amethyst × COLLEEN Co-Orchestration Queue (NDR P-07).

Serializes to/from:
  - CO_ORCH_QUEUE.md  (human-readable SSoT, append-only)
  - co_orch_queue.json (machine-readable, for automated tooling)

Usage:
    from pptl.co_orchestration_schema import CoOrchQueue, load_queue, save_queue

    queue = load_queue()          # reads co_orch_queue.json
    opp   = queue.next_for_amethyst()
    print(queue.colleen_scan_report())

    opp.status     = "DONE"
    opp.commit_sha = "3b0295e7"
    save_queue(queue)             # writes co_orch_queue.json

CLI:
    python -m pptl.co_orchestration_schema
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional, Protocol

from .attestation_gate import AttestationGate, AttestationRecord

# ── Types ────────────────────────────────────────────────────────────

OpportunityMode   = Literal["ADOPT", "CUSTOMIZE", "ALTER", "COMPOSE"]
OpportunityStatus = Literal["PENDING", "IN_PROGRESS", "DONE", "DEFERRED", "REJECTED"]
GateLabel         = Literal["fit", "risk", "effort", "priority"]

QUEUE_JSON_PATH = Path("co_orch_queue.json")


class SupportsAttestation(Protocol):
    def attest(self, record: AttestationRecord): ...


# ── Dataclasses ────────────────────────────────────────────────────────

@dataclass
class AlignmentGate:
    """
    COLLEEN’s 1-1-1-1 binary gate. All four must be True to PASS.
    Fail any → DEFERRED or REJECTED. Never silent drop.

    Optional integration:
        attestation_gate — when provided, claim/evidence must attest before PASS.
    """
    fit:      bool = False  # belongs in this repo/layer
    risk:     bool = False  # CI-safe to implement
    effort:   bool = False  # completable in ≤1 session
    priority: bool = False  # unblocks something downstream
    attestation_gate: Optional[SupportsAttestation] = field(default=None, repr=False, compare=False)

    @property
    def passes(self) -> bool:
        return self.fit and self.risk and self.effort and self.priority

    def verdict(self) -> str:
        failed = [k for k, v in {
            "fit": self.fit, "risk": self.risk,
            "effort": self.effort, "priority": self.priority,
        }.items() if not v]
        return "PASS" if not failed else f"FAIL:{','.join(failed)}"

    def evaluate_claim(self, agent_id: str, claim: str, evidence: str) -> bool:
        """
        Combined governance gate:
        1) 1-1-1-1 alignment must pass
        2) If attestation_gate exists, claim/evidence must attest

        Returns True only if both conditions pass.
        """
        if not self.passes:
            return False
        if not self.attestation_gate:
            return True
        record = AttestationRecord(agent_id=agent_id, claim=claim, evidence=evidence)
        result = self.attestation_gate.attest(record)
        return bool(getattr(result, "passed", False))

    def __str__(self) -> str:
        marks = {
            "fit":      "✅" if self.fit      else "❌",
            "risk":     "✅" if self.risk     else "❌",
            "effort":   "✅" if self.effort   else "❌",
            "priority": "✅" if self.priority else "❌",
        }
        return (f"fit={marks['fit']} risk={marks['risk']} "
                f"effort={marks['effort']} priority={marks['priority']} "
                f"→ {self.verdict()}")


@dataclass
class Opportunity:
    """
    A single detected improvement opportunity.
    Written by COLLEEN; executed by Amethyst.
    """
    id:            str                           # e.g. "OPP-001"
    title:         str                           # human-readable
    layer:         str                           # repo path or module
    detected_by:   Literal["COLLEEN", "Amethyst", "Both"]
    mode:          OpportunityMode               # ADOPT / CUSTOMIZE / ALTER / COMPOSE
    pattern_ref:   str                           # e.g. "P-03" or "NEW:P-09"
    gate:          AlignmentGate = field(default_factory=AlignmentGate)
    status:        OpportunityStatus = "PENDING"
    blocked_by:    str = ""                      # OPP-ID if blocked
    session_in:    str = ""                      # session stamp when detected
    session_done:  str = ""                      # session stamp when completed
    impl_notes:    str = ""                      # Amethyst’s implementation plan
    commit_sha:    str = ""                      # SHA after implementation
    colleen_note:  str = ""                      # COLLEEN audit note
    amethyst_note: str = ""                      # Amethyst impl decision note

    def is_ready(self) -> bool:
        """PENDING + gate passes + not blocked."""
        return (
            self.status == "PENDING"
            and self.gate.passes
            and not self.blocked_by
        )

    def mark_done(self, commit_sha: str, session: str, note: str = "") -> None:
        self.status       = "DONE"
        self.commit_sha   = commit_sha
        self.session_done = session
        if note:
            self.amethyst_note = note

    def __str__(self) -> str:
        return (
            f"{self.id} [{self.status}] {self.mode} · {self.pattern_ref}\n"
            f"  Layer: {self.layer}\n"
            f"  Gate:  {self.gate}\n"
            f"  Title: {self.title}"
        )


@dataclass
class CoOrchQueue:
    """
    Persistent hand-off substrate between COLLEEN and Amethyst.
    Serialized to co_orch_queue.json (machine) + CO_ORCH_QUEUE.md (human).
    Append-only: completed entries are archived, never deleted.
    """
    version:       str = "1.0"
    cycle:         int = 1
    last_updated:  str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    opportunities: list[Opportunity] = field(default_factory=list)

    # ── Query helpers ──────────────────────────────────────────────

    def by_status(self, status: OpportunityStatus) -> list[Opportunity]:
        return [o for o in self.opportunities if o.status == status]

    def pending(self) -> list[Opportunity]:
        return self.by_status("PENDING")

    def ready(self) -> list[Opportunity]:
        """Pending + gate passes + not blocked — safe for Amethyst to execute."""
        return [o for o in self.pending() if o.is_ready()]

    def next_for_amethyst(self) -> Opportunity | None:
        """First ready opportunity in detection order."""
        ready = self.ready()
        return ready[0] if ready else None

    def blocked(self) -> list[Opportunity]:
        return [o for o in self.pending() if o.blocked_by]

    # ── Reporting ────────────────────────────────────────────────

    def colleen_scan_report(self) -> str:
        total       = len(self.opportunities)
        by_s        = {s: len(self.by_status(s))  # type: ignore[arg-type]
                       for s in ("PENDING","IN_PROGRESS","DONE","DEFERRED","REJECTED")}
        by_m        = {m: sum(1 for o in self.opportunities if o.mode == m)
                       for m in ("ADOPT","CUSTOMIZE","ALTER","COMPOSE")}
        next_up     = self.next_for_amethyst()
        lines = [
            f"CoOrchQueue v{self.version} · Cycle {self.cycle}",
            f"Updated: {self.last_updated}",
            f"Total: {total}  |  " +
            "  ".join(f"{s}: {n}" for s, n in by_s.items() if n),
            f"Modes: " + "  ".join(f"{m}: {n}" for m, n in by_m.items() if n),
            f"Next for Amethyst: {next_up.id if next_up else 'NONE'}",
        ]
        return "\n".join(lines)

    # ── Serialization ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        d = asdict(self)
        # Remove non-serializable runtime dependency
        for o in d.get("opportunities", []):
            if "gate" in o and "attestation_gate" in o["gate"]:
                o["gate"].pop("attestation_gate", None)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CoOrchQueue":
        opps = []
        for o in d.get("opportunities", []):
            gate_d = o.pop("gate", {})
            gate_d.pop("attestation_gate", None)
            gate   = AlignmentGate(**gate_d)
            opps.append(Opportunity(gate=gate, **o))
        return cls(
            version       = d.get("version", "1.0"),
            cycle         = d.get("cycle", 1),
            last_updated  = d.get("last_updated", ""),
            opportunities = opps,
        )


# ── I/O helpers ───────────────────────────────────────────────────────────

def load_queue(path: Path = QUEUE_JSON_PATH) -> CoOrchQueue:
    """Load queue from JSON. Returns empty queue if file not found."""
    if not path.exists():
        return CoOrchQueue()
    with path.open("r", encoding="utf-8") as fh:
        return CoOrchQueue.from_dict(json.load(fh))


def save_queue(queue: CoOrchQueue, path: Path = QUEUE_JSON_PATH) -> None:
    """Persist queue to JSON. Updates last_updated timestamp."""
    queue.last_updated = datetime.now(timezone.utc).isoformat()
    with path.open("w", encoding="utf-8") as fh:
        json.dump(queue.to_dict(), fh, indent=2, default=str)


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    queue = load_queue()
    print(queue.colleen_scan_report())
    print()
    next_up = queue.next_for_amethyst()
    if next_up:
        print("Next for Amethyst:")
        print(next_up)
    else:
        print("Queue empty or all blocked. COLLEEN re-scan needed.")
    print()
    print("All opportunities:")
    for opp in queue.opportunities:
        flag = "🟡" if opp.status == "PENDING" else "🟢" if opp.status == "DONE" else "🔵"
        print(f"  {flag} {opp.id} [{opp.status}] {opp.mode} · {opp.pattern_ref} · {opp.title[:50]}")
