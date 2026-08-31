# Historical Gate Recovery Source Index — 2026-08-30

| Gate | Primary historical source | Strength | Action |
|---|---|---|---|
| P-31 | `patterns/NDR_SCPE_v1.md` + `components/ensemble_v16.py` @ `49854ea1e50d9e95e2338b690276635c0cbefb6f` | Production v1.0 contract + same-commit implementation | RESTORE mapping |
| P-33 | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` + `components/ensemble_v16.py` @ `49854ea1e50d9e95e2338b690276635c0cbefb6f` | Production v1.0 contract + same-commit implementation | RESTORE mapping |
| P-32 | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` + `components/ensemble_v16.py` @ `49854ea1e50d9e95e2338b690276635c0cbefb6f` | Production v1.0 contract + same historical implementation family | RESTORE mapping |
| P-27 | `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` + `dynamic_weight_router.py` @ `66b79e2457bad9a2a26c5a2836f7cba52a6d57a6` | Versioned ACTIVE component contract + implementation + calibration | R5 semantic binding |
| P-29 | Historical Sentinel integration wave @ `7a944cd759570c5427e85034029cbe43b2326e78` | Implementation/integration evidence located; normative contract not yet isolated | Extract exact contract |
| P-30 | P-30 gate creation + normative-attestation wave @ `d786731fc527140ea8895e3d0fffd3761142e1e8` | Historical gate creation and attestation machinery located; acceptance contract not yet isolated | Extract exact contract |
| DemiJoule | DemiJoule KB/spec/integration wave @ `4f505b68e20f2c7c223e30840f428bb40f9ab417` | Historical role/spec/integration material; six-axis TGL contract not yet isolated | Extract exact contract |

## Provenance rule

A historical description, registry entry, agent profile, or integration note may identify a gate but does not by itself establish the gate's normative executable semantics. Promotion to evidence-qualified requires an explicit contract or a contract-plus-implementation evidence chain.

## Current boundary

No source in this index authorizes apparatus mutation by itself. The new candidate cycle begins only when the implementation work is actually performed and bound to a new exact candidate SHA.
