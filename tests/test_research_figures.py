from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import networkx as nx
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "research_figures" / "generate_research_figures.py"


def load_module():
    spec = importlib.util.spec_from_file_location("research_figures", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_fixture_sources(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "experiments" / "pdmal_topology").mkdir(parents=True, exist_ok=True)
    (root / "tools" / "research_figures").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "CURRENT_STATE.md").write_text(
        """---
status: ACTIVE
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
canonical_high_assurance_empirical_n: 0
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_successor_collection: COMPLETE_50_PAIRED_SEED_UNITS_2250_BLINDED_OBSERVATIONS
track_a_successor_dataset_lock: NOT_ESTABLISHED
track_a_successor_unblinding: NOT_AUTHORIZED
track_a_successor_materialization: NOT_ESTABLISHED
track_a_successor_primary_analysis: NOT_AUTHORIZED_NOT_RUN
---
# Current state

The accepted Epoch 002 design remains:
- 50 prospective seeds: `20270201..20270250`;
- 5 topologies: ring, PDMAL, random-regular, small-world, complete;
- 9 failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`;
- 45 blinded cells per seed / 2,250 raw observations;

The current governed order is:

`repository custody acceptance — ACCEPTED`
`→ precollection preflight — ACCEPTED`
`→ Epoch 002 immutable freeze — ESTABLISHED`
`→ empirical collection — COMPLETE`
`→ operator retained-byte admission — CURRENT FRONTIER`
`→ PASS QC ledger`
`→ dataset-lock receipt`
`→ separate human-controlled unblinding decision`
`→ controlled local materialization`
`→ immutable materialization receipt`
`→ separate primary-analysis authorization`
`→ locked primary analysis`
`→ interpretation/adjudication`
""",
        encoding="utf-8",
    )
    (root / "experiments" / "pdmal_topology" / "seeds.py").write_text(
        """import hashlib

def derive_seed(master_seed: int, stream: str) -> int:
    raw = f"pdmal-v1|{master_seed}|{stream}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")
""",
        encoding="utf-8",
    )
    (root / "experiments" / "pdmal_topology" / "graph_harness.py").write_text(
        """import networkx as nx
from seeds import derive_seed

def build_topologies(seed: int):
    topology_seed = derive_seed(seed, "topology")
    return {
        "ring": nx.cycle_graph(20),
        "pdmal": nx.dodecahedral_graph(),
        "random_regular": nx.random_regular_graph(3, 20, seed=topology_seed),
        "small_world": nx.watts_strogatz_graph(20, 4, 0.3, seed=topology_seed),
        "complete": nx.complete_graph(20),
    }
""",
        encoding="utf-8",
    )


def write_manifest(root: Path) -> None:
    manifest = [
        {"id": "FIG-001", "title": "Research Program Architecture Map", "priority": "P0", "epistemic_class": "DESIGN", "source_bindings": ["docs/CURRENT_STATE.md"], "output": "docs/research_figures/generated/fig001_research_program_architecture.svg"},
        {"id": "FIG-002", "title": "Five-Topology Structural Comparison", "priority": "P0", "epistemic_class": "STRUCTURAL", "source_bindings": ["experiments/pdmal_topology/graph_harness.py"], "output": "docs/research_figures/generated/fig002_topology_comparison.svg"},
        {"id": "FIG-003", "title": "Track A Epoch 002 Design Matrix", "priority": "P0", "epistemic_class": "DESIGN", "source_bindings": ["docs/CURRENT_STATE.md"], "output": "docs/research_figures/generated/fig003_epoch002_design_matrix.svg"},
        {"id": "FIG-004", "title": "Governance Transition State Machine", "priority": "P0", "epistemic_class": "GOVERNANCE", "source_bindings": ["docs/CURRENT_STATE.md"], "output": "docs/research_figures/generated/fig004_governance_state_machine.svg"},
        {"id": "FIG-005", "title": "Evidence and Provenance DAG", "priority": "P0", "epistemic_class": "PROVENANCE", "source_bindings": ["docs/CURRENT_STATE.md"], "output": "docs/research_figures/generated/fig005_evidence_provenance_dag.svg"},
    ]
    path = root / "tools" / "research_figures" / "figure_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def test_generator_module_exists():
    assert MODULE_PATH.exists(), "research-figure generator must be present"


def test_manifest_and_parsers(tmp_path: Path):
    mod = load_module()
    write_fixture_sources(tmp_path)
    write_manifest(tmp_path)
    specs = mod.load_manifest(tmp_path)
    assert [s.figure_id for s in specs] == [f"FIG-{i:03d}" for i in range(1, 6)]
    state = (tmp_path / "docs" / "CURRENT_STATE.md").read_text(encoding="utf-8")
    frontmatter = mod.parse_frontmatter(state)
    assert frontmatter["canonical_high_assurance_empirical_n"] == "0"
    chain = mod.parse_transition_chain(state)
    assert chain[0] == "repository custody acceptance — ACCEPTED"
    assert "operator retained-byte admission — CURRENT FRONTIER" in chain


