# PDMAL Current State — 2026-08-18

## Authoritative state snapshot

```text
Branch:                         epistemic/evidence-architecture-v1
Current documentation head:    fe325c8a5d083db02acf8284ddafcec68a6fedb5
Latest code correction:         ffde0b9a52d114649a5a0603d9499cecfcd3e7c6
Earlier CI dependency fix:      067f8706f4bd720e16fb4676cf6e2f75295dd3b8
Previous verified head:         17a9e2e737f54046a1f1f93dbd70d287825fc6ee
Epistemic CI on 17a9e2e7:      PASS — run 32098754363
PDMAL pre-freeze CI on 17a9e2e7: PASS — run 32098754451
Fresh adapter CI:               OBSERVED FAILURE DURING COLLECTION; latest corrected head pending
Protocol:                       PRE-FREEZE
Pilot authorization:            NOT GRANTED
Empirical data:                 0
```

## Runtime and interface findings

The repository does not expose the previously proposed numeric `dgaf.engine.run_governance_cycle` interface.

The verified governance primitive is:

```text
pptl.triadic_governance_loop.TriadicGovernanceLoop.run_turn(
    input_text: str,
    context: Optional[dict]
) -> TurnAuditRecord
```

The primitive is text/context-oriented and returns a sealed governance audit record rather than numeric consensus weights.

`pptl/orchestrator.py` remains an inconsistent legacy path: it references `TGLConfig` and `TurnContext`, while the current TGL implementation exposes `TGLHooks` and `run_turn`. The adapter does not depend on `IntegratedOrchestrator` and instead uses the current TGL API directly.

## Pre-freeze CI findings and corrections

### Dependency environment

The first observed blocker was `ModuleNotFoundError: pandas` during collection of `test_dgaf_tgl_adapter.py`.

Repository verification showed `pptl/requirements.txt` declares `pandas>=2.0.0`, while the PDMAL direct-pin manifest omits it by design. Commit `067f8706...` corrected the workflow to install both dependency manifests.

### PPTL import mismatch

After the dependency correction, collection progressed to a PPTL API mismatch: `orchestrator.py` attempted to import the non-existent `TGLConfig` from `triadic_governance_loop.py`.

Because the adapter does not use `IntegratedOrchestrator`, commit `ffde0b9a...` removed that unrelated orchestrator import/export from `pptl/__init__.py` rather than introducing compatibility classes or rewriting the adapter.

### Current validation boundary

The latest observed CI evidence in this sequence demonstrated the dependency issue was resolved sufficiently to expose the PPTL API mismatch. A fresh CI result for the corrected import boundary (`ffde0b9a...`) has not yet been observed through the connected workflow-run interface.

## Path A implementation

Candidate specification:

```text
 docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md
```

Implemented pre-freeze components:

```text
experiments/pdmal_pilot/dgaf_tgl_adapter.py
experiments/pdmal_pilot/test_dgaf_tgl_adapter.py
experiments/pdmal_pilot/task_engine.py (existing contract engine)
```

Implementation contract:

```text
ConsensusState
  -> canonical deterministic serialization
  -> TGL.run_turn()
  -> structured governance decision
  -> bounded numeric update or FAIL_CLOSED
```

Decision vocabulary:

```text
NO_CHANGE
CONSERVATIVE_MIX
ISOLATE_FAILED_NEIGHBORS
FAIL_CLOSED
```

No free-form natural-language interpretation, hidden model call, or discretionary decision occurs in the adapter.

## CI integration

`.github/workflows/pdmal-pre-freeze-runner.yml` includes `test_dgaf_tgl_adapter.py` in the pre-freeze contract suite.

Dependency-install sequence is now:

```text
experiments/pdmal_pilot/requirements-lock.txt
pptl/requirements.txt
```

A fresh run of the corrected current head is still required. The documentation commit `fe325c8...` contains documentation only and does not alter adapter, TGL, or workflow implementation behavior.

## Documentation / issue references

- Candidate adapter specification: `docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md`
- Adapter implementation note: `docs/experiment/PDMAL_TGL_ADAPTER_IMPLEMENTATION_NOTE.md`
- Current-state record: `docs/experiment/PDMAL_CURRENT_STATE_2026-08-18.md`
- CI evidence log: `docs/experiment/PDMAL_CI_EVIDENCE_LOG_2026-08-18.md`
- Documentation gap audit: `docs/experiment/DOCUMENTATION_GAP_AUDIT.md`
- Interface mismatch tracker: GitHub issue `#71`

## Remaining gates

```text
v0.7 panel approval                   PENDING
TGL interface mismatch resolution    BLOCKED until corrected import path is CI-verified
Adapter implementation               IMPLEMENTED / PRE-FREEZE
Adapter contract CI                  PENDING FRESH CURRENT-HEAD RESULT
Current-head CI                       PENDING
Runtime characterization              PENDING
Artifact/custody verification         PENDING
Protocol freeze                       BLOCKED
Pilot authorization                   BLOCKED
```

## Evidence boundary

Green CI evidence from `17a9e2e7` is historical for the earlier verified head. The later dependency and import-boundary corrections have not yet been validated by a fresh successful current-head run. No CI result in this sequence establishes PDMAL efficacy, superiority, convergence, robustness, causal attribution, or real-world benefit.

No pilot or final experimental seed may be generated while the protocol remains PRE-FREEZE and pilot authorization is absent.
