"""Issue #1399: reproducible *risk characterization*, not a blinding assurance test.

Only independently generated synthetic observations and disposable demonstration
keys are used. A passing test confirms the scope of *known linkability*, not
adequate confidentiality, independent validation, or empirical authorization.

Do not import protected blinding keys, inspect retained experimental artifacts,
dispatch an experiment, or turn these results into scientific N.
"""

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOPOLOGY_SOURCE = REPO / "experiments" / "pdmal_topology"
METADATA = ("seed", "failure_count", "failure_nodes")


@pytest.fixture(scope="module")
def source_known_cases():
    pytest.importorskip(
        "networkx",
        reason="Synthetic simulator needs independently pinned NetworkX; source-only CI is not a reconstruction test",
    )
    sys.path.insert(0, str(TOPOLOGY_SOURCE))
    try:
        from artifacts import blind_rows
        from experiment import run_structural_pilot
    finally:
        sys.path.remove(str(TOPOLOGY_SOURCE))

    named_reference = run_structural_pilot(5)
    publisher_rows = run_structural_pilot(5)
    assert named_reference == publisher_rows
    assert len(publisher_rows) == 225
    assert {row["topology"] for row in named_reference} == {
        "complete",
        "pdmal",
        "random_regular",
        "ring",
        "small_world",
    }
    synthetic_keys = ("synthetic-dummy-A-never-a-real-secret", "synthetic-dummy-B-never-a-real-secret")
    masked_sets = []
    for key in synthetic_keys:
        masked = blind_rows(publisher_rows, key)
        assert all(row["topology"].startswith("Topology_") for row in masked)
        assert all(
            masked_row[key] == named_row[key]
            for named_row, masked_row in zip(publisher_rows, masked)
            for key in named_row
            if key != "topology"
        )
        random.Random(1399).shuffle(masked)
        masked_sets.append(masked)
    metrics = tuple(sorted(set(named_reference[0]) - {"topology", *METADATA}))
    return named_reference, masked_sets, metrics


def _reidentify(reference, masked_rows, fields):
    """Source-aware matching; never use the dummy key or unmasked class labels."""

    def signature(row):
        return json.dumps([row.get(field) for field in fields], separators=(",", ":"))

    lookup = defaultdict(set)
    for row in reference:
        lookup[signature(row)].add(row["topology"])

    possible_by_pseudonym = defaultdict(list)
    unique_rows = 0
    for row in masked_rows:
        candidates = lookup.get(signature(row), set())
        unique_rows += len(candidates) == 1
        possible_by_pseudonym[row["topology"]].append(candidates)

    inferred = {}
    for pseudonym, candidates_by_row in possible_by_pseudonym.items():
        if not all(candidates_by_row):
            continue
        intersection = set.intersection(*candidates_by_row)
        if len(intersection) == 1:
            inferred[pseudonym] = next(iter(intersection))
    return unique_rows, inferred, sum(len(rows) for name, rows in possible_by_pseudonym.items() if name in inferred)


@pytest.mark.parametrize(
    ("fields_category", "expected_inferred", "expected_attributed"),
    [
        ("metadata_only", 0, 0),
        ("metadata_with_nodes", 0, 0),
        ("metrics_only", 4, 180),
        ("metadata_and_metrics", 5, 225),
        ("all_retained_fields", 5, 225),
    ],
)
def test_structural_topology_pseudonyms_are_source_linkable_under_documented_fields(
    source_known_cases, fields_category, expected_inferred, expected_attributed
):
    reference, masked_sets, metrics = source_known_cases
    dimensions = {
        "metadata_only": ("seed", "failure_count"),
        "metadata_with_nodes": METADATA,
        "metrics_only": metrics,
        "metadata_and_metrics": ("seed", "failure_count", *metrics),
        "all_retained_fields": tuple(sorted(set(reference[0]) - {"topology"})),
    }
    fields = dimensions[fields_category]
    for masked in masked_sets:
        _uniques, mapping, attributed = _reidentify(reference, masked, fields)
        assert len(mapping) == expected_inferred
        assert attributed == expected_attributed


def test_hmac_masking_works_as_label_substitution_but_not_identity_confidentiality(source_known_cases):
    reference, masked_sets, metrics = source_known_cases
    for masked in masked_sets:
        unique_rows, topology_map, attributed = _reidentify(reference, masked, ("seed", "failure_count", *metrics))
        assert unique_rows == 65
        assert set(topology_map.values()) == {row["topology"] for row in reference}
        assert attributed == 225
    assert {row["topology"] for row in masked_sets[0]} != {row["topology"] for row in masked_sets[1]}


def test_source_and_documentation_do_not_promote_blinding_or_scientific_status():
    """Always runnable, including CI environments without the simulation dependency."""
    import re

    workflow = (REPO / ".github" / "workflows" / "pdmal-instrumentation-dry-run.yml").read_text(encoding="utf-8")
    scope = (REPO / "docs" / "research" / "PDMAL_DRY_RUN_TOPOLOGY_LABEL_LINKABILITY_2026-10-19.md").read_text(
        encoding="utf-8"
    )
    assert "TOPOLOGY CONFIDENTIALITY NOT ESTABLISHED" in scope
    assert "A passed characterization test is affirmative evidence of a limitation" in scope
    governance_ci = (REPO / ".github" / "workflows" / "governance-ci.yml").read_text(encoding="utf-8")
    assert "python -m pytest -q tests/test_pdmal_structural_masking_linkability.py -ra" in governance_ci
    assert "networkx.__version__ == '3.6.1'" in governance_ci
    assert '"freeze_authorized": False' in workflow
    assert '"pilot_authorized": False' in workflow
    assert '"empirical_execution_requested": False' in workflow
    assert re.search(r'"id": "P4"[^\n]*"status": "OPEN"', workflow)
    assert re.search(r'"id": "P7"[^\n]*"status": "OPEN"', workflow)
    assert re.search(r'"id": "P9"[^\n]*"status": "NOT_EXECUTED"', workflow)
