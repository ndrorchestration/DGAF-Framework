# Dynamic Freeze-Admissibility Control — 2026-08-26

## Purpose

Provide a single epistemically hardened execution model for completing the maximum admissible amount of DGAF/PDMAL pre-freeze work in parallel while preventing candidate drift, evidence inheritance, duplicated controls, or accidental authorization.

## Immutable boundary

- State starts and remains `PRE-FREEZE / FAIL-CLOSED` until all required predicates are satisfied.
- Current executable candidate: `e6beeb66335e1b50a239697badab22dab50eb5ba`.
- Current verified production deployment: `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`.
- Freeze: `NOT CREATED`.
- Authorization: `NOT GRANTED`.
- Empirical `N = 0`.
- A documentation change never creates execution evidence.
- A passing component test never closes a higher-order predicate unless its acceptance rule explicitly names that test as sufficient evidence.

## Control model

Every obligation is represented as:

`predicate = scope + prerequisite set + evidence requirement + freshness rule + invalidation rule + closure rule`

Each predicate has exactly one current disposition:

- `OPEN` — not yet satisfied;
- `READY` — prerequisites satisfied and executable;
- `PASS` — sufficient evidence exists for the current candidate/scope;
- `BLOCKED` — an external prerequisite prevents execution;
- `STALE` — evidence no longer applies to current scope/candidate;
- `INVALIDATED` — a substantive change broke the binding;
- `CONTROLLED` — risk handled by another authoritative predicate;
- `DEFERRED` — legitimate but not required for the next gate.

`PASS` is never inherited by a descendant candidate. `PASS` may be reused only when the predicate explicitly declares its scope unchanged and the evidence remains within its freshness rule.

## Dynamic scheduler

At every reconciliation cycle:

1. Resolve live GitHub `main` SHA.
2. Resolve current executable candidate SHA.
3. Compare candidate against live main and classify intervening commits as `APPARATUS`, `GOVERNANCE`, or `HISTORICAL`.
4. Recompute predicate dependencies.
5. Mark stale/invalidated predicates before dispatching new work.
6. Dispatch every `READY` predicate whose execution cannot mutate the candidate or contaminate an empirical state.
7. Retain evidence artifacts with exact SHA/run/environment bindings.
8. Recompute the closure graph after each result.
9. Promote only predicates whose explicit acceptance conditions are met.
10. Stop automatically at `BLOCKED`, `REVIEW`, or authorization boundaries rather than guessing through them.

## Parallel execution lanes

### Lane A — Runtime

- P2 authenticated five-case matrix.
- P6a authenticated four-case CORS matrix.
- Exact deployment identity verification.

External blocker: `VERCEL_AUTOMATION_BYPASS_SECRET`.

### Lane B — Artifact and analysis

- P3 schema and canonical artifact verification.
- P8 analysis/configuration binding.
- Negative-path and malformed-input tests.
- Canonical SHA consistency.
- Unblinding-map bijection.
- Unique/finite paired-seed analysis inputs.

### Lane C — Security and blinding

- P4 custody separation.
- Secret-handling checks.
- Operational blinding rehearsal.
- Unblinding authorization boundary.

### Lane D — Reproducibility and custody

- P5 environment fingerprint.
- E2b verification-toolchain hash pinning.
- P6 archive/retrieve/re-hash cycle.
- Independent artifact retrieval.

### Lane E — Governance and scientific closure

- P7 authority adoption.
- Protocol/schema/statistical freeze preparation.
- H1–H3 mapping reconciliation.
- Baseline and negative-control freeze.

### Lane F — Independent verification

Prepare P9 verifier package while P2–P8 remain open. P9 may inspect design and evidence structure but cannot certify predicates whose execution evidence does not yet exist.

## Evidence discipline

Every evidence item must record:

- predicate ID;
- candidate SHA or historical SHA;
- Git tree identity where applicable;
- workflow/run ID;
- artifact ID and hash;
- environment fingerprint where execution occurred;
- deployment ID where runtime occurred;
- timestamp;
- producer;
- verifier, if independently checked;
- evidence class: `DEFINED`, `IMPLEMENTED`, `COMPUTED`, `VERIFIED`, `ATTESTED`, `HISTORICAL`, `HYPOTHESIS`, or `UNSUPPORTED`.

Evidence is not strengthened by repetition across documents.

## Evidence freshness

### Immutable-by-definition

Protocol decisions, endpoint definitions, statistical rules, and authorization rules are versioned artifacts. A new version requires explicit supersession.

### Candidate-scoped

Code tests, schemas, runner behavior, dependency checks, workflow evidence, and deployment evidence remain bound to the exact candidate.

