"""
topology_router.py
==================
DGAF Topology Router — v1.1 (SWEEP-002 / Q-S043-04 fix)
Amethyst × COLLEEN · S043 · 2026-06-26

Bug fixed: Sequential and fan-out predicates were shadowed by
hierarchical catch-all (TC1, TC2, TC7, TC8 failures).
Fix: Reorder predicate evaluation to specific-before-general;
fan-out and sequential checks now run before hierarchical.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TopologyClass(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    HIERARCHICAL = "HIERARCHICAL"
    REFLEXIVE = "REFLEXIVE"
    FAN_OUT = "FAN_OUT"
    REJECTED = "REJECTED"


@dataclass
class RoutingPayload:
    agent_ids: List[str]
    authority_chain: List[str]
    dimensional_anchors: int  # Da
    open_blgs: int
    fan_out_declared: bool = False
    self_loop: bool = False


@dataclass
class RoutingDecision:
    topology: TopologyClass
    reason: str
    payload: RoutingPayload


class TopologyRouter:
    """
    Routes agentic payloads to topology class.

    Predicate evaluation order (specific → general — fixes TC1/TC2/TC7/TC8 shadow bug):
      1. Preflight gates (open_blgs, dimensional anchors)
      2. REJECTED (authority chain violations)
      3. REFLEXIVE (self-loop)
      4. FAN_OUT (declared fan-out with multiple agents)   ← was shadowed before
      5. SEQUENTIAL (ordered chain, single authority)       ← was shadowed before
      6. HIERARCHICAL (catch-all for multi-agent, multi-authority)
    """

    DA_MIN: int = 10

    def route(self, payload: RoutingPayload) -> RoutingDecision:
        # Preflight: open BLGs
        if payload.open_blgs > 0:
            return RoutingDecision(
                topology=TopologyClass.REJECTED,
                reason=f"Preflight failed: {payload.open_blgs} open BLG(s). Seal before routing.",
                payload=payload,
            )

        # Preflight: dimensional anchors
        if payload.dimensional_anchors < self.DA_MIN:
            return RoutingDecision(
                topology=TopologyClass.REJECTED,
                reason=f"Preflight failed: Da={payload.dimensional_anchors} < {self.DA_MIN} minimum.",
                payload=payload,
            )

        # Authority chain: must have at least one entry
        if not payload.authority_chain:
            return RoutingDecision(
                topology=TopologyClass.REJECTED,
                reason="Authority chain is empty.",
                payload=payload,
            )

        # REFLEXIVE: single agent, self-loop declared
        if payload.self_loop and len(payload.agent_ids) == 1:
            return RoutingDecision(
                topology=TopologyClass.REFLEXIVE,
                reason="Single agent self-loop declared.",
                payload=payload,
            )

        # FAN_OUT: fan_out explicitly declared + multiple agents (SPECIFIC — before hierarchical)
        if payload.fan_out_declared and len(payload.agent_ids) > 1:
            return RoutingDecision(
                topology=TopologyClass.FAN_OUT,
                reason=f"Fan-out declared across {len(payload.agent_ids)} agents.",
                payload=payload,
            )

        # SEQUENTIAL: ordered chain, single authority, multiple agents, no fan-out
        if (
            len(payload.agent_ids) > 1
            and len(payload.authority_chain) == 1
            and not payload.fan_out_declared
            and not payload.self_loop
        ):
            return RoutingDecision(
                topology=TopologyClass.SEQUENTIAL,
                reason="Ordered chain: multiple agents, single authority, no fan-out.",
                payload=payload,
            )

        # HIERARCHICAL: catch-all for multi-authority or ambiguous multi-agent
        return RoutingDecision(
            topology=TopologyClass.HIERARCHICAL,
            reason="Multi-authority or ambiguous multi-agent topology.",
            payload=payload,
        )


# ---------------------------------------------------------------------------
# Convenience factory
# ---------------------------------------------------------------------------

def make_router() -> TopologyRouter:
    return TopologyRouter()
