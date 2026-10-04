"""Current N8nHeraldSink contract tests.

The production sink implements the HeraldAgent emit(event) protocol,
buffers writes, flushes on threshold/close, retries urllib transport, and
dead-letters permanent failures. Historical send/buffer_event/requests/
ring-buffer APIs are intentionally not part of this contract.
"""

from unittest.mock import MagicMock, patch

import pytest

from pptl.n8n_herald_sink import N8nHeraldSink


WEBHOOK = "https://n8n.example.com/webhook/test"


@pytest.fixture
def sink_dry():
    return N8nHeraldSink(webhook_url=WEBHOOK, dry_run=True, batch_size=1)


@pytest.fixture
def sink_live():
    return N8nHeraldSink(webhook_url=WEBHOOK, dry_run=False, batch_size=3)


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_emit_is_herald_sink_protocol_and_dry_run_never_calls_http(sink_dry):
    with patch("urllib.request.urlopen") as urlopen:
        sink_dry.emit({"event_type": "test", "data": {}})
    urlopen.assert_not_called()
    assert sink_dry._batch == []


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_write_remains_compatible_sink_entry_point(sink_dry):
    with patch.object(sink_dry, "_send_with_retry") as send:
        sink_dry.write({"event_type": "test", "data": {}})
    send.assert_called_once()


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_batch_threshold_flushes_and_drains_buffer(sink_live):
    with patch.object(sink_live, "_send_with_retry") as send:
        for index in range(3):
            sink_live.emit({"event_type": f"e{index}", "data": {}})
    send.assert_called_once()
    batch = send.call_args.args[0]
    assert [event["event_type"] for event in batch] == ["e0", "e1", "e2"]
    assert sink_live._batch == []


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_close_flushes_remaining_batch(sink_live):
    with patch.object(sink_live, "_send_with_retry") as send:
        sink_live.emit({"event_type": "e0", "data": {}})
        assert len(sink_live._batch) == 1
        sink_live.close()
    send.assert_called_once()
    assert sink_live._batch == []


def _successful_response(status=200):
    response = MagicMock()
    response.status = status
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_retry_succeeds_after_first_transport_failure(sink_live):
    with (
        patch(
            "urllib.request.urlopen",
            side_effect=[OSError("temporary"), _successful_response()],
        ) as urlopen,
        patch("pptl.n8n_herald_sink.time.sleep") as sleep,
    ):
        sink_live._send_with_retry([{"event_type": "test"}])

    assert urlopen.call_count == 2
    sleep.assert_called_once_with(sink_live.RETRY_BASE_S)


@pytest.mark.n8n_sink
@pytest.mark.governance
def test_retry_exhaustion_dead_letters_without_raising(sink_live):
    batch = [{"event_type": "test"}]
    with (
        patch("urllib.request.urlopen", side_effect=OSError("network")) as urlopen,
        patch("pptl.n8n_herald_sink.time.sleep"),
        patch.object(sink_live, "_write_dead_letter") as dead_letter,
    ):
        sink_live._send_with_retry(batch)

    assert urlopen.call_count == sink_live.MAX_RETRIES
    dead_letter.assert_called_once_with(batch)


@pytest.mark.n8n_sink
def test_hmac_signature_is_added_without_exposing_secret():
    sink = N8nHeraldSink(
        webhook_url=WEBHOOK,
        hmac_secret="test-secret",
        dry_run=False,
        batch_size=1,
    )
    response = _successful_response()
    with patch("urllib.request.urlopen", return_value=response) as urlopen:
        sink.emit({"event_type": "signed"})

    request = urlopen.call_args.args[0]
    assert request.headers["X-herald-signature"].startswith("sha256=")
    assert "test-secret" not in request.headers["X-herald-signature"]