### Time-sensitive

Deployment health, secrets/configuration state, external-service behavior, and environment fingerprints must be rechecked when the underlying environment changes.

## Invalidation graph

A substantive change to any of the following invalidates the current candidate binding and triggers affected-predicate recomputation:

- executable code;
- workflow behavior;
- dependency or lockfile;
- artifact schema;
- protocol semantics;
- analysis semantics/configuration;
- blinding semantics;
- failure/recovery semantics;
- deployment behavior.

Documentation-only changes may proceed without candidate transition when an audit proves that none of the substantive surfaces changed.

## Evidence-monoculture controls

A predicate must not be considered independently verified merely because multiple checks derive from the same:

- validator;
- artifact;
- parser;
- transformation;
- workflow;
- dependency chain;
- human assertion.

Where independence matters, the verifier must cross the evidence boundary: recompute, independently retrieve, independently parse, or independently inspect the underlying source.

## State-transition controls

No document may directly promote:

`IMPLEMENTED → VERIFIED`

`VERIFIED → FROZEN`

`FROZEN → AUTHORIZED`

without the corresponding evidence predicate.

Required transitions are:

`OPEN → READY → PASS`

then, only after all dependent predicates pass:

`PASS set → FREEZE CANDIDATE → INDEPENDENT VERIFICATION → IMMUTABLE FREEZE → EXPLICIT AUTHORIZATION`.

## Maximum-progress rule

When a hard blocker exists, execute every independent `READY` lane that:

1. does not require the blocked predicate;
2. cannot alter the empirical dataset;
3. cannot silently alter the candidate apparatus;
4. produces reusable evidence or removes a future blocker.

Do not idle on blocked work and do not bypass it.

## Candidate transition rule

If a new executable commit is required:

1. create a new candidate identity;
2. retain the predecessor as historical candidate evidence;
3. recompute only predicates affected by the change first;
4. run the complete candidate integrity gate before relying on inherited unaffected evidence;
5. never relabel historical evidence as current evidence.

## Closure algorithm

A gate closes only when:

`required predicates = PASS`

and

`freshness = current`

and

`scope = exact`

and

`provenance = complete`

and, where required,

`independence = demonstrated`.

Otherwise it remains open or explicitly blocked.

## Freeze admissibility set

The corrected candidate is freeze-admissible only when all of these are satisfied:

- P1 candidate identity;
- P2 authenticated runtime;
- P3 artifact contract;
- P4 blinding/security;
- P5 reproducibility;
- P6 durable custody;
- P6a authenticated CORS;
- P7 formal authority adoption and exact binding;
- P8 analysis lock;
- E2b verification-toolchain pinning;
- baseline and negative-control freeze;
- endpoint/statistical-analysis freeze;
- P9 independent verification;
- immutable freeze manifest created and independently checked.

Authorization remains a separate explicit governance transition.

## Current dynamic queue

| Lane | Predicate | Current disposition | Blocking dependency |
|---|---|---|---|
| Runtime | P2 | `BLOCKED` | `VERCEL_AUTOMATION_BYPASS_SECRET` |
| Runtime | P6a | `BLOCKED` | same authenticated deployment path |
| Artifact | P3 | `READY/PARTIAL` | candidate-scoped evidence retention |
| Analysis | P8 | `OPEN` | exact candidate/protocol binding |
| Security | P4 | `READY/PARTIAL` | operational custody evidence |
| Reproducibility | P5 | `READY/PARTIAL` | execution-time fingerprint |
| Toolchain | E2b | `OPEN` | version/hash pinning of verifier toolchain |
| Custody | P6 | `OPEN` | direct archive/retrieval proof |
| Science | P7 | `FORMALLY OPEN` | authority adoption + cryptographic binding |
| Independent | P9 | `NOT EXECUTED` | complete candidate evidence package |
| Freeze | Freeze | `NOT CREATED` | P1–P9 + E2b |
| Authorization | Pilot authorization | `NOT GRANTED` | immutable freeze + explicit decision |

## Operational stop conditions

Stop and reclassify rather than continue when:

- candidate identity is ambiguous;
- a supposedly documentation-only commit changes executable behavior;
- evidence cannot be bound to an exact source/run/artifact;
- a control shares the same hidden dependency as the evidence it is meant to independently judge;
- a closure depends on an undocumented interpretation;
- a protocol or analysis change is proposed after freeze;
- a state transition would be created solely by changing documentation.

## Final safety invariant

Until explicit authorization is recorded against an independently verified immutable freeze:

`NO PILOT`
`NO UNBLINDING`
`NO EFFICACY CLAIM`
`N = 0`
