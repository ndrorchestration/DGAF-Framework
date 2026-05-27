"""
test_topology.py — Unit tests for topology constants.

Covers:
  - PHI value precision
  - All Triad-C agents exist in AGENT_ROLES
  - All PENTAGON_EDGES keys reference known agents
  - All edge weights are in (0, 1]
  - Pentagon has correct number of edges (10)
  - TRIAD_C maps three distinct roles to three distinct agents
"""
from __future__ import annotations
import math
import pytest

from pptl.topology import PHI, PENTAGON_EDGES, AGENT_ROLES, TRIAD_C

KNOWN_AGENTS = set(AGENT_ROLES.keys())


@pytest.mark.unit
def test_phi_value_precision():
    """PHI = 1/phi = phi - 1 = 0.6180..."""
    assert math.isclose(PHI, 0.6180339887, rel_tol=1e-9)


@pytest.mark.unit
def test_phi_golden_ratio_identity():
    """PHI^2 + PHI == 1  (defining identity of conjugate golden ratio)"""
    assert math.isclose(PHI ** 2 + PHI, 1.0, rel_tol=1e-9)


@pytest.mark.unit
def test_pentagon_edge_count():
    assert len(PENTAGON_EDGES) == 10


@pytest.mark.unit
def test_all_edge_agents_known():
    for src, dst in PENTAGON_EDGES:
        assert src in KNOWN_AGENTS, f"Unknown source agent: {src}"
        assert dst in KNOWN_AGENTS, f"Unknown dest agent: {dst}"


@pytest.mark.unit
def test_all_edge_weights_in_range():
    for edge, w in PENTAGON_EDGES.items():
        assert 0 < w <= 1.0, f"Edge {edge} weight {w} out of (0, 1]"


@pytest.mark.unit
def test_triad_c_roles():
    assert set(TRIAD_C.keys()) == {"Task", "Style", "Safety"}


@pytest.mark.unit
def test_triad_c_agents_known():
    for role, agent in TRIAD_C.items():
        assert agent in KNOWN_AGENTS, f"Triad-C {role} → unknown agent {agent}"


@pytest.mark.unit
def test_triad_c_agents_distinct():
    agents = list(TRIAD_C.values())
    assert len(agents) == len(set(agents)), "Triad-C agents must be distinct"
