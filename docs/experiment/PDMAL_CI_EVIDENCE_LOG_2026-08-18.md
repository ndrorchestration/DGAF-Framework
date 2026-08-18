# PDMAL CI Evidence Log — 2026-08-18

## Purpose

Chronological record of pre-freeze CI findings and documentation-relevant corrections. This log records implementation/provenance evidence only. It does not establish PDMAL efficacy or authorize empirical execution.

## Evidence sequence

### 1. Dependency failure

**Observed failure:** `ModuleNotFoundError: No module named 'pandas'` during collection of `test_dgaf_tgl_adapter.py`.

**Import chain:**

```text
experiments/pdmal_pilot/test_dgaf_tgl_adapter.py
  -> dgaf_tgl_adapter.py
  -> pptl.triadic_governance_loop
  -> pptl/__init__.py
  -> pptl.herald_agent
  -> import pandas
```

**Repository verification:** `pptl/requirements.txt` declares `pandas>=2.0.0`.

**Root cause:** the pre-freeze workflow installed only `experiments/pdmal_pilot/requirements-lock.txt`, which is a direct-pin manifest and did not include the PPTL dependency manifest.

**Correction:** commit `067f8706f4bd720e16fb4676cf6e2f75295dd3b8` updated `.github/workflows/pdmal-pre-freeze-runner.yml` to install both dependency manifests.

### 2. PPTL API mismatch

**Observed after dependency correction:** `ImportError: cannot import name 'TGLConfig' from 'pptl.triadic_governance_loop'` during collection.

**Repository verification:**

- `triadic_governance_loop.py` exposes `TGLHooks` and `TriadicGovernanceLoop.run_turn()`.
- `orchestrator.py` imports and instantiates the non-existent `TGLConfig` and `TurnContext`, and expects a `run()` API.

**Root cause:** stale/inconsistent `orchestrator.py` API path.

**Adapter relevance:** the adapter directly imports `TriadicGovernanceLoop`, `TGLHooks`, and related current TGL types and does not use `IntegratedOrchestrator`.

### 3. Import-boundary correction

**Correction:** commit `ffde0b9a52d114649a5a0603d9499cecfcd3e7c6` removed `IntegratedOrchestrator` from `pptl/__init__.py` and its `__all__` export list.

**Intent:** prevent unrelated stale orchestrator imports from executing when the adapter imports `pptl.triadic_governance_loop`.

**Scope:** no adapter logic and no orchestrator logic changed.

## Current verification boundary

The correction at `ffde0b9a...` has not yet received a fresh observed CI result through the connected workflow-run interface.

Therefore:

- adapter functional execution remains unverified;
- Issue #71 remains open;
- protocol remains PRE-FREEZE;
- pilot authorization remains absent;
- empirical data remains 0.

## Evidence classification

```text
DEFINED             configuration/specification
IMPLEMENTED         dependency and import-boundary corrections committed
TESTED              prior local/CI observations as specifically recorded
VERIFIED            only when exact current-head CI evidence is observed
EMPIRICALLY SUPPORTED  not established
```

## Next evidence gate

Observe a fresh pre-freeze workflow run from the branch containing `ffde0b9a...`. Verify the checkout SHA, dependency-install step, four-test suite, `test_dgaf_tgl_adapter.py`, fail-closed checks, and artifact/provenance output before advancing any gate.
