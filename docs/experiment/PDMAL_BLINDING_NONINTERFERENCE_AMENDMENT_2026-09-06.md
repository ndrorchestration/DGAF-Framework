# PDMAL Blinding Noninterference Amendment — 2026-09-06

**Status:** PRE-FREEZE / PROPOSED APPARATUS CORRECTION  
**Issue:** #307  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0

## Purpose

Correct deterministic condition-identity side channels in the pre-freeze pilot artifact before any P4/P7 final binding, freeze, authorization, or empirical execution.

The current apparatus HMAC-blinds the condition label, but the public trial schedule, integer `trial_id`, record order, and treatment-specific `governance_trace` can reconstruct or directly signal condition identity without the blinding key. Because empirical N is still zero, the apparatus can be corrected without contaminating an observation.

## Controlling noninterference principle

Before the authorized unblinding/release boundary, a pilot artifact may expose the predeclared outcome surface under opaque condition identifiers, but **public non-outcome metadata must not deterministically reconstruct a named condition from public source/protocol information alone**.

Blinding is not claimed to make all subjective inference from outcome patterns impossible. The requirement here is narrower and enforceable: eliminate avoidable deterministic identity channels created by the apparatus itself.

## Protected key contract and HMAC domains

The production pilot runner must fail closed unless `PDMAL_BLINDING_KEY` contains at least 32 characters, preserving the existing minimum-key contract already documented elsewhere in the repository.

The same protected key may support both label blinding and trial ordering only through explicit domain separation:

```text
condition identifier domain = PDMAL-BLINDED-CONDITION-ID-v1
trial ordering domain       = PDMAL-BLINDED-TRIAL-ORDER-v1
```

A raw `HMAC(key, condition)` construction is not the v0.7.6 contract. The condition identifier is derived from the condition-ID domain plus the condition name; the ordering token is derived independently from the trial-order domain plus the complete cell identity.

## Secret-keyed trial schedule

For each seed, the complete canonical 180-cell matrix remains unchanged:

```text
5 topologies × 4 conditions × 9 failure counts = 180 cells
```

The runner must construct all canonical cells first and then derive a per-cell ordering token using HMAC-SHA-256 under the protected blinding key with the trial-order domain separator and the tuple:

```text
(seed, topology, condition, failure_count)
```

The 180 cells are executed and serialized in ascending ordering-token order. Any ordering-token collision is fail-closed.

Properties:

- same protected key + seed + frozen matrix → identical schedule;
- different protected key or seed → independently keyed schedule;
- public seed alone cannot reconstruct the schedule;
- `trial_id` is the integer execution position in this protected schedule, not the canonical condition position;
- after authorized release of the protected mapping/key material, the exact schedule is independently reconstructible.

A public RNG stream derived only from the root seed is not sufficient for blinding because the analyst knows the root seed and implementation.

## Public blinded artifact minimization

The pre-unblinding public seed artifact must not contain plaintext treatment-specific diagnostic material.

Specifically:

- `governance_trace` is prohibited from the public blinded record;
- per-trial `runtime_ms` is prohibited from the public blinded record because it is not required for the primary FFCR analysis and can be condition-correlated;
- the seed-level aggregate `runtime_seconds` may remain because it does not identify a condition within the seed;
- the public artifact schema must reject **unexpected fields**, not merely require a minimum field set.

If detailed treatment traces or per-trial timing are later required for execution audit, they must be specified as a separately protected evidence surface whose pre-release representation does not reveal condition identity. No such new protected surface is implicitly accepted by this amendment.

## Public record contract

The blinded record retains only the fields currently required for integrity, matrix identity, the predeclared outcome surface, exclusion semantics, and environment binding. The record hash covers the exact allowed record.

No field outside the exact schema allowlist may be serialized into a validated public blinded record.

The schema revision for this correction is `1.1`.

## Adversarial acceptance tests

The corrected apparatus must demonstrate at minimum:

1. the schedule contains every canonical matrix cell exactly once;
2. schedule derivation is deterministic for the same seed/key;
3. schedule derivation changes when the protected key changes;
4. schedule derivation changes across seeds;
5. the protected schedule is not the canonical topology→condition→failure ordering for the fixed regression fixture;
6. `trial_id` spans exactly `0..179` but indexes the protected schedule;
7. a short production blinding key is rejected before archive/pilot execution;
8. the condition-ID HMAC is domain-separated from the legacy raw-condition construction and from the schedule HMAC;
9. unexpected public fields are rejected by the artifact validator;
10. explicit attempts to add `governance_trace` or `runtime_ms` fail validation;
11. public record construction contains neither field;
12. a complete fixed-seed 180-cell run produces identical per-cell results under canonical order and the protected permutation;
13. primary analysis remains independent of record order and `trial_id` condition semantics;
14. release of the correct protected key can reconstruct both blinded labels and the exact trial schedule;
15. no test or implementation creates empirical observations, freeze, authorization, or unblinding state.

## Outcome-inference limitation

Even after deterministic metadata leaks are removed, an analyst who sees blinded outcomes might form guesses about which condition is DGAF or a control. The protocol must not overstate blindness as mathematically perfect concealment against statistical inference.

For Mode T, the stronger candidate lifecycle remains to perform the pre-release primary analysis inside an accepted attested execution environment and lock that analysis before releasing condition identity. That separate custody design does not weaken this artifact-level noninterference requirement.

## Effect on existing evidence

Historical synthetic/engineering artifacts remain evidence only for their exact prior apparatus identities. They do not demonstrate the corrected blinding contract.

No empirical pilot artifact exists, so there is no empirical record to migrate or reinterpret.

Any final candidate must repeat all candidate-scoped validations affected by this apparatus change before P7 final binding.

## Hard boundary

This amendment does not close P4 or P7, establish a freeze, grant authorization, execute the pilot, or increase N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
