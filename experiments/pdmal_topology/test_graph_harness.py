import networkx as nx

from graph_harness import apply_node_failures, build_topologies, random_node_failures, structural_metrics
from seeds import derive_seed


def test_topology_invariants():
    graphs = build_topologies(7)
    assert set(graphs) == {"ring", "pdmal", "random_regular", "small_world", "complete"}
    assert all(g.number_of_nodes() == 20 for g in graphs.values())
    assert graphs["ring"].number_of_edges() == 20
    assert graphs["pdmal"].number_of_edges() == 30
    assert graphs["random_regular"].number_of_edges() == 30
    assert graphs["small_world"].number_of_edges() == 40
    assert graphs["complete"].number_of_edges() == 190
    assert nx.is_connected(graphs["pdmal"])
    assert nx.node_connectivity(graphs["pdmal"]) == 3
    assert nx.diameter(graphs["pdmal"]) == 5
    assert nx.node_connectivity(graphs["ring"]) == 2
    assert nx.diameter(graphs["ring"]) == 10


def test_seed_reproducibility_for_randomized_topologies():
    a = build_topologies(123)
    b = build_topologies(123)
    for name in ("random_regular", "small_world"):
        assert nx.utils.graphs_equal(a[name], b[name])


def test_rng_streams_are_deterministic_but_distinct():
    assert derive_seed(123, "topology") == derive_seed(123, "topology")
    assert derive_seed(123, "failure") == derive_seed(123, "failure")
    assert derive_seed(123, "topology") != derive_seed(123, "failure")


def test_failure_sets_are_reproducible_and_without_replacement():
    a = random_node_failures(123, 6)
    b = random_node_failures(123, 6)
    assert a == b
    assert len(a) == len(set(a)) == 6


def test_failure_application_and_metrics():
    graph = build_topologies(1)["pdmal"]
    failed = random_node_failures(1, 2)
    result = apply_node_failures(graph, failed)
    metrics = structural_metrics(result)
    assert result.number_of_nodes() == 18
    assert 0.0 <= metrics["largest_component_fraction"] <= 1.0
    assert metrics["component_count"] >= 1


def test_population_denominator_and_connectivity_threshold_are_frozen():
    graph = nx.path_graph(10)
    metrics = structural_metrics(graph, original_nodes=20)
    assert metrics["nodes_remaining"] == 10
    assert metrics["largest_component_fraction"] == 0.5
    assert metrics["connectivity_threshold_met"] is True
