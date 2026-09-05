from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


CONSTITUTION = ROOT / "docs" / "agents" / "LAYER_0_CONSTITUTION.md"
MATRIX = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_MATRIX.md"
INVARIANT = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_INVARIANT.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"required Layer-0 artifact missing: {path}"
    return path.read_text(encoding="utf-8")


def test_layer0_is_constitutional_substrate():
    text = _read(CONSTITUTION)
    invariant = _read(INVARIANT)
    assert "ACTIVE — CONSTITUTIONAL SUBSTRATE" in text
    assert "Layer 0 defines the constraints that precede technical optimization." in text
    assert "Layer 0 is the constitutional governance boundary" in invariant


def test_layer0_distinguishes_law_standards_frameworks_and_design_choices():
    text = _read(CONSTITUTION)
    for marker in (
        "applicable law or regulation",
        "recognized standards",
        "governance frameworks",
        "human-rights instruments",
        "social expectations",
        "engineering conventions",
        "DGAF design choices",
    ):
        assert marker in text
    assert "A framework resemblance is not evidence of legal compliance." in text


def test_layer0_preserves_role_separation():
    text = _read(CONSTITUTION)
    matrix = _read(MATRIX)
    for agent in (
        "Perigee",
        "Sentinel-Φ",
        "Reciprocity",
        "Professor Prodigy",
        "Amethyst",
        "DemiJoule",
        "Herald",
        "Apogee",
    ):
        assert agent in text
    assert "This composition is descriptive of existing or proposed domain responsibilities." in text
    assert "does not supersede canonical gate ownership" in text
    assert "Capability overlap does not create authority overlap." in matrix


def test_layer0_requires_public_legibility_and_disclosure_statuses():
    text = _read(CONSTITUTION)
    assert "Accessibility → Comprehensibility → Appropriateness of Disclosure." in text
    for status in (
        "IMPLEMENTED",
        "TESTED",
        "VERIFIED",
        "EXPERIMENTALLY DEMONSTRATED",
        "PROPOSED",
        "HYPOTHETICAL",
        "HISTORICAL",
        "NOT ESTABLISHED",
    ):
        assert status in text


def test_layer0_blocks_evidence_promotion_and_unauthorized_action():
    text = _read(CONSTITUTION)
    assert "MUST NOT be treated as human authorization" in text
    assert "block, escalate, abstain, or request human review" in text
    assert (
        "No synthetic test, model output, expert consensus, deployment status, or documentation quality result may be promoted into empirical efficacy"
        in text
    )
