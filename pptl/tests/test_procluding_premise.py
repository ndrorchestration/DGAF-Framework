"""
test_procluding_premise.py — P-35 Procluding Premise Gate tests
DGAF-Framework · pptl/tests · S068 · 2026-05-31

Governance contract tests for ProcludingPremiseGate (P-03 × 4 contracts each gate):
  1. Correct pass/kill status
  2. Correct event_type on violation
  3. Correct downstream execution state (no continuation on KILL)
  4. Correct gate-specific invariant (T0 + KILL enforcement)
"""

import json
import pytest

from pptl.procluding_premise import (
    ConstitutionalInvariant,
    DGAF_CONSTITUTIONAL_INVARIANTS,
    PremiseViolationError,
    PremiseViolationEvent,
    PremiseViolationPolicy,
    ProcludingPremiseGate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def gate():
    return ProcludingPremiseGate(
        invariants=DGAF_CONSTITUTIONAL_INVARIANTS,
        session_id="S068-TEST",
        agent_id="test-agent",
    )


@pytest.fixture
def single_invariant_gate():
    return ProcludingPremiseGate(
        invariants=[
            ConstitutionalInvariant(
                id="INV-TEST",
                name="Test Invariant",
                description="Used for isolated contract testing.",
            )
        ],
        session_id="S068-TEST",
        agent_id="test-agent",
    )


# ---------------------------------------------------------------------------
# Contract 1 — Correct pass/kill status
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_pass_when_all_invariants_satisfied(gate):
    """All invariants satisfied → gate returns True."""
    result = gate.evaluate("compliant input", check_fn=lambda text, inv: True)
    assert result is True


@pytest.mark.governance
def test_kill_raised_on_single_violation(single_invariant_gate):
    """Single violated invariant → PremiseViolationError raised."""
    with pytest.raises(PremiseViolationError):
        single_invariant_gate.evaluate(
            "violating input",
            check_fn=lambda text, inv: False,
        )


# ---------------------------------------------------------------------------
# Contract 2 — Correct event_type on violation
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_violation_event_type_is_premise_violation(single_invariant_gate):
    """Violation event must carry event_type=PREMISE_VIOLATION."""
    with pytest.raises(PremiseViolationError) as exc_info:
        single_invariant_gate.evaluate(
            "bad input",
            check_fn=lambda text, inv: False,
        )
    event_dict = exc_info.value.event.to_dict()
    assert event_dict["event_type"] == "PREMISE_VIOLATION"


@pytest.mark.governance
def test_violation_event_carries_correct_invariant_id(single_invariant_gate):
    """Violation event invariant_id must match the violated invariant."""
    with pytest.raises(PremiseViolationError) as exc_info:
        single_invariant_gate.evaluate(
            "bad input",
            check_fn=lambda text, inv: False,
        )
    assert exc_info.value.event.invariant_id == "INV-TEST"


# ---------------------------------------------------------------------------
# Contract 3 — Correct downstream execution state (no continuation on KILL)
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_no_downstream_execution_on_kill(single_invariant_gate):
    """Execution must halt on KILL — downstream side effect must not run."""
    side_effect_ran = []

    def check_and_side_effect(text, inv):
        return False  # always violate

    def downstream():
        side_effect_ran.append(True)

    try:
        single_invariant_gate.evaluate("bad", check_fn=check_and_side_effect)
        downstream()  # must never reach here
    except PremiseViolationError:
        pass

    assert len(side_effect_ran) == 0


@pytest.mark.governance
def test_violation_logged_in_gate_violation_log(single_invariant_gate):
    """Violation must appear in gate.violation_log after KILL."""
    with pytest.raises(PremiseViolationError):
        single_invariant_gate.evaluate("bad", check_fn=lambda t, i: False)
    assert len(single_invariant_gate.violation_log) == 1


# ---------------------------------------------------------------------------
# Contract 4 — Gate-specific invariant: T0 + KILL enforcement
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_non_t0_invariant_rejected_at_instantiation():
    """Instantiation must fail if any invariant is not T0."""
    with pytest.raises(ValueError, match="T0"):
        ConstitutionalInvariant(
            id="BAD-01",
            name="Non-T0 Invariant",
            description="This should be rejected.",
            tier="T1",  # invalid
        )


@pytest.mark.governance
def test_non_kill_policy_rejected_at_instantiation():
    """Instantiation must fail if policy is not KILL."""
    with pytest.raises(ValueError, match="KILL"):
        ConstitutionalInvariant(
            id="BAD-02",
            name="Non-KILL Invariant",
            description="This should be rejected.",
            policy=PremiseViolationPolicy.WARN,  # invalid for T0
        )


@pytest.mark.governance
def test_gate_invariant_set_is_immutable(gate):
    """Gate invariant set must be a frozenset — immutable after instantiation."""
    assert isinstance(gate.invariants, frozenset)


@pytest.mark.governance
def test_export_log_is_valid_json(single_invariant_gate):
    """export_log() must return valid JSON string after violation."""
    with pytest.raises(PremiseViolationError):
        single_invariant_gate.evaluate("bad", check_fn=lambda t, i: False)
    log_json = single_invariant_gate.export_log()
    parsed = json.loads(log_json)
    assert isinstance(parsed, list)
    assert parsed[0]["event_type"] == "PREMISE_VIOLATION"


# ---------------------------------------------------------------------------
# DGAF canonical invariant set smoke test
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_dgaf_invariants_all_t0_kill():
    """All DGAF_CONSTITUTIONAL_INVARIANTS must be T0 + KILL."""
    for inv in DGAF_CONSTITUTIONAL_INVARIANTS:
        assert inv.tier == "T0"
        assert inv.policy == PremiseViolationPolicy.KILL


@pytest.mark.governance
def test_dgaf_invariants_count():
    """DGAF canonical set must contain exactly 5 invariants."""
    assert len(DGAF_CONSTITUTIONAL_INVARIANTS) == 5


@pytest.mark.governance
def test_dgaf_invariant_ids_unique():
    """All DGAF invariant IDs must be unique."""
    ids = [inv.id for inv in DGAF_CONSTITUTIONAL_INVARIANTS]
    assert len(ids) == len(set(ids))
