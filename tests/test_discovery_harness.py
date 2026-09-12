import pytest

from dgaf_discovery.blindspots import (
    DetectionRecord,
    method_overlap,
    unique_discovery_rate,
    unexplained_shared_misses,
)
from dgaf_discovery.harness import DiscoveryEnvelope, validate_discovery_envelope
from dgaf_discovery.interactions import ControlContract, analyze_pairwise
from dgaf_discovery.mutations import critical_mutations
from dgaf_discovery.state_coverage import compute_transition_coverage


def test_envelope_rejects_authorization_and_scientific_changes():
    with pytest.raises(ValueError):
        validate_discovery_envelope(
            DiscoveryEnvelope("DETECTED", authorizes_transition=True)
        )
    with pytest.raises(ValueError):
        validate_discovery_envelope(
            DiscoveryEnvelope("DETECTED", scientific_n_increment=1)
        )


def test_default_envelope_is_non_authorizing():
    envelope = DiscoveryEnvelope("DETECTED")
    validate_discovery_envelope(envelope)
    assert envelope.mutation_performed_on_repository is False
    assert envelope.scientific_state_effect == "NONE"
    assert envelope.scientific_n_increment == 0


def test_critical_mutations_only_change_ephemeral_copies():
    source = {
        "authorization": "NOT_AUTHORIZED",
        "scientific_n": 0,
        "decision": "UNKNOWN",
        "evidence": {"independent": False, "predecessor_sha": "abc"},
    }
    for mutation in critical_mutations():
        mutated = mutation.apply(source)
        assert mutated is not source
    assert source["authorization"] == "NOT_AUTHORIZED"
    assert source["scientific_n"] == 0
    assert source["evidence"]["predecessor_sha"] == "abc"


def test_state_transition_coverage_separates_positive_and_negative_paths():
    result = compute_transition_coverage(
        {"A", "B", "C"},
        {("A", "B"), ("B", "C")},
        {"A", "B"},
        {("A", "B")},
        {("A", "C")},
        {("A", "C")},
    )
    assert result.state_coverage == 2 / 3
    assert result.legal_transition_coverage == 0.5
    assert result.forbidden_rejection_coverage == 1.0


def test_control_interaction_detects_collisions():
    controls = (
        ControlContract(
            "A",
            writes=frozenset({"state"}),
            requires=frozenset({"ready"}),
        ),
        ControlContract(
            "B",
            reads=frozenset({"state"}),
            writes=frozenset({"state"}),
            forbids=frozenset({"ready"}),
        ),
    )
    result = analyze_pairwise(controls)
    assert len(result) == 1
    assert set(result[0].codes) == {"F", "R", "W"}


def test_blind_spot_metrics_measure_method_diversity_and_shared_misses():
    records = (
        DetectionRecord("F1", frozenset({"mutation"}), frozenset({"formal", "chaos"})),
        DetectionRecord("F2", frozenset({"mutation", "formal"})),
        DetectionRecord("F3", frozenset({"formal"}), frozenset({"mutation", "chaos"})),
    )
    assert unique_discovery_rate(records, "mutation") == 0.5
    assert method_overlap(records, "mutation", "formal") == 1 / 3
    shared = unexplained_shared_misses(records)
    assert shared[frozenset({"formal", "chaos"})] == ("F1",)
