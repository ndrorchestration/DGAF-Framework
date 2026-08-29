"""Deterministic resource and active-concurrency ledger for v1."""
from __future__ import annotations
from dataclasses import dataclass
from .governance_envelope import ResourceBudget

@dataclass(frozen=True)
class Consumption:
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    elapsed_ms: int = 0
    rounds: int = 0
    nodes: int = 0
    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if not isinstance(value, int) or value < 0: raise ValueError(f"{name} must be a non-negative integer")

class BudgetExceeded(RuntimeError):
    pass

class BudgetLedger:
    def __init__(self, budget: ResourceBudget) -> None:
        self.budget, self.consumed, self.reserved, self.active_concurrency = budget, Consumption(), Consumption(), 0
    @staticmethod
    def _add(a: Consumption, b: Consumption) -> Consumption:
        return Consumption(*(getattr(a, f) + getattr(b, f) for f in Consumption.__dataclass_fields__))
    @staticmethod
    def _fits(budget: ResourceBudget, value: Consumption) -> bool:
        limits = {"input_tokens": budget.max_input_tokens,"output_tokens": budget.max_output_tokens,"tool_calls": budget.max_tool_calls,"elapsed_ms": budget.max_elapsed_ms,"rounds": budget.max_rounds,"nodes": budget.max_nodes}
        return all(getattr(value, field) <= limit for field, limit in limits.items())
    def remaining(self) -> Consumption:
        used = self._add(self.consumed, self.reserved)
        limits = {"input_tokens": self.budget.max_input_tokens,"output_tokens": self.budget.max_output_tokens,"tool_calls": self.budget.max_tool_calls,"elapsed_ms": self.budget.max_elapsed_ms,"rounds": self.budget.max_rounds,"nodes": self.budget.max_nodes}
        return Consumption(**{k: max(0, v - getattr(used, k)) for k, v in limits.items()})
    def acquire_concurrency(self, slots: int = 1) -> None:
        if not isinstance(slots, int) or slots < 1: raise ValueError("slots must be a positive integer")
        if self.active_concurrency + slots > self.budget.max_concurrency: raise BudgetExceeded("active concurrency exceeds budget")
        self.active_concurrency += slots
    def release_concurrency(self, slots: int = 1) -> None:
        if not isinstance(slots, int) or slots < 1: raise ValueError("slots must be a positive integer")
        if slots > self.active_concurrency: raise ValueError("cannot release more active concurrency than acquired")
        self.active_concurrency -= slots
    def reserve(self, amount: Consumption) -> None:
        candidate = self._add(self._add(self.consumed, self.reserved), amount)
        if not self._fits(self.budget, candidate): raise BudgetExceeded("resource reservation exceeds budget")
        self.reserved = self._add(self.reserved, amount)
    def release(self, amount: Consumption) -> None:
        values = {f: getattr(self.reserved, f) - getattr(amount, f) for f in Consumption.__dataclass_fields__}
        if any(v < 0 for v in values.values()): raise ValueError("cannot release more than reserved")
        self.reserved = Consumption(**values)
    def consume(self, amount: Consumption) -> None:
        new_consumed = self._add(self.consumed, amount)
        if not self._fits(self.budget, new_consumed): raise BudgetExceeded("resource consumption exceeds budget")
        self.consumed = new_consumed
