from __future__ import annotations

from pathlib import Path

import pytest

from scripts import ci_changed_python_targets as targets


def test_normalize_changed_paths_keeps_python_across_repository_roots(tmp_path: Path) -> None:
    paths = [
        "components/core.py",
        "tests/test_core.py",
        "scripts/validator.py",
        "api/handler.py",
        "experiments/probe.pyi",
    ]
    for path in paths:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("", encoding="utf-8")

    raw = b"\0".join(path.encode() for path in reversed(paths)) + b"\0"

    assert targets._normalize_changed_paths(raw, tmp_path) == sorted(paths)


def test_normalize_changed_paths_excludes_deleted_and_non_python_files(tmp_path: Path) -> None:
    existing = tmp_path / "scripts/live.py"
    existing.parent.mkdir(parents=True)
    existing.write_text("", encoding="utf-8")

    raw = b"scripts/live.py\0scripts/deleted.py\0docs/readme.md\0"

    assert targets._normalize_changed_paths(raw, tmp_path) == ["scripts/live.py"]


@pytest.mark.parametrize("path", [b"../escape.py", b"/absolute.py"])
def test_normalize_changed_paths_rejects_unsafe_paths(tmp_path: Path, path: bytes) -> None:
    with pytest.raises(ValueError, match="unsafe changed path"):
        targets._normalize_changed_paths(path + b"\0", tmp_path)


def test_changed_python_files_uses_acmr_diff_and_python_pathspecs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    script = tmp_path / "scripts/tool.py"
    script.parent.mkdir(parents=True)
    script.write_text("", encoding="utf-8")

    observed: dict[str, object] = {}

    def fake_check_output(command: list[str], cwd: Path) -> bytes:
        observed["command"] = command
        observed["cwd"] = cwd
        return b"scripts/tool.py\0"

    monkeypatch.setattr(targets.subprocess, "check_output", fake_check_output)

    assert targets.changed_python_files("base", "head", tmp_path) == ["scripts/tool.py"]
    assert observed["cwd"] == tmp_path
    assert observed["command"] == [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMR",
        "-z",
        "base",
        "head",
        "--",
        "*.py",
        "*.pyi",
    ]
