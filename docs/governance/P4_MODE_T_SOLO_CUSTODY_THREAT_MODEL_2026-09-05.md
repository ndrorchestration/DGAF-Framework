# P4 Mode T Solo Custody — Threat Model and Lifecycle Design

**Status:** DESIGN / THREAT MODEL / NOT EXECUTED  
**Issue:** #287  
**Scope:** Mode T independently enforced technical custody for a solo execution/analysis principal.  
**Scientific state:** P4-A OPEN · P7 OPEN · P8 OPEN / FAIL-CLOSED · P9 NOT EXECUTED · FREEZE NOT ESTABLISHED · AUTHORIZATION NOT GRANTED · empirical N=0.

## Purpose

Define a fail-closed Mode T lifecycle that can be reviewed and tested without creating a real blinding key, condition mapping, empirical observation, freeze, or authorization.

This document does **not** assert that GitHub-hosted runners plus a timelock network satisfy P4. It specifies the conditions that such a mechanism would have to satisfy before promotion.

## Core problem

The current P4 v2 contract assumes the real key, mapping, nonces, and their commitments exist before P7/freeze. That ordering works for Mode H and Mode I because an independent custodian can hold the material.

For a zero-human Mode T implementation, pre-generating recoverable protected material creates a contradiction: if the solo analyst can later make the runner retrieve it, the analyst may possess an equivalent unilateral recovery path; if nobody can retrieve it, the empirical runner cannot apply the mapping.

Mode T therefore needs a separate lifecycle in which **mechanism closure precedes freeze, while secret instantiation occurs only after separate pilot authorization inside the frozen execution environment**.

## Proposed lifecycle

### P4-T-A — mechanism closure, pre-freeze

No real key, mapping, commitment nonce, or empirical workload exists.

Freeze-verifiable inputs must include:

- exact candidate, workflow, helper, artifact-schema, analysis and protocol identities;
- exact timelock client binary/source digest and chain identity;
- predeclared future-release-round selection algorithm and minimum safety margin;
- no-secret-output contract;
- artifact/log/cache/output/summary denylist;
- network allowlist required by the mechanism;
- hosted-runner trust assumptions;
- immutable authorization identity consumed by the execution workflow;
- one-run/rerun policy;
- analysis-lock-before-release rule;
- explicit invalidation conditions;
- adversarial synthetic-fixture tests.

P4-T-A may close only as **MECHANISM VERIFIED / SECRET NOT YET INSTANTIATED**.

### P4-T-X — custody instantiation, authorized execution

This phase is unreachable until the separately frozen chain passes and explicit pilot authorization exists.

Inside the exact authorized ephemeral runner:

1. reverify frozen candidate/workflow/helper/protocol/analysis/schema identities;
2. verify the authorization record and one-run identity;
3. select the release round using the frozen deterministic policy; reject a past or insufficiently distant round;
4. generate the real blinding key, mapping and independent commitment nonces from the runner CSPRNG;
5. compute domain-separated commitments in memory;
6. execute the blinded workload using the mapping in memory;
7. construct a release bundle containing only the material required for later continuity verification;
8. timelock-encrypt the release bundle to the selected future round;
9. emit the blinded dataset, commitments, ciphertext, exact identities, and non-secret execution evidence;
10. run a secret-leak scan over artifacts/logs/outputs/summaries before successful completion;
11. never export plaintext protected material.

Failure at any step invalidates the execution instance. It must not be retried under the same authorization unless the frozen rerun policy explicitly permits an objectively identified infrastructure failure before any usable blinded result exists.

### P4-T-L — analysis lock, pre-release

Before the timelock release round:

- retrieve the exact blinded dataset by immutable artifact identity/digest;
- run only the frozen primary analysis;
- publish dataset digest, analysis implementation/config identities, primary result digest, workflow/run identity, and server-side timestamp;
- prove that the analysis-lock completion timestamp precedes the release round.

If this ordering cannot be established, the pilot is **INVALID / NO SCIENTIFIC INTERPRETATION**. A later analysis cannot repair it.

### P4-B — post-release continuity audit

After the release round:

- decrypt the release bundle using the predeclared mechanism;
- recompute key/mapping commitments exactly;
- verify mapping continuity against the blinded dataset;
- verify P4-T-X and P4-T-L identities/timestamps;
- record any contradiction, leak, override, rerun, or unexpected recovery path.

P4-B appends evidence. It never retroactively changes what P4-T-A established.

## Threat model