def test_manifest_rejects_escaping_output(tmp_path: Path):
    mod = load_module()
    write_fixture_sources(tmp_path)
    write_manifest(tmp_path)
    path = tmp_path / "tools" / "research_figures" / "figure_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data[0]["output"] = "../escape.svg"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(mod.FigureGenerationError):
        mod.load_manifest(tmp_path)


def test_canonical_topology_invariants(tmp_path: Path):
    mod = load_module()
    write_fixture_sources(tmp_path)
    graphs = mod.load_topologies(tmp_path, reference_seed=20270201)
    assert list(graphs) == ["ring", "pdmal", "random_regular", "small_world", "complete"]
    assert {name: g.number_of_nodes() for name, g in graphs.items()} == {name: 20 for name in graphs}
    assert {name: g.number_of_edges() for name, g in graphs.items()} == {
        "ring": 20,
        "pdmal": 30,
        "random_regular": 30,
        "small_world": 40,
        "complete": 190,
    }
    assert {degree for _, degree in graphs["pdmal"].degree()} == {3}


def test_render_all_is_deterministic_and_source_bound(tmp_path: Path):
    mod = load_module()
    write_fixture_sources(tmp_path)
    write_manifest(tmp_path)
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    files1 = mod.render_all(tmp_path, out1)
    files2 = mod.render_all(tmp_path, out2)
    assert len(files1) == 5
    assert len(files2) == 5
    for a, b in zip(files1, files2, strict=True):
        raw_a = a.read_bytes()
        raw_b = b.read_bytes()
        assert raw_a == raw_b
        assert hashlib.sha256(raw_a).hexdigest() == hashlib.sha256(raw_b).hexdigest()
        root = ET.fromstring(raw_a)
        assert root.tag.endswith("svg")
        assert root.attrib["data-figure-id"].startswith("FIG-")
        assert root.attrib["data-epistemic-class"] in {"DESIGN", "STRUCTURAL", "GOVERNANCE", "PROVENANCE"}
        assert root.attrib["data-source-digest"]


def test_design_matrix_is_descriptive_not_outcome_bearing(tmp_path: Path):
    mod = load_module()
    write_fixture_sources(tmp_path)
    write_manifest(tmp_path)
    path = mod.render_all(tmp_path, tmp_path / "generated")[2]
    text = path.read_text(encoding="utf-8")
    assert "2,250 blinded cells" in text
    assert "50 paired seed units" in text
    assert "failure counts" in text
    forbidden = ["effect size", "confidence interval", "dgaf wins", "efficacy established", "unblinded result"]
    lowered = text.lower()
    assert all(term not in lowered for term in forbidden)


def test_repository_sources_generate_all_first_wave_figures(tmp_path: Path):
    mod = load_module()
    outputs = mod.render_all(ROOT, tmp_path / "repo_render")
    assert [p.name for p in outputs] == [
        "fig001_research_program_architecture.svg",
        "fig002_topology_comparison.svg",
        "fig003_epoch002_design_matrix.svg",
        "fig004_governance_state_machine.svg",
        "fig005_evidence_provenance_dag.svg",
    ]
    assert all(p.stat().st_size > 1000 for p in outputs)


def test_current_state_figures_humanize_machine_tokens_and_show_source_freshness(tmp_path: Path):
    mod = load_module()
    outputs = mod.render_all(ROOT, tmp_path / "humanized")
    fig1 = outputs[0].read_text(encoding="utf-8")
    fig4 = outputs[3].read_text(encoding="utf-8")
    assert "COMPLETE_50_PAIRED_SEED_UNITS_2250_BLINDED_OBSERVATIONS" not in fig1
    assert "50 paired seed units / 2,250 blinded observations" in fig1
    assert "efficacy: NOT ESTABLISHED" in fig1
    state = (ROOT / "docs" / "CURRENT_STATE.md").read_text(encoding="utf-8")
    stamp = mod.parse_frontmatter(state)["last_verified"]
    assert f"Source snapshot last_verified: {stamp}" in fig1
    assert f"Source snapshot last_verified: {stamp}" in fig4


def test_committed_first_wave_outputs_match_fresh_regeneration(tmp_path: Path):
    mod = load_module()
    fresh = mod.render_all(ROOT, tmp_path / "fresh")
    committed_root = ROOT / "docs" / "research_figures" / "generated"
    for generated in fresh:
        committed = committed_root / generated.name
        assert committed.is_file(), f"missing committed figure: {committed}"
        assert committed.read_bytes() == generated.read_bytes(), f"stale committed figure: {committed.name}"
