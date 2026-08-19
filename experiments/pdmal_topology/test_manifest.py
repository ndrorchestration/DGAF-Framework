from pathlib import Path

import yaml


ROOT = Path(__file__).parent
MANIFEST = yaml.safe_load((ROOT / "manifest.yaml").read_text())


def test_manifest_freezes_primary_design():
    assert MANIFEST["experiment"]["nodes"] == 20
    assert MANIFEST["experiment"]["pilot_seeds"] == 50
    assert MANIFEST["failures"]["primary_class"] == "random_node"
    assert MANIFEST["failures"]["counts"] == [0, 1, 2, 3, 4, 5, 6, 8, 10]
    assert MANIFEST["analysis"]["paired_by_seed"] is True


def test_all_required_topologies_are_present():
    assert set(MANIFEST["topologies"]) == {
        "ring",
        "pdmal",
        "random_regular",
        "small_world",
        "complete",
    }


def test_results_are_not_predeclared():
    assert MANIFEST["provenance"]["results"] == "none"
