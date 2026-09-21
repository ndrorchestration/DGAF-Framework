import inspect
from pathlib import Path

import pytest


def test_missing_acp_checkout_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, inspect_preflight

    with pytest.raises(PreflightError, match="ACP_REPOSITORY_MISSING"):
        inspect_preflight(Path.cwd(), tmp_path / "absent")


def test_preflight_has_no_outcome_destination():
    from scripts.aoss_stage_a.preflight import inspect_preflight

    assert list(inspect.signature(inspect_preflight).parameters) == ["dgaf", "acp"]
