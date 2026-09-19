import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "role_capability_registry.v1.json"
LINEAGE = ROOT / "governance" / "persona_role_lineage.v1.json"
BRAND_SPEC = ROOT / "docs" / "brand" / "IMP_05_BRAND_SPEC.md"
TEMPLATE_REGISTRY = ROOT / "docs" / "needle" / "TEMPLATE_REGISTRY.md"
NOTICE_FILE = ROOT / "NOTICE"
GOVERNANCE_README = ROOT / "README.governance.md"

REFERENCE_CLASSES = {"FD", "PP", "FX", "HP", "UN"}
AUTHORITY_STATUSES = {"equivalent", "none", "unresolved"}


def _load(path: Path) -> dict:
    assert path.is_file(), f"required architecture artifact missing: {path}"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_registry_has_versioned_unique_functional_ids():
    registry = _load(REGISTRY)
    assert registry["schema_version"] == 1
    assert registry["architecture"] == "persona-to-role"

    role_ids = [role["id"] for role in registry["roles"]]
    capability_ids = [capability["id"] for capability in registry["capabilities"]]

    assert role_ids
    assert capability_ids
    assert len(role_ids) == len(set(role_ids))
    assert len(capability_ids) == len(set(capability_ids))
    assert all(role_id.startswith("role.") for role_id in role_ids)
    assert all(capability_id.startswith("cap.") for capability_id in capability_ids)


def test_every_role_resolves_capabilities_and_authority_classes():
    registry = _load(REGISTRY)
    capability_ids = {capability["id"] for capability in registry["capabilities"]}
    allowed_authority = set(registry["authority_classes"])

    for role in registry["roles"]:
        assert role["capabilities"], f"role has no capabilities: {role['id']}"
        assert set(role["capabilities"]) <= capability_ids
        assert set(role["authority_classes"]) <= allowed_authority
        assert role["boundary"].strip()


def test_lineage_maps_identity_without_granting_new_authority():
    registry = _load(REGISTRY)
    lineage = _load(LINEAGE)
    role_ids = {role["id"] for role in registry["roles"]}

    assert lineage["schema_version"] == 1
    assert lineage["registry_schema_version"] == registry["schema_version"]

    legacy_ids = []
    for entry in lineage["entries"]:
        legacy_ids.append(entry["legacy_identity"])
        assert entry["reference_class"] in REFERENCE_CLASSES
        assert entry["authority_equivalence"]["status"] in AUTHORITY_STATUSES
        assert entry["authority_equivalence"]["authority_change"] is False

        role_id = entry.get("role_id")
        if entry["reference_class"] == "FD":
            assert role_id in role_ids
            assert entry["authority_equivalence"]["status"] == "equivalent"
        elif role_id is not None:
            assert role_id in role_ids

    assert len(legacy_ids) == len(set(legacy_ids))


def test_state_and_historical_aliases_cannot_become_authority_seats():
    registry = _load(REGISTRY)
    lineage = _load(LINEAGE)
    roles = {role["id"]: role for role in registry["roles"]}
    entries = {entry["legacy_identity"]: entry for entry in lineage["entries"]}

    ionia = entries["Ionia"]
    assert ionia["role_id"] == "role.convergence-state-observer"
    assert roles[ionia["role_id"]]["authority_classes"] == ["STATE", "ADVISORY"]
    assert "no independent governance authority" in roles[ionia["role_id"]]["boundary"].lower()

    sentinel = entries["Sentinel"]
    sentience = entries["Sentience"]
    assert sentinel["reference_class"] == "HP"
    assert sentience["reference_class"] == "HP"
    assert sentinel["role_id"] is None
    assert sentience["role_id"] is None
    assert sentinel["authority_equivalence"]["status"] == "none"
    assert sentience["authority_equivalence"]["status"] == "none"


def test_current_brand_generator_uses_functional_authority_not_persona_authority():
    text = BRAND_SPEC.read_text(encoding="utf-8")

    assert "Governed by Agent Amethyst-Conductor" not in text
    assert "Meta-Orchestrator: Agent Amethyst-Conductor" not in text
    assert "role.governance-orchestrator" in text
    assert "persona label grants authority" in text


