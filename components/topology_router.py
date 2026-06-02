"""
topology_router.py
NDR Pattern P-02 — Sentinel Firewall: predicate ordering invariant.
Fixes Q-S043-04: Sequential + Fan-Out predicates shadowed by hierarchical catch-all.

Agent: Amethyst (author) · Reson (domain owner)
Session: S044 · 2026-06-01
Ensemble: v1.6
Governed by: DGAF-Framework · Apache 2.0
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TopologyType(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    FAN_OUT = "FAN_OUT"
    REFLEXIVE = "REFLEXIVE"
    HIERARCHICAL = "HIERARCHICAL"
    REJECTED = "REJECTED"


@dataclass
class Topology:
    type: TopologyType
    node_count: int = 1
    depth: Optional[int] = None
    fan_factor: Optional[int] = None


class UnroutableTopologyError(Exception):
    """Raised when no predicate matches the given topology."""


class SequentialRouter:
    name = "SequentialRouter"

    @staticmethod
    def route(topology: Topology) -> dict:
        return {"router": "SEQUENTIAL", "nodes": topology.node_count}


class FanOutRouter:
    name = "FanOutRouter"

    @staticmethod
    def route(topology: Topology) -> dict:
        return {"router": "FAN_OUT", "fan_factor": topology.fan_factor}


class ReflexiveRouter:
    name = "ReflexiveRouter"

    @staticmethod
    def route(topology: Topology) -> dict:
        return {"router": "REFLEXIVE", "nodes": topology.node_count}


class HierarchicalRouter:
    name = "HierarchicalRouter"

    @staticmethod
    def route(topology: Topology) -> dict:
        return {"router": "HIERARCHICAL", "depth": topology.depth}


def route(topology: Topology):
    """
    NDR P-02 COMPLIANT predicate order:
    Specific predicates evaluated first; hierarchical catch-all is LAST.
    This resolves the TC1/TC2 (SEQUENTIAL) and TC7/TC8 (FAN_OUT) shadow bug.

    Order:
      1. REJECTED  — exit immediately, no routing
      2. SEQUENTIAL — ordered linear chain
      3. FAN_OUT    — broadcast to N workers
      4. REFLEXIVE  — single-node self-loop
      5. HIERARCHICAL — catch-all for tree structures (LAST)
    """
    if topology.type == TopologyType.REJECTED:
        raise UnroutableTopologyError(
            f"Topology explicitly REJECTED: {topology}"
        )
    if topology.type == TopologyType.SEQUENTIAL:
        return SequentialRouter
    if topology.type == TopologyType.FAN_OUT:
        return FanOutRouter
    if topology.type == TopologyType.REFLEXIVE:
        return ReflexiveRouter
    if topology.type == TopologyType.HIERARCHICAL:
        return HierarchicalRouter
    raise UnroutableTopologyError(
        f"No router found for topology type: {topology.type}"
    )


def route_and_execute(topology: Topology) -> dict:
    """Convenience: resolve router class and execute routing in one call."""
    router_cls = route(topology)
    return router_cls.route(topology)
