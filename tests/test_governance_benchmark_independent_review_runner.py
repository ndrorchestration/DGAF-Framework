"""Tests for the independent governance-benchmark reviewer runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts/run_governance_benchmark_independent_review.py"

spec = importlib.util.spec_from_file_location("independent_review_runner", MODULE_PATH)
assert spec and spec.loader
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def _write_bundle(path: Path, *, commit: str, corrupt_layer: str | None = None) -> str:
    payloads = {
        name: {"layer": layer, "value": 1, "elapsed_ns_informational": 123}
        for name, layer in runner.PAYLOAD_TO_LAYER.items()
    }
    layer_digests = {
        layer: runner.canonical_digest(payloads[name])
        for name, layer in runner.PAYLOAD_TO_LAYER.items()
    }
    if corrupt_layer is not None:
        layer_digests[corrupt_layer] = "0" * 64

    files: dict[str, bytes] = {
        name: (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
        for name, payload in payloads.items()
    }
    files["evidence-envelope.json"] = (
        json.dumps(
            {
                "version": "DGAF_GOVERNANCE_BENCHMARK_EVIDENCE_ENVELOPE_V2",
                "repository_commit": commit,
                "canonical_layer_digests": layer_digests,
            },
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    files["evidence-manifest.json"] = b"{}\n"
    files["REVIEWER_HANDOFF.md"] = f"Repository commit: {commit}\n".encode("utf-8")

    sums = "".join(
        f"{hashlib.sha256(files[name]).hexdigest()}  {name}\n"
        for name in sorted(files)
    ).encode("ascii")
    files["SHA256SUMS.txt"] = sums

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr(name, data)

    return runner.sha256_file(path)


def test_canonical_digest_ignores_informational_timing() -> None:
    left = {"decision": "ALLOW", "elapsed_ns_informational": 1}
    right = {"decision": "ALLOW", "elapsed_ns_informational": 999}
    assert runner.canonical_digest(left) == runner.canonical_digest(right)


def test_verify_bundle_accepts_complete_matching_bundle(tmp_path: Path) -> None:
    commit = "a" * 40
    bundle = tmp_path / "review.zip"
    digest = _write_bundle(bundle, commit=commit)

    checks = runner.verify_bundle(
        bundle,
        expected_commit=commit,
        expected_bundle_sha256=digest,
    )

    assert checks["all_identity_checks_pass"] is True
    assert checks["sha256sums_valid"] is True
    assert checks["sha256sums_complete"] is True
    assert checks["handoff_commit_matches"] is True
    assert checks["envelope_commit_matches"] is True
    assert checks["envelope_layers_complete"] is True
    assert checks["canonical_layer_digests_match"] is True


def test_verify_bundle_rejects_envelope_digest_mismatch(tmp_path: Path) -> None:
    commit = "b" * 40
    bundle = tmp_path / "review.zip"
    digest = _write_bundle(bundle, commit=commit, corrupt_layer="provenance_custody")

    checks = runner.verify_bundle(
        bundle,
        expected_commit=commit,
        expected_bundle_sha256=digest,
    )

    assert checks["all_identity_checks_pass"] is False
    assert checks["canonical_layer_digests_match"] is False
    assert any("provenance-custody.json" in error for error in checks["errors"])


def test_disposition_reproduced_only_when_every_gate_passes() -> None:
    command_ok = {"started": True, "returncode": 0}
    bundle_ok = {"all_identity_checks_pass": True}
    assert (
        runner.disposition(
            head_matches=True,
            tests=command_ok,
            package=command_ok,
            bundle_checks=bundle_ok,
        )
        == "REPRODUCED"
    )


def test_disposition_preserves_mismatch_and_blocked_outcomes() -> None:
    ok = {"started": True, "returncode": 0}
    failed = {"started": True, "returncode": 1}
    bundle_ok = {"all_identity_checks_pass": True}

    assert (
        runner.disposition(
            head_matches=True,
            tests=failed,
            package=ok,
            bundle_checks=bundle_ok,
        )
        == "MISMATCH"
    )
    assert (
        runner.disposition(
            head_matches=False,
            tests=ok,
            package=ok,
            bundle_checks=bundle_ok,
        )
        == "BLOCKED"
    )


def test_required_test_contract_includes_all_current_benchmark_layers() -> None:
    joined = " ".join(runner.TEST_PATHS)
    for name in (
        "strong_policy",
        "semantic_equivalence",
        "configuration_scaling",
        "recovery_composition",
        "provenance_custody",
        "evidence_envelope",
        "review_bundle",
    ):
        assert name in joined
