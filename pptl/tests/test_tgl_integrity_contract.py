from pptl.triadic_governance_loop import GateResult, TGLHooks, TriadicGovernanceLoop


def test_hpg_requires_phi_pass():
    called = []
    tgl = TriadicGovernanceLoop(
        session_id="TEST",
        agent_id="tester",
        hooks=TGLHooks(
            premise_check_fn=lambda _text, _ctx: GateResult.PASS,
            phi_closure_fn=lambda _text, _ctx: GateResult.WARN,
            hpg_fn=lambda _text, _ctx: called.append(True) or GateResult.PASS,
        ),
    )
    audit = tgl.run_turn("input")
    assert not called
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result is GateResult.SKIP
    assert "Phi-Closure did not PASS" in hpg.notes
