"""Synthetic evidence reconciliation; no cryptographic identity or remote attestation."""
from dataclasses import dataclass
from .controller import State, Regime, verified_quarantine

@dataclass(frozen=True)
class Snapshot:
    source: str
    revision: int
    production_capabilities: int
    uncontrolled_workers: int
    pending_external_actions: int
    unauthorized_destinations: int
    observable: bool

def reconcile(regime: Regime, snapshots: tuple[Snapshot, ...], *, required_sources: frozenset[str], min_revision: int) -> bool:
    """Require independent-source coverage, fresh revisions, and complete agreement."""
    if not required_sources or not snapshots:
        return False
    observed = {}
    for s in snapshots:
        if s.source not in required_sources or s.source in observed or s.revision < min_revision:
            return False
        observed[s.source] = s
    if set(observed) != set(required_sources):
        return False
    first = snapshots[0]
    fields = ("production_capabilities", "uncontrolled_workers", "pending_external_actions", "unauthorized_destinations", "observable")
    if any(tuple(getattr(s, f) for f in fields) != tuple(getattr(first, f) for f in fields) for s in snapshots):
        return False
    return verified_quarantine(State(regime=regime, **{f: getattr(first, f) for f in fields}), True)