def test_current_template_registry_bounds_internal_review_and_standards_crosswalk():
    text = TEMPLATE_REGISTRY.read_text(encoding="utf-8")

    assert "GOLD STAR CERTIFIED" not in text
    assert "⭐ GOLD STAR" not in text
    assert "endorsed runnable implementations" not in text
    assert "| NIST Function | Control | Satisfied By |" not in text
    assert "| Clause | Requirement | Satisfied By |" not in text
    assert "does not establish certification, endorsement, compliance, or standards conformance" in text


def test_current_notice_does_not_advertise_persona_authority_or_unbounded_claims():
    text = NOTICE_FILE.read_text(encoding="utf-8")

    assert "Agent Amethyst meta-orchestration and QA authority" not in text
    assert "Gold Star certification validation processes" not in text
    assert "Enterprise-grade governance and compliance standards" not in text
    assert "constitutes trademark infringement" not in text
    assert "does not alter the Apache 2.0 license terms" in text


def test_governance_readme_uses_current_track_and_functional_governance_contacts():
    text = GOVERNANCE_README.read_text(encoding="utf-8")

    assert "This is separate from **Track A Epoch 001**" not in text
    assert "Track A Epoch 002" in text
    assert "| **Meta-Orchestrator** | Agent Amethyst |" not in text
    assert "| **Evidence Governor** | Agent Apogee |" not in text
    assert "| **Safety / Veto Authority** | Agent Sentinel |" not in text
    assert "role.governance-orchestrator" in text
    assert "role.evidence-verification-reviewer" in text
    assert "role.security-containment-gate" in text


def test_gate_unit_template_uses_functional_roles_and_noncertifying_status_language():
    text = (ROOT / "docs" / "gates" / "GATE_UNIT_TEMPLATE.md").read_text(encoding="utf-8")

    assert "Status:       DRAFT | REVIEW | CERTIFIED" not in text
    assert "Certified-by: Agent Apogee" not in text
    assert "**Maintained by:** Agent Amethyst" not in text
    assert "Escalate to Sentinel" not in text
    assert "role.governance-orchestrator" in text
    assert "role.evidence-verification-reviewer" in text
    assert "role.security-containment-gate" in text
    assert "does not establish external certification" in text


def test_agent_roster_is_identity_lineage_not_current_authority_source():
    text = (ROOT / "docs" / "agents" / "AGENT_ROSTER.md").read_text(encoding="utf-8")

    assert "single source of truth for agent names, roles, and duty assignments" not in text
    assert "Sentinel sovereign veto overrides Amethyst" not in text
    assert "This file is a sovereign reference" not in text
    assert "governance/role_capability_registry.v1.json" in text
    assert "governance/persona_role_lineage.v1.json" in text
    assert "identity and historical duty lineage" in text.lower()


def test_notice_uses_canonical_axis_and_pptl_expansions():
    text = NOTICE_FILE.read_text(encoding="utf-8")

    assert "AXIS (Agentic eXecution Integrity System)" not in text
    assert "PPTL (Prof Prodigy Theorem Layer)" not in text
    assert "AXIS (Agent X-axis Invariant Spectrum)" in text
    assert "PPTL (Phi-Pentagon Topology Lab)" in text


def test_acronym_registry_contains_no_chat_file_citation_tokens():
    text = (ROOT / "docs" / "taxonomy" / "NDR_ACRONYM_REGISTRY.md").read_text(encoding="utf-8")

    assert "filecite" not in text
    assert "turn231file0" not in text
    assert "docs/qa/AXIS_METRIC_SPEC.md" in text


def test_security_policy_routes_current_authority_through_functional_contracts():
    text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

    assert "governed by the DGAF framework under Agent Amethyst" not in text
    assert "Agent Sentinel (integrity enforcement)" not in text
    assert "role.security-containment-gate" in text
    assert "role.governance-orchestrator" in text
    assert "sentinel-governance" not in text


