from __future__ import annotations

import pytest

from api import ahg_herald


@pytest.fixture(autouse=True)
def clear_auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("VERCEL_ENV", "AHG_HERALD_API_KEY", "AHG_HERALD_ALLOW_INSECURE_LOCAL"):
        monkeypatch.delenv(name, raising=False)


@pytest.mark.parametrize("vercel_env", ["production", "preview", "unexpected"])
def test_missing_key_denies_deployed_or_unknown_environments(
    monkeypatch: pytest.MonkeyPatch, vercel_env: str
) -> None:
    monkeypatch.setenv("VERCEL_ENV", vercel_env)
    assert ahg_herald._check_auth({}) is False


def test_missing_key_denies_unset_environment_by_default() -> None:
    assert ahg_herald._check_auth({}) is False


@pytest.mark.parametrize("vercel_env", ["", "development"])
def test_explicit_local_opt_in_allows_only_local_or_development(
    monkeypatch: pytest.MonkeyPatch, vercel_env: str
) -> None:
    monkeypatch.setenv("AHG_HERALD_ALLOW_INSECURE_LOCAL", "true")
    if vercel_env:
        monkeypatch.setenv("VERCEL_ENV", vercel_env)
    assert ahg_herald._check_auth({}) is True


@pytest.mark.parametrize("vercel_env", ["preview", "production", "unexpected"])
def test_explicit_local_opt_in_cannot_open_deployed_or_unknown_environment(
    monkeypatch: pytest.MonkeyPatch, vercel_env: str
) -> None:
    monkeypatch.setenv("AHG_HERALD_ALLOW_INSECURE_LOCAL", "true")
    monkeypatch.setenv("VERCEL_ENV", vercel_env)
    assert ahg_herald._check_auth({}) is False


def test_key_requires_correct_bearer_in_preview(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VERCEL_ENV", "preview")
    monkeypatch.setenv("AHG_HERALD_API_KEY", "secret")
    assert ahg_herald._check_auth({}) is False
    assert ahg_herald._check_auth({"authorization": "Bearer wrong"}) is False
    assert ahg_herald._check_auth({"Authorization": "Bearer secret"}) is True


def test_key_requires_correct_bearer_in_production(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VERCEL_ENV", "production")
    monkeypatch.setenv("AHG_HERALD_API_KEY", "secret")
    assert ahg_herald._check_auth({}) is False
    assert ahg_herald._check_auth({"authorization": "Bearer wrong"}) is False
    assert ahg_herald._check_auth({"authorization": "Bearer secret"}) is True

[executed on device: neontic (fd6ceb3c-855d-43bd-a34e-d95659a36a0f)]