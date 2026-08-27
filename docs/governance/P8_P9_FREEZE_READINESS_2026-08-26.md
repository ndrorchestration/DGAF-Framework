# P8 / P9 / Freeze Readiness — Reconciled 2026-08-27

## Control status

- State: `PRE-FREEZE / FAIL-CLOSED`
- Current `main`: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- Current-tree verification boundary: `ac8ea26…`
- E2b exact-tree closure: `d299dd152…` / run `33047380487` / artifact `9636185725`
- Current-tree M6: `OPEN / VERIFICATION REQUIRED`
- Freeze: `NOT CREATED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

This is a readiness/control artifact. It is not evidence that any unchecked predicate has passed and it does not authorize execution.

## Dynamic control model

Every gate is a predicate with explicit scope, prerequisites, evidence requirements, freshness conditions, invalidation triggers, and closure rules. Independent READY lanes may proceed in parallel when they cannot mutate the experimental dataset or silently alter the apparatus. Documentation repetition does not increase epistemic strength.

## Predicate matrix

| Predicate | State | Closure requirement |
|---|---|---|
| P1 candidate identity | OPEN | Exact current-tree/source binding and retained evidence |
| P2 runtime | BLOCKED / OPEN | Authenticated five-case runtime matrix on exact deployment |
| P3 artifact contract | OPEN | Current-candidate schema/identity/uniqueness/balance evidence |
| P4 blinding/security | OPEN | Operational custody, access separation, bijection, and unblinding evidence |
| P5 reproducibility | OPEN | Environment fingerprint plus deterministic reproduction |
| P6 durable custody | OPEN | Archive/retrieve/hash round trip with retained evidence |
| P6a CORS | BLOCKED / OPEN | Authenticated four-case CORS matrix on same deployment |
| P7 scientific target | FORMALLY OPEN | Authority adoption + exact cryptographic binding |
| P8 analysis lock | OPEN / FAIL-CLOSED | Exact analysis/configuration/protocol/current-tree binding |
| E2b verifier toolchain | CLOSED / VERIFIED @ `d299dd1…` | Historical exact-tree verification retained; current-tree applicability requires affected-boundary re-verification |
| M6 negative state | OPEN / CURRENT-TREE VERIFICATION REQUIRED | Machine-retained, independently hash-verifiable PRE-FREEZE/N=0/no-authorization evidence for `ac8ea26…` |
| P9 independent verification | NOT EXECUTED | Independent verification of complete evidence chain |

## E2b provenance boundary

Run `33047380487` successfully verified exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167`, including exact checkout/target assertion, source requirements fingerprint, hash-pinned installation, exact-tree provenance, and artifact retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure remains valid for its executed tree. The subsequent Governance CI change at `ac8ea26…` binds `PDMAL_TARGET_CANDIDATE_SHA` to `${{ github.sha }}` and therefore establishes a new current-tree verification boundary.

## M6 negative-state boundary

M6 must establish the observed current verification workspace state only: PRE-FREEZE, N=0, no authorization, no pilot mode, no blinding key, no pilot artifacts, and no pilot invocation. Historical M6 evidence targeting `e6beeb…` and verifier merge-ref `2516f32…` is non-closing for `ac8ea26…`.

## P2 / P6a boundary

The READY deployment remains supporting deployment evidence, not runtime-predicate closure. P2 and P6a require authenticated execution against the exact deployment identity. The automation-bypass secret must be configured out-of-band before those lanes can execute.

## P7 / freeze boundary

P7 scientific adjudication is technically complete but formal adoption remains open. Freeze requires P1–P9 plus E2b/M6, frozen baselines/negative controls/endpoints/statistical analysis plan, immutable manifest creation, and independent verification. Pilot authorization remains a separate explicit state transition.

**No pilot execution. No unblinding. No efficacy claim. Empirical N remains 0.**
