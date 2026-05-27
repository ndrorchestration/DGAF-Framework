"""
triumvirate_mandate.py — TriumvirateMandate schema (NDR P-09).

Machine-readable mandate issuance and sign-off for Triumvirate governance.
Enforces MECE Prefect domain split at construction time.
All mandate lifecycle events emitted via HeraldAgent (P-01).

OPP-007 (COMPOSE P-09): No prior pattern covered Triumvirate mandate schema.
Registered as NDR P-09 in docs/NDR_PATTERN_REGISTRY.md.

Usage:
    from pptl.triumvirate_mandate import TriumvirateMandate, PrefectDomain

    mandate = TriumvirateMandate(
        prime        = "Amethyst",
        task         = "S041 Cycle 1 execution",
        scope        = "DGAF-Framework — OPP-002 through OPP-008",
        constraints  = ["CI must remain green", "append-only CO_ORCH_QUEUE"],
        prefect_a    = PrefectDomain(agent="COLLEEN", domain="coherence",
                                     agents_governed=["Herald", "Echolette"]),
        prefect_b    = PrefectDomain(agent="Apogee",  domain="quality",
                                     agents_governed=["DemiJoule", "Sentinel"]),
        herald       = herald_instance,
    )
    mandate.issue()    # emits mandate_issued event
    mandate.sign_off() # emits mandate_signed_off event
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .herald_agent import HeraldAgent


@dataclass
class PrefectDomain:
    """
    One Prefect’s governance domain within a Triumvirate.
    agent_governed must be disjoint from the other PrefectDomain.
    """
    agent:            str           # e.g. "COLLEEN"
    domain:           str           # e.g. "coherence/identity"
    agents_governed:  list[str] = field(default_factory=list)
    aggregate:        str = ""      # Prefect’s aggregated report (filled post-exec)
    aggregate_ts:     str = ""      # ISO timestamp when aggregate submitted

    def submit_aggregate(self, report: str) -> None:
        self.aggregate    = report
        self.aggregate_ts = datetime.now(timezone.utc).isoformat()


@dataclass
class TriumvirateMandate:
    """
    Formal mandate issued by the Prime, governing a choreographed ensemble.

    Governance contracts (P-09):
      1. Prime issues signed mandate (task + scope + constraints)
      2. Prefect domain split is MECE (validated at construction)
      3. Prefects choreograph sub-agents and aggregate results
      4. Prime reviews Prefect aggregates and issues final sign-off
      5. All lifecycle events traced via HeraldAgent (P-01)
    """
    prime:       str
    task:        str
    scope:       str
    constraints: list[str]
    prefect_a:   PrefectDomain
    prefect_b:   PrefectDomain
    herald:      "HeraldAgent"

    mandate_id:  str = ""
    issued_at:   str = ""
    signed_off:  bool = False
    signoff_ts:  str = ""
    signoff_note:str = ""

    def __post_init__(self) -> None:
        # Validate MECE: domain names must differ
        if self.prefect_a.domain == self.prefect_b.domain:
            raise ValueError(
                f"Prefect domains must be distinct. "
                f"Both set to '{self.prefect_a.domain}'. "
                "MECE split required — ungoverned agents are a hard failure."
            )
        # Validate MECE: no agent governed by both prefects
        overlap = set(self.prefect_a.agents_governed) & set(self.prefect_b.agents_governed)
        if overlap:
            raise ValueError(
                f"MECE violation: agents {overlap} governed by both prefects. "
                "Each ensemble agent must have exactly one Prefect."
            )
        # Generate mandate ID
        ts = datetime.now(timezone.utc)
        self.mandate_id = f"MANDATE-{self.prime[:3].upper()}-{ts.strftime('%Y%m%dT%H%M%S')}"

    # ── Lifecycle ────────────────────────────────────────────────────

    def issue(self) -> dict[str, Any]:
        """
        Contract 1: Prime issues the mandate. Emits 'mandate_issued' event.
        Must be called before any Prefect submits an aggregate.
        """
        self.issued_at = datetime.now(timezone.utc).isoformat()
        event_data = {
            "mandate_id":        self.mandate_id,
            "prime":             self.prime,
            "task":              self.task,
            "scope":             self.scope,
            "constraints":       self.constraints,
            "prefect_a_agent":   self.prefect_a.agent,
            "prefect_a_domain":  self.prefect_a.domain,
            "prefect_b_agent":   self.prefect_b.agent,
            "prefect_b_domain":  self.prefect_b.domain,
            "issued_at":         self.issued_at,
        }
        self.herald.emit(event_type="mandate_issued", data=event_data)
        return event_data

    def submit_prefect_aggregate(
        self,
        prefect_agent: str,
        report: str,
    ) -> None:
        """
        Contract 3: Prefect submits aggregated results.
        Emits 'prefect_aggregate' event.
        """
        if not self.issued_at:
            raise RuntimeError("Mandate must be issued before aggregates are submitted.")
        if prefect_agent == self.prefect_a.agent:
            self.prefect_a.submit_aggregate(report)
        elif prefect_agent == self.prefect_b.agent:
            self.prefect_b.submit_aggregate(report)
        else:
            raise ValueError(f"Agent '{prefect_agent}' is not a Prefect of this mandate.")
        self.herald.emit(event_type="prefect_aggregate", data={
            "mandate_id":    self.mandate_id,
            "prefect_agent": prefect_agent,
            "aggregate_ts":  datetime.now(timezone.utc).isoformat(),
            "report_len":    len(report),
        })

    def sign_off(self, note: str = "") -> dict[str, Any]:
        """
        Contract 4: Prime signs off after reviewing both Prefect aggregates.
        Raises if either Prefect has not submitted an aggregate.
        Emits 'mandate_signed_off' event.
        """
        missing = []
        if not self.prefect_a.aggregate:
            missing.append(self.prefect_a.agent)
        if not self.prefect_b.aggregate:
            missing.append(self.prefect_b.agent)
        if missing:
            raise RuntimeError(
                f"Cannot sign off: Prefect(s) {missing} have not submitted aggregates."
            )
        self.signed_off  = True
        self.signoff_ts  = datetime.now(timezone.utc).isoformat()
        self.signoff_note = note
        event_data = {
            "mandate_id":   self.mandate_id,
            "prime":        self.prime,
            "signoff_ts":   self.signoff_ts,
            "note":         note,
            "prefect_a_aggregate_len": len(self.prefect_a.aggregate),
            "prefect_b_aggregate_len": len(self.prefect_b.aggregate),
        }
        self.herald.emit(event_type="mandate_signed_off", data=event_data)
        return event_data

    # ── Inspection ─────────────────────────────────────────────────────

    def status_report(self) -> str:
        a_done = bool(self.prefect_a.aggregate)
        b_done = bool(self.prefect_b.aggregate)
        return (
            f"Mandate {self.mandate_id}\n"
            f"  Prime:     {self.prime}\n"
            f"  Task:      {self.task}\n"
            f"  Prefect A: {self.prefect_a.agent} [{self.prefect_a.domain}] "
            f"aggregate={'done' if a_done else 'pending'}\n"
            f"  Prefect B: {self.prefect_b.agent} [{self.prefect_b.domain}] "
            f"aggregate={'done' if b_done else 'pending'}\n"
            f"  Signed off: {self.signed_off}"
        )
