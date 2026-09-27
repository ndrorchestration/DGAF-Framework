"""Tests for the governance benchmark evidence envelope."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "experiments/governance_benchmark/build_evidence_envelope.py"

spec = importlib.util.spec_from_file_location("benchmark_envelope", MODULE_PATH)
assert spec and spec.loader
envelope_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(envelope_module)


def build() -> dict:
    return envelope_module.build_envelope(REPO_ROOT)


def test_envelope_is_bound_to_exact_repository_commit() -> None:
    envelope = build()
    assert len(envelope["repository_commit"]) == 40
    assert envelope["repository_commit"] == envelope_module.git_head(REPO_ROOT)


def test_envelope_version_is_v2() -> None:
    assert build()["version"] == "DGAF_GOVERNANCE_BENCHMARK_EVIDENCE_ENVELOPE_V2"


def test_verification_class_remains_same_system_engineering_only() -> None:
    envelope = build()
    assert envelope["verification_class"] == "SAME_SYSTEM_LOCAL_ENGINEERING_VERIFICATION"
    assert envelope["state_projection"]["INDEPENDENT_VALIDATION"] == "NOT_ESTABLISHED"


def test_state_projection_preserves_claim_ceiling() -> None:
    state = build()["state_projection"]
    assert state["SCIENTIFIC_N_INCREMENT"] == 0
    assert state["CANONICAL_DGAF_EFFICACY"] == "NOT_ESTABLISHED"
    assert state["STATE_OF_THE_ART"] == "NOT_ESTABLISHED"
    assert state["HIGH_ASSURANCE"] == "NOT_AUTHORIZED"


def test_prohibited_inferences_cover_common_overclaims() -> None:
    prohibited = " ".join(build()["prohibited_inferences"])
    for phrase in (
        "state of the art",
        "generally safer",
        "efficacy is established",
        "independent validation",
        "production certified",
        "Scientific N",
    ):
        assert phrase in prohibited


def test_envelope_binds_all_canonical_layer_digests() -> None:
    envelope = build()
    assert set(envelope["canonical_layer_digests"]) == {
        "fixed",
        "mutations",
        "same_domain_interactions",
        "cross_domain_interactions",
        "strong_policy_comparator",
        "semantic_equivalence",
        "configuration_scaling",
        "recovery_composition",
        "provenance_custody",
    }
    assert all(len(value) == 64 for value in envelope["canonical_layer_digests"].values())


def test_envelope_scope_covers_all_admitted_layers() -> None:
    scope = build()["evidence_scope"]
    assert scope["fixed_cases"] == 13
    assert scope["one_field_mutations"] == 10
    assert scope["same_domain_interactions"] == 7
    assert scope["cross_domain_interactions"] == 6
    assert scope["strong_policy_cases"] == 13
    assert scope["semantic_equivalence_states"] == 112200
    assert scope["configuration_scaling_points"] == 4
    assert scope["recovery_composition_cases"] == 11
    assert scope["provenance_custody_mutations"] == 8
