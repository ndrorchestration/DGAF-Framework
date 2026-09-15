"""Regression guard for the DGAF live-runtime production endpoint binding."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_PRODUCTION_URL = "https://dgaf-framework.vercel.app"
CANONICAL_PRODUCTION_URL = "https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app"


@pytest.mark.parametrize(
    "relative_path",
    [
        ".github/workflows/regression.yml",
        "scripts/live_regression_v17.py",
    ],
)
def test_live_regression_defaults_bind_to_canonical_production_url(relative_path: str) -> None:
    text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    assert LEGACY_PRODUCTION_URL not in text
    assert CANONICAL_PRODUCTION_URL in text


def test_scheduled_live_regression_cannot_be_redirected_by_repository_variable() -> None:
    workflow = (REPO_ROOT / ".github/workflows/regression.yml").read_text(encoding="utf-8")

    assert "vars.DGAF_URL" not in workflow
    assert "inputs.dgaf_url" in workflow
