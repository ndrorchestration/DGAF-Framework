"""Tests for the governance-benchmark evidence manifest."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/build_evidence_manifest.py"

spec = importlib.util.spec_from_file_location("benchmark_manifest", MODULE_PATH)
assert spec and spec.loader
manifest_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest_module)


def test_manifest_covers_all_benchmark_layers() -> None:
    manifest = manifest_module.build_manifest()
    assert set(manifest["entries"]) == {
        "fixed",
        "mutations",
        "same_domain_interactions",
        "cross_domain_interactions",
    }


def test_canonical_digest_excludes_informational_timing() -> None:
    report = manifest_module.benchmark.run()
    altered = dict(report)
    altered["results"] = [dict(row) for row in report["results"]]
    for row in altered["results"]:
        row["elapsed_ns_informational"] = row["elapsed_ns_informational"] + 999999
    assert manifest_module.digest(report) == manifest_module.digest(altered)


def test_manifest_preserves_non_promoting_boundaries() -> None:
    manifest = manifest_module.build_manifest()
    assert "NO_SCIENTIFIC_N_INCREMENT" in manifest["non_effects"]
    assert "NO_INDEPENDENT_VALIDATION" in manifest["non_effects"]
    assert "NO_CANONICAL_EFFICACY" in manifest["non_effects"]
    assert "NO_STATE_OF_THE_ART_CLAIM" in manifest["non_effects"]


def test_all_adversarial_layers_report_pass() -> None:
    manifest = manifest_module.build_manifest()
    for name in ("mutations", "same_domain_interactions", "cross_domain_interactions"):
        assert manifest["entries"][name]["all_pass"] is True


def test_fixed_summary_retains_incremental_cost_and_protection_signals() -> None:
    manifest = manifest_module.build_manifest()
    fixed = manifest["entries"]["fixed"]["summary"]
    assert fixed["C2_HARDENED_POLICY_AS_CODE"]["unsafe_action_or_flow_admitted"] == 2
    assert fixed["D_DGAF"]["unsafe_action_or_flow_admitted"] == 0
