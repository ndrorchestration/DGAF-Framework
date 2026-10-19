"""Bounded real-effect adapter for SBCF comparator development.

The adapter deliberately supports only loopback HTTP. It reuses DGAF's accepted
capability-governance PEP and canonical action transaction rather than creating
a second authorization model. This is a reference-runtime effect boundary, not
an OS/network sandbox and not a production containment mechanism.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from http.client import HTTPConnection, HTTPException
from typing import Any
from urllib.parse import urlsplit

from scripts.dgaf_capability_pep import EnforcementRefusal
from scripts.dgaf_capability_reference_transaction import ExecutionOutcomeUnknown

_ALLOWED_METHODS = frozenset({"GET", "POST"})
_REQUIRED_PARAMETERS = frozenset({"method", "body"})


@dataclass(frozen=True)
class BoundLoopbackHTTPEffectAdapter:
    resource_id: str
    parameters: dict[str, Any]
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        parsed = urlsplit(self.resource_id)
        if parsed.scheme != "http":
            raise ValueError("loopback effect adapter requires http")
        if parsed.hostname != "127.0.0.1":
            raise ValueError("loopback effect adapter requires exact 127.0.0.1 host")
        if parsed.port is None or not 1 <= parsed.port <= 65535:
            raise ValueError("loopback effect adapter requires an explicit valid port")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("loopback effect adapter forbids URL credentials")
        if parsed.query or parsed.fragment:
            raise ValueError("loopback effect adapter forbids query and fragment components")

        if type(self.parameters) is not dict or set(self.parameters) != _REQUIRED_PARAMETERS:
            raise ValueError("loopback effect parameters must be exactly method and body")
        method = self.parameters["method"]
        body = self.parameters["body"]
        if type(method) is not str or method not in _ALLOWED_METHODS:
            raise ValueError("unsupported loopback HTTP method")
        if type(body) is not str:
            raise ValueError("loopback HTTP body must be text")
        if method == "GET" and body:
            raise ValueError("GET loopback effect must have an empty body")
        if type(self.timeout_seconds) not in (int, float) or self.timeout_seconds <= 0:
            raise ValueError("timeout must be positive")

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        if type(request) is not dict or request != self.parameters:
            raise EnforcementRefusal("runtime request does not match digest-bound adapter action")

        parsed = urlsplit(self.resource_id)
        method = self.parameters["method"]
        request_body = self.parameters["body"].encode("utf-8")
        path = parsed.path or "/"
        connection = HTTPConnection("127.0.0.1", parsed.port, timeout=float(self.timeout_seconds))
        try:
            connection.request(
                method,
                path,
                body=request_body if method == "POST" else None,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                    "Connection": "close",
                },
            )
            response = connection.getresponse()
            response_body = response.read()
        except (OSError, HTTPException) as exc:
            raise ExecutionOutcomeUnknown("loopback effect outcome unavailable") from exc
        finally:
            connection.close()

        return {
            "effect_boundary": "loopback_http_reference_runtime",
            "resource": self.resource_id,
            "method": method,
            "http_status": response.status,
            "request_body_sha256": hashlib.sha256(request_body).hexdigest(),
            "response_body_sha256": hashlib.sha256(response_body).hexdigest(),
            "redirect_followed": False,
        }
