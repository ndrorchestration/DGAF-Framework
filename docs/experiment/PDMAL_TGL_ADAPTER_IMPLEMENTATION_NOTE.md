# PDMAL / DGAF-TGL Adapter Implementation Note

## State

**PRE-FREEZE / IMPLEMENTED / CURRENT-HEAD CI PENDING / PILOT NOT AUTHORIZED**

## Implemented files

- `experiments/pdmal_pilot/dgaf_tgl_adapter.py`
- `experiments/pdmal_pilot/test_dgaf_tgl_adapter.py`
- `.github/workflows/pdmal-pre-freeze-runner.yml` updated to execute the adapter contract tests.

## Runtime interface

The adapter directly imports the verified repository primitive:

```python
from pptl.triadic_governance_loop import TriadicGovernanceLoop

audit = tgl.run_turn(input_text, context=context)
```

The adapter deliberately does not use the nonexistent `dgaf.engine.run_governance_cycle` interface or the currently inconsistent `pptl.orchestrator.py` integration path.

## Contract boundary

The adapter is deterministic and finite-state at the governance boundary:

```text
ConsensusState
  -> canonical deterministic serialization
  -> TGL run_turn()
  -> structured TurnStatus / P-33 gate result
  -> one of four decisions
  -> bounded numeric update or fail-closed
```

Decision vocabulary:

```text
NO_CHANGE
CONSERVATIVE_MIX
ISOLATE_FAILED_NEIGHBORS
FAIL_CLOSED
```

No free-form prompt interpretation or model-generated decision is used.

## Current evidence boundary

The adapter has been committed but has not yet been verified by CI. The last authoritative green current-head evidence remains commit `17a9e2e7` with runs `32098754363` and `32098754451`.

Fresh CI is required for the new adapter implementation before the implementation gate can be reopened.

## Safety / governance

- Pilot mode remains fail-closed.
- No unblinding occurs.
- No 50-seed dataset is generated.
- Protocol remains PRE-FREEZE.
- Empirical data remains 0.

## Next gate

Fresh CI on the current head, including `test_dgaf_tgl_adapter.py`, followed by expert-panel evidence review. The TGL interface mismatch remains tracked in Issue #71; direct use of the verified `run_turn` interface is the selected resolution path for the adapter.
