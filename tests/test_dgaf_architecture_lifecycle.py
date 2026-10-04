import json
from pathlib import Path

from scripts.validate_dgaf_architecture_lifecycle import (
    ACCEPTED,
    ACTIVE_NON_AUTHORIZING,
    read_lifecycle,
    validate_architecture_lifecycle,
)


def test_canonical_architecture_lifecycle_passes():
    assert validate_architecture_lifecycle() == []


def test_markdown_lifecycle_is_parsed(tmp_path: Path):
    path = tmp_path / "CONTROL.md"
    path.write_text(
        "# Control\n\n**Status:** ACTIVE_NON_AUTHORIZING / NON-AUTHORIZING\n",
        encoding="utf-8",
    )
    assert read_lifecycle(path) == ACTIVE_NON_AUTHORIZING


def test_json_lifecycle_is_parsed(tmp_path: Path):
    path = tmp_path / "registry.json"
    path.write_text(
        json.dumps({"status": ACTIVE_NON_AUTHORIZING}),
        encoding="utf-8",
    )
    assert read_lifecycle(path) == ACTIVE_NON_AUTHORIZING


def test_stale_proposed_adopted_control_fails(tmp_path: Path):
    path = tmp_path / "CONTROL.md"
    path.write_text("# Control\n\n**Status:** PROPOSED / NON-AUTHORIZING\n", encoding="utf-8")
    baseline = {"CONTROL.md": ACTIVE_NON_AUTHORIZING}
    errors = validate_architecture_lifecycle(root=tmp_path, baseline=baseline)
    assert any("adopted baseline" in error for error in errors)


def test_accepted_is_reserved_for_adr(tmp_path: Path):
    path = tmp_path / "CONTROL.md"
    path.write_text("# Control\n\n**Status:** ACCEPTED\n", encoding="utf-8")
    baseline = {"CONTROL.md": ACCEPTED}
    errors = validate_architecture_lifecycle(root=tmp_path, baseline=baseline)
    assert any("reserved for architecture decision records" in error for error in errors)


def test_accepted_adr_is_allowed(tmp_path: Path):
    path = tmp_path / "ADR-999-test.md"
    path.write_text("# ADR\n\n**Status:** ACCEPTED\n", encoding="utf-8")
    baseline = {"ADR-999-test.md": ACCEPTED}
    assert validate_architecture_lifecycle(root=tmp_path, baseline=baseline) == []
