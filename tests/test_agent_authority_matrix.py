from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_MATRIX.md"
INVARIANT = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_INVARIANT.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"required governance artifact missing: {path}"
    return path.read_text(encoding="utf-8")


def test_authority_matrix_is_present_and_scoped():
    matrix = _read(MATRIX)
    invariant = _read(INVARIANT)

    assert "DGAF-AUTH-001" in matrix
    assert "ACTIVE — BASELINE DERIVATIVE" in matrix
    assert "does not grant authority" in matrix
    assert "Shared governance ontology MUST NOT imply shared authority." in invariant
    assert "Layer 0 is a **shared constitutional substrate**" in matrix


def test_matrix_preserves_non_delegation_boundaries():
    matrix = _read(MATRIX)
    required = (
        "Capability overlap does not create authority overlap.",
        "Advisory output MUST NOT silently become authorization.",
        "Execution MUST require the authorization defined by the governing contract.",
        "A system STATE such as Ionia/0Hz MUST NOT be treated as an agent with independent authority.",
        "T3/SOVEREIGN material remains subject to the repository's IP firewall and Drive-only rules.",
    )
    for text in required:
        assert text in matrix


def test_matrix_contains_all_key_specialists():
    matrix = _read(MATRIX)
    for agent in (
        "Amethyst",
        "Apogee",
        "Perigee",
        "Professor Prodigy",
        "COLLEEN",
        "The Librarian",
        "The Auditor",
        "The Actualizer",
        "Zenith",
        "Reson",
        "Lyra",
        "Echolette",
        "Ionia",
        "DemiJoule",
        "Herald",
        "Reciprocity",
        "Sentinel-Φ / Sentinel",
        "Sentience",
    ):
        assert agent in matrix


def test_reconciliation_targets_are_explicit():
    matrix = _read(MATRIX)
    assert "legacy role text" in matrix
    assert "Layer-0 attribution/ownership language" in matrix
    assert "Sentinel versus Sentinel-Φ naming" in matrix
    assert "historical IDs versus current formation IDs" in matrix
