"""Shared pytest fixtures for the PPTL test suite.

Fixture hierarchy:
  herald            — fresh HeraldAgent per test (no sinks)
  herald_with_sink  — HeraldAgent + CaptureSink for assertion
  tmp_jsonl         — temp-file path for JSONLSink tests
"""

from __future__ import annotations

import pytest

from pptl.herald_agent import HeraldAgent


class CaptureSink:
    """In-memory sink that collects emitted events for assertion."""

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
    """Sink that always raises to test Herald isolation."""

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
def tmp_jsonl(tmp_path):
    return str(tmp_path / "herald_test.jsonl")
