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

The execution order and dependency rules are governed by [`DYNAMIC_FREEZE_ADMISSIBILITY_CONTROL_2026-08-26.md`](DYNAMIC_FREEZE_ADMISSIBILITY_CONTROL_2026-08-26.md).

Every gate is treated as a predicate with explicit scope, prerequisite set, evidence requirement, freshness rule, invalidation rule, and closure rule. Independent `READY` lanes may proceed in parallel; `BLOCKED`, `STALE`, `INVALIDATED`, `REVIEW`, and authorization states are fail-closed and cannot be bypassed by documentation.

## P8 candidate evidence matrix

| Predicate | Required evidence | Current state |
|---|---|---|
| P1 candidate identity | exact SHA/tree binding | Candidate identified; fresh closure evidence pending |
| P2 runtime | authenticated five-case runtime matrix on exact deployment | **OPEN — requires `VERCEL_AUTOMATION_BYPASS_SECRET`** |
| P3 artifact | schema, identity, uniqueness, balance, canonical matrix, deviation integrity | Controls implemented; candidate-scoped evidence pending |
| P4 blinding | custody, bijection, access separation, operational procedure | Controls implemented; operational evidence pending |
| P5 reproducibility | environment fingerprint and deterministic reproduction | Partially specified; execution-time fingerprint pending |
| P6 custody | archive → retrieve → hash verification | **OPEN** |
| P6a runtime | authenticated four-case CORS matrix on exact deployment | **OPEN — blocked by authenticated deployment path** |
| P7 scientific target | authority adoption + cryptographic binding | **FORMALLY OPEN** |
| P8 analysis lock | exact analysis implementation/configuration + protocol binding | **OPEN / FAIL-CLOSED** |
| E2b verifier toolchain | pinned dependency/toolchain identity for evidence judge | **OPEN — tracked by #105; required before freeze admissibility** |
| M6 negative-state observability | machine-retained proof of N=0/no authorization/no pilot/no unblinding | **OPEN — tracked by #106** |

## P6a runtime evidence

P6a requires an authenticated four-case CORS matrix against the same candidate/deployment identity as P2:

1. allowed-origin POST;
2. disallowed-origin POST;
3. allowed-origin preflight;
4. disallowed-origin preflight.

No historical P6a result may be substituted for current-candidate execution.

## P7 formal closure

P7 scientific decisions are technically adjudicated. Formal closure still requires:

1. explicit experimental-control authority adoption;
2. treatment/reference verification against the eventual frozen apparatus;
3. cryptographic binding of the adopted record to the protocol, runner/apparatus, analysis specification, and freeze manifest;
4. recording the authority, adoption date, and adopted decision identity.

P7 closure does not authorize the pilot.

## Freeze inputs

The freeze manifest must bind, at minimum:

- executable candidate SHA and tree identity;
- canonical protocol blob SHA;
- artifact-schema SHA/hash;
- analysis configuration hash;
- runner identity/hash;
- environment fingerprint;
- deployment ID and deployment URL;
- P7 decision-record hash;
- H1–H3 publication mapping hash;
- baseline matrix hash;
- negative-control matrix hash;
- verification-toolchain/E2b lock hash;
- machine-retained negative-state/M6 artifact hash;
- exact workflow run IDs;
- retained evidence artifact IDs;
- durable custody/retrieval hashes;
- blinding/custody control identifier.

## P9 independent verification checklist

The independent verifier must establish, without relying solely on the same evidence path used to construct the candidate:

- candidate identity is stable;
- protocol and analysis hashes correspond to the intended specification;
- runner and schema are mutually consistent;
- P2 and P6a evidence is exact-candidate and exact-deployment scoped;
- artifact identity and canonical SHA calculation are consistent;
- blinding boundary remains intact;
- custody evidence is independently retrievable and hash-verifiable;
- environment fingerprint is recorded and reproducible;
- E2b verifier toolchain is pinned and reproducible;
- M6 negative-state evidence is machine-retained and independently hash-verifiable;
- P7 authority adoption is explicit;
- freeze manifest represents exactly the apparatus being verified;
- no post-freeze executable mutation exists.

## Authorization boundary

Authorization requires all P1–P9 predicates plus E2b and M6 where applicable, an independently verified immutable freeze, and an explicit authorization decision. Until then:

- no pilot execution;
- no unblinding;
- no efficacy claim;
- N remains `0`.

## Dynamic invalidation rule

Any substantive change to executable code, workflow behavior, dependencies, schemas, protocol semantics, analysis semantics, blinding semantics, failure/recovery semantics, deployment behavior, or verification-toolchain provenance invalidates the affected candidate/predicate bindings and requires candidate transition or affected-predicate re-verification.

Documentation-only successors may update living governance records without advancing the executable candidate, provided an audit confirms that none of those substantive surfaces changed.
