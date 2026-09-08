from components.ensemble_v17 import ContextToken, Tier
from experiments.pdmal_pilot.b2_stateful_context_closure_profile import (
    PersistentContextClosureSession, registered_unstable_checkpoint_session,
)

def test_phi_checkpoints_reached_without_counter_injection():
    s=registered_unstable_checkpoint_session()
    events=s["phi_checkpoint_events"]
    assert [e["fib_index"] for e in events] == [13,21,34,55]
    assert [e["decision"] for e in events] == ["warn","escalate","kill_rec","kill_rec"]
    assert s["phi_total_count"] == 55
    assert s["scientific_n_increment"] == 0

def test_scpe_operates_on_populated_store_and_prunes():
    s=registered_unstable_checkpoint_session()
    assert "axiom" in s["token_store"]
    assert "old-explore" not in s["token_store"]
    assert s["prune_event_count"] >= 1

def test_state_persists_across_turns():
    s=PersistentContextClosureSession("persist")
    s.apply_turn("t1","payload 1",tokens=(ContextToken("a","axiom",Tier.AXIOM),),is_stable=True)
    e=s.apply_turn("t2","payload 2",is_stable=False)
    assert "a" in e["scpe_snapshot"]
    assert e["phi_total_count"] == 2
    assert e["phi_stable_count"] == 1

def test_new_session_resets_state_exactly():
    a=PersistentContextClosureSession("a")
    a.apply_turn("t1","payload",tokens=(ContextToken("a","axiom",Tier.AXIOM),),is_stable=True)
    b=PersistentContextClosureSession("b")
    assert b.turns == 0
    assert b.scpe.snapshot() == {}
    assert b.phi._total == 0 and b.phi._stable == 0 and b.phi._consec_fails == 0
