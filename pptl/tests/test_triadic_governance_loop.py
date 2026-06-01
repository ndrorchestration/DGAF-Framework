"""
test_triadic_governance_loop.py — TGL governance contract tests
DGAF-Framework · pptl/tests · S068 · 2026-05-31

P-03 × 4 contracts per gate:
  1. Correct pass/kill/warn status
  2. Correct event_type emitted
  3. Correct downstream execution state
  4. Correct gate-specific invariant
"""

import pytest

from pptl.procluding_premise import PremiseViolationError
from pptl.triadic_governance_loop import (
    GateResult,
    TriadicGovernanceLoop,
    TGLHooks,
    TurnStatus,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_tgl(hooks: TGLHooks = None) -> TriadicGovernanceLoop:
    return TriadicGovernanceLoop(
        session_id="S068-TEST",
        agent_id="test-amethyst",
        hooks=hooks or TGLHooks(),
    )


# ---------------------------------------------------------------------------
# Contract 1 — pass/kill/warn status
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_full_skip_turn_returns_pass():
    """All hooks None (SKIP) → final_status PASS."""
    tgl = make_tgl()
    audit = tgl.run_turn("safe input")
    assert audit.final_status == TurnStatus.PASS


@pytest.mark.governance
def test_premise_violation_raises_and_kills():
    """P-35 KILL → PremiseViolationError raised, gate logged as KILL."""
    hooks = TGLHooks(premise_check_fn=lambda text, inv: False)
    tgl = make_tgl(hooks)
    with pytest.raises(PremiseViolationError):
        tgl.run_turn("constitutional violation")


@pytest.mark.governance
def test_downstream_gate_kill_sets_status():
    """Gate KILL at step 3 → final_status KILL, no further steps executed."""
    executed_steps = []

    def kill_gate(text, ctx):
        executed_steps.append(3)
        return GateResult.KILL

    def should_not_run(text, ctx):
        executed_steps.append(99)  # must never appear
        return GateResult.PASS

    hooks = TGLHooks(
        demijoul_fn=kill_gate,
        kappa_fn=should_not_run,
    )
    tgl = make_tgl(hooks)
    audit = tgl.run_turn("trigger kill")
    assert audit.final_status == TurnStatus.KILL
    assert 99 not in executed_steps


@pytest.mark.governance
def test_phi_closure_kill_sets_kill_rec():
    """P-32 KILL → final_status KILL_REC."""
    hooks = TGLHooks(phi_closure_fn=lambda t, c: GateResult.KILL)
    tgl = make_tgl(hooks)
    audit = tgl.run_turn("phi closure fail")
    assert audit.final_status == TurnStatus.KILL_REC


# ---------------------------------------------------------------------------
# Contract 2 — event_type emitted
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_herald_receives_tgl_turn_audit_event():
    """Herald hook receives dict with event_type TGL_TURN_AUDIT."""
    received = []

    def capture_herald(audit_dict, ctx):
        received.append(audit_dict.get("audit_record", {}))
        return GateResult.PASS

    hooks = TGLHooks(herald_fn=capture_herald)
    tgl = make_tgl(hooks)
    tgl.run_turn("test input")
    assert len(received) == 1
    assert received[0]["event_type"] == "TGL_TURN_AUDIT"


# ---------------------------------------------------------------------------
# Contract 3 — downstream execution state
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_turn_counter_increments_per_run():
    """turn_counter must increment by 1 per run_turn call."""
    tgl = make_tgl()
    assert tgl.turn_counter == 0
    tgl.run_turn("first")
    assert tgl.turn_counter == 1
    tgl.run_turn("second")
    assert tgl.turn_counter == 2


@pytest.mark.governance
def test_audit_record_is_sealed():
    """TurnAuditRecord must have a non-empty seal_hash after run."""
    tgl = make_tgl()
    audit = tgl.run_turn("sealed turn")
    assert audit.seal_hash != ""
    assert len(audit.seal_hash) == 64  # SHA-256 hex


# ---------------------------------------------------------------------------
# Contract 4 — gate-specific invariant
# ---------------------------------------------------------------------------

@pytest.mark.governance
def test_gate_records_include_all_10_steps():
    """Gate records must include one entry per TGL step (0–9)."""
    tgl = make_tgl()
    audit = tgl.run_turn("full pass")
    steps = {g.step for g in audit.gate_records}
    assert steps == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


@pytest.mark.governance
def test_all_unwired_gates_marked_skip():
    """Unwired gates (hooks=None) must be marked SKIP, not PASS or KILL."""
    tgl = make_tgl()  # no hooks
    audit = tgl.run_turn("skip test")
    # Step 0 (P-35) always runs; steps 1-8 should be SKIP
    skip_steps = [g for g in audit.gate_records if g.step in range(1, 9)]
    assert all(g.result == GateResult.SKIP for g in skip_steps)


@pytest.mark.governance
def test_p35_always_fires_regardless_of_hooks():
    """P-35 gate must always run (step 0), even when all other hooks are None."""
    tgl = make_tgl()
    audit = tgl.run_turn("p35 check")
    step0 = next(g for g in audit.gate_records if g.step == 0)
    assert step0.pattern == "P-35"
    assert step0.result in (GateResult.PASS, GateResult.SKIP, GateResult.KILL)
    # P-35 runs with pass-through when premise_check_fn is None
    assert step0.result == GateResult.PASS
