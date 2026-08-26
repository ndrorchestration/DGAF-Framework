# P8 / P9 / Freeze Readiness — 2026-08-26

## Control status

- State: `PRE-FREEZE / FAIL-CLOSED`
- Current executable verification candidate: `e6beeb66335e1b50a239697badab22dab50eb5ba`
- Current Vercel deployment: `dpl_HgSv9hTrvMNBHxboDhkkvHKeogc5`
- Deployment state: `READY`
- Freeze: `NOT CREATED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

This is a readiness/control artifact. It is not evidence that any unchecked predicate has passed and it does not authorize execution.

## Dynamic control model

Every gate is a predicate with explicit scope, prerequisites, evidence requirements, freshness conditions, invalidation triggers, and closure rules. Independent READY lanes may proceed in parallel when they cannot mutate the experimental dataset or silently alter the apparatus. Documentation repetition does not increase epistemic strength.

## Predicate matrix

| Predicate | State | Closure requirement |
|---|---|---|
| P1 candidate identity | PARTIAL | Exact candidate/tree/source binding and retained evidence package |
| P2 runtime | BLOCKED | Authenticated five-case runtime matrix on exact READY deployment |
| P3 artifact contract | PARTIAL | Candidate-scoped schema/identity/uniqueness/balance evidence |
| P4 blinding/security | OPEN | Operational custody, access separation, bijection, and unblinding procedure evidence |
| P5 reproducibility | OPEN | Environment fingerprint plus deterministic reproduction |
| P6 durable custody | OPEN | Archive/retrieve/hash round trip with retained evidence |
| P6a CORS | BLOCKED | Authenticated four-case CORS matrix on same deployment |
| P7 scientific target | FORMALLY OPEN | Authority adoption + exact cryptographic binding |
| P8 analysis lock | OPEN / FAIL-CLOSED | Exact analysis/configuration/protocol/candidate binding |
| E2b verifier toolchain | OPEN | Complete immutable transitive verifier dependency lock and executed fingerprint |
| M6 negative state | OPEN | Machine-retained, independently hash-verifiable PRE-FREEZE/N=0/no-authorization evidence |
| P9 independent verification | NOT EXECUTED | Independent verification of the complete evidence chain |

## E2b verifier boundary

The apparatus dependency lock and verifier-policy dependency set are separate control surfaces. Governance CI uses the PDMAL full lock in an isolated Python 3.12 environment with `--require-hashes`; the evidence emitter separately records the verifier commit and the explicit target apparatus candidate and hashes target source objects directly from the target Git SHA.

The functional Epistemic Evidence Validation workflow intentionally does **not** use `--require-hashes` against `requirements-epistemic.txt` and `experiments/pdmal_topology/requirements.txt`, because those files are not a complete immutable transitive hash lock. It runs functional validation with `pip check` and explicitly records `E2b = NOT PASS`.

E2b therefore remains open until the verifier-policy dependency surface itself has a complete reproducible pinning strategy.

## M6 negative-state boundary

M6 records the observed state of the current verification workspace/job only. It must not be interpreted as retrospective proof of global historical absence. The artifact records PRE-FREEZE, N=0, no authorization, no pilot mode, no blinding key, no pilot artifacts, and no pilot invocation in the current job, and fails closed when those conditions are not met.

## P2 / P6a boundary

The READY Vercel deployment is supporting deployment evidence, not runtime-predicate closure. P2 and P6a require authenticated execution against the exact deployment identity. Current external blocker: `VERCEL_AUTOMATION_BYPASS_SECRET`.

## P7 / freeze boundary

P7 scientific adjudication is technically complete but formal adoption remains open. Freeze requires P1–P9 plus E2b/M6, frozen baselines/negative controls/endpoints/statistical analysis plan, immutable manifest creation, and independent verification. Pilot authorization remains a separate explicit state transition.

**No pilot execution. No unblinding. No efficacy claim. Empirical N remains 0.**
