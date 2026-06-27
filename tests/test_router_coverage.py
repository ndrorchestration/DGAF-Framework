"""
test_router_coverage.py
=======================
Topology Router Coverage Tests — 8/8 TC (SWEEP-002 Q-S043-04 fix)
Amethyst × COLLEEN · S043 · 2026-06-26

Fixed: TC1 (SEQUENTIAL single-pair), TC2 (SEQUENTIAL chain),
       TC7 (FAN_OUT 3-agent), TC8 (FAN_OUT 2-agent) previously
       misclassified as HIERARCHICAL due to predicate shadowing.
"""
import pytest
from components.topology_router import TopologyRouter, TopologyClass, RoutingPayload, make_router


@pytest.fixture
def router() -> TopologyRouter:
    return make_router()


def _payload(agents=None, authority=None, da=15, open_blgs=0, fan_out=False, self_loop=False):
    return RoutingPayload(
        agent_ids=agents or ["Amethyst"],
        authority_chain=authority or ["human_owner"],
        dimensional_anchors=da,
        open_blgs=open_blgs,
        fan_out_declared=fan_out,
        self_loop=self_loop,
    )


class TestTC1Sequential:
    def test_tc1_sequential_pair(self, router):
        """TC1: Two agents, single authority → SEQUENTIAL (was HIERARCHICAL)."""
        r = router.route(_payload(agents=["Amethyst", "COLLEEN"], authority=["human_owner"]))
        assert r.topology == TopologyClass.SEQUENTIAL, f"TC1 failed: got {r.topology}"


class TestTC2Sequential:
    def test_tc2_sequential_chain(self, router):
        """TC2: Three agents, single authority → SEQUENTIAL (was HIERARCHICAL)."""
        r = router.route(_payload(agents=["Amethyst", "COLLEEN", "Herald"], authority=["human_owner"]))
        assert r.topology == TopologyClass.SEQUENTIAL, f"TC2 failed: got {r.topology}"


class TestTC3Reflexive:
    def test_tc3_reflexive(self, router):
        r = router.route(_payload(agents=["Amethyst"], self_loop=True))
        assert r.topology == TopologyClass.REFLEXIVE


class TestTC4Hierarchical:
    def test_tc4_hierarchical_multi_authority(self, router):
        r = router.route(_payload(agents=["Amethyst", "COLLEEN"], authority=["human_owner", "Ender"]))
        assert r.topology == TopologyClass.HIERARCHICAL


class TestTC5Rejected:
    def test_tc5_rejected_open_blgs(self, router):
        r = router.route(_payload(open_blgs=2))
        assert r.topology == TopologyClass.REJECTED


class TestTC6Rejected:
    def test_tc6_rejected_low_da(self, router):
        r = router.route(_payload(da=5))
        assert r.topology == TopologyClass.REJECTED


class TestTC7FanOut:
    def test_tc7_fan_out_three_agents(self, router):
        """TC7: Explicit fan-out, 3 agents → FAN_OUT (was HIERARCHICAL)."""
        r = router.route(_payload(agents=["Amethyst", "COLLEEN", "Herald"], fan_out=True))
        assert r.topology == TopologyClass.FAN_OUT, f"TC7 failed: got {r.topology}"


class TestTC8FanOut:
    def test_tc8_fan_out_two_agents(self, router):
        """TC8: Explicit fan-out, 2 agents → FAN_OUT (was HIERARCHICAL)."""
        r = router.route(_payload(agents=["Amethyst", "DemiJoule"], fan_out=True))
        assert r.topology == TopologyClass.FAN_OUT, f"TC8 failed: got {r.topology}"


class TestFullCoverage:
    def test_all_eight_cases_pass(self, router):
        """Regression: all 8 topology classes reachable, 0 shadowing."""
        cases = [
            (_payload(agents=["A", "B"], authority=["human_owner"]), TopologyClass.SEQUENTIAL),
            (_payload(agents=["A", "B", "C"], authority=["human_owner"]), TopologyClass.SEQUENTIAL),
            (_payload(agents=["A"], self_loop=True), TopologyClass.REFLEXIVE),
            (_payload(agents=["A", "B"], authority=["human_owner", "Ender"]), TopologyClass.HIERARCHICAL),
            (_payload(open_blgs=1), TopologyClass.REJECTED),
            (_payload(da=3), TopologyClass.REJECTED),
            (_payload(agents=["A", "B", "C"], fan_out=True), TopologyClass.FAN_OUT),
            (_payload(agents=["A", "B"], fan_out=True), TopologyClass.FAN_OUT),
        ]
        failures = [(got, exp) for got, exp in [(router.route(p).topology, e) for p, e in cases] if got != exp]
        assert not failures, f"Coverage failures: {failures}"
