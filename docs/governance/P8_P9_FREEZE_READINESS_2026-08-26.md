# P8 / P9 / Freeze Readiness — Reconciled 2026-08-29

## Control status

- State: `PRE-FREEZE / FAIL-CLOSED`
- Current `main`: active documentation/evidence lineage; resolve the branch directly rather than freezing a documentation tip into the apparatus identity
- Experimental verification boundary: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- Current-tree E2b: `OPEN / VERIFICATION REQUIRED`
- Candidate-scoped M6: `CLOSED / VERIFIED` for `ac8ea267…` / run `33050398324`
- TGL contract: `REMEDIATION / VALIDATION IN PROGRESS` — PR #134 is current-main remediation; PRs #132/#133 are historical diagnostic/remediation records
- DGAF v1 control-plane: `ENGINEERING CANDIDATE / VALIDATION IN PROGRESS` — PR #136 current head requires fresh exact-head CI after the latest regression-fixture correction
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
| P6a CORS | BLOCKED / OPEN | Authenticated four-case CORS matrix on same deployment identity |
| P7 scientific target | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact cryptographic binding of adopted decision to frozen protocol/apparatus/analysis/manifest |
| P8 analysis lock | OPEN / FAIL-CLOSED | Exact analysis/configuration/protocol/current-tree binding |
| E2b verifier toolchain | CLOSED / VERIFIED @ `d299dd1…` | Historical exact-tree verification retained; current-tree applicability requires affected-boundary re-verification |
| M6 negative state | CLOSED / VERIFIED @ `ac8ea26…` | Candidate exact-tree/workspace negative-state evidence retained; does not authorize execution |
| DGAF v1 control-plane | ENGINEERING / VALIDATION IN PROGRESS | Current PR head must complete dedicated contract CI and adversarial adapter-boundary review; this lane is non-authorizing |
| P9 independent verification | NOT EXECUTED | Independent verification of complete evidence chain |

## TGL/P-35 contract boundary

The PR #132 41-pass / 2-fail result remains a historical diagnostic signal at the TGL → P-35 integration boundary. PR #134 is the current-main remediation lane; PRs #132/#133 are historical diagnostic/remediation records. The remediation must be validated independently at its exact head before candidate-scoped experimental rebinding.

The remediation remains intentionally minimal: restore the established P-35 API and TGL fail-closed behavior, make required/conditional gate semantics explicit, implement deterministic status reduction, make the final seal correspond to the authoritative returned audit state, and expand regression coverage.

No TGL remediation changes the experimental treatment, creates a freeze, closes P7/P8, grants authorization, or increases empirical N.

## DGAF v1 control-plane boundary

PR #136 is generic engineering infrastructure. Its lifecycle, resource, provenance, concurrency, and commit-boundary checks are engineering evidence only. `COMMIT_READY` is not execution, and control-plane CI is not PDMAL evidence. Any adapter that changes the experimental apparatus requires a new candidate identity and affected-predicate re-verification.

## Current lineage versus experimental boundary

The current `main` branch is a living documentation/evidence lineage and must not be silently substituted for the experimental verification boundary. The experimental verification boundary remains `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Subsequent documentation corrections do not retroactively change candidate-scoped verification results.

## E2b provenance boundary

Run `33047380487` successfully verified exact tree `d299dd152fb82d48a066d66a64bf0917e20d6167`, including exact checkout/target assertion, source requirements fingerprint, hash-pinned installation, exact-tree provenance, and artifact retention. Artifact `9636185725` has digest `sha256:723aa9d5a1b60242212a8d7533ccf296de37a36349b4a60f53714bb6898ca1fd`.

This closure remains valid for its executed tree. The corrected `ac8ea26…` workflow change binds the candidate target SHA to the executing workflow SHA and therefore establishes a separate current candidate verification boundary.

## M6 boundary

M6 is CLOSED/VERIFIED for exact candidate/tree `ac8ea267…` via run `33050398324`. Its retained negative-state evidence establishes only the observed PRE-FREEZE/N=0/no-authorization state for that exact verification workspace/job. It does not authorize execution.

## P2 / P6a boundary

The READY deployment remains supporting deployment evidence, not runtime-predicate closure. P2 and P6a require authenticated execution against the exact deployment identity. The automation-bypass secret must be configured out-of-band before those lanes can execute. Issue #137 separately tracks the current GitHub-main versus Vercel-source SHA mismatch.

## P7 / P8 boundary

P7 scientific content has been adopted: primary contrast is full `dgaf` versus `null` on FFCR, with paired root-seed analysis, 10,000-resample percentile bootstrap, seed `20260823`, alpha `0.05`, and positive-estimate/CI-above-zero directional support. Formal P7 closure remains pending exact freeze identity binding. P8 remains fail-closed until the executable analysis, schema, runner, protocol, candidate identity, and required verification evidence are bound to the same admissible freeze target.

## Independent verification / freeze boundary

P9 has not executed. No new immutable freeze exists. Pilot authorization remains a separate explicit transition after all required predicates and freeze verification close.

**No pilot execution. No unblinding. No efficacy claim. Empirical N remains 0.**
