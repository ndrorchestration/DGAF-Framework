"""Synthetic reconciliation negatives: spoofable source strings are NOT independent evidence."""
from experiments.sbcf.attestation import Snapshot, reconcile
from experiments.sbcf.controller import Regime

SOURCES = frozenset({"enforcer", "worker_registry"})
def snap(source, **changes):
    data = dict(source=source, revision=7, production_capabilities=0, uncontrolled_workers=0, pending_external_actions=0, unauthorized_destinations=0, observable=True)
    data.update(changes)
    return Snapshot(**data)

def check(*snapshots, regime=Regime.QUARANTINED, revision=7):
    return reconcile(regime, snapshots, required_sources=SOURCES, min_revision=revision)

def test_consistent_fresh_source_coverage():
    assert check(snap("enforcer"), snap("worker_registry"))

def test_missing_source_denied():
    assert not check(snap("enforcer"))

def test_duplicate_source_denied():
    assert not check(snap("enforcer"), snap("enforcer"), snap("worker_registry"))

def test_unexpected_source_denied():
    assert not check(snap("enforcer"), snap("worker_registry"), snap("agent"))

def test_stale_source_denied():
    assert not check(snap("enforcer", revision=6), snap("worker_registry"))

def test_mismatch_denied():
    assert not check(snap("enforcer"), snap("worker_registry", uncontrolled_workers=1))

def test_incomplete_state_denied():
    assert not check(snap("enforcer", observable=False), snap("worker_registry", observable=False))

def test_regime_label_alone_denied():
    assert not check(snap("enforcer"), snap("worker_registry"), regime=Regime.RESTRICTED)
