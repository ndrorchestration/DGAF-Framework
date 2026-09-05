# P8 / P9 / Freeze Readiness — Reconciled 2026-09-05

## Current control status

- Experimental state: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED`
- Designated runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`
- Candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- P1: `CLOSED / VERIFIED`
- P2: `CLOSED / VERIFIED`
- P3: `CLOSED / VERIFIED`
- P4: `OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED`
- P5: `CLOSED / VERIFIED`
- P6: `CLOSED / VERIFIED`
- P6a: `CLOSED / VERIFIED`
- P7: `ADOPTED / FINAL BINDING OPEN`
- P8: `OPEN / FAIL-CLOSED`
- P9: `NOT EXECUTED / OPEN` for the final frozen chain
- Freeze: `NOT ESTABLISHED`
- Pilot authorization: `NOT GRANTED`
- Empirical N: `0`

This is a readiness/control artifact. It does not create a freeze, authorize execution, or promote synthetic/engineering evidence into efficacy evidence.

## Closed pre-freeze inputs

| Predicate | State | Evidence boundary |
|---|---|---|
| P1 candidate integrity | CLOSED / VERIFIED | exact apparatus/source, candidate/tree, provenance, candidate deployment identity |
| P2 runtime | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704`; five-case authenticated matrix |
| P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; artifacts `9961526468` / `9961526662`; exact-candidate structural/contract evidence |
| P5 provenance/reproducibility | CLOSED / VERIFIED | analysis blob `a269ed22…`; config `6cab3f1e…`; runner `b5152fa3…`; schema `c620d375…`; deterministic/environment/RNG/topology evidence |
| P6 durable custody | CLOSED / VERIFIED | independent archive → retrieval → SHA-256 equality for retained evidence set |
| P6a CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299`; four-case authenticated matrix |

These closures do not imply P4, P7, P8, P9, freeze, authorization, or empirical efficacy.

## First unresolved prerequisite — P4

P4 is the first substantive blocker and is operational rather than repository-synthetic.

The repository already contains:

- `docs/governance/P4_HUMAN_KEY_CUSTODY_PROCEDURE.md`;
- `docs/governance/P4_HUMAN_CUSTODY_EXECUTION_RECORD_2026-09-05.md`;
- Issue #255 as the operational checkpoint.

Still required:

1. a genuinely distinct human Key Custodian;
2. a distinct execution/analysis principal;
3. real nonce-hardened key/mapping commitments generated outside repository-visible state;
4. attributable custody and no-access attestations;
5. independent review of role/access separation without disclosure of secret material.

Until those events exist, P4 remains OPEN and no repository-side automation may substitute invented principals or attestations.

## P7 readiness

The P7 binding draft already fixes the scientific and technical identities that can legitimately be known before P4:

- candidate/tree and candidate deployment;
- protocol `0.7.5`;
- `dgaf` versus `null` primary contrast;
- FFCR endpoint and paired-root-seed estimand;
- 10,000 paired percentile bootstrap resamples, seed `20260823`, two-sided 95% interval;
- exact analysis/configuration/runner/schema identities;
- P2/P3/P5/P6/P6a evidence identities.

P7 remains open because actual P4 custody evidence and final freeze-specific protocol/control-plane identities are not yet available.

## P8 readiness

The analysis implementation/configuration is already bound through P5. P8 is therefore no longer blocked on selecting or reproducing the primary analysis; it is blocked on constructing an immutable freeze from a fully closed P7 tuple.

After P4 and P7 close, P8 must:

1. select the exact final protocol blob/commit identity;
2. select the exact final accepted control-plane commit;
3. create an immutable freeze manifest containing the complete exact tuple;
4. compute/retain the freeze-manifest digest;
5. independently retrieve/recompute the freeze representation;
6. verify all bound identities/digests and retain the independent freeze-verification record.

Until then: **P8 OPEN / FAIL-CLOSED; Freeze NOT ESTABLISHED.**

## P9 readiness

Historical P9 work demonstrated scoped independent-verification mechanisms on superseded candidates. Those records remain provenance only.

The final P9 has not been executed. It must occur after the immutable P8 freeze exists and must independently verify the complete final chain, including:

- freeze manifest identity/digest;
- candidate/tree/deployment identity;
- final protocol/control-plane identities;
- analysis/configuration/runner/schema identities;
- P1/P2/P3/P4/P5/P6/P6a evidence bindings;
- custody commitments/attestations without secret disclosure;
- absence of unauthorized empirical execution before authorization.

The final P9 verifier identity and final P9 artifact/digest must be recorded as new evidence. Historical scoped P9 artifacts cannot be relabeled as final-chain verification.

## Exact remaining sequence

`real P4 custody → P7 final exact binding → P8 immutable freeze → independent freeze verification → final P9 → separate explicit pilot authorization → blinded empirical execution`

No later step may be inferred from completion of an earlier one.

## Current hard boundary

**Freeze: NOT ESTABLISHED · Pilot authorization: NOT GRANTED · Unblinding: NOT EXECUTED · Empirical N: 0.**
