from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_MATRIX.md"
INVARIANT = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_INVARIANT.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"required governance artifact missing: {path}"
    return path.read_text(encoding="utf-8")


def _persona_lineage_rows(matrix: str) -> set[str]:
    rows = set()
    in_lineage = False
    for line in matrix.splitlines():
        if line.strip() == "## 3. Persona / Identity Lineage Derivative (Non-Authoritative)":
            in_lineage = True
            continue
        if in_lineage and line.startswith("## "):
            break
        if in_lineage and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 1 and cells[0] not in {"Persona / identity", "---"}:
                rows.add(cells[0])
    return rows


def test_authority_matrix_is_present_and_scoped():
    matrix = _read(MATRIX)
    invariant = _read(INVARIANT)
    assert "DGAF-AUTH-001" in matrix
    assert "ACTIVE — BASELINE DERIVATIVE" in matrix
    assert "does not grant authority" in matrix
    assert "Shared governance ontology MUST NOT imply shared authority." in invariant
    assert "Layer 0 is a distributed constitutional constraint" in matrix


def test_matrix_preserves_non_delegation_boundaries():
    matrix = _read(MATRIX)
    required = (
        "Capability overlap does not create authority overlap.",
        "Advisory output MUST NOT silently become authorization.",
        "Execution MUST require the authorization defined by the governing contract.",
        "State representations such as Ionia/0Hz MUST NOT be treated as independent agents with authority.",
        "T3/SOVEREIGN material remains subject to the repository IP firewall and Drive-only rules.",
        "Historical aliases or merged identities MUST NOT be treated as additional active seats.",
    )
    for text in required:
        assert text in matrix


def test_matrix_preserves_persona_lineage_without_granting_current_authority():
    matrix = _read(MATRIX)
    persona_rows = _persona_lineage_rows(matrix)
    assert "governance/role_capability_registry.v1.json" in matrix
    assert "governance/persona_role_lineage.v1.json" in matrix
    assert "Persona labels do not independently grant authority." in matrix
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
        "Sentinel-Φ",
    ):
        assert agent in persona_rows
    assert "Sentience" not in persona_rows
    assert "Sentinel-Φ / Sentinel" not in persona_rows


def test_reconciliation_targets_are_explicit():
    matrix = _read(MATRIX)
    for text in (
        "legacy `AGENT_ROSTER.md` text versus newer Notion taxonomy/registry state",
        "historical versus current formation IDs",
        "expanded registry agent count versus visible enumerations",
        "Layer-0 ownership language across legacy gates, roster, topology, and current profiles",
        "Drive/GitHub representation drift",
        "exact source SHA/provenance for current claims",
    ):
        assert text in matrix
