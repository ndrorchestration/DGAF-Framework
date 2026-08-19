# PDMAL / DGAF-TGL Adapter Implementation Note

## State

PRE-FREEZE / IMPLEMENTED / FRESH CURRENT-HEAD CI PENDING / PILOT NOT AUTHORIZED

## Implemented files

- `experiments/pdmal_pilot/dgaf_tgl_adapter.py`
- `experiments/pdmal_pilot/test_dgaf_tgl_adapter.py`
- `.github/workflows/pdmal-pre-freeze-runner.yml` updated to execute the adapter contract tests and install the PPTL dependency manifest.
- `pptl/__init__.py` import boundary corrected so the adapter can load the current TGL module without importing the inconsistent legacy orchestrator path.

## Runtime interface

The adapter directly imports the verified repository primitive:

```python
from pptl.triadic_governance_loop import TriadicGovernanceLoop

audit = tgl.run_turn(input_text, context=context)
```

The adapter deliberately does not use the nonexistent `dgaf.engine.run_governance_cycle` interface or the inconsistent `pptl.orchestrator.py` integration path.

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

## CI findings and corrective actions

### Dependency finding

The pre-freeze workflow initially failed during adapter-test collection because `pandas` was absent. The dependency is correctly declared in `pptl/requirements.txt`.

Commit `067f8706...` changed the workflow to install both:

```text
experiments/pdmal_pilot/requirements-lock.txt
pptl/requirements.txt
```

### Import-boundary finding

After the dependency correction, collection exposed a stale PPTL API import: `pptl/orchestrator.py` expects `TGLConfig` and `TurnContext`, while the current TGL exposes `TGLHooks` and `run_turn()`.

The adapter does not use `IntegratedOrchestrator`. Commit `ffde0b9a...` therefore removed `IntegratedOrchestrator` from `pptl/__init__.py` rather than modifying adapter logic, introducing compatibility shims, or rewriting the orchestrator.

## Current evidence boundary

A fresh CI run after the `ffde0b9a...` import-boundary correction has not yet been observed through the connected workflow-run interface.

The most recent observed failure in this sequence was the stale `TGLConfig` import; that observation is evidence of the failure boundary only and is not evidence of adapter functional correctness.

## Safety / governance

- Pilot mode remains fail-closed.
- No unblinding occurs.
- No 50-seed dataset is generated.
- Protocol remains PRE-FREEZE.
- Empirical data remains 0.

## Documentation references

- `docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md`
- `docs/experiment/PDMAL_CURRENT_STATE_2026-08-18.md`
- `docs/experiment/PDMAL_CI_EVIDENCE_LOG_2026-08-18.md`
- `docs/experiment/DOCUMENTATION_GAP_AUDIT.md`

## Next gate

Fresh CI on the current branch head, including `test_dgaf_tgl_adapter.py`, followed by full fail-closed contract verification and artifact/provenance inspection. Issue #71 remains open until the exact corrected current-head evidence is observed.
