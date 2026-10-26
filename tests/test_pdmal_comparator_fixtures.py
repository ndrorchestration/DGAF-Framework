"""Structural fixture tests only: NO PDMAL oscillator data or empirical N."""

import pytest

from tools.pdmal.comparator_fixtures import (
    circular_ladder_edges,
    derive_seed,
    fixture_fingerprint,
    named_comparator_edges,
    random_connected_cubic_edges,
    validate_cubic_graph,
)
from tools.pdmal.lattice_harness import DODECAHEDRAL_EDGES


def test_all_comparator_families_match_node_edge_and_degree_budget():
    fixtures = named_comparator_edges(seed=271828)
    assert set(fixtures) == {"dodecahedral_proxy", "circular_ladder", "random_connected_cubic"}
    for edges in fixtures.values():
        assert len(edges) == 30
        assert len({vertex for edge in edges for vertex in edge}) == 20
        assert all(sum(i in edge for edge in edges) == 3 for i in range(20))
        assert edges == validate_cubic_graph(edges)
    assert fixtures["dodecahedral_proxy"] == validate_cubic_graph(DODECAHEDRAL_EDGES)


def test_circular_ladder_contains_two_cycles_and_rungs():
    edges = set(circular_ladder_edges())
    assert (0, 9) in edges
    assert (10, 19) in edges
    assert (0, 10) in edges
    assert (9, 19) in edges


def test_random_cubic_fixed_seed_replays_and_has_stable_labeled_fingerprint():
    one = random_connected_cubic_edges(seed=103)
    two = random_connected_cubic_edges(seed=103)
    assert one == two
    assert fixture_fingerprint(one) == fixture_fingerprint(two)
    assert len(fixture_fingerprint(one)) == 64


def test_multiple_seed_draws_satisfy_only_structural_invariants():
    # These are structural smoke checks, NOT sampling observations or efficacy data.
    for index in range(4):
        edges = random_connected_cubic_edges(seed=derive_seed(123, "graph", index))
        assert len(validate_cubic_graph(edges)) == 30


def test_separate_graph_and_perturbation_seed_domains():
    assert derive_seed(123, "graph", 0) == derive_seed(123, "graph", 0)
    assert derive_seed(123, "graph", 0) != derive_seed(123, "graph", 1)
    assert derive_seed(123, "graph", 0) != derive_seed(123, "perturbation", 0)
    assert derive_seed(123, "perturbation", 0) != derive_seed(124, "perturbation", 0)


@pytest.mark.parametrize(
    "bad_edges",
    [
        ((0, 1),),
        ((0, 0),),
        ((0, 20),),
        ((0, 1), (1, 0)),
        ((True, 1),),
    ],
)
def test_invalid_or_incomplete_graphs_rejected(bad_edges):
    with pytest.raises(ValueError):
        validate_cubic_graph(bad_edges)


@pytest.mark.parametrize(
    "options",
    [
        {"seed": True},
        {"seed": 1.5},
        {"seed": 3, "max_attempts": 0},
        {"seed": 3, "max_attempts": True},
    ],
)
def test_random_graph_invalid_seeds_fail_closed(options):
    with pytest.raises(ValueError):
        random_connected_cubic_edges(**options)


def test_bounded_retry_failure_is_explicit():
    # Stub pairing may reject a particular first draw; fix the seed as a fixture.
    with pytest.raises(RuntimeError):
        random_connected_cubic_edges(seed=0, max_attempts=1)


@pytest.mark.parametrize(
    "master, domain, index",
    [
        (True, "graph", 0),
        (1, "topology", 0),
        (1, "perturbation", -1),
        (1, "graph", 1.1),
    ],
)
def test_seed_derivation_invalid_inputs_rejected(master, domain, index):
    with pytest.raises(ValueError):
        derive_seed(master, domain, index)


def test_labeled_fingerprints_distinguish_the_fixed_comparators():
    assert fixture_fingerprint(DODECAHEDRAL_EDGES) != fixture_fingerprint(circular_ladder_edges())
