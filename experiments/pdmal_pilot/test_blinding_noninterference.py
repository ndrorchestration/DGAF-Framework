"""Non-empirical blinding noninterference regressions for PDMAL v0.7.6."""
from __future__ import annotations

from run_pilot import _trial_combinations, blinded_trial_schedule
from task_engine import ConsensusTask


def _execute(schedule: list[tuple[str, str, int]], *, seed: int) -> dict[tuple[str, str, int], tuple]:
    outputs: dict[tuple[str, str, int], tuple] = {}
    for topology, condition, failure_count in schedule:
        result = ConsensusTask(
            topology=topology,
            failure_count=failure_count,
            condition=condition,
        ).run_detailed(seed=seed, attempt=1)
        key = (topology, condition, failure_count)
        outputs[key] = (
            result.attempt_status.value,
            result.failure_nodes,
            result.initial_values,
            result.final_values,
            result.final_std,
            result.topology_fingerprint,
            result.iterations_completed,
            result.consensus_success,
            result.deviation,
        )
    return outputs


def test_keyed_order_preserves_all_180_cell_results_for_fixed_seed() -> None:
    """Changing execution order must not change the scientific cell results."""
    seed = 20260817
    canonical = _trial_combinations()
    protected = blinded_trial_schedule(
        seed=seed,
        key="fixed-order-invariance-test-key-0000000000000000",
    )

    assert protected != canonical
    assert set(protected) == set(canonical)
    assert len(protected) == len(canonical) == 180

    canonical_outputs = _execute(canonical, seed=seed)
    protected_outputs = _execute(protected, seed=seed)

    assert protected_outputs == canonical_outputs
