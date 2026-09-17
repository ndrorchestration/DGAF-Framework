from __future__ import annotations

import pytest

from components.ahg_sidecar import AgentHeartbeat, TurnBuffer


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize(
    "field_name",
    [
        "D_e_signal",
        "D_explore_signal",
        "D_correct_signal",
        "novelty_signal",
        "coherence_signal",
    ],
)
def test_turn_buffer_rejects_nonfinite_heartbeat_signals(field_name: str, value: float) -> None:
    heartbeat = AgentHeartbeat(agent_id="agent-1", turn_id=1)
    setattr(heartbeat, field_name, value)
    buffer = TurnBuffer(turn_id=1, heartbeats=[heartbeat])

    with pytest.raises(ValueError, match="non-finite heartbeat signal"):
        buffer.to_state_vector()
