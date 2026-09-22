from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_SNAPSHOTS = (
    "docs/governance/CURRENT_STATE_2026-09-01.md",
    "docs/governance/CURRENT_CANDIDATE_POST_KICKOFF_CONTROL_2026-09-01.md",
    "docs/governance/CURRENT_CANDIDATE_EVIDENCE_READINESS_2026-09-01.md",
)


def test_historical_snapshot_notices_route_live_state_to_canonical_authority():
    for relative_path in HISTORICAL_SNAPSHOTS:
        first_line = (ROOT / relative_path).read_text(encoding="utf-8").splitlines()[0]

        assert "`docs/CURRENT_STATE.md`" in first_line
        assert "`docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`" not in first_line


def test_multimedia_report_does_not_route_current_gate_truth_to_legacy_state():
    readme = (ROOT / "docs/reports/pdmal-multimedia-report-2026-09-05/README.md").read_text(encoding="utf-8")
    gate_section = readme.split("For current gate truth,", 1)[1].split("## Epistemic boundary", 1)[0]

    assert "`docs/CURRENT_STATE.md`" in gate_section
    assert "`docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`" not in gate_section
    assert "`docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`" in gate_section


def test_historical_authority_sources_are_registered_in_lifecycle():
    lifecycle = (ROOT / "docs/DOCUMENT_LIFECYCLE.md").read_text(encoding="utf-8")

    for relative_path in HISTORICAL_SNAPSHOTS:
        assert f"| `{relative_path}` | HISTORICAL |" in lifecycle

    report_path = "docs/reports/pdmal-multimedia-report-2026-09-05/README.md"
    assert f"| `{report_path}` | HISTORICAL / DERIVATIVE |" in lifecycle
