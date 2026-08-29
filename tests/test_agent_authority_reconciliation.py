from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECON = ROOT / "docs" / "agents" / "AGENT_AUTHORITY_RECONCILIATION.md"


def test_reconciliation_record_is_controlled_and_non_authoritative():
    text = RECON.read_text(encoding="utf-8")
    assert "ACTIVE — RECONCILIATION RECORD" in text
    assert "does not supersede guarded canonical sources" in text
    assert "CONTROLLED / NO AUTHORITY TRANSFER" in text
    assert "prevent automated inference of new authority" in text


def test_reconciliation_identifies_current_high_risk_conflicts():
    text = RECON.read_text(encoding="utf-8")
    for marker in (
        "R-001 — Roster/topology generation mismatch",
        "R-002 — Layer-0 attribution is distributed",
        "R-003 — Sentinel / Sentinel-Phi identity continuity",
        "R-004 — ID / formation drift",
        "R-005 — Individual contracts contain legacy role language",
        "R-006 — Public/IP visibility is already a governed concern",
    ):
        assert marker in text
