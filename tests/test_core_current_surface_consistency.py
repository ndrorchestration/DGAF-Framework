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
