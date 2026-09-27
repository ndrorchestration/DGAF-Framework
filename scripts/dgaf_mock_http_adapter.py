from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class MockHttpAdapterRefusal(RuntimeError):
    pass


@dataclass(frozen=True)
class Route:
    method: str
    path: str
    bridge_action: str
    capability_id: str


ROUTES = {
    ("GET", "/v1/status"): Route(
        method="GET",
        path="/v1/status",
        bridge_action="status",
        capability_id="dgaf.local.status",
    )
}


def dispatch_http(
    request: dict[str, Any],
    *,
    bridge_dispatch: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Pure in-process HTTP-style adapter; opens no socket and performs no I/O."""
    if set(request) != {"method", "path"}:
        raise MockHttpAdapterRefusal("request must contain exactly method and path")

    method = request.get("method")
    path = request.get("path")
    if not isinstance(method, str) or not isinstance(path, str):
        raise MockHttpAdapterRefusal("method and path must be strings")

    route = ROUTES.get((method.upper(), path))
    if route is None:
        raise MockHttpAdapterRefusal("route is not admitted")

    response = bridge_dispatch({"action": route.bridge_action})
    return {
        "adapter": "DGAF_MOCK_HTTP_ADAPTER",
        "network_listener": False,
        "transport": "mock-http",
        "method": route.method,
        "path": route.path,
        "capability_id": route.capability_id,
        "provider_response": response,
    }
