"""Isolated in-memory enforcement contract. NOT OS/network sandboxing."""
from dataclasses import dataclass, field
from .controller import Regime

@dataclass
class SimulatedGate:
    """Deny-by-default production effects; no authority restoration API."""
    regime: Regime = Regime.NORMAL
    grants: frozenset[str] = frozenset()
    history: list[tuple[str, str]] = field(default_factory=list)

    def restrict(self, regime: Regime) -> None:
        if regime < self.regime:
            raise PermissionError("restriction downgrade requires separate adjudication")
        self.regime = regime
        self.history.append(("restrict", regime.name))

    def attempt(self, action: str) -> bool:
        permitted = self.regime == Regime.NORMAL and action in self.grants
        self.history.append(("allow" if permitted else "deny", action))
        return permitted

    def snapshot(self) -> dict:
        return {"regime": self.regime.name, "history": tuple(self.history)}
