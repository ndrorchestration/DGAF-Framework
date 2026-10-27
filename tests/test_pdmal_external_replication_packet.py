"""Guard the standalone non-author DDE input packet against inadvertent drift.

This validates input custody and structure only, not numerical DDE accuracy,
a topology advantage, an independent review, or the canonical PDMAL pilot.
"""

import copy
import hashlib
import json
import math
from pathlib import Path

import pytest

from tools.pdmal.jitcdde_reference_probe import (
    EXPECTED_FIXTURE_SHA256,
    fixture_manifest,
    fixture_sha256,
)

_INPUT_FILE = (
    Path(__file__).resolve().parents[1] / "docs" / "experiment" / "PDMAL_DDE_EXTERNAL_REPLICATION_FIXTURE_V1.json"
)


def _input_packet():
    return json.loads(_INPUT_FILE.read_text(encoding="utf-8"))


def _digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_external_packet_matches_frozen_source_fixture_bit_for_bit():
    packet = _input_packet()
    assert packet == fixture_manifest()
    assert _digest(packet) == EXPECTED_FIXTURE_SHA256
    assert fixture_sha256() == EXPECTED_FIXTURE_SHA256
    assert packet["schema"] == "pdmal-gr-jitcdde-fixture-v1"


def test_external_fixture_is_four_node_degree_normalized_graph_with_41_grid_times():
    packet = _input_packet()
    edges = {frozenset(edge) for edge in packet["graph"]}
    assert len(edges) == len(packet["graph"]) == 5
    degree = [sum(i in edge for edge in edges) for i in range(4)]
    assert degree == [3, 2, 3, 2]
    assert len(packet["initial_phases"]) == len(packet["frequencies"]) == 4
    assert math.isclose(packet["horizon_s"] / packet["sample_grid_s"], 40, abs_tol=1e-10)
    assert packet["history"] == "constant phase vector for all t <= 0"


def test_every_directed_delay_is_valid_ordered_receiver_sender_edge():
    packet = _input_packet()
    edges = {frozenset(edge) for edge in packet["graph"]}
    delays = {(i, j): tau for i, j, tau in packet["directed_physical_delays"]}
    assert len(delays) == len(packet["directed_physical_delays"]) == 5
    assert min(delays.values()) == pytest.approx(0.04)
    assert delays[(0, 1)] == pytest.approx(0.12)
    assert delays[(1, 0)] == pytest.approx(0.06)
    assert (1, 2) not in delays
    for i, j in delays:
        assert frozenset((i, j)) in edges


@pytest.mark.parametrize(
    "field,replacement",
    [
        ("initial_phases", [0.21, -0.8, 1.4, -0.4]),
        ("frequencies", [0.13, -0.17, 0.32, 0.08]),
        ("coupling", 1.11),
        ("graph", [[0, 1], [1, 2], [2, 3], [3, 0], [1, 3]]),
        ("sample_grid_s", 0.01),
        ("bootstrap_step_s", 0.0005),
    ],
)
def test_any_fixture_or_numerical_setting_change_requires_new_receipt_hash(field, replacement):
    packet = copy.deepcopy(_input_packet())
    packet[field] = replacement
    assert _digest(packet) != EXPECTED_FIXTURE_SHA256


def test_reversing_one_delay_orientation_fails_input_parity():
    packet = copy.deepcopy(_input_packet())
    packet["directed_physical_delays"][0] = [1, 0, 0.12]
    assert _digest(packet) != EXPECTED_FIXTURE_SHA256


def test_review_return_template_is_explicitly_unsubmitted_and_has_no_fabricated_results():
    path = _INPUT_FILE.with_name("PDMAL_DDE_NONAUTHOR_RETURN_TEMPLATE_V1.json")
    template = json.loads(path.read_text(encoding="utf-8"))
    assert template["submission_state"] == "NOT_SUBMITTED_TEMPLATE_ONLY"
    assert template["canonical_fixture_sha256"] == EXPECTED_FIXTURE_SHA256
    assert template["reviewer_id"] is None
    assert template["non_author_declaration"] is None
    assert template["physical_input_parity_confirmed"] is None
    assert template["conclusion"] is None
    assert template["observations"]["unwrapped_phases_rad"] is None
    assert template["observations"]["timestamps_s"] is None
    assert template["observations"]["missing_timepoints_s"] is None
    assert template["independent_validation"] == "NOT_ESTABLISHED"
    assert template["pilot_authorization"] == "NOT_GRANTED"
    assert template["scientific_n_increment"] == 0
    assert template["dgaf_v1_release"] == "HOLD"
