from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import networkx as nx


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "pdmal" / "lattice_harness.py"
SPEC = spec_from_file_location("pdmal_lattice_harness", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
HARNESS = module_from_spec(SPEC)
SPEC.loader.exec_module(HARNESS)


def test_dodecahedral_unweighted_curvature_reports_no_discriminating_signal():
    graph = HARNESS.build_pdmal_lattice()
    audit = HARNESS.lattice_audit(graph)

    assert graph.number_of_nodes() == 20
    assert graph.number_of_edges() == 30
    assert audit["n_edges"] == 30
    assert audit["ricci_min"] == -2.0
    assert audit["ricci_mean"] == -2.0
    assert audit["ricci_variance"] == 0.0
    assert audit["signal_state"] == HARNESS.NO_DISCRIMINATING_SIGNAL
    assert audit["threshold_flagging_available"] is False
    assert audit["flagged_edges"] == []


def test_nonregular_graph_retains_explicit_threshold_semantics():
    graph = nx.path_graph(4)
    audit = HARNESS.lattice_audit(graph, ricci_floor=0.0)

    assert audit["ricci_variance"] > 0.0
    assert audit["signal_state"] == HARNESS.THRESHOLD_APPLIED
    assert audit["threshold_flagging_available"] is True
    assert audit["flagged_edges"] == [(1, 2)]


def test_source_artifact_identity_is_preserved_as_provenance_only():
    assert HARNESS.SOURCE_ARTIFACT_SHA256 == (
        "f8382b68bbf155fe574bd76118db6fc2142c558c21d0f109e3b92103a1611216"
    )
