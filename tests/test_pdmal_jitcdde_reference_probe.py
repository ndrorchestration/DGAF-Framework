"""Pure contract checks for the optional external-library DDE probe.

These tests require only pytest and Python. They intentionally DO NOT import,
install, compile, or execute JiTCDDE, and create no scientific outcomes.
"""

import hashlib
import json
import math

import pytest

import tools.pdmal.jitcdde_reference_probe as probe


def test_four_node_fixture_contract_and_grid_are_exact():
    assert probe.validate_fixture() == 40
    manifest = probe.fixture_manifest()
    assert manifest["schema"] == "pdmal-gr-jitcdde-fixture-v1"
    assert manifest["history"] == "constant phase vector for all t <= 0"
    assert manifest["sample_grid_s"] == 0.02
    assert manifest["horizon_s"] == 0.8
    assert len(manifest["directed_physical_delays"]) == 5
    assert manifest["bootstrap_step_s"] == 0.001
    assert len(manifest["graph"]) == 5


def test_fixture_fingerprint_is_canonical_json_stable():
    fixture = probe.fixture_manifest()
    canonical = json.dumps(fixture, sort_keys=True, separators=(",", ":")).encode("utf-8")
    # Frozen fixture identity catches accidental changes in any canonical field.
    assert hashlib.sha256(canonical).hexdigest() == "9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15"
    modified = {**fixture, "coupling": 1.2}
    changed_bytes = json.dumps(modified, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(changed_bytes).hexdigest() != hashlib.sha256(canonical).hexdigest()
    assert fixture["directed_physical_delays"] == [
        [0, 1, 0.12],
        [0, 3, 0.1],
        [1, 0, 0.06],
        [2, 1, 0.04],
        [3, 2, 0.08],
    ]


def test_directed_rhs_preserves_receiver_sender_orientation_and_default_zero_delay():
    """Numeric substitute for symbolic y(t): no optional solver is involved."""
    phases = (0.2, -0.8, 1.4, -0.4)

    def sample_y(index, time=None):
        if time is None:
            return phases[index]
        return phases[index] + (time - 1.0) * 0.4 * (index + 1)

    rhs = probe.build_symbolic_rhs(sample_y, 1.0, math.sin)
    expected = []
    for receiver in range(4):
        neighbors = [v if u == receiver else u for u, v in probe.GRAPH if receiver in (u, v)]
        terms = []
        for sender in neighbors:
            lag = probe.DELAYS.get((receiver, sender), 0.0)
            sender_value = phases[sender] - lag * 0.4 * (sender + 1)
            terms.append(math.sin(sender_value - phases[receiver]))
        expected.append(probe.FREQUENCIES[receiver] + probe.COUPLING * sum(terms) / len(neighbors))
    assert rhs == pytest.approx(expected, abs=1e-14)


@pytest.mark.parametrize("bad", [0.03, -0.02, float("nan"), True])
def test_delay_alignment_changes_fail_closed(monkeypatch, bad):
    corrupted = dict(probe.DELAYS)
    corrupted[(0, 1)] = bad
    monkeypatch.setattr(probe, "DELAYS", corrupted)
    with pytest.raises(ValueError):
        probe.validate_fixture()


def test_graph_mutation_fail_closed(monkeypatch):
    monkeypatch.setattr(probe, "GRAPH", ((0, 1), (1, 0)))
    with pytest.raises(ValueError):
        probe.validate_fixture()


def test_invalid_bootstrap_spacing_fail_closed(monkeypatch):
    monkeypatch.setattr(probe, "FIXED_BOOTSTRAP_STEP", 0.003)
    with pytest.raises(ValueError):
        probe.validate_fixture()
