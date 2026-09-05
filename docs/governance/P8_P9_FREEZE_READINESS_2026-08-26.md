# P8 / P9 / Freeze Readiness — Reconciled 2026-09-05

## Current control status

- Experimental state: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED`
- Designated runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`
- Candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- P1: `CLOSED / VERIFIED`
- P2: `CLOSED / VERIFIED`
- P3: `CLOSED / VERIFIED`
- P4: `OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED`
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

## First unresolved prerequisite — P4-A independently enforceable custody

P4-A is the first substantive blocker. The canonical surfaces are:

- `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`
- active execution record: `docs/governance/P4_INDEPENDENT_CUSTODY_EXECUTION_RECORD_2026-09-05.md`
- completed governance architecture correction: Issue #285 / PR #286 / merge `a3bafa6f…`
- active zero-human Mode-T design/threat-model lane: Issue #287 — design only, not accepted custody evidence

The governing invariant is effective control separation: before the predeclared release condition, the execution/analysis principal must be unable to obtain the raw blinding key, cleartext mapping, commitment nonces, or functionally equivalent recovery material by unilateral ordinary, administrative, recovery, backup, policy-edit, credential-reset, export, or break-glass action.

Exactly one real custody mode must be instantiated:

1. **Mode H — distinct-human custody.** A genuinely distinct human Key Custodian remains a valid path.
2. **Mode I — institutional/third-party custody.** An external organization/service controls custody and release outside the analyst's unilateral administration or recovery.
3. **Mode T — independently enforced technical custody.** A cryptographic/HSM/KMS/threshold/equivalent mechanism is acceptable only if the analyst lacks every effective owner/admin/recovery/export/break-glass path capable of defeating the blind.

Still required for every mode under the current canonical lifecycle:

1. a selected custody mode and unique custody-instance identity;
2. an attributable execution/analysis principal and custody authority/system identity;
3. real nonce-hardened key/mapping commitments generated before empirical execution;
4. a predeclared release rule;
5. a complete non-secret inventory of ordinary/admin/recovery/backup/export/break-glass paths;
6. evidence that the execution/analysis principal cannot use any inventoried path alone to recover protected material before release;
7. independent review evidence appropriate to the selected custody mode.

### Mode-T lifecycle caveat

No solo Mode-T implementation is currently accepted. Issue #287 explores a possible transient-runner/timelock lifecycle in which the real mapping would be generated only inside a separately authorized empirical environment. That proposal may require a future mode-specific P4/P7/P8/P9 lifecycle revision because the current canonical procedure expects real key/mapping commitments to exist before freeze.

Until a future revision is independently reviewed, merged, and verified, the current pre-freeze predicates remain controlling. GitHub-hosted runners, drand/timelock tooling, HSM/KMS products, or any other candidate mechanism do not become P4 evidence merely because they are technically plausible.

AI agents/personas, aliases, same-operator accounts, ordinary repository secrets, analyst-recoverable password vaults, analyst-administered KMS/HSM arrangements, and preregistration alone do not satisfy P4-A.

Until one mode is actually instantiated and verified, P4 remains OPEN. Repository-side documentation or automation may not substitute invented independence evidence.

## P7 readiness

The P7 binding draft already fixes the scientific and technical identities known before P4-A:

- candidate/tree and candidate deployment;
- protocol `0.7.5`;
- `dgaf` versus `null` primary contrast;
- FFCR endpoint and paired-root-seed estimand;
- 10,000 paired percentile bootstrap resamples, seed `20260823`, two-sided 95% interval;
- exact analysis/configuration/runner/schema identities;
- P2/P3/P5/P6/P6a evidence identities.

P7 remains open because actual P4-A custody evidence and final pre-freeze protocol/control-plane/verifier identities are not yet available.

## P8 readiness

The analysis implementation/configuration is already bound through P5. P8 is blocked on constructing immutable freeze object F from a fully closed P7 tuple.

After P4-A and P7 close, P8 must:

1. bind the exact final protocol blob/content identity;
2. bind the exact accepted pre-freeze control-plane commit;
3. create immutable freeze object F containing the complete exact tuple;
4. retain the byte-level digest of F externally;
5. independently retrieve and re-hash F;
6. create separate descendant verification record V without modifying F;
7. retain V's byte digest externally.

Until then: **P8 OPEN / FAIL-CLOSED; Freeze NOT ESTABLISHED.**

## P9 readiness

Historical P9 work demonstrated scoped independent-verification mechanisms on superseded candidates. Those records remain provenance only.

The final P9 has not been executed. It must occur after immutable F and independent verification record V exist and must independently verify the complete final chain, including:

- F and V identities/digests;
- candidate/tree/deployment identity;
- final protocol/control-plane identities;
- analysis/configuration/runner/schema identities;
- P1/P2/P3/P4/P5/P6/P6a evidence bindings;
- selected P4 custody-mode/instance, commitments, no-unilateral-access evidence, and independent-review evidence without secret disclosure;
- absence of unauthorized empirical execution before authorization;
- P9 verifier script/workflow non-drift between F and V.

Historical scoped P9 artifacts cannot be relabeled as final-chain verification.

## Exact remaining sequence

`real independently enforceable P4-A custody → P7 final exact binding → immutable freeze F → independent P8 verification record V → final P9 → separate explicit pilot authorization → blinded empirical execution`

No later step may be inferred from completion of an earlier one.

## Current hard boundary

**P4-A: OPEN / NOT EXECUTED · Freeze: NOT ESTABLISHED · Pilot authorization: NOT GRANTED · Unblinding: NOT EXECUTED · Empirical N: 0.**
