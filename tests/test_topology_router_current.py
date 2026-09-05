"""Current TopologyRouter regression suite.

Ported from the intent of historical SWEEP-002 TC1-TC8 tests to the
current TopologyRouter API. These tests validate behavior, not historical
class/function names.
"""

import pytest

from components.topology_router import (
    RoutingPayload,
    TopologyClass,
    TopologyRouter,
)


@pytest.fixture
def router():
    return TopologyRouter()


def payload(**overrides):
    base = dict(
        agent_ids=["a", "b"],
        authority_chain=["root"],
        dimensional_anchors=10,
        open_blgs=0,
    )
    base.update(overrides)
    return RoutingPayload(**base)


def test_sequential_basic(router):
    decision = router.route(payload())
    assert decision.topology is TopologyClass.SEQUENTIAL


def test_sequential_requires_single_authority(router):
    decision = router.route(payload(authority_chain=["root", "delegate"]))
    assert decision.topology is TopologyClass.HIERARCHICAL


def test_reflexive_single_agent(router):
    decision = router.route(payload(agent_ids=["a"], self_loop=True))
    assert decision.topology is TopologyClass.REFLEXIVE


def test_reflexive_requires_single_agent(router):
    decision = router.route(payload(self_loop=True))
    assert decision.topology is TopologyClass.HIERARCHICAL


def test_hierarchical_multi_authority(router):
    decision = router.route(payload(authority_chain=["root", "delegate"]))
    assert decision.topology is TopologyClass.HIERARCHICAL


def test_rejected_open_blgs(router):
    decision = router.route(payload(open_blgs=1))
    assert decision.topology is TopologyClass.REJECTED
    assert "open BLG" in decision.reason


def test_rejected_insufficient_dimensional_anchors(router):
    decision = router.route(payload(dimensional_anchors=9))
    assert decision.topology is TopologyClass.REJECTED
    assert "Da=9" in decision.reason


def test_rejected_empty_authority_chain(router):
    decision = router.route(payload(authority_chain=[]))
    assert decision.topology is TopologyClass.REJECTED
    assert "Authority chain" in decision.reason


def test_fan_out_basic(router):
    decision = router.route(payload(fan_out_declared=True))
    assert decision.topology is TopologyClass.FAN_OUT


def test_fan_out_requires_multiple_agents(router):
    decision = router.route(payload(agent_ids=["a"], fan_out_declared=True))
    assert decision.topology is TopologyClass.HIERARCHICAL


def test_predicate_order_sequential_not_hierarchical(router):
    decision = router.route(payload())
    assert decision.topology is not TopologyClass.HIERARCHICAL
    assert decision.topology is TopologyClass.SEQUENTIAL


def test_predicate_order_fanout_not_hierarchical(router):
    decision = router.route(payload(fan_out_declared=True))
    assert decision.topology is not TopologyClass.HIERARCHICAL
    assert decision.topology is TopologyClass.FAN_OUT


def test_preflight_takes_precedence_over_topology(router):
    decision = router.route(payload(fan_out_declared=True, open_blgs=1))
    assert decision.topology is TopologyClass.REJECTED


def test_deterministic_routing(router):
    p = payload(fan_out_declared=True)
    first = router.route(p)
    second = router.route(p)
    assert first.topology is second.topology
    assert first.reason == second.reason
