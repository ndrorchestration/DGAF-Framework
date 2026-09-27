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
        "strong-policy-comparator.json",
        "semantic-equivalence.json",
        "configuration-scaling.json",
        "recovery-composition.json",
        "provenance-custody.json",
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
    expected_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()

    with zipfile.ZipFile(output) as archive:
        envelope = json.loads(archive.read("evidence-envelope.json"))
        handoff = archive.read("REVIEWER_HANDOFF.md").decode("utf-8")
        fixed = archive.read("fixed-benchmark.json").decode("utf-8")
        strong = json.loads(archive.read("strong-policy-comparator.json"))
        equivalence = json.loads(archive.read("semantic-equivalence.json"))
        scaling = json.loads(archive.read("configuration-scaling.json"))
        recovery = json.loads(archive.read("recovery-composition.json"))
        custody = json.loads(archive.read("provenance-custody.json"))

    assert envelope["repository_commit"] == expected_head
    assert f"`{expected_head}`" in handoff
    assert envelope["state_projection"]["SCIENTIFIC_N_INCREMENT"] == 0
    assert envelope["state_projection"]["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["CANONICAL_DGAF_EFFICACY"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["STATE_OF_THE_ART"] == "NOT_ESTABLISHED"
    assert envelope["state_projection"]["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"
    assert "elapsed_ns_informational" not in fixed
    assert strong["falsification_outcome"] == "PARITY_ON_CURRENT_FIXED_FIXTURES"
    assert strong["summary"]["difference_count"] == 0
    assert equivalence["summary"]["difference_count"] == 0
    assert equivalence["summary"]["semantically_equivalent_on_enumerated_schema"] is True
    assert scaling["falsification_outcome"] == "NO_UNIQUE_CONFIGURATION_SCALING_ADVANTAGE_IN_NEUTRAL_REUSE_MODEL"
    assert recovery["falsification_outcome"] == "NO_UNIQUE_COMPOSITION_OR_RECOVERY_ADVANTAGE_IN_MATCHED_SEMANTICS_CASES"
    assert recovery["summary"]["difference_count"] == 0
    assert custody["falsification_outcome"] == "NO_UNIQUE_PROVENANCE_CUSTODY_ADVANTAGE_IN_MATCHED_CHECKS"
    assert custody["summary"]["difference_count"] == 0
    for payload in (strong, equivalence, scaling, recovery, custody):
        assert "STATE_OF_THE_ART_NOT_ESTABLISHED" in payload["claim_ceiling"]
        assert "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED" in payload["claim_ceiling"]
        assert "INDEPENDENT_VALIDATION_NOT_ESTABLISHED" in payload["claim_ceiling"]

def test_bundle_evidence_payloads_are_indexed_by_envelope(tmp_path: Path) -> None:
    output = tmp_path / "review.zip"
    bundle.build_bundle(output)

    payload_to_layer = {
        "fixed-benchmark.json": "fixed",
        "mutations.json": "mutations",
        "same-domain-interactions.json": "same_domain_interactions",
        "cross-domain-interactions.json": "cross_domain_interactions",
        "strong-policy-comparator.json": "strong_policy_comparator",
        "semantic-equivalence.json": "semantic_equivalence",
        "configuration-scaling.json": "configuration_scaling",
        "recovery-composition.json": "recovery_composition",
        "provenance-custody.json": "provenance_custody",
    }

    with zipfile.ZipFile(output) as archive:
        envelope = json.loads(archive.read("evidence-envelope.json"))
        indexed = envelope["canonical_layer_digests"]
        assert set(indexed) == set(payload_to_layer.values())

        for payload_name, layer_name in payload_to_layer.items():
            payload = json.loads(archive.read(payload_name))
            assert bundle.manifest_module.digest(payload) == indexed[layer_name]

