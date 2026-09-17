from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_TEMPLATE = ROOT / "docs" / "gates" / "GATE_UNIT_TEMPLATE.md"
AGENT_ROSTER = ROOT / "docs" / "agents" / "AGENT_ROSTER.md"


def test_gate_unit_template_uses_functional_roles_not_persona_certification():
    text = GATE_TEMPLATE.read_text(encoding="utf-8")

    for forbidden in (
        "Status:       DRAFT | REVIEW | CERTIFIED",
        "Certified-by:",
        "[Sentinel | Amethyst | Njineer]",
        '"agent": "[owner agent]"',
        "[what agent takes what action]",
        "| **Certifier** | Agent Apogee |",
        "**Maintained by:** Agent Amethyst",
    ):
        assert forbidden not in text

    for required in (
        "Status:       DRAFT | REVIEW | ADOPTED",
        "role.governance-orchestrator",
        "role.evidence-verification-reviewer",
        "role.security-containment-gate",
        '"owner_role": "[role.*]"',
        "does not establish certification, compliance, or standards conformance",
    ):
        assert required in text


def test_agent_roster_is_lineage_projection_not_authority_ssot():
    text = AGENT_ROSTER.read_text(encoding="utf-8")

    for forbidden in (
        "single source of truth for agent names, roles, and duty assignments",
        "Sovereign SSoT",
        "Hard veto (all commits)",
        "certification sign-off",
        "Sentinel sovereign veto overrides Amethyst",
        "No agent may impersonate Amethyst",
    ):
        assert forbidden not in text

    for required in (
        "identity and historical lineage projection",
        "does not grant authority",
        "governance/role_capability_registry.v1.json",
        "governance/persona_role_lineage.v1.json",
        "role.governance-orchestrator",
        "role.evidence-verification-reviewer",
        "role.convergence-state-observer",
        "role.security-containment-gate",
        "bare `Sentinel` is historical-only",
        "STATE / ADVISORY",
    ):
        assert required in text
