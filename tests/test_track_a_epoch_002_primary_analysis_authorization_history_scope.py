from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "epoch_002_primary_analysis_authorization_history_scope",
        MODULE_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_authorization_event_shape_scopes_history_to_requested_event(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40

    def fake_git(*args: str) -> str:
        if args == ("rev-list", "--parents", "-n", "1", head):
            return f"{head} {parent}"
        if args == ("diff-tree", "--no-commit-id", "--name-only", "-r", head):
            return validator.AUTH_REL
        if args == ("log", "--format=%H", head, "--", validator.AUTH_REL):
            return head
        raise AssertionError(f"history escaped requested event scope: {args}")

    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", lambda spec: False)

    assert validator.validate_authorization_event_shape(head) == parent


def test_authorization_event_scopes_receipt_history_to_event_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40
    receipt_event = "a" * 40
    receipt_parent = "9" * 40
    receipt_bytes = b"receipt\n"

    monkeypatch.setattr(validator, "validate_authorization_event_shape", lambda event_head: parent)
    monkeypatch.setattr(validator, "validate_semantic_policy", lambda: None)
    monkeypatch.setattr(validator, "validate_materialization_receipt", lambda receipt: None)
    monkeypatch.setattr(validator, "validate_authorization_object", lambda *args, **kwargs: None)
    monkeypatch.setattr(validator, "validate_frozen_analysis_identities", lambda ref: None)
    monkeypatch.setattr(validator, "read_git_bytes", lambda ref, relpath: receipt_bytes)
    monkeypatch.setattr(validator, "load_json_at_ref", lambda ref, relpath: {})

    def fake_exists(spec: str) -> bool:
        if spec in {
            f"{parent}:{validator.MATERIALIZATION_RECEIPT_REL}",
            f"{head}:{validator.MATERIALIZATION_RECEIPT_REL}",
        }:
            return True
        return False

    def fake_git(*args: str) -> str:
        if args == (
            "log",
            "--format=%H",
            parent,
            "--",
            validator.MATERIALIZATION_RECEIPT_REL,
        ):
            return receipt_event
        if args == ("rev-list", "--parents", "-n", "1", receipt_event):
            return f"{receipt_event} {receipt_parent}"
        if args == ("diff-tree", "--no-commit-id", "--name-only", "-r", receipt_event):
            return validator.MATERIALIZATION_RECEIPT_REL
        if args == ("merge-base", "--is-ancestor", receipt_event, parent):
            return ""
        raise AssertionError(f"history escaped authorization-parent scope: {args}")

    monkeypatch.setattr(validator, "git_object_exists", fake_exists)
    monkeypatch.setattr(validator, "git", fake_git)

    assert validator.validate_authorization_event(head, accepted_parent_sha=parent) == parent
