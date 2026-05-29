# resonant_decay/adapters/langgraph.py
# LangGraph node — insert before router_node in StateGraph.
from __future__ import annotations
from typing import Any, Dict

from ..engine import StructuralContextPruningEngine


def make_scpe_node(engine: StructuralContextPruningEngine):
    """Returns a LangGraph-compatible node function.

    Usage:
        builder.add_node("scpe", make_scpe_node(engine))
        builder.add_edge("scpe", "router_node")
    """
    def scpe_node(state: Dict[str, Any]) -> Dict[str, Any]:
        stats = engine.prune()
        state["scpe_stats"]       = stats
        state["context_snapshot"] = engine.snapshot()
        return state
    return scpe_node
