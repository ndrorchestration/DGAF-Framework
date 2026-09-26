"""Tests for reproducible governance benchmark review bundles."""

import hashlib
import importlib.util
import json
import subprocess
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


def test_sha256sums_match_every_archived_payload(tmp_path: Path) -> None:
    output = tmp_path / "review.zip"
    bundle.build_bundle(output)

    with zipfile.ZipFile(output) as archive:
        checksum_lines = archive.read("SHA256SUMS.txt").decode("ascii").splitlines()
        checksums = {}
        for line in checksum_lines:
            if not line:
                continue
            digest_value, name = line.split("  ", 1)
            checksums[name] = digest_value
        payload_names = set(archive.namelist()) - {"SHA256SUMS.txt"}
        assert set(checksums) == payload_names
        for name in payload_names:
            assert hashlib.sha256(archive.read(name)).hexdigest() == checksums[name]


def test_bundle_binds_evidence_to_exact_repository_head(tmp_path: Path) -> None:
    output = tmp_path / "review.zip"
    bundle.build_bundle(output)
    expected_head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()

    with zipfile.ZipFile(output) as archive:
        envelope = json.loads(archive.read("evidence-envelope.json"))
        handoff = archive.read("REVIEWER_HANDOFF.md").decode("utf-8")
        fixed = archive.read("fixed-benchmark.json").decode("utf-8")

    assert envelope["repository_commit"] == expected_head
    assert f"`{expected_head}`" in handoff
    assert envelope["state_projection"]["SCIENTIFIC_N_INCREMENT"] == 0
    assert envelope["state_projection"]["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["CANONICAL_DGAF_EFFICACY"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["STATE_OF_THE_ART"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"
    assert "elapsed_ns_informational" not in fixed
