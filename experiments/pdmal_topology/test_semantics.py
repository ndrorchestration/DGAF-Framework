import networkx as nx

from graph_harness import apply_node_failures, structural_metrics


def test_original_population_denominator_on_healthy_graph():
    g = nx.path_graph(10)
    metrics = structural_metrics(g, original_nodes=10)
    assert metrics["largest_component_size"] == 10
    assert metrics["largest_component_fraction"] == 1.0
    assert metrics["connectivity_threshold_met"] is True


def test_post_failure_component_semantics():
    g = nx.path_graph(10)
    post = apply_node_failures(g, (4,))
    metrics = structural_metrics(post, original_nodes=10)
    assert metrics["largest_component_size"] == 5
    assert metrics["largest_component_fraction"] == 0.5
    assert metrics["connectivity_threshold_met"] is True


def test_post_failure_metrics_use_surviving_components_not_original_graph():
    g = nx.path_graph(10)
    post = apply_node_failures(g, (4, 5))
    metrics = structural_metrics(post, original_nodes=10)
    assert metrics["largest_component_size"] == 4
    assert metrics["largest_component_fraction"] == 0.4
    assert metrics["connectivity_threshold_met"] is False
