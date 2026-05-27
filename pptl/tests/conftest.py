"""
Shared pytest fixtures for PPTL test suite.

Fixture hierarchy:
  herald            — fresh HeraldAgent per test (no sinks)
  herald_with_sink  — HeraldAgent + CaptureSink for assertion
  orch              — IntegratedOrchestrator wired to herald_with_sink
  tmp_jsonl         — temp-file path for JSONLSink tests
"""
from __future__ import annotations
import os, sys, tempfile, pytest

# Ensure repo root on path so `pptl` is importable without install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pptl.herald_agent  import HeraldAgent
from pptl.rag_verifier  import SentinelRAGVerifier
from pptl.orchestrator  import IntegratedOrchestrator


class CaptureSink:
    """In-memory sink — collects all emitted events for assertion."""
    def __init__(self):
        self.events: list[dict] = []
        self.closed = False

    def emit(self, event: dict) -> None:
        self.events.append(event)

    def close(self) -> None:
        self.closed = True

    def health(self) -> dict:
        return {"captured": len(self.events)}

    def of_type(self, et: str) -> list[dict]:
        return [e for e in self.events if e.get("event_type") == et]

    def __len__(self):
        return len(self.events)


class BrokenSink:
    """Sink that always raises — tests Herald isolation."""
    def emit(self, event: dict) -> None:
        raise RuntimeError("sink exploded")


@pytest.fixture
def herald():
    h = HeraldAgent(session_id="test-sess")
    yield h
    # no close() — keep test hermetic


@pytest.fixture
def capture():
    return CaptureSink()


@pytest.fixture
def herald_with_sink(capture):
    h = HeraldAgent(session_id="test-sess")
    h.register_sink(capture)
    yield h, capture


@pytest.fixture
def orch(herald_with_sink):
    h, cap = herald_with_sink
    o = IntegratedOrchestrator(
        herald     = h,
        rag_scorer = SentinelRAGVerifier(),
    )
    yield o, h, cap


@pytest.fixture
def tmp_jsonl(tmp_path):
    return str(tmp_path / "herald_test.jsonl")
