"""
test_session_graduation_check.py — P-10 self-test suite.

Tests run_graduation_check() and write_graduation_report() directly.
Markers: governance
"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "session_graduation_check.py"


# ── Helpers ─────────────────────────────────────────────────────────────

def make_anchor(tmp_path: Path, session: str = "S042", has_blg_closed: bool = True) -> Path:
    blg_line = "| S041-BLG-01 | ✅ CLOSED S041 |" if has_blg_closed else "| S041-BLG-01 | OPEN |"
    content = f"""# SESSION ANCHOR — {session}
**Seal status:** ✅ GRADUATED

## BLG Status — ALL CLEAR

| ID | Status |
|---|---|
{blg_line}
"""
    p = tmp_path / "SESSION_ANCHOR.md"
    p.write_text(content, encoding="utf-8")
    return p


def make_cross_ref(tmp_path: Path, include_all: bool = True) -> Path:
    paths = "pptl/\ndocs/NDR_PATTERN_REGISTRY.md\n.github/workflows/\nCO_ORCH_QUEUE.md\nENSEMBLE_ROSTER.md\nSESSION_ANCHOR.md\nSWEEP_LOG.md\n"
    content = paths if include_all else "pptl/\n"
    p = tmp_path / "CROSS_REF.md"
    p.write_text(content, encoding="utf-8")
    return p


def make_queue(tmp_path: Path, has_pending: bool = False) -> Path:
    content = "## Queue\n\n| OPP | Status |\n|---|---|\n"
    if has_pending:
        content += "| OPP-001 | PENDING |\n"
    else:
        content += "| OPP-001 | DONE |\n"
    p = tmp_path / "CO_ORCH_QUEUE.md"
    p.write_text(content, encoding="utf-8")
    return p


# ── Import and run checks directly ──────────────────────────────────────

sys.path.insert(0, str(SCRIPT.parent.parent))
from scripts.session_graduation_check import run_graduation_check, write_graduation_report


@pytest.mark.governance
def test_all_checks_pass(tmp_path):
    anchor = make_anchor(tmp_path, session="S042")
    cross_ref = make_cross_ref(tmp_path)
    queue = make_queue(tmp_path, has_pending=False)
    result = run_graduation_check("S042", anchor_path=anchor, queue_path=queue, cross_ref_path=cross_ref)
    assert result["all_pass"] is True
    assert result["verdict"] == "GRADUATED"


@pytest.mark.governance
def test_anchor_mismatch_fails(tmp_path):
    anchor = make_anchor(tmp_path, session="S041")  # wrong session
    cross_ref = make_cross_ref(tmp_path)
    queue = make_queue(tmp_path)
    result = run_graduation_check("S042", anchor_path=anchor, queue_path=queue, cross_ref_path=cross_ref)
    assert result["checks"]["SESSION_ANCHOR sealed"]["pass"] is False
    assert result["all_pass"] is False


@pytest.mark.governance
def test_cross_ref_incomplete_fails(tmp_path):
    anchor = make_anchor(tmp_path, session="S042")
    cross_ref = make_cross_ref(tmp_path, include_all=False)  # missing paths
    queue = make_queue(tmp_path)
    result = run_graduation_check("S042", anchor_path=anchor, queue_path=queue, cross_ref_path=cross_ref)
    assert result["checks"]["CROSS_REF complete"]["pass"] is False


@pytest.mark.governance
def test_pending_queue_fails(tmp_path):
    anchor = make_anchor(tmp_path, session="S042")
    cross_ref = make_cross_ref(tmp_path)
    queue = make_queue(tmp_path, has_pending=True)
    result = run_graduation_check("S042", anchor_path=anchor, queue_path=queue, cross_ref_path=cross_ref)
    assert result["checks"]["CO_ORCH_QUEUE clear"]["pass"] is False


@pytest.mark.governance
def test_write_report_graduated(tmp_path):
    result = {
        "session": "S042",
        "verdict": "GRADUATED",
        "all_pass": True,
        "checks": {
            "SESSION_ANCHOR sealed": {"pass": True, "detail": "ok"},
            "CROSS_REF complete":    {"pass": True, "detail": "ok"},
            "CO_ORCH_QUEUE clear":   {"pass": True, "detail": "ok"},
            "Zero open BLGs":        {"pass": True, "detail": "ok"},
        }
    }
    report_path = tmp_path / "GRADUATION_REPORT.md"
    write_graduation_report(result, report_path=report_path)
    content = report_path.read_text()
    assert "GRADUATED" in content
    assert "PASS" in content
    assert "Action Items" not in content


@pytest.mark.governance
def test_write_report_not_ready_includes_action_items(tmp_path):
    result = {
        "session": "S042",
        "verdict": "NOT READY",
        "all_pass": False,
        "checks": {
            "SESSION_ANCHOR sealed": {"pass": False, "detail": "missing"},
            "CROSS_REF complete":    {"pass": True,  "detail": "ok"},
            "CO_ORCH_QUEUE clear":   {"pass": True,  "detail": "ok"},
            "Zero open BLGs":        {"pass": True,  "detail": "ok"},
        }
    }
    report_path = tmp_path / "GRADUATION_REPORT.md"
    write_graduation_report(result, report_path=report_path)
    content = report_path.read_text()
    assert "NOT READY" in content
    assert "Action Items" in content
