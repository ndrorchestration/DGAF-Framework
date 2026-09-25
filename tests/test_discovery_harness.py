import subprocess

import pytest

from dgaf_discovery.blindspots import (
    DetectionRecord,
    method_overlap,
    unexplained_shared_misses,
    unique_discovery_rate,
)
from dgaf_discovery.harness import DiscoveryEnvelope, validate_discovery_envelope
from dgaf_discovery.historical_replay import (
    HistoricalReplayResult,
    validate_historical_replay_result,
)
from dgaf_discovery.interactions import ControlContract, analyze_pairwise
from dgaf_discovery.mutations import critical_mutations
from dgaf_discovery.state_coverage import (
    compute_transition_coverage,
    validate_positive_path_liveness,
)
from pptl.control_plane import _ALLOWED, ControlPlane, ControlTask
from pptl.governance_envelope import GovernanceEnvelope, ResourceBudget
from pptl.triadic_governance_loop import TurnAuditRecord, TurnStatus


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_envelope_rejects_authorization_and_scientific_changes():
    with pytest.raises(ValueError):
        validate_discovery_envelope(DiscoveryEnvelope("DETECTED", authorizes_transition=True))
    with pytest.raises(ValueError):
        validate_discovery_envelope(DiscoveryEnvelope("DETECTED", scientific_n_increment=1))


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


def test_positive_path_liveness_rejects_unreachable_declared_legal_transition():
    with pytest.raises(ValueError, match="A->C"):
        validate_positive_path_liveness(
            {("A", "B"), ("A", "C")},
            {("A", "B")},
        )


def test_positive_path_liveness_has_no_authorizing_or_scientific_effect():
    result = validate_positive_path_liveness(
        {("DATASET_LOCKED", "UNBLINDING_AUTHORIZED")},
        {("DATASET_LOCKED", "UNBLINDING_AUTHORIZED")},
    )
    assert result.liveness_established_for_declared_scope is True
    assert result.authoritative_effect == "NONE"
    assert result.scientific_state_effect == "NONE"
    assert result.scientific_n_increment == 0


def test_historical_crlf_exact_byte_defect_is_detected_now(tmp_path):
    from scripts.aoss_stage_a.preflight import PreflightError, _require_blob

    repo = tmp_path / "crlf-replay"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "replay@example.invalid")
    _git(repo, "config", "user.name", "DGAF Historical Replay")

    fixture = repo / "fixture.txt"
    fixture.write_bytes(b"line-one\nline-two\n")
    _git(repo, "add", "fixture.txt")
    _git(repo, "commit", "-m", "retain canonical LF bytes")
    expected_blob = _git(repo, "rev-parse", "HEAD:fixture.txt")

    fixture.write_bytes(b"line-one\r\nline-two\r\n")
    assert _git(repo, "rev-parse", "HEAD:fixture.txt") == expected_blob
    assert _git(repo, "hash-object", "--", "fixture.txt") != expected_blob

    with pytest.raises(PreflightError) as caught:
        _require_blob(repo, "HEAD", "fixture.txt", expected_blob)

    assert caught.value.code == "WORKTREE_BLOB_MISMATCH"
    result = HistoricalReplayResult(
        case_id="HIST-CRLF-EXACT-BYTE-001",
        historical_defect="LF index bytes rematerialized as CRLF worktree bytes",
        detector="scripts.aoss_stage_a.preflight._require_blob",
        expected_disposition="FAIL_CLOSED",
        observed_disposition="FAIL_CLOSED",
        observed_code=caught.value.code,
        detected_now=True,
    )
    validate_historical_replay_result(result)
    assert result.replay_pass is True
    assert result.historical_prevention_claimed is False
    assert result.scientific_n_increment == 0


def test_historical_replay_rejects_counterfactual_prevention_claim():
    result = HistoricalReplayResult(
        case_id="HIST-CRLF-EXACT-BYTE-001",
        historical_defect="CRLF exact-byte mismatch",
        detector="scripts.aoss_stage_a.preflight._require_blob",
        expected_disposition="FAIL_CLOSED",
        observed_disposition="FAIL_CLOSED",
        observed_code="WORKTREE_BLOB_MISMATCH",
        detected_now=True,
        historical_prevention_claimed=True,
    )
    with pytest.raises(ValueError, match="counterfactual"):
        validate_historical_replay_result(result)


def test_historical_replay_may_retain_an_escape_without_claim_inflation():
    escaped = HistoricalReplayResult(
        case_id="HIST-FUTURE-ESCAPE",
        historical_defect="placeholder retained escaped defect",
        detector="example.detector",
        expected_disposition="FAIL_CLOSED",
        observed_disposition="ESCAPED",
        observed_code=None,
        detected_now=False,
    )
    validate_historical_replay_result(escaped)
    assert escaped.replay_pass is False
    assert escaped.authoritative_effect == "NONE"
    assert escaped.canonical_dgaf_efficacy == "NOT_ESTABLISHED"


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


