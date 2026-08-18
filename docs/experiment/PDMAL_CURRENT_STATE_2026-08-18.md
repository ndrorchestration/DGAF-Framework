# PDMAL Current State — 2026-08-18

## Authoritative state snapshot

```text
Branch:                         epistemic/evidence-architecture-v1
Current implementation head:   f9cab0d0585c0f33ce42cfe9313e3133969f88e4
Previous verified head:        17a9e2e737f54046a1f1f93dbd70d287825fc6ee
Epistemic CI on 17a9e2e7:      PASS — run 32098754363
PDMAL pre-freeze CI on 17a9e2e7: PASS — run 32098754451
Current-head CI:               PENDING
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

`pptl/orchestrator.py` references `TGLConfig` and `TurnContext`, while the verified TGL implementation exposes `TGLHooks` and `run_turn`. This repository interface mismatch remains a pre-freeze integration concern and is tracked by Issue #71. The new adapter deliberately imports the verified `run_turn` interface directly rather than relying on the inconsistent orchestrator path.

## Design decision

**Working path: Path A — deterministic numeric-to-TGL adapter.**

Candidate specification:

```text
 docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md
```

Implemented pre-freeze component:

```text
experiments/pdmal_pilot/dgaf_tgl_adapter.py
experiments/pdmal_pilot/test_dgaf_tgl_adapter.py
```

The adapter:

1. canonicalizes consensus state, topology, failure, and runtime context;
2. serializes that state deterministically;
3. invokes the exact pinned TGL `run_turn` interface;
4. converts only structured audit fields into a finite decision vocabulary;
5. applies a bounded deterministic numeric update operator;
6. records input/audit hashes through the adapter result;
7. fails closed on interface, serialization, timeout, or decision-contract errors.

No free-form natural-language interpretation, hidden model call, or discretionary decision occurs in the adapter. The canonical text representation is deterministic machine-readable input, not a natural-language prompt.

## CI integration

`.github/workflows/pdmal-pre-freeze-runner.yml` now includes `test_dgaf_tgl_adapter.py` in the pre-freeze contract suite.

The current head therefore requires a fresh CI run before any implementation-gate advancement.

## Documentation / issue references

- Candidate adapter specification: `docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md`
- Current-state record: `docs/experiment/PDMAL_CURRENT_STATE_2026-08-18.md`
- Interface mismatch tracker: GitHub issue `#71`

## Remaining gates

```text
v0.7 panel approval                   PENDING
TGL interface mismatch resolution    OPEN / tracked by #71
Adapter implementation               IMPLEMENTED / PRE-FREEZE
2-seed contract validation            PENDING
Current-head CI                       PENDING
Runtime characterization              PENDING
Artifact/custody verification         PENDING
Protocol freeze                       BLOCKED
Pilot authorization                   BLOCKED
```

## Evidence boundary

Current CI success on `17a9e2e7` proves the previously covered software gates execute in the tested environment. It does not verify the new adapter or establish PDMAL efficacy, superiority, convergence, robustness, causal attribution, or real-world benefit.

No pilot or final experimental seed may be generated while the protocol remains PRE-FREEZE and pilot authorization is absent.
