# PDMAL Current State — 2026-08-18

## Authoritative state snapshot

```text
Branch:                         epistemic/evidence-architecture-v1
Current implementation head:   273135e2898563f446d1a0751984afdda4d18111
Previous verified head:        17a9e2e737f54046a1f1f93dbd70d287825fc6ee
Epistemic CI on 17a9e2e7:      PASS — run 32098754363
PDMAL pre-freeze CI on 17a9e2e7: PASS — run 32098754451
Current-head CI on adapter:    PENDING
Protocol:                      PRE-FREEZE
Pilot authorization:           NOT GRANTED
Empirical data:                0
```

## Runtime finding

The repository does not expose the previously proposed numeric `dgaf.engine.run_governance_cycle` interface.

The verified governance primitive at `8677ea0` is:

```text
pptl.triadic_governance_loop.TriadicGovernanceLoop.run_turn(
    input_text: str,
    context: Optional[dict]
) -> TurnAuditRecord
```

The primitive is text/context-oriented and returns a sealed governance audit record rather than numeric consensus weights.

`pptl/orchestrator.py` references `TGLConfig` and `TurnContext`, while the verified TGL implementation exposes `TGLHooks` and `run_turn`. This repository interface mismatch remains tracked by Issue #71. The adapter deliberately pins the verified `run_turn` interface directly and does not depend on the inconsistent orchestrator path.

## Path A implementation

Candidate specification:

```text
 docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md
```

Implemented pre-freeze components:

```text
experiments/pdmal_pilot/dgaf_tgl_adapter.py
experiments/pdmal_pilot/test_dgaf_tgl_adapter.py
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

`.github/workflows/pdmal-pre-freeze-runner.yml` now includes `test_dgaf_tgl_adapter.py` in the pre-freeze contract suite.

The latest adapter implementation has not yet received a fresh CI run. GitHub returned no workflow runs for the latest documentation/implementation head when checked.

## Documentation / issue references

- Candidate adapter specification: `docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md`
- Adapter implementation note: `docs/experiment/PDMAL_TGL_ADAPTER_IMPLEMENTATION_NOTE.md`
- Current-state record: `docs/experiment/PDMAL_CURRENT_STATE_2026-08-18.md`
- Interface mismatch tracker: GitHub issue `#71`

## Remaining gates

```text
v0.7 panel approval                   PENDING
TGL interface mismatch resolution    OPEN / tracked by #71
Adapter implementation               IMPLEMENTED / PRE-FREEZE
Adapter contract CI                  PENDING
Current-head CI                       PENDING
Runtime characterization              PENDING
Artifact/custody verification         PENDING
Protocol freeze                       BLOCKED
Pilot authorization                   BLOCKED
```

## Evidence boundary

Current green CI evidence applies to the earlier verified head `17a9e2e7`. It does not verify the new adapter or establish PDMAL efficacy, superiority, convergence, robustness, causal attribution, or real-world benefit.

No pilot or final experimental seed may be generated while the protocol remains PRE-FREEZE and pilot authorization is absent.
