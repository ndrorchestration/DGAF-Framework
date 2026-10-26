"""Structural fixture tests only: NO PDMAL oscillator data or empirical N."""

import pytest

from tools.pdmal.comparator_fixtures import (
    circular_ladder_edges,
    derive_seed,
    fixture_fingerprint,
    label_permutation,
    named_comparator_edges,
    prospective_perturbation_vertex,
    random_connected_cubic_edges,
    relabel_cubic_graph,
    relabel_directed_delays,
    relabel_vertex_values,
    structural_distance_profile,
    validate_cubic_graph,
)
from tools.pdmal.delay_sandbox import simulate_delayed_kuramoto
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


def test_relabeling_seed_domains_are_reproducible_and_arm_specific():
    one = label_permutation(123, "dodecahedral_proxy", 0)
    assert one == label_permutation(123, "dodecahedral_proxy", 0)
    assert tuple(sorted(one)) == tuple(range(20))
    assert one != label_permutation(123, "circular_ladder", 0)
    assert one != label_permutation(123, "dodecahedral_proxy", 1)
    assert one != tuple(range(20))


def test_relabeling_preserves_graph_identity_up_to_vertex_permutation():
    for arm, edges in named_comparator_edges(seed=42).items():
        permutation = label_permutation(1234, arm, 1)
        remapped = relabel_cubic_graph(edges, permutation)
        inverse = [0] * 20
        for old, new in enumerate(permutation):
            inverse[new] = old
        assert relabel_cubic_graph(remapped, inverse) == edges
        assert len(remapped) == 30
        assert all(sum(node in edge for edge in remapped) == 3 for node in range(20))


@pytest.mark.parametrize(
    "bad_map",
    [
        tuple(range(19)),
        tuple([0] * 20),
        tuple(range(19)) + (20,),
        (True,) + tuple(range(1, 20)),
        (0.0,) + tuple(range(1, 20)),
    ],
)
def test_malformed_vertex_permutations_fail_closed(bad_map):
    with pytest.raises(ValueError):
        relabel_cubic_graph(DODECAHEDRAL_EDGES, bad_map)
    with pytest.raises(ValueError):
        relabel_vertex_values(tuple(range(20)), bad_map)
    with pytest.raises(ValueError):
        relabel_directed_delays({(0, 1): 2}, bad_map)


@pytest.mark.parametrize(
    "master, arm, replicate",
    [
        (True, "dodecahedral_proxy", 0),
        (123, "unknown", 0),
        (123, "circular_ladder", -1),
        (123, "random_connected_cubic", 1.25),
    ],
)
def test_labeling_invalid_seed_or_arm_fail_closed(master, arm, replicate):
    with pytest.raises(ValueError):
        label_permutation(master, arm, replicate)


def test_delay_orientation_validation_survives_relabeling():
    mapping = label_permutation(55, "dodecahedral_proxy", 0)
    remapped = relabel_directed_delays({(0, 1): 2, (1, 0): 7}, mapping)
    assert remapped[(mapping[0], mapping[1])] == 2
    assert remapped[(mapping[1], mapping[0])] == 7
    with pytest.raises(ValueError):
        relabel_directed_delays({(0, 20): 2}, mapping)
    with pytest.raises(ValueError):
        relabel_directed_delays({(0, 1): True}, mapping)


def test_delayed_oscillator_is_equivariant_under_coordinated_vertex_relabeling():
    # Metamorphic algorithm test on ONE graph, not any comparison or scientific outcome.
    base_edges = validate_cubic_graph(DODECAHEDRAL_EDGES)
    theta = tuple(0.15 * i for i in range(20))
    frequencies = tuple(0.02 * (i % 5 - 2) for i in range(20))
    directed_lags = {(0, 1): 2, (1, 0): 3, (0, 10): 1, (10, 0): 4}
    mapping = label_permutation(8888, "dodecahedral_proxy", 2)
    base = simulate_delayed_kuramoto(base_edges, theta, frequencies, delays=directed_lags, dt=0.05, steps=6)
    moved = simulate_delayed_kuramoto(
        relabel_cubic_graph(base_edges, mapping),
        relabel_vertex_values(theta, mapping),
        relabel_vertex_values(frequencies, mapping),
        delays=relabel_directed_delays(directed_lags, mapping),
        dt=0.05,
        steps=6,
    )
    for original, relabeled in zip(base, moved):
        assert max(abs(original[i] - relabeled[mapping[i]]) for i in range(20)) < 1e-12


def test_placement_sampling_separate_from_label_mapping():
    """A sampled *source* disturbance site and a relabeled site are distinct concepts."""
    site = prospective_perturbation_vertex(1963, "random_connected_cubic", 2)
    mapping = label_permutation(1963, "random_connected_cubic", 2)
    assert site == prospective_perturbation_vertex(1963, "random_connected_cubic", 2)
    assert 0 <= site < 20
    assert set(mapping) == set(range(20))
    mapped_site = mapping[site]
    inverse = [0] * 20
    for old, new in enumerate(mapping):
        inverse[new] = old
    assert inverse[mapped_site] == site
    assert derive_seed(1963, "label", 0) != derive_seed(1963, "placement", 0)


@pytest.mark.parametrize(
    "master, arm, replicate",
    [
        (True, "dodecahedral_proxy", 0),
        (123, "unknown", 0),
        (123, "circular_ladder", -1),
        (123, "random_connected_cubic", 2.5),
    ],
)
def test_prospective_placement_rejects_invalid_inputs(master, arm, replicate):
    with pytest.raises(ValueError):
        prospective_perturbation_vertex(master, arm, replicate)


def test_distance_profile_preserved_at_same_structural_site_after_relabeling():
    """Graph distances are label-invariant metadata, not robustness outcomes."""
    for arm, edges in named_comparator_edges(seed=271828).items():
        source = prospective_perturbation_vertex(90210, arm, 0)
        permutation = label_permutation(90210, arm, 0)
        original_profile = structural_distance_profile(edges, source)
        mapped_graph = relabel_cubic_graph(edges, permutation)
        mapped_profile = structural_distance_profile(mapped_graph, permutation[source])
        assert original_profile == mapped_profile
        assert len(original_profile) == 20
        assert original_profile[:4] == (0, 1, 1, 1)
        assert all(distance >= 0 for distance in original_profile)


@pytest.mark.parametrize("invalid_site", [True, -1, 20, 1.5, "0"])
def test_distance_profile_rejects_invalid_site_indices(invalid_site):
    with pytest.raises(ValueError):
        structural_distance_profile(DODECAHEDRAL_EDGES, invalid_site)
