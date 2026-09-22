import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_SURFACES = {
    "README.md": ROOT / "README.md",
    "CURRENT_STATE": ROOT / "docs" / "CURRENT_STATE.md",
    "PROJECT_STATUS": ROOT / "docs" / "PROJECT_STATUS.md",
    "UI_CURRENT_STATE": ROOT / "docs" / "ui" / "UI_CURRENT_STATE.md",
}


def _read(name: str) -> str:
    return CURRENT_SURFACES[name].read_text(encoding="utf-8")


def test_current_surfaces_preserve_external_review_boundary():
    current = _read("CURRENT_STATE")
    project = _read("PROJECT_STATUS")
    ui = _read("UI_CURRENT_STATE")
    readme = _read("README.md")

    for text in (current, project, ui, readme):
        assert "canonical DGAF efficacy" in text
        assert "NOT ESTABLISHED" in text

    assert "Issue #929" in current
    assert "Issue #929" in ui
    assert "external review: NOT EXECUTED" in ui
    assert "execution allowed: FALSE" in ui
    assert "collection execution readiness: NOT ESTABLISHED" in ui


def test_epoch_002_remains_closed_and_non_promoting():
    current = _read("CURRENT_STATE")
    ui = _read("UI_CURRENT_STATE")

    assert "CLOSED_FOR_EXACT_PREREGISTERED_SCOPE" in current
    assert "closed for its exact preregistered scope" in ui
    assert "scientific-N increment: 0" in ui


def test_ui_current_state_is_not_the_stale_september_19_snapshot():
    ui = _read("UI_CURRENT_STATE")

    assert "CURRENT DOCUMENTATION / RECONCILED 2026-09-22" in ui
    assert "133dbab5622882f02d5ec5cacad9841c3a97a2df" not in ui
    assert "independent-validation handoff: ACCEPTED" in ui
    assert "reviewer independence: NOT VERIFIED LOCALLY" in ui


def test_ui_current_state_is_registered_as_derivative_lifecycle_surface():
    lifecycle = (ROOT / "docs" / "DOCUMENT_LIFECYCLE.md").read_text(encoding="utf-8")

    assert "| `docs/ui/UI_CURRENT_STATE.md` | DERIVATIVE | Presentation/documentation |" in lifecycle
    assert "must defer to CURRENT_STATE" in lifecycle


def test_stale_pdmal_current_control_snapshot_is_not_live_authority():
    pdmal = (ROOT / "docs" / "experiment" / "PDMAL_CURRENT_CONTROL_STATE.md").read_text(encoding="utf-8")
    lifecycle = (ROOT / "docs" / "DOCUMENT_LIFECYCLE.md").read_text(encoding="utf-8")

    assert "status: HISTORICAL / SUPERSEDED" in pdmal
    assert "current_authority: docs/CURRENT_STATE.md" in pdmal
    assert "no longer a live current-state authority" in pdmal
    assert "| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | HISTORICAL / SUPERSEDED |" in lifecycle


def test_legacy_pdmal_protocol_authority_is_scoped_without_rewriting_protocol():
    lifecycle = (ROOT / "docs" / "DOCUMENT_LIFECYCLE.md").read_text(encoding="utf-8")
    protocol = ROOT / "docs" / "experiment" / "PDMAL_EXPERIMENT_PROTOCOL.md"

    assert "| `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | ACTIVE / SPECIFICATION / PRE-FREEZE |" in lifecycle
    assert "not live project-state authority" in lifecycle
    assert protocol.exists()


def test_legacy_pdmal_evidence_index_is_exact_scope_not_live_gate_truth():
    evidence = (ROOT / "docs" / "evidence" / "PDMAL_EVIDENCE_INDEX.md").read_text(encoding="utf-8")
    lifecycle = (ROOT / "docs" / "DOCUMENT_LIFECYCLE.md").read_text(encoding="utf-8")

    assert "status: ACTIVE / EXACT-SCOPE HISTORICAL INDEX" in evidence
    assert "current_state_authority: docs/CURRENT_STATE.md" in evidence
    assert "supersede this file as a source of present-tense project gate truth" in evidence
    assert "| `docs/evidence/PDMAL_EVIDENCE_INDEX.md` | ACTIVE / EXACT-SCOPE HISTORICAL INDEX |" in lifecycle


def test_machine_readable_current_authority_fixture_does_not_route_to_stale_pdmal_state():
    fixture = (ROOT / "docs" / "governance" / "fixtures" / "current-authority-current-state.yaml").read_text(
        encoding="utf-8"
    )

    assert "next_gate: external reviewer engagement and independently retained evidence under issue #929" in fixture
    assert "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md" not in fixture
    assert "docs/CURRENT_STATE.md" in fixture


def test_claim_evidence_index_routes_live_truth_to_current_state():
    claims = (ROOT / "docs" / "CLAIM_EVIDENCE_INDEX.md").read_text(encoding="utf-8")

    assert "**Current reconciliation:** 2026-09-22" in claims
    assert "**Live project-state authority is `docs/CURRENT_STATE.md`**" in claims
    assert "Issue #929 owns the next external evidence-changing transition" in claims
    assert "| Claim | Recorded / exact-scope status |" in claims
    assert "CLOSED_FOR_EXACT_PREREGISTERED_SCOPE" in claims
    assert "HANDOFF ACCEPTED / EXTERNAL REVIEW NOT EXECUTED" in claims


def test_canonical_technical_overview_does_not_present_legacy_pdmal_as_live_state():
    overview = (ROOT / "docs" / "CANONICAL_TECHNICAL_OVERVIEW.md").read_text(encoding="utf-8")

    assert "**Date:** 2026-09-22" in overview
    assert "not the live project-state authority" in overview
    assert "Track A Epoch 002 successor lifecycle" in overview
    assert "current evidence-changing frontier is AOSS Stage-A external review" in overview


def test_completion_reconciler_separates_current_authority_from_historical_context():
    graph = json.loads((ROOT / "registry" / "dgaf_completion_state_reconciler.v0.1.json").read_text(encoding="utf-8"))

    assert graph["lifecycle_scope"] == "HISTORICAL_FIXED_SCOPE_TRACK_A_EPOCH_002_PRECOLLECTION"
    assert graph["current_state_authority"] == "docs/CURRENT_STATE.md"
    assert "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md" not in graph["authority"]["canonical_authority_sources"]
    assert "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md" in graph["historical_source_context"]


def test_publication_spine_routes_present_claims_to_current_state():
    spine = (ROOT / "docs" / "PUBLICATION_AND_PROVENANCE_SPINE.md").read_text(encoding="utf-8")

    assert "**Updated:** 2026-09-22" in spine
    assert "route present-tense project claims through `docs/CURRENT_STATE.md`" in spine
    assert "Track A Epoch 002 is closed for its exact preregistered scope" in spine
    assert "external review is NOT EXECUTED" in spine
    assert "historical September 6 control snapshot" in spine
