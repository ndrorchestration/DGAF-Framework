import json
from pathlib import Path

from scripts.validate_structural_epistemics_claim_graph import validate_claim_graph

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "docs/research/claim_graphs"


def test_all_registered_structural_epistemics_claim_graphs_validate() -> None:
    assert REGISTRY_DIR.is_dir()
    for path in sorted(REGISTRY_DIR.glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        validate_claim_graph(value)
