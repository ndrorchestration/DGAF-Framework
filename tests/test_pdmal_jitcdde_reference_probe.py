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


def test_runtime_fixture_digest_must_match_frozen_identity(monkeypatch):
    assert probe.fixture_sha256() == probe.EXPECTED_FIXTURE_SHA256
    monkeypatch.setattr(probe, "COUPLING", 1.2)
    assert probe.fixture_sha256() != probe.EXPECTED_FIXTURE_SHA256
    with pytest.raises(ValueError, match="fixture identity changed"):
        probe.validate_fixture()


@pytest.mark.parametrize(
    "field,invalid",
    [
        ("GRID", 0.0),
        ("GRID", float("nan")),
        ("HORIZON", float("inf")),
        ("COUPLING", False),
        ("COUPLING", -1.0),
        ("FIXED_BOOTSTRAP_STEP", 0.0),
        ("FIXED_BOOTSTRAP_STEP", float("nan")),
        ("ADAPTIVE_MAX_STEP", 0.0),
        ("ADAPTIVE_MAX_STEP", float("inf")),
    ],
)
def test_runtime_fixture_rejects_nonfinite_or_out_of_range_scalars(monkeypatch, field, invalid):
    monkeypatch.setattr(probe, field, invalid)
    with pytest.raises(ValueError):
        probe.validate_fixture()


def test_mock_sampling_preserves_all_early_times_and_adaptive_handoff():
    """Mock only: validates time requests, never claims DDE solver correctness."""

    class FakeSolver:
        def __init__(self):
            self.calls = []

        def integrate_blindly(self, time, step):
            self.calls.append(("blind", time, step))
            return probe.INITIAL

        def integrate(self, time):
            self.calls.append(("adaptive", time, None))
            return probe.INITIAL

    fake = FakeSolver()
    trace = probe.collect_reference_trajectory(fake, probe.validate_fixture())
    assert len(trace) == 41
    assert all(state == probe.INITIAL for state in trace)
    assert len(fake.calls) == 40
    assert fake.calls[0] == ("blind", 0.02, 0.001)
    assert fake.calls[5] == ("blind", 0.12, 0.001)
    assert fake.calls[6] == ("adaptive", 0.14, None)
    assert fake.calls[-1] == ("adaptive", 0.8, None)
    assert [call[1] for call in fake.calls] == [round(i * 0.02, 12) for i in range(1, 41)]


@pytest.mark.parametrize("bad_state", [(0.0,), (0.0, 0.0, float("nan"), 0.0)])
def test_mock_solver_malformed_output_fails_closed(bad_state):
    """Mock only: reject bad external outputs before writing JSON receipts."""

    class FakeSolver:
        def integrate_blindly(self, time, step):
            return bad_state

        def integrate(self, time):
            return bad_state

    with pytest.raises(ArithmeticError):
        probe.collect_reference_trajectory(FakeSolver(), 1)


def test_mock_sampler_rejects_bad_sample_count():
    with pytest.raises(ValueError):
        probe.collect_reference_trajectory(object(), True)
    with pytest.raises(ValueError):
        probe.collect_reference_trajectory(object(), 0)
