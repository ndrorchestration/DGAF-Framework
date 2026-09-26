"""Tests for reproducible governance benchmark review bundles."""

import hashlib
import importlib.util
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/package_review_bundle.py"

spec = importlib.util.spec_from_file_location("review_bundle", MODULE_PATH)
assert spec and spec.loader
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_bundle_is_reproducible_and_contains_required_files(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    bundle.build_bundle(first)
    bundle.build_bundle(second)
    assert digest(first) == digest(second)

    with zipfile.ZipFile(first) as archive:
        names = set(archive.namelist())
    assert names == {
        "REVIEWER_HANDOFF.md",
        "SHA256SUMS.txt",
        "cross-domain-interactions.json",
        "evidence-envelope.json",
        "evidence-manifest.json",
        "fixed-benchmark.json",
        "mutations.json",
        "same-domain-interactions.json",
    }
