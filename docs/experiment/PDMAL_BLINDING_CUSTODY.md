# PDMAL Blinding Custody and Separation-of-Control Record

## Status

**PRE-FREEZE / v0.7.6 BLINDING CORRECTION UNDER REVIEW / OPERATIONAL CUSTODY OPEN / N=0**

This record distinguishes four separate claims that must not be collapsed:

1. a deterministic test-only blinding primitive exists;
2. the proposed v0.7.6 pilot artifact no longer deterministically reveals condition identity through public ordering/metadata;
3. operational custody/effective control separation prevents a pre-release actor from obtaining the protected mapping or secret;
4. unblinding/release occurs only after the accepted analysis-lock boundary.

Only the first claim is historical established engineering evidence. Claims 2–4 remain pre-freeze gates until the exact candidate apparatus and custody mechanism are independently verified.

## Historical contract-only primitive

`experiments/pdmal_pilot/harness_contract.py` contains an older deterministic HMAC-SHA256 helper used by pre-freeze contract tests. It is useful engineering evidence that opaque identifiers can be produced with a test key, but it is **not the current pilot blinding contract** and must not be used as evidence that operational custody or v0.7.6 noninterference is closed.

Historical synthetic/contract artifacts produced with that helper remain evidence only for their exact historical apparatus identities.

## Proposed v0.7.6 pilot blinding contract

Issue #307 identified deterministic identity channels in the pre-freeze pilot apparatus: public trial order/`trial_id` encoded the named condition order, and `governance_trace` could directly single out the DGAF treatment. No empirical run had occurred when the defect was discovered.

Draft PR #308 proposes protocol `0.7.6` and public pilot artifact schema `1.1` with the following requirements:

### Protected key

- production `PDMAL_BLINDING_KEY` must contain at least 32 characters;
- the operational value must not be committed, printed, or included in normal artifacts;
- condition identifiers and trial ordering use separate HMAC domains.

### Domain-separated condition identifiers

```text
HMAC-SHA256(
  protected_key,
  "PDMAL-BLINDED-CONDITION-ID-v1" || "|" || condition
)
  -> blind_<first-16-hex-digest-characters>
```

### Secret-keyed per-seed trial schedule

The scientific matrix remains exactly 5 topologies × 4 conditions × 9 failure counts = 180 cells per seed.

For each seed, every canonical cell receives an HMAC-SHA256 ordering token under the separate domain:

```text
PDMAL-BLINDED-TRIAL-ORDER-v1
```

bound to:

```text
(seed, topology, condition, failure_count)
```

The 180 cells are executed and serialized in ascending token order. `trial_id` is assigned only after this protected permutation is constructed. Public seed/source information alone therefore cannot reconstruct the named-condition position. Any token collision or incomplete/duplicate matrix is fail-closed.

After authorized release of the protected key/mapping material, the exact label mapping and per-seed schedule are independently reconstructible.

### Public blinded artifact minimization

The v0.7.6 public seed artifact is an exact allowlist. It excludes at minimum:

- plaintext named condition;
- plaintext condition mapping;
- `governance_trace`;
- per-trial `runtime_ms`;
- any unexpected record or document field.

The predeclared outcome surface and matrix coordinates remain available under opaque condition identifiers because they are required by the locked primary analysis. The protocol does **not** claim that outcome patterns can never support subjective guesses about condition identity; it claims that avoidable deterministic metadata channels must be absent.

## Operational custody is a separate gate

Correct artifact blinding does not by itself solve custody. The protected key/mapping and any protected pre-release evidence must remain outside the effective control of an actor who could use them before the accepted analysis-lock/release boundary.

The repository is currently evaluating Mode T under Issue #287. Standard GitHub-hosted execution has not established the required effective control separation. A confidential-computing execution substrate such as a production attested Confidential Space workload is a design candidate because it may generate the protected secret inside an accepted workload and reject debug/override identities, but that design remains **NOT EXECUTED / NOT ACCEPTED** until its exact threat model and implementation are independently verified.

A technical control may satisfy a role boundary; separate human friends/collaborators are not intrinsically required if the accepted mechanism demonstrably removes effective pre-release access from the operator. Conversely, merely naming separate roles does not establish separation.

## Required control roles / functions

| Function | Required access boundary |
|---|---|
| Authorization / C issuer | Creates the single-use authorization/reservation record; must not receive protected outcomes or mapping as a side effect. |
| Accepted executor | Executes only the exact frozen apparatus under the accepted run identity. Protected material may exist inside this boundary only as required by the protocol. |
| Pre-release analyst / analysis-lock function | Computes the frozen primary analysis without exposing the protected condition mapping to a mutable operator before lock. |
| Custody / release mechanism | Prevents release of mapping/key material until the frozen release predicate is satisfied. |
| Independent verifier | Verifies exact apparatus/run/attestation/artifact/retention bindings and cannot convert missing evidence into PASS. |

