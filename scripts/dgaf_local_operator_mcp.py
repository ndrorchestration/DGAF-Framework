#!/usr/bin/env python3
"""MCP stdio adapter for the DGAF Epoch 002 local operator bridge.

This adapter exposes exactly four local tools and delegates every operation to
scripts/dgaf_local_operator_bridge.py. It does not expose arbitrary shell,
filesystem, GitHub, network, receipt, authorization, or analysis operations.

PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN
"""

from __future__ import annotations

from typing import Any

from dgaf_local_operator_bridge import dispatch
from mcp.server.mcpserver import MCPServer

SERVER_NAME = "dgaf-epoch002-local-operator"

mcp = MCPServer(
    SERVER_NAME,
    instructions=(
        "Local-only DGAF Epoch 002 operator boundary. "
        "Use status before other actions. verify_inputs checks locally configured "
        "custody inputs without returning their paths. materialize invokes the "
        "accepted fail-closed materializer and still does not authorize or run "
        "primary analysis. get_evidence returns only non-secret materialization "
        "evidence. No other machine or governance authority is exposed."
    ),
)


@mcp.tool()
def status() -> dict[str, Any]:
    """Report the local operator bridge state and non-authorizing invariants."""
    return dispatch({"action": "status"})


@mcp.tool()
def verify_inputs() -> dict[str, Any]:
    """Verify locked archives and local custody prerequisites without exposing paths."""
    return dispatch({"action": "verify_inputs"})


@mcp.tool()
def materialize() -> dict[str, Any]:
    """Run accepted Epoch 002 materialization locally; never run primary analysis."""
    return dispatch({"action": "materialize"})


@mcp.tool()
def get_evidence() -> dict[str, Any]:
    """Return only the non-secret materialization evidence and its digest."""
    return dispatch({"action": "get_evidence"})


def main() -> None:
    """Run the adapter exclusively over MCP stdio."""
    mcp.run("stdio")


if __name__ == "__main__":
    main()