| Threat | Required fail-closed control |
|---|---|
| Analyst can inspect/attach to live runner | Mode T is not promotable until authoritative evidence establishes whether this is possible and the residual risk is accepted. |
| Debug logging exposes process/env state | Frozen workflow must disable debug modes and tests must prove secret values never enter shell tracing, outputs, summaries, artifacts or logs. |
| Mutable action/dependency changes secret handling | Every action/helper/client must be immutable by commit/content digest; no floating tags or runtime package upgrade. |
| Analyst chooses past/near release | Release round must be derived by frozen policy from server-observed execution time plus a minimum margin and independently checked. |
| Analysis occurs after release but is represented as pre-release | Machine verification must compare server-side analysis-lock completion time with the selected release round/time. |
| Reruns enable cherry-picking | One authorization maps to one accepted execution identity. Duplicate successful/usable executions fail closed. |
| Plaintext survives in artifact/cache/log/crash output | No caches; minimal artifact allowlist; post-run leak scanner; any detected protected material invalidates the instance. |
| Analyst changes workflow after freeze | Execution verifies exact frozen workflow/helper hashes before secret generation. Mismatch exits before P4-T-X. |
| Timelock chain/client substitution | Chain identity and client digest are frozen; runtime re-verifies both before secret generation. |
| Timelock/network unavailable | Execution or release audit fails closed; unavailability cannot authorize an alternate early-recovery path. |
| Repository/admin privilege reveals plaintext | Design must demonstrate that repository administration can alter future runs but cannot recover plaintext from the already-running/finished accepted instance. |
| Multiple authorization records | Authorization identity must be unique and freeze-compatible; conflicting authorizations block execution. |

## Trust assumptions requiring authoritative verification

Before implementation promotion, retain source-backed answers for:

1. lifecycle/isolation properties of the selected hosted runner;
2. whether repository owners can attach to, snapshot, introspect, or otherwise recover process memory from a standard hosted job;
3. debug/logging controls that can be enabled without modifying the frozen workflow;
4. artifact, cache, environment, step-output and job-summary persistence behavior;
5. timelock cryptographic/security assumptions, threshold/network trust model, chain identity and future-round semantics;
6. behavior under chain reorganization, outage, client failure, or delayed beacon publication.

Unknown remains **UNKNOWN** and blocks promotion where it affects early secret recovery.

## Schema consequence

Mode H/I retain P4 v2 pre-freeze key/mapping commitments unchanged.

Mode T must not fabricate nonexistent pre-freeze secret commitments. A future schema revision should distinguish:

- `p4_pre_freeze_class: mechanism`
- `p4_custody_mode: T`
- `p4_t_mechanism_evidence_sha256`
- `p4_t_runner_contract_sha256`
- `p4_t_timelock_policy_sha256`
- `p4_t_analysis_lock_policy_sha256`
- `p4_t_rerun_policy_sha256`
- `p4_t_secret_instantiation_status: NOT_EXECUTED`

The real `key_commitment_sha256` and `mapping_commitment_sha256` become execution-phase P4-T-X evidence and must not be required by pre-authorization P7/freeze/P9 for Mode T.

No schema/code change is authorized by this design record alone.

## Promotion gates

Implementation work may begin only after the following design questions are resolved:

- [ ] authoritative hosted-runner capability/limits evidence retained;
- [ ] timelock chain/client/security assumptions pinned;
- [ ] minimum release-margin policy specified;
- [ ] no-secret-output contract specified;
- [ ] analysis-lock timestamp verifier specified;
- [ ] rerun/multiple-execution semantics specified;
- [ ] invalidation taxonomy specified;
- [ ] P4/P7/P8/P9 schema migration reviewed for H/I non-regression;
- [ ] synthetic-only adversarial test plan accepted;
- [ ] independent red-team review completed.

## Non-regression invariants

Any Mode T implementation must preserve:

- Mode H and Mode I semantics exactly;
- PRE-FREEZE / NOT AUTHORIZED / N=0 until their real transitions occur;
- no real secret generation during development or pre-freeze validation;
- no empirical workload during development;
- no claim that CI success proves external custody independence;
- no silent fallback from Mode T to analyst-controlled storage;
- no post-release analysis accepted as blinded primary analysis;
- no rerun-based selection among usable results.

## Current disposition

**DESIGN ADVANCED; IMPLEMENTATION NOT YET PROMOTABLE.**

The immediate next evidence task is to resolve the authoritative hosted-runner and timelock assumptions above. Until then, P4-T-A remains OPEN and no P7/freeze/P9 transition is permitted.
