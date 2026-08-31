# Historical Seven-Gate Recovery Status — 2026-08-30

**Purpose:** Record the current evidence-qualified recovery boundary without changing the experimental apparatus.

**Status:** ANALYSIS / PROVENANCE RECONCILIATION ONLY  
**Experimental state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

## Recovery rule

A gate is **evidence-qualified** only when an authoritative historical contract/specification and, where available, a historically co-located implementation establish the semantic target. Evidence qualification does **not** authorize adaptation, wiring, candidate designation, freeze, or execution.

## Gate matrix

| Gate | Historical evidence | Current substrate | Current disposition |
|---|---|---|---|
| P-31 SCPE | v1.0 pattern + implementation co-located at `49854ea1e50d9e95e2338b690276635c0cbefb6f` | Missing token/tier/age/trust-edge substrate | EVIDENCE-QUALIFIED; RESTORE mapping |
| P-33 Convergence | v1.0 pattern + implementation co-located at `49854ea1e50d9e95e2338b690276635c0cbefb6f` | Missing weighted `W_t` / `W_{t-1}` substrate | EVIDENCE-QUALIFIED; RESTORE mapping |
| P-32 Phi Closure | Production v1.0 pattern at `49854ea1e50d9e95e2338b690276635c0cbefb6f`; historical implementation present in same ensemble | Current candidate lacks required phi trajectory/checkpoint substrate | EVIDENCE-QUALIFIED; RESTORE mapping |
| P-27 KAPPA | Historical v3.5 component card + router implementation at `66b79e2457bad9a2a26c5a2836f7cba52a6d57a6`; later v3.6 calibration history also exists | Current candidate lacks required KAPPA category/confidence/routing substrate | EVIDENCE-QUALIFIED for R5 mapping; exact semantic binding still required |
| P-29 Sentinel | Historical registration/integration evidence at `7a944cd759570c5427e85034029cbe43b2326e78`; implementation history exists | Current candidate does not expose the historical risk-review substrate required by the gate | HISTORICAL LEAD; exact contract extraction still required |
| P-30 Apogee | Historical P-30 gate creation at `d786731fc527140ea8895e3d0fffd3761142e1e8`; normative-constraint and attestation artifacts co-located | Current candidate does not expose the historical attestation substrate required by the gate | HISTORICAL LEAD; exact contract extraction still required |
| DemiJoule | Historical DemiJoule KB/spec/integration material exists, including `4f505b68e20f2c7c223e30840f428bb40f9ab417` | Current candidate lacks the six-axis safety payload identified by the recovery audit | HISTORICAL LEAD; exact gate contract extraction still required |

## Important correction

`docs/gates/GATE_SPECS.md` remains historical/legacy material and is not treated as current authority. Recovery is therefore based on earlier authoritative artifacts, versioned pattern cards, implementation commits, and explicit provenance chains rather than assuming the legacy gate catalog is current.

## Known strongest provenance anchors

- `49854ea1e50d9e95e2338b690276635c0cbefb6f`: historical ensemble plus P-31/P-32/P-33 pattern cards.
- `66b79e2457bad9a2a26c5a2836f7cba52a6d57a6`: KAPPA v3.5 component contract and implementation.
- `7a944cd759570c5427e85034029cbe43b2326e78`: Sentinel/P-29 integration wave.
- `d786731fc527140ea8895e3d0fffd3761142e1e8`: P-30 Apogee attestation gate wave.
- `4f505b68e20f2c7c223e30840f428bb40f9ab417`: DemiJoule canonicalized KB/spec/integration wave.

## Execution boundary

This document deliberately does **not**:

1. alter `ConsensusState`;
2. implement adapters;
3. designate a new candidate;
4. create a freeze;
5. dispatch P2/P6a/P3-P9;
6. authorize N=1.

The next apparatus-changing step is a **fresh candidate cycle** containing faithful RESTORE/adaptation work. Existing historical P2/P6a evidence cannot be transferred across that apparatus boundary.

## Anti-loop condition

Once a gate has an evidence-qualified historical source, repeat searches for the same source are unnecessary unless a materially new authoritative artifact is introduced. Work should advance to semantic state-delta mapping, preservation tests, or the explicit governed decision rather than re-running discovery scans.
