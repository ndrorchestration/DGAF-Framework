# PDMAL Current State — 2026-08-18

## Authoritative state

```text
Branch:                         epistemic/evidence-architecture-v1
Latest documentation commit:   b49a245110e19a99d3f4750496ae5817c9af617b
Previous verified head:        17a9e2e737f54046a1f1f93dbd70d287825fc6ee
Epistemic CI on 17a9e2e7:      PASS — run 32098754363
PDMAL pre-freeze CI on 17a9e2e7: PASS — run 32098754451
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

`pptl/orchestrator.py` references `TGLConfig` and `TurnContext`, while the verified TGL implementation exposes `TGLHooks` and `run_turn`. This repository interface mismatch is a pre-freeze blocker and must be resolved or explicitly bypassed by pinning the verified `run_turn` interface directly.

## Design decision

**Working path: Path A — deterministic numeric-to-TGL adapter.**

Candidate specification:

```text
 docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md
```

The adapter must:

1. canonicalize consensus state, topology, failure, and runtime context;
2. serialize that state deterministically;
3. invoke the exact pinned TGL `run_turn` interface;
4. convert only structured audit fields into a finite decision vocabulary;
5. apply a bounded deterministic numeric update operator;
6. record full provenance;
7. fail closed on interface, serialization, timeout, or decision-contract errors.

No free-form natural-language interpretation, hidden model call, or discretionary decision may occur in the experimental loop.

## Documentation / issue references

- Candidate adapter specification: `docs/experiment/PDMAL_TGL_ADAPTER_SPEC_v0.7.md`
- Current-state record: `docs/experiment/PDMAL_CURRENT_STATE_2026-08-18.md`
- Interface mismatch tracker: GitHub issue `#71`

## Remaining gates

```text
v0.7 panel approval                   PENDING
TGL interface mismatch resolution    OPEN
Adapter implementation               BLOCKED
2-seed contract validation            PENDING
Current-head CI after adapter         PENDING
Runtime characterization              PENDING
Artifact/custody verification         PENDING
Protocol freeze                       BLOCKED
Pilot authorization                   BLOCKED
```

## Evidence boundary

Current CI success proves the covered software gates execute in the tested environment. It does not establish PDMAL efficacy, superiority, convergence, robustness, causal attribution, or real-world benefit.

No pilot or final experimental seed may be generated while the protocol remains PRE-FREEZE and pilot authorization is absent.
