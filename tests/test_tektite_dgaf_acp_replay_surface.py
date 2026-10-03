from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "app" / "components" / "tektite-governed-replay-trace.tsx"
PAGE = ROOT / "app" / "(command-center)" / "demo" / "page.tsx"


def test_tektite_replay_surface_is_explicitly_non_live() -> None:
    text = COMPONENT.read_text(encoding="utf-8")
    assert "STATIC REPLAY · NO LIVE ACP EXECUTION" in text
    assert "does not call ACP" in text
    assert "Real-project mutation authorized" in text
    assert "Distributed/global lineage" in text
    assert "FRESH ADJUDICATION" in text
    assert "NEXT AUTHORITY" not in text


def test_tektite_replay_surface_fetches_only_local_static_fixture() -> None:
    text = COMPONENT.read_text(encoding="utf-8")
    assert "const TRACE_URL = '/evidence/tektite-dgaf-acp-replay-trace-v0.json'" in text
    assert "http://" not in text
    assert "https://" not in text
    assert "/api/" not in text


def test_demo_page_includes_replay_trace_without_replacing_live_demo() -> None:
    text = PAGE.read_text(encoding="utf-8")
    assert "<TektiteDemoView />" in text
    assert "<TektiteGovernedReplayTrace />" in text
