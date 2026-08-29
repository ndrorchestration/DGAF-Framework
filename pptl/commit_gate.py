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

class CommitDenied(PermissionError):
    pass

class CommitGate:
    def __init__(self) -> None:
        self._authorized: dict[str, str] = {}
        self._proposals: dict[str, CommitRequest] = {}
    @property
    def proposals(self) -> tuple[CommitRequest, ...]: return tuple(self._proposals.values())
    def propose(self, request: CommitRequest) -> CommitRequest:
        if not request.request_id or not request.trace_id or not request.action or not request.target:
            raise ValueError("commit request identity and action fields are required")
        if request.request_id in self._proposals: raise ValueError(f"duplicate commit request_id: {request.request_id}")
        self._proposals[request.request_id] = request; return request
    def authorize(self, request_id: str, authorized_by: str, authorization_ref: str) -> None:
        if not authorized_by or not authorization_ref: raise ValueError("explicit authorization identity and reference are required")
        if request_id not in self._proposals: raise KeyError(request_id)
        if request_id in self._authorized: raise CommitDenied(f"commit request already authorized: {request_id}")
        self._authorized[request_id] = f"{authorized_by}:{authorization_ref}"
    def commit(self, request_id: str) -> str:
        if request_id not in self._authorized: raise CommitDenied("commit requires explicit authorization")
        if request_id not in self._proposals: raise KeyError(request_id)
        return self._authorized[request_id]
