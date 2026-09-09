from __future__ import annotations

import threading
import urllib.request

import pytest

from components.ahg_herald_trace import HeraldHTTPSink, HeraldSinkConfig, validate_http_endpoint


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://herald.example/api/v1/trace",
        "http://localhost:8080/trace",
    ],
)
def test_validate_http_endpoint_accepts_absolute_http_urls(endpoint: str) -> None:
    assert validate_http_endpoint(endpoint) == endpoint


@pytest.mark.parametrize(
    "endpoint",
    [
        "file:///etc/passwd",
        "ftp://example.com/trace",
        "data:text/plain,trace",
        "herald.example/trace",
        "https:///missing-host",
    ],
)
def test_validate_http_endpoint_rejects_non_http_or_non_absolute_urls(endpoint: str) -> None:
    with pytest.raises(ValueError, match="absolute http:// or https:// URL"):
        validate_http_endpoint(endpoint)


def test_invalid_scheme_fails_closed_before_urlopen(monkeypatch: pytest.MonkeyPatch) -> None:
    sink = object.__new__(HeraldHTTPSink)
    sink.config = HeraldSinkConfig(endpoint="file:///tmp/trace", max_retries=1)
    sink._circuit_open = False
    sink._circuit_opened_at = None
    sink._consecutive_failures = 0
    sink._total_pushed = 0
    sink._total_failed = 0
    sink._lock = threading.Lock()

    called = False

    def forbidden_urlopen(*args: object, **kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be reached for a non-HTTP endpoint")

    monkeypatch.setattr(urllib.request, "urlopen", forbidden_urlopen)

    assert sink._push_batch([{"session_id": "test", "turn_id": 1}]) is False
    assert called is False
