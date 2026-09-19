from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_active_maintenance_surfaces_use_functional_roles() -> None:
    deferred = read("DEFERRED_ITEMS.md")
    contributing = read("CONTRIBUTING.md")
    components = read("components/README.md")
    drive = read("docs/sync/DRIVE_SYNC_POLICY.md")
    outreach = read("docs/outreach/OUTREACH_LOG.md")

    assert "**Maintained by:** Agent Amethyst × COLLEEN" not in deferred
    assert "and Amethyst will rehydrate" not in deferred
    assert "role.governance-orchestrator" in deferred
    assert "role.continuity-archive-coordinator" in deferred

    assert "DGAF / Agent Amethyst" not in contributing
    assert "governance/role_capability_registry.v1.json" in contributing
    assert "governance/persona_role_lineage.v1.json" in contributing

    assert "**Maintainer:** Agent Amethyst + COLLEEN" not in components
    assert "role.governance-orchestrator" in components
    assert "role.continuity-archive-coordinator" in components

    assert "Maintained by: **Agent COLLEEN**" not in drive
    assert "Policy authority: Agent COLLEEN" not in drive
    assert "role.continuity-archive-coordinator" in drive
    assert "role.governance-orchestrator" in drive

    assert "Maintained by Agent COLLEEN" not in outreach
    assert "role.continuity-archive-coordinator" in outreach
    assert "role.governance-orchestrator" in outreach


def test_current_gate_headers_use_functional_role_contracts() -> None:
    gate11q = read("docs/gates/GATE_11Q.md")
    gate1111 = read("docs/gates/GATE_1111.md")
    telescopic = read("docs/gates/TELESCOPIC_LENS.md")
    acoustic = read("docs/gates/ACOUSTIC_GATES.md")
    p35 = read("docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md")

    assert "**Owner:** Agent Apogee" not in gate11q
    assert "| **Agent** | Apogee" not in gate11q
    assert "role.evidence-verification-reviewer" in gate11q
    assert "role.security-containment-gate" in gate11q

    assert "**Owner:** Agent Apogee" not in gate1111
    assert "| **Agent** | Apogee" not in gate1111
    assert "role.evidence-verification-reviewer" in gate1111
    assert "role.governance-orchestrator" in gate1111

    assert "**Owner:** Agent Apogee" not in telescopic
    assert "role.evidence-verification-reviewer" in telescopic
    assert "role.governance-orchestrator" in telescopic

    assert "**Owner:** Agent Amethyst" not in acoustic
    assert "role.governance-orchestrator" in acoustic
    assert "role.efficiency-resource-advisor" in acoustic

    assert "**Maintained by:** Agent Amethyst" not in p35
    assert "role.governance-orchestrator" in p35
    assert "governance/role_capability_registry.v1.json" in p35
    assert "governance/persona_role_lineage.v1.json" in p35


def test_historical_persona_provenance_is_preserved() -> None:
    for path in (
        "docs/gates/GATE_11Q.md",
        "docs/gates/GATE_1111.md",
        "docs/gates/TELESCOPIC_LENS.md",
        "docs/gates/ACOUSTIC_GATES.md",
        "docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md",
    ):
        text = read(path)
        assert "Historical" in text or "HISTORICAL" in text
        assert "Author" in text or "certifier" in text.lower()