def test_operations_docs_do_not_grant_current_authority_to_persona_labels():
    paths = (
        ROOT / ".operations" / "README.md",
        ROOT / ".operations" / "seal_checklist.md",
        ROOT / ".operations" / "sweep_session_init.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "**Authority:** Agent Amethyst" not in combined
    assert "Sentinel veto authority" not in combined
    assert "*Authority: Agent COLLEEN + Agent Sentinel" not in combined
    assert "role.governance-orchestrator" in combined
    assert "role.security-containment-gate" in combined
    assert "governance/persona_role_lineage.v1.json" in combined


def test_pattern_registry_uses_functional_review_and_execution_authority():
    text = (ROOT / "registry" / "PATTERN_REGISTRY_v2.md").read_text(encoding="utf-8")

    assert "**Enforced by:** Amethyst" not in text
    assert "signed off by Amethyst" not in text
    assert "hard gate enforced by Sentinel-Phi" not in text
    assert "role.governance-orchestrator" in text
    assert "role.evidence-verification-reviewer" in text
    assert "role.security-containment-gate" in text


def test_authority_matrix_defers_current_authority_to_role_registry():
    text = (ROOT / "docs" / "agents" / "AGENT_AUTHORITY_MATRIX.md").read_text(encoding="utf-8")

    assert "## 2. Current Authority Baseline" not in text
    assert "governance/role_capability_registry.v1.json" in text
    assert "governance/persona_role_lineage.v1.json" in text
    assert "functional role" in text.lower()
    assert "persona" in text.lower()
    assert "does not grant authority" in text.lower()


def test_workspace_bootstrap_current_overlay_uses_current_taxonomy_and_nonpersona_authority():
    text = (ROOT / "docs" / "WORKSPACE_BOOTSTRAP.md").read_text(encoding="utf-8")

    assert "| PPTL | Procluding Premise Triadic Loop (uppercase) | ✅ CANONICAL |" not in text
    assert "PPTL | **Phi-Pentagon Topology Lab**" in text
    assert "**Authority order:** User → Space instruction (Amethyst host)" not in text
    assert "historical s071 authority order" in text.lower()
    assert "current executable authority" in text.lower()
    assert "governance/role_capability_registry.v1.json" in text


def test_technical_reference_does_not_publish_stale_protected_main_marker():
    text = (ROOT / "README.technical.md").read_text(encoding="utf-8")

    assert "through protected-main `b1d91621...`" not in text
    assert "exact source identity" in text.lower()
    assert "git history" in text.lower()


def test_taxonomy_controls_phdge_orbit_language_and_math_notation():
    text = (ROOT / "docs" / "taxonomy" / "NDR_ACRONYM_REGISTRY.md").read_text(encoding="utf-8")

    assert "| **PHDGE** | Phi-Harmonic Dynamic Governance Ecosystem |" in text
    assert "HISTORICAL / NON-CANONICAL" in text
    assert "Orbit" in text
    assert "not a confirmed acronym" in text
    assert "Observable Multi-Agent Reasoning" in text
    assert "not an O-R-B-I-T expansion" in text
    for token in ("noetic", "neotic", "ontic", "epistemic", "neontic"):
        assert f"**{token}**" in text
    assert "1.774732842" in text
    assert "1.3247179572447454" in text
    assert "Never conflate it with Platinum Mean" in text


def test_pptl_persona_names_are_compatibility_nodes_not_authority_seats():
    topology = (ROOT / "pptl" / "topology.py").read_text(encoding="utf-8")
    readme = (ROOT / "pptl" / "README.md").read_text(encoding="utf-8")

    assert "frozen experimental/compatibility node identifiers" in topology
    assert "They do not grant current" in topology
    assert "governance/role_capability_registry.v1.json" in topology
    assert "Agent Amethyst meta-orchestrated" not in readme
    assert "stable experimental/compatibility node identifiers" in readme
    assert "bare `Sentinel` remains a historical/compatibility label" in readme
    assert "role_capability_registry.v1.json" in readme
    assert "persona_role_lineage.v1.json" in readme
