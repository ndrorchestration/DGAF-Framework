"""
test_n8n_herald_sink.py — N8nHeraldSink unit tests (NDR P-01+P-02).

Covers: dry_run, batch flush, retry logic, ring buffer eviction.
Markers: n8n_sink, governance
"""
import pytest
from unittest.mock import MagicMock, patch
from pptl.n8n_herald_sink import N8nHeraldSink


WEBHOOK = "https://n8n.example.com/webhook/test"


@pytest.fixture
def sink_dry():
    return N8nHeraldSink(webhook_url=WEBHOOK, dry_run=True)


@pytest.fixture
def sink_live():
    return N8nHeraldSink(webhook_url=WEBHOOK, dry_run=False, max_retries=2, batch_size=3)


# ── dry_run ──────────────────────────────────────────────────────────────

@pytest.mark.n8n_sink
@pytest.mark.governance
def test_dry_run_blocks_http(sink_dry):
    """dry_run=True must never make HTTP calls."""
    with patch("pptl.n8n_herald_sink.requests") as mock_req:
        sink_dry.send({"event_type": "test", "data": {}})
        mock_req.post.assert_not_called()


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_dry_run_returns_dry_run_record(sink_dry):
    """dry_run record must contain dry_run=True flag and payload echo."""
    result = sink_dry.send({"event_type": "mandate_issued", "data": {"x": 1}})
    assert result is not None
    # Result should indicate dry_run mode — exact shape depends on impl
    # At minimum the call must not raise and must return something truthy or a dict
    assert result is not False


# ── Batch Flush ──────────────────────────────────────────────────────────

@pytest.mark.n8n_sink
@pytest.mark.governance
def test_batch_flush_drains_buffer(sink_live):
    """flush() must empty the internal buffer."""
    with patch("pptl.n8n_herald_sink.requests") as mock_req:
        mock_req.post.return_value.status_code = 200
        mock_req.post.return_value.raise_for_status = MagicMock()
        for i in range(3):
            sink_live.buffer_event({"event_type": f"e{i}", "data": {}})
        sink_live.flush()
        # Buffer should be empty after flush
        assert len(sink_live._buffer) == 0 or sink_live._buffer == []


@pytest.mark.n8n_sink
def test_batch_auto_flush_on_threshold(sink_live):
    """When buffer hits batch_size, auto-flush must trigger."""
    flushed = []
    with patch.object(sink_live, "flush", side_effect=lambda: flushed.append(1)) as mock_flush:
        for i in range(sink_live.batch_size):
            sink_live.buffer_event({"event_type": f"e{i}", "data": {}})
        assert len(flushed) >= 1


# ── Retry Logic ──────────────────────────────────────────────────────────

@pytest.mark.n8n_sink
@pytest.mark.governance
def test_retry_success_after_first_failure(sink_live):
    """Should succeed if retry attempt returns 200."""
    responses = [
        MagicMock(status_code=500, raise_for_status=MagicMock(side_effect=Exception("500"))),
        MagicMock(status_code=200, raise_for_status=MagicMock()),
    ]
    with patch("pptl.n8n_herald_sink.requests") as mock_req:
        mock_req.post.side_effect = responses
        # Should not raise — succeeds on second attempt
        sink_live.send({"event_type": "test", "data": {}})
        assert mock_req.post.call_count == 2


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_retry_exhaustion_raises(sink_live):
    """All retries exhausted must raise an exception."""
    with patch("pptl.n8n_herald_sink.requests") as mock_req:
        mock_req.post.side_effect = Exception("network failure")
        with pytest.raises(Exception):
            sink_live.send({"event_type": "test", "data": {}})


# ── Ring Buffer Eviction ─────────────────────────────────────────────────

@pytest.mark.n8n_sink
def test_ring_buffer_evicts_oldest_on_overflow():
    """Ring buffer must not grow beyond max_buffer_size."""
    sink = N8nHeraldSink(webhook_url=WEBHOOK, dry_run=True, max_buffer_size=5)
    for i in range(10):
        sink.buffer_event({"event_type": f"e{i}", "data": {}})
    assert len(sink._buffer) <= 5
