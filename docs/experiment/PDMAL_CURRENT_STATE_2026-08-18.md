# PDMAL Current State — 2026-08-18

## Authoritative state snapshot

```text
Branch:                         epistemic/evidence-architecture-v1
Latest adapter CI run:          32102382285 (#42)
Verified checkout SHA:          ffde0b9a52d114649a5a0603d9499cecfcd3e7c6
Adapter CI conclusion:          SUCCESS
Contract suite:                 30 passed
Adapter test:                   PASS
Contract mode:                  PASS — 2 validation seeds; no empirical collection
Pilot fail-closed check:        PASS — pilot rejected while freeze/authorization absent
Artifact:                       9312000148
Artifact SHA-256:               2af2a89124b699be2175f767552a1f58fb32864268b4e4c5d98dc9124a6b3184
Latest documentation update:    9711543
Protocol:                       PRE-FREEZE
Pilot authorization:            NOT GRANTED
Empirical data:                 0
```

## Runtime and interface findings

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

Repository verification showed `pptl/requirements.txt` declares `pandas>=2.0.0`, while the PDMAL direct-pin manifest omits transitive dependencies by design. Commit `067f8706...` corrected the workflow to install both dependency manifests.

### PPTL import mismatch

After the dependency correction, collection progressed to a PPTL API mismatch: `orchestrator.py` attempted to import the non-existent `TGLConfig` from `triadic_governance_loop.py`.

Because the adapter does not use `IntegratedOrchestrator`, commit `ffde0b9a...` removed that unrelated orchestrator import/export from `pptl/__init__.py` rather than introducing compatibility classes or rewriting the adapter.

### Current validation result

The corrected import boundary was subsequently verified on the exact `ffde0b9a...` checkout by pre-freeze workflow run `32102382285` / `#42`. The run checked out `ffde0b9a...` directly, installed `pptl/requirements.txt` including `pandas-3.0.5`, and completed the four-test contract suite with `30 passed`.

## Path A implementation

Candidate specification:

```text
 docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md
```

Implemented pre-freeze components:

```text
experiments/pdmal_pilot/dgaf_tgl_adapter.py
experiments/pdmal_pilot/test_dgaf_tgl_adapter.py
experiments/pdmal_pilot/task_engine.py (contract engine)
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

Verified run `32102382285` demonstrates that this installation path is functional on the corrected source.

## Freeze-control assessment

The adapter/CI control is closed, but protocol freeze remains blocked by independent controls:

| Control | Current state |
|---|---|
| Adapter contract CI | VERIFIED — run 32102382285 |
| Direct dependency pins | VERIFIED |
| Full resolver/hash lock | NOT GENERATED; requires network-enabled trusted environment |
| Timeout/retry/runtime values | IMPLEMENTED as 60s / 3 attempts / 30s recovery / 300s seed ceiling; dedicated characterization still required |
| Sample-size implementation | IMPLEMENTED to the protocol's paired-difference normal-approximation formula; dedicated verification evidence still required |
| Artifact schema/retention | PARTIALLY IMPLEMENTED; exact schema/retention verification still required |
| Blinding custody/separation | NOT YET OPERATIONALLY VERIFIED |
| Topology implementation SHAs/graph fingerprints | NOT YET FULLY RECORDED/VERIFIED |
| Exact execution environment | NOT FULLY PINNED |
| Protocol internal-consistency audit | PENDING |
| Protocol freeze | BLOCKED |
| Pilot authorization | BLOCKED |

## Experimental task boundary

The verified DGAF/TGL governance adapter is not the experimental workload itself. `task_engine.py` defines protocol mechanics and a `TaskAdapter` interface, but explicitly does not define a real empirical workload. The actual experimental task adapter remains unimplemented and is therefore a material pre-freeze boundary.

## Evidence boundary

The successful pre-freeze CI run demonstrates implementation/runner-contract behavior under the tested environment. It does not establish PDMAL efficacy, superiority, convergence, robustness, causal attribution, or real-world benefit.

Contract-mode execution generated no empirical observations. Pilot execution remains fail-closed until protocol freeze and explicit authorization.

No pilot or final experimental seed may be generated while the protocol remains PRE-FREEZE and pilot authorization is absent.
