from experiment import FAILURE_COUNTS, run_structural_pilot


def test_pilot_row_count_and_factor_grid():
    rows = run_structural_pilot(2)
    assert len(rows) == 2 * 5 * len(FAILURE_COUNTS)
    assert {r["topology"] for r in rows} == {
        "ring", "pdmal", "random_regular", "small_world", "complete"
    }
    assert {r["failure_count"] for r in rows} == set(FAILURE_COUNTS)


def test_paired_seed_uses_same_failure_nodes_across_topologies():
    rows = run_structural_pilot(1)
    for failure_count in FAILURE_COUNTS:
        selected = [r["failure_nodes"] for r in rows if r["failure_count"] == failure_count]
        assert len({tuple(x) for x in selected}) == 1


def test_pilot_does_not_emit_inferential_claims():
    rows = run_structural_pilot(1)
    assert rows
    assert not any("p_value" in row or "effect_size" in row for row in rows)
