from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "scripts/aoss_v0_6_stage_a_decision_policy.py"


def load_policy():
    spec = importlib.util.spec_from_file_location("aoss_v06_stage_a_policy_test", POLICY_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_reference_actions_are_executable_with_frozen_precedence() -> None:
    policy = load_policy()
    cases = [
        (policy.PolicyInput(terminal=True, blocked=True), "RECORD_OUTCOME", "TERMINAL"),
        (policy.PolicyInput(blocked=True, deadlock_candidate=True), "ESCALATE_BLOCK", "BLOCKED"),
        (policy.PolicyInput(deadlock_candidate=True, conflicted=True), "PERTURB", "DEADLOCK_CANDIDATE"),
        (policy.PolicyInput(conflicted=True, uncertain=True), "ESCALATE_CONFLICT", "CONFLICTED"),
        (policy.PolicyInput(uncertain=True), "REQUEST_EVIDENCE", "UNCERTAIN"),
        (
            policy.PolicyInput(
                authorization="TRUE",
                validation="TRUE",
                provenance_valid="TRUE",
            ),
            "EXECUTE",
            "AUTHORIZED_AND_VALIDATED_AND_PROVENANCE_VALID",
        ),
        (
            policy.PolicyInput(
                authorization="FALSE",
                validation="TRUE",
                provenance_valid="TRUE",
            ),
            "REQUEST_AUTHORIZATION",
            "VALIDATED_AND_NOT_AUTHORIZED",
        ),
    ]
    for state, expected_decision, expected_rule in cases:
        result = policy.evaluate_policy(state)
        assert result.policy_version == policy.POLICY_VERSION
        assert result.decision == expected_decision
        assert result.matched_rule == expected_rule
        assert result.input_valid is True


def test_inconclusive_required_state_cannot_execute() -> None:
    policy = load_policy()
    state = policy.PolicyInput(
        authorization="TRUE",
        validation="TRUE",
        provenance_valid="INCONCLUSIVE",
    )
    result = policy.evaluate_policy(state)
    assert result.decision == "HOLD"
    assert result.matched_rule == "REQUIRED_PREDICATE_INCONCLUSIVE"


def test_explicit_inconclusive_guard_cannot_be_hidden_by_true_execution_inputs() -> None:
    policy = load_policy()
    state = policy.PolicyInput(
        authorization="TRUE",
        validation="TRUE",
        provenance_valid="TRUE",
        required_predicate_inconclusive=True,
    )
    result = policy.evaluate_policy(state)
    assert result.decision == "HOLD"
    assert result.matched_rule == "REQUIRED_PREDICATE_INCONCLUSIVE"


def test_invalid_tri_state_fails_closed() -> None:
    policy = load_policy()
    state = policy.PolicyInput(
        authorization="MAYBE",
        validation="TRUE",
        provenance_valid="TRUE",
    )
    result = policy.evaluate_policy(state)
    assert result.decision == "HOLD"
    assert result.input_valid is False


def test_default_state_fails_closed() -> None:
    policy = load_policy()
    result = policy.evaluate_policy(
        policy.PolicyInput(
            authorization="FALSE",
            validation="FALSE",
            provenance_valid="FALSE",
        )
    )
    assert result.decision == "HOLD"
    assert result.matched_rule == "DEFAULT_FAIL_CLOSED"
