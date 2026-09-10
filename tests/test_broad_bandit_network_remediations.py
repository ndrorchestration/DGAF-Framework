from __future__ import annotations

import urllib.request

import pytest

from api import ahg_herald
from scripts import p2_runtime_matrix


@pytest.mark.parametrize(
    "url",
    [
        "https://example.test/path",
        "http://localhost:3000/path",
    ],
)
def test_herald_validated_http_url_accepts_http_and_https(url: str) -> None:
    assert ahg_herald._validated_http_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/secret",
        "ftp://example.test/archive",
        "data:text/plain,secret",
        "example.test/no-scheme",
        "/relative/path",
    ],
)
def test_herald_validated_http_url_rejects_non_network_schemes(url: str) -> None:
    with pytest.raises(ValueError, match="absolute HTTP"):
        ahg_herald._validated_http_url(url)


def test_herald_kv_rejected_scheme_never_reaches_urlopen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_urlopen(*args: object, **kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be reached")

    monkeypatch.setenv("AHG_KV_REST_API_URL", "file:///tmp/not-network")
    monkeypatch.setenv("AHG_KV_REST_API_TOKEN", "synthetic-token")
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert ahg_herald._kv_set("key", {"value": 1}) is False
    assert called is False


def test_herald_webhook_rejected_scheme_never_reaches_urlopen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_urlopen(*args: object, **kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be reached")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert ahg_herald._post_webhook("file:///tmp/not-network", {"text": "x"}) is False
    assert called is False


@pytest.mark.parametrize(
    "url",
    [
        "https://example.test/api/orchestrate",
        "http://127.0.0.1:3000/api/orchestrate",
    ],
)
def test_p2_validate_http_url_accepts_http_and_https(url: str) -> None:
    assert p2_runtime_matrix.validate_http_url(url) == url


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/secret",
        "ftp://example.test/archive",
        "data:text/plain,secret",
        "example.test/no-scheme",
        "/relative/path",
    ],
)
def test_p2_validate_http_url_rejects_non_network_schemes(url: str) -> None:
    with pytest.raises(ValueError, match="absolute HTTP"):
        p2_runtime_matrix.validate_http_url(url)


def test_p2_rejected_scheme_never_reaches_urlopen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = False

    def fake_urlopen(*args: object, **kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("urlopen must not be reached")

    monkeypatch.setattr(p2_runtime_matrix, "urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="absolute HTTP"):
        p2_runtime_matrix.request_raw("file:///tmp/not-network", b"{}")
    assert called is False
