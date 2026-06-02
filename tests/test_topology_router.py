"""
test_topology_router.py
Full TC1–TC8 coverage for topology_router.py.
Closes Q-S043-04: 8/8 TC pass rate required.

Agent: Amethyst · Session: S044 · 2026-06-01
"""

import pytest
from components.topology_router import (
    Topology, TopologyType, route, route_and_execute,
    SequentialRouter, FanOutRouter, ReflexiveRouter, HierarchicalRouter,
    UnroutableTopologyError,
)


# TC1 — SEQUENTIAL basic
def test_tc1_sequential_basic():
    t = Topology(type=TopologyType.SEQUENTIAL, node_count=3)
    assert route(t) is SequentialRouter


# TC2 — SEQUENTIAL with execute
def test_tc2_sequential_execute():
    t = Topology(type=TopologyType.SEQUENTIAL, node_count=5)
    result = route_and_execute(t)
    assert result["router"] == "SEQUENTIAL"
    assert result["nodes"] == 5


# TC3 — REFLEXIVE
def test_tc3_reflexive():
    t = Topology(type=TopologyType.REFLEXIVE, node_count=1)
    assert route(t) is ReflexiveRouter


# TC4 — HIERARCHICAL
def test_tc4_hierarchical():
    t = Topology(type=TopologyType.HIERARCHICAL, depth=4)
    assert route(t) is HierarchicalRouter


# TC5 — REJECTED raises
def test_tc5_rejected_raises():
    t = Topology(type=TopologyType.REJECTED)
    with pytest.raises(UnroutableTopologyError):
        route(t)


# TC6 — REJECTED does not route to hierarchical
def test_tc6_rejected_no_fallthrough():
    t = Topology(type=TopologyType.REJECTED)
    with pytest.raises(UnroutableTopologyError) as exc_info:
        route(t)
    assert "REJECTED" in str(exc_info.value)


# TC7 — FAN_OUT basic
def test_tc7_fanout_basic():
    t = Topology(type=TopologyType.FAN_OUT, fan_factor=8)
    assert route(t) is FanOutRouter


# TC8 — FAN_OUT execute
def test_tc8_fanout_execute():
    t = Topology(type=TopologyType.FAN_OUT, fan_factor=4)
    result = route_and_execute(t)
    assert result["router"] == "FAN_OUT"
    assert result["fan_factor"] == 4


# PREDICATE ORDER INVARIANT — SEQUENTIAL must not resolve as HIERARCHICAL
def test_predicate_order_sequential_not_hierarchical():
    t = Topology(type=TopologyType.SEQUENTIAL, node_count=2)
    router = route(t)
    assert router is not HierarchicalRouter, (
        "SEQUENTIAL resolved as HIERARCHICAL — predicate shadow bug regressed"
    )


# PREDICATE ORDER INVARIANT — FAN_OUT must not resolve as HIERARCHICAL
def test_predicate_order_fanout_not_hierarchical():
    t = Topology(type=TopologyType.FAN_OUT, fan_factor=2)
    router = route(t)
    assert router is not HierarchicalRouter, (
        "FAN_OUT resolved as HIERARCHICAL — predicate shadow bug regressed"
    )
