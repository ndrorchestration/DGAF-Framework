from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVARIANT = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_INVARIANT.md"
ROSTER = ROOT / "docs" / "agents" / "AGENT_ROSTER.md"
TOPOLOGY = ROOT / "docs" / "agents" / "FORMATION_TOPOLOGY.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"required governance artifact missing: {path}"
    return path.read_text(encoding="utf-8")


def test_agent_authority_invariant_is_present_and_canonical():
    text = _read(INVARIANT)
    assert "DGAF-AUTH-001" in text
    assert "ACTIVE — ADOPTION BASELINE" in text
    assert "Shared governance ontology MUST NOT imply shared authority." in text
    assert "Capability overlap is not authority overlap." in text
    assert "Historical documentation MUST NOT be upgraded into current evidence" in text
    assert "BLOCK / ESCALATE / REQUEST HUMAN REVIEW" in text


def test_canonical_roster_and_topology_remain_distinct_authority_sources():
    roster = _read(ROSTER)
    topology = _read(TOPOLOGY)

    assert "single source of truth for agent names, roles, and duty assignments" in roster
    assert "Changes require Amethyst sign-off + Njineer confirmation." in roster
    assert "canonical specification for all named agent formations" in topology
    assert "Sealed formation seat change" in topology


def test_known_role_boundaries_are_explicit():
    roster = _read(ROSTER)

    required_boundaries = (
        "Amethyst does not score artifacts",
        "Prof Prodigy does not orchestrate",
        "No agent may impersonate Amethyst",
        "T3 agents (A-14→A-19) have no GitHub write authority",
    )
    for boundary in required_boundaries:
        assert boundary in roster
