# Track A Epoch 002 Primary-Analysis Authorization Procedure

## Status and purpose

This document defines the prospective, fail-closed procedure for a future Track A Epoch 002 primary-analysis authorization event. It installs tooling and acceptance criteria only. It does **not** create an authorization record, run primary analysis, create a locked analysis result, increment scientific N, establish canonical DGAF efficacy, establish independent validation, or authorize High-Assurance operation.

The permitted future scope is exactly `LOCKED_PRIMARY_ANALYSIS_ONLY`.

## Current scientific and authorization boundary

Track A Epoch 002 collection is complete at **50 paired seed units** and **2,250 blinded observations**. Those observations exist and remain part of the locked Epoch 002 evidence chain; the canonical scientific-N increment remains zero because no authorized primary analysis result has yet been admitted.

Current state remains:

- `PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN`
- `SCIENTIFIC_N_INCREMENT=0`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`

The current repository does not establish the real operator materialization event or an accepted canonical materialization receipt. Therefore no positive Epoch 002 primary-analysis authorization event is currently admissible.

## Canonical future chain

A future positive authorization event is downstream of an accepted, immutable materialization receipt and remains upstream of any locked analysis result:

1. real operator-controlled materialization is completed outside this authorization tooling lane;
2. validated non-secret materialization evidence is admitted under its own contract;
3. `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json` is accepted as the immutable materialization predecessor;
4. the prospective authorization validator re-verifies the frozen preregistration, analysis lock, analysis implementation, analysis configuration digest, dependency lock, result-record schema, result-record semantics, and exact materialization receipt identity;
5. only then may a candidate `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json` be created for protected-main review;
6. a later, separately controlled analysis execution may produce `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json` only after an authorization event has actually been accepted.

This procedure does not perform steps 1-3 or step 6.

## Preconditions for a future positive authorization event

All of the following must hold simultaneously. Any missing or conflicting condition fails closed:

- the canonical materialization receipt exists and has a unique immutable repository history;
- the authorization event's sole parent is exactly the **accepted protected-main parent** supplied by the repository event context;
- the materialization receipt already exists in that accepted protected-main parent, so a receipt created only on the authorization PR branch cannot satisfy the prerequisite;
- its accepted receipt event is an ancestor of the proposed authorization event parent;
- the receipt content is byte-identical at the authorization parent and authorization head;
- the locked analysis result does not exist at either the authorization parent or authorization head;
- the frozen Epoch 002 preregistration identity matches the validator-bound blob identity;
- the frozen analysis-lock identity matches the validator-bound blob identity;
- the primary analysis implementation identity matches the validator-bound blob identity;
- the frozen analysis configuration digest remains exact;
- the dependency-lock identity remains exact;
- the shared Epoch 002 result-record schema and semantic policy validate without widening authority;
- no secret, key, passphrase, protected mapping value, or equivalent custody material is admitted to the repository authorization record.

## Future authorization-event shape

The future accepted authorization event is deliberately narrow. Its commit must have **exactly one parent** and **exactly one changed file**: the canonical primary-analysis authorization record. The event is **creation-only** and must be the **first-and-only history** for that record path at admission time.

The sole parent must equal the accepted protected-main parent used for validation. For a pull request, that identity is the exact PR base SHA. For a direct protected-main push, it is the push event's previous-main SHA. Event-mode validation fails closed when neither repository event can supply that accepted predecessor. This prevents a multi-commit candidate branch from manufacturing a materialization receipt and then treating it as already accepted authority.

The authorization record must bind the exact accepted `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json` record and content digest. It must use the closed shared result-record envelope without adding a second authority schema. The record's exact evidence scope is `LOCKED_PRIMARY_ANALYSIS_ONLY`.

A validator PASS on a pull-request head is only `VALIDATED_PENDING_ACCEPTANCE`. It is not an authorization state transition. Repository authority arises only from the separately reviewed and accepted protected-main event satisfying this procedure and the validator contract.

## Dedicated CI behavior

The dedicated workflow is read-only (`contents: read`) and checks out the exact subject head with full repository history and credential persistence disabled. It has two fail-closed modes:

- **tooling mode**: while the canonical authorization and result records are absent, validate frozen identities, semantic policy, tooling boundaries, adversarial tests, and continued absence of unauthorized state;
- **event mode**: when an authorization record is present and the result remains absent, validate `HEAD` as the exact prospective one-parent / one-file / creation-only authorization event and require `HEAD^` to equal the accepted protected-main parent derived from the PR base SHA or previous-main push SHA.

The workflow never executes primary analysis and never writes the materialization receipt, authorization record, or locked result record. It does not receive or persist protected mapping material or custody secrets.

## Failure semantics

Any failed identity, accepted-parent binding, ancestry, uniqueness, content, scope, schema, semantic-policy, event-shape, result-absence, or secret-boundary check rejects the candidate. Rejection preserves the pre-event state:

- `PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN`
- `SCIENTIFIC_N_INCREMENT=0`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`

No failed or merely proposed authorization event may be interpreted as partial authorization.

## Non-effects of an accepted authorization event

Even a future accepted authorization record would authorize only the later locked primary analysis defined by the frozen Epoch 002 contract. The authorization event itself:

- does not execute analysis;
- does not create `TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json`;
- does not increment scientific N;
- does not establish canonical DGAF efficacy;
- does not establish independent validation;
- does not authorize High-Assurance operation;
- does not authorize exploratory analysis, historical pooling, endpoint substitution, estimand substitution, alpha changes, or Epoch 004 substitution;
- does not alter the custody classification of Epoch 002 evidence.

## Explicit exclusions

This procedure does not authorize or implement real materialization, materialization-receipt creation, primary-analysis execution, result interpretation, adjudication, public efficacy claims, or any transfer of state from separate shadow-assurance / discovery work. Those are separate controlled stages with separate evidence and acceptance boundaries.