def _control_budget():
    return ResourceBudget(
        max_input_tokens=100,
        max_output_tokens=100,
        max_tool_calls=4,
        max_elapsed_ms=1000,
        max_rounds=4,
        max_nodes=8,
        max_depth=2,
        max_concurrency=2,
    )


def _control_envelope(*, side_effect_mode="PROPOSE_ONLY"):
    return GovernanceEnvelope(
        trace_id="liveness-trace",
        task_id="root",
        authority_scope={"research"},
        permitted_tools={"read"},
        data_classes={"public"},
        prohibited_actions={"delete"},
        budget=_control_budget(),
        side_effect_mode=side_effect_mode,
    )


def _sealed_pass_result():
    audit = TurnAuditRecord(
        session_id="liveness-test",
        turn_index=1,
        agent_id="test-agent",
        input_hash="a" * 64,
        gate_records=[],
        final_status=TurnStatus("PASS"),
        timestamp="2026-09-25T00:00:00+00:00",
    )
    audit.seal()
    return audit


def _observe_state_change(task, action):
    before = task.state.value
    action()
    after = task.state.value
    assert before != after
    return before, after


def _public_control_plane_transition_edges():
    observed = set()

    def fresh(*, side_effect_mode="PROPOSE_ONLY", with_tgl=False):
        runner = (lambda _input, _context: _sealed_pass_result()) if with_tgl else None
        plane = ControlPlane(tgl_runner=runner)
        task = ControlTask("root", _control_envelope(side_effect_mode=side_effect_mode))
        observed.add(_observe_state_change(task, lambda: plane.submit(task)))
        return plane, task

    def admitted(*, side_effect_mode="PROPOSE_ONLY", with_tgl=False):
        plane, task = fresh(side_effect_mode=side_effect_mode, with_tgl=with_tgl)
        observed.add(_observe_state_change(task, lambda: plane.admit("root")))
        return plane, task

    def expanding():
        plane, task = admitted()
        observed.add(_observe_state_change(task, lambda: plane.start_expansion("root")))
        return plane, task

    def evaluating(*, side_effect_mode="PROPOSE_ONLY", with_tgl=False):
        plane, task = admitted(side_effect_mode=side_effect_mode, with_tgl=with_tgl)
        observed.add(_observe_state_change(task, lambda: plane.begin_evaluation("root")))
        return plane, task

    def merge_ready(*, side_effect_mode="PROPOSE_ONLY"):
        plane, task = evaluating(side_effect_mode=side_effect_mode, with_tgl=True)
        plane.evaluate_turn("root", "liveness")
        observed.add(_observe_state_change(task, lambda: plane.mark_merge_ready("root")))
        return plane, task

    # PREFLIGHT exits.
    plane, task = fresh()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    plane, task = fresh()
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    # ADMITTED exits.
    plane, task = admitted()
    observed.add(_observe_state_change(task, lambda: plane.start_expansion("root")))
    plane, task = admitted()
    observed.add(_observe_state_change(task, lambda: plane.begin_evaluation("root")))
    plane, task = admitted()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    plane, task = admitted()
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    # EXPANDING exits.
    plane, task = expanding()
    observed.add(_observe_state_change(task, lambda: plane.begin_evaluation("root")))
    plane, task = expanding()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    plane, task = expanding()
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    # EVALUATING exits.
    plane, task = evaluating()
    observed.add(_observe_state_change(task, lambda: plane.start_expansion("root")))
    plane, task = merge_ready()
    plane, task = evaluating()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    plane, task = evaluating()
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    # MERGE_READY exits.
    plane, task = merge_ready(side_effect_mode="COMMIT_ALLOWED")
    observed.add(_observe_state_change(task, lambda: plane.mark_commit_ready("root")))
    plane, task = merge_ready()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    plane, task = merge_ready()
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    # COMMIT_READY exits.
    plane, task = merge_ready(side_effect_mode="COMMIT_ALLOWED")
    observed.add(_observe_state_change(task, lambda: plane.mark_commit_ready("root")))
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))
    plane, task = merge_ready(side_effect_mode="COMMIT_ALLOWED")
    observed.add(_observe_state_change(task, lambda: plane.mark_commit_ready("root")))
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))

    # ESCALATED exit.
    plane, task = fresh()
    observed.add(_observe_state_change(task, lambda: plane.veto("root", "liveness")))
    observed.add(_observe_state_change(task, lambda: plane.terminate("root")))

    return observed


def test_control_plane_declared_liveness_exposes_received_termination_gap():
    declared = {
        (source.value, target.value)
        for source, targets in _ALLOWED.items()
        for target in targets
    }
    observed = _public_control_plane_transition_edges()

    assert len(declared) == 22
    assert observed <= declared
    assert declared - observed == {("RECEIVED", "TERMINATED")}

    plane = ControlPlane()
    task = ControlTask("root", _control_envelope())
    with pytest.raises(KeyError):
        plane.terminate("root")
    assert task.state.value == "RECEIVED"

    with pytest.raises(ValueError, match="RECEIVED->TERMINATED"):
        validate_positive_path_liveness(declared, observed)
