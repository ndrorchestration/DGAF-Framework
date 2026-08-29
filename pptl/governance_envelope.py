"""Immutable governance scope inherited by DGAF recursive work items.

V1 control-plane contract: a child may only narrow its parent's authority,
tool/data scope, and remaining resource budget.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping


def _freeze(items: Iterable[str]) -> frozenset[str]:
    return frozenset(str(item) for item in items)


@dataclass(frozen=True)
class ResourceBudget:
    max_input_tokens: int = 0
    max_output_tokens: int = 0
    max_tool_calls: int = 0
    max_elapsed_ms: int = 0
    max_rounds: int = 0
    max_nodes: int = 0
    max_depth: int = 0
    max_concurrency: int = 1

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer")
        if self.max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")

    def child_allowed(self, child: "ResourceBudget") -> bool:
        return all(
            getattr(child, name) <= getattr(self, name)
            for name in self.__dataclass_fields__
        )


@dataclass(frozen=True)
class GovernanceEnvelope:
    trace_id: str
    task_id: str
    authority_scope: frozenset[str] = field(default_factory=frozenset)
    permitted_tools: frozenset[str] = field(default_factory=frozenset)
    data_classes: frozenset[str] = field(default_factory=frozenset)
    prohibited_actions: frozenset[str] = field(default_factory=frozenset)
    risk_tier: str = "low"
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    policy_version: str = "dgaf-v1"
    side_effect_mode: str = "PROPOSE_ONLY"
    parent_trace_id: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("authority_scope", "permitted_tools", "data_classes", "prohibited_actions"):
            object.__setattr__(self, field_name, _freeze(getattr(self, field_name)))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        if not self.trace_id or not self.task_id:
            raise ValueError("trace_id and task_id are required")
        if self.risk_tier not in {"low", "medium", "high", "critical"}:
            raise ValueError("invalid risk_tier")
        if self.side_effect_mode not in {"PROPOSE_ONLY", "COMMIT_ALLOWED"}:
            raise ValueError("invalid side_effect_mode")

    def derive_child(
        self,
        *,
        trace_id: str,
        task_id: str,
        authority_scope: Iterable[str],
        permitted_tools: Iterable[str],
        data_classes: Iterable[str],
        budget: ResourceBudget,
        risk_tier: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> "GovernanceEnvelope":
        child_authority = _freeze(authority_scope)
        child_tools = _freeze(permitted_tools)
        child_data = _freeze(data_classes)
        if not child_authority <= self.authority_scope:
            raise PermissionError("child authority exceeds parent scope")
        if not child_tools <= self.permitted_tools:
            raise PermissionError("child tool scope exceeds parent scope")
        if not child_data <= self.data_classes:
            raise PermissionError("child data scope exceeds parent scope")
        if not self.budget.child_allowed(budget):
            raise PermissionError("child budget exceeds parent budget")
        child_risk = risk_tier or self.risk_tier
        risk_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        if risk_rank[child_risk] > risk_rank[self.risk_tier]:
            raise PermissionError("child risk tier cannot increase")
        return GovernanceEnvelope(
            trace_id=trace_id,
            task_id=task_id,
            authority_scope=child_authority,
            permitted_tools=child_tools,
            data_classes=child_data,
            prohibited_actions=self.prohibited_actions,
            risk_tier=child_risk,
            budget=budget,
            policy_version=self.policy_version,
            side_effect_mode=self.side_effect_mode,
            parent_trace_id=self.trace_id,
            metadata=metadata or {},
        )
