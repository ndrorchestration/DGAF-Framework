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


def test_audit_seal_covers_full_input_hash_and_gate_records():
    tgl = TriadicGovernanceLoop(
        session_id="TEST",
        agent_id="tester",
        hooks=TGLHooks(premise_check_fn=lambda _text, _ctx: GateResult.PASS),
    )
    audit = tgl.run_turn("input")
    original = audit.seal_hash
    audit.gate_records[0].notes = "tampered"
    assert audit.seal() != original


def test_input_hash_is_full_sha256():
    tgl = TriadicGovernanceLoop(
        session_id="TEST",
        agent_id="tester",
        hooks=TGLHooks(),
    )
    assert len(tgl._hash_input("input")) == 64