These functions may be implemented by humans, services, attested workloads, or combinations thereof, but the effective access/control separation must be evidenced for the exact chosen mechanism.

## Protected mapping / secret lifecycle

The accepted design must make the following lifecycle concrete and auditable:

```text
protected key / mapping
        |
        +-- not committed to Git
        +-- not emitted in CI/application logs
        +-- not included in normal blinded artifacts
        +-- unavailable to the pre-release operator/analyst under the accepted threat model
        +-- bound to the exact accepted run / authorization record
        +-- released only after the accepted analysis-lock predicate
        +-- independently verifiable after release
```

If Mode T uses secret-born-inside-an-attested-workload semantics, the protected secret should not exist before the accepted workload generates it. That design is preferable to relying on a mutable external secret store controlled by the same operator, but it is not accepted until demonstrated.

## Analysis-lock / unblinding boundary

Unblinding may occur only after all accepted pre-release predicates are satisfied. At minimum the final design must bind:

1. exact frozen apparatus/candidate identity;
2. valid single-use authorization/reservation C;
3. exact accepted execution identity;
4. complete blinded observation/artifact set and integrity commitments;
5. frozen preprocessing/exclusion rules;
6. exact locked primary-analysis implementation/configuration;
7. durable publication/retention evidence where required;
8. analysis-lock L created before the frozen release boundary;
9. independent verification that C→L continuity and release conditions were satisfied;
10. explicit accepted release/unblinding event.

The operational secret itself must never appear in the unblinding record.

## Access-control / noninterference verification

Before freeze, the exact candidate must demonstrate separately that:

- production blinding key length/domain requirements are enforced;
- public `trial_id`/record order cannot reconstruct named condition order from public source alone;
- public records reject treatment-specific trace/runtime fields and all unexpected fields;
- changing execution order does not change deterministic per-cell scientific outcomes;
- the operator cannot obtain the accepted run's protected mapping/key before release under the chosen custody threat model;
- debug/override/restart/substitution paths cannot become accepted runs;
- repository/CI logs and normal artifacts contain no protected key/mapping material;
- the accepted retention/transparency mechanism can be independently retrieved and re-hashed;
- release of the correct protected material reconstructs the exact mapping/schedule after lock;
- missing or partial evidence remains FAIL/BLOCKED/UNKNOWN rather than being inferred as PASS.

## Current evidence state

| Control | Current status | Evidence boundary |
|---|---|---|
| Historical contract-only HMAC helper | **IMPLEMENTED / ENGINEERING ONLY** | `harness_contract.py`; not the v0.7.6 pilot contract. |
| v0.7.6 deterministic metadata-leak correction | **DRAFT / UNDER EXACT-HEAD VERIFICATION** | Issue #307 / draft PR #308. |
| v0.7.6 key-length/domain separation | **DRAFT / UNDER EXACT-HEAD VERIFICATION** | PR #308 runner/tests. |
| Secret-keyed 180-cell schedule | **DRAFT / UNDER EXACT-HEAD VERIFICATION** | PR #308 runner/tests. |
| Exact public artifact allowlist | **DRAFT / UNDER EXACT-HEAD VERIFICATION** | proposed schema 1.1. |
| Operational custody / effective control separation | **OPEN / UNKNOWN** | Issue #287 Mode-T admission remains unresolved. |
| Accepted analysis-lock window W | **OPEN** | corrected 50-seed task-shape timing exists, but complete C→L timing is not established. |
| Authorized unblinding/release event | **NOT EXECUTED** | no empirical pilot exists. |

## Freeze criterion

The P4 blinding/custody gate cannot be marked PASS merely because an HMAC helper or a green unit test exists. Before freeze, the exact candidate must have:

- Issue #307 remediated and independently adversarially verified;
- a selected and accepted custody/control-separation mechanism;
- complete candidate-bound P4 evidence;
- accepted C→L timing/window rule for Mode T if Mode T is selected;
- candidate-scoped P7/P8/P9 identities regenerated after the v0.7.6 apparatus change;
- durable evidence and independent verification required by the closure matrix.

Until then:

```text
v0.7.6 blinding correction:  UNDER REVIEW
Operational custody:         OPEN / UNKNOWN
Protocol freeze:             NOT ESTABLISHED
Pilot authorization:         NOT GRANTED
Empirical N:                 0
```

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
