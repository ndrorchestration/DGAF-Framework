# AOSS v0.6 Stage A — Comparator Input Derivation Gap

**Controller:** #810  
**Status:** BLOCKED / FAIL-CLOSED / PRE-DATA  
**Outcome collection:** NOT AUTHORIZED

The Stage-A comparator decision rule is frozen, but the three coarse comparator inputs `(O,M,R)` are not yet machine-derivable from the exact ACP telemetry by an accepted contract.

What is established:

- comparator version: `AOSS_V0_5_OMR_FROZEN`;
- decision rule: missing coarse state → `HOLD`; `O=0 ∧ R=0` → `STOP`; otherwise → `CONTINUE`;
- historical controlled AOSS evidence documents a reference projection `(3,1,1.0)`.

What is not established:

- authoritative semantic definitions for each coarse dimension sufficient to construct a new ACP mapping;
- exact ACP source-field → `O`, `M`, and `R` extraction functions;
- units and tolerances for those three comparator inputs.

The historical reference projection is evidence about a prior controlled fixture, not an extraction rule. Dimension meanings must not be guessed from the letters or reconstructed after viewing Stage-A outcomes.

Resolution is fail-closed: either locate and bind an independently identifiable authoritative derivation, or prospectively define, review, test, and freeze a new v0.6 ACP→OMR derivation before any Stage-A outcomes are collected.

Machine-readable gap record:

- `registry/aoss_v0_6_stage_a_comparator_input_derivation_gap_v1.json`
