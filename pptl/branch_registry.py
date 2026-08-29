"""Append-oriented branch lineage and evidence registry."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping


@dataclass(frozen=True)
class BranchRecord:
    branch_id: str
    parent_branch_id: str | None
    role: str
    state_id: str
    claims: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    uncertainty: float | None = None
    source_overlap: float | None = None
    dependency_overlap: float | None = None
    policy_verdict: str = "PASS"
    merge_status: str = "accepted"
    terminal: bool = False
    metadata: Mapping[str, str] = None

    def __post_init__(self) -> None:
        if not self.branch_id or not self.role or not self.state_id:
            raise ValueError("branch_id, role, and state_id are required")
        for name in ("uncertainty", "source_overlap", "dependency_overlap"):
            value = getattr(self, name)
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.policy_verdict not in {"PASS", "WARN", "KILL", "ESCALATE"}:
            raise ValueError("invalid policy_verdict")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata or {})))


class BranchRegistry:
    def __init__(self) -> None:
        self._branches: list[BranchRecord] = []
        self._states: dict[str, str] = {}

    @property
    def count(self) -> int:
        return len(self._branches)

    def add(self, record: BranchRecord) -> None:
        if any(b.branch_id == record.branch_id for b in self._branches):
            raise ValueError(f"duplicate branch_id: {record.branch_id}")
        self._branches.append(record)
        self._states[record.state_id] = record.branch_id

    def get(self, branch_id: str) -> BranchRecord:
        for branch in self._branches:
            if branch.branch_id == branch_id:
                return branch
        raise KeyError(branch_id)

    def all(self) -> tuple[BranchRecord, ...]:
        return tuple(self._branches)

    def by_status(self, merge_status: str) -> tuple[BranchRecord, ...]:
        return tuple(b for b in self._branches if b.merge_status == merge_status)

    def lineage(self, branch_id: str) -> tuple[BranchRecord, ...]:
        chain: list[BranchRecord] = []
        current = self.get(branch_id)
        visited: set[str] = set()
        while True:
            if current.branch_id in visited:
                raise ValueError("branch lineage cycle detected")
            visited.add(current.branch_id)
            chain.append(current)
            if current.parent_branch_id is None:
                break
            current = self.get(current.parent_branch_id)
        chain.reverse()
        return tuple(chain)

    def ids(self) -> Iterable[str]:
        return tuple(b.branch_id for b in self._branches)
