"""Explicit proposal/authorization/commit barrier for consequential actions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class CommitRequest:
    request_id: str
    trace_id: str
    action: str
    target: str
    parameters: Mapping[str, str]
    authorized_by: str | None = None
    authorization_ref: str | None = None


class CommitDenied(PermissionError):
    """Raised when a consequential action lacks explicit authorization."""


class CommitGate:
    """Stores proposals and permits execution only after explicit authorization."""

    def __init__(self) -> None:
        self._authorized: dict[str, str] = {}
        self.proposals: list[CommitRequest] = []

    def propose(self, request: CommitRequest) -> CommitRequest:
        if not request.request_id or not request.trace_id or not request.action or not request.target:
            raise ValueError("commit request identity and action fields are required")
        self.proposals.append(request)
        return request

    def authorize(self, request_id: str, authorized_by: str, authorization_ref: str) -> None:
        if not authorized_by or not authorization_ref:
            raise ValueError("explicit authorization identity and reference are required")
        if not any(r.request_id == request_id for r in self.proposals):
            raise KeyError(request_id)
        self._authorized[request_id] = f"{authorized_by}:{authorization_ref}"

    def commit(self, request_id: str) -> str:
        if request_id not in self._authorized:
            raise CommitDenied("commit requires explicit authorization")
        request = next((r for r in self.proposals if r.request_id == request_id), None)
        if request is None:
            raise KeyError(request_id)
        return self._authorized[request_id]
