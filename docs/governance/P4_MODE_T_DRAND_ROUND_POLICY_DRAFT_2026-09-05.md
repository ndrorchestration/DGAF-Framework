# P4 Mode T drand Release-Round Policy Draft — 2026-09-05

**Status:** DRAFT / NONCANONICAL / SYNTHETIC-ONLY  
**Issue:** #287  
**Scientific boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Define a deterministic release-round selection rule that cannot be chosen after observing empirical outcomes and that provides a machine-checkable ordering target for P4-T-L analysis lock.

This draft deliberately does **not** choose the final analysis-lock window duration. That duration remains an OPEN pre-freeze protocol parameter and must be frozen before any empirical execution.

## Frozen quicknet clock

The reviewed quicknet identity is:

```yaml
chain_hash: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971
genesis_time_unix: 1692803367
period_seconds: 3
```

Source: [drand quicknet launch record](https://docs.drand.love/blog/2023/10/16/quicknet-is-live/).

drand documents the current-round relationship as a function of current timestamp, genesis timestamp, and period. For the frozen quicknet parameters, round `r >= 1` corresponds to deterministic nominal round time:

```text
round_time(r) = genesis_time_unix + (r - 1) * period_seconds
```

The first round whose nominal time is at or after target Unix timestamp `t` is:

```text
first_round_at_or_after(t) = ceil((t - genesis_time_unix) / period_seconds) + 1
```

with round 1 used for timestamps at or before genesis.

## Why authorization-consumption time is the anchor

The release round must be selected before any real key, mapping, or commitment nonce exists. Using the later X execution timestamp would create an unnecessary dependency between secret generation and release selection.

The proposed anchor is therefore the independently verified transparency-log integration time of **C — authorization consumption**, because C is published after exact-run authorization validation but while `secret_instantiation_status` is still `NOT_EXECUTED`.

Let:

- `T_C` = independently verified C transparency integration Unix time;
- `W` = frozen `analysis_lock_window_seconds`, selected before freeze;
- `T_target = T_C + W`.

Then:

```text
release_round = first_round_at_or_after(T_target)
release_time = round_time(release_round)
```

The P4-T-X helper may generate protected material only after it has verified C and deterministically derived this release round from the frozen policy.

## Analysis-lock ordering rule

P4-T-L succeeds only if the independently verified transparency-log integration time of L satisfies:

```text
T_L < release_time
```

Strict inequality is required. An L entry integrated at or after the release time is too late and the pilot is invalid for primary blinded interpretation.

A self-authored timestamp inside R/A/C/X/L is never sufficient for this comparison.

## Window-selection rule — still OPEN

`analysis_lock_window_seconds` is a load-bearing protocol value and must not be invented from convenience.

Repository apparatus currently contains a **per-seed** runtime ceiling of 300 seconds (`SEED_RUNTIME_CEILING_SECONDS`) in `experiments/pdmal_pilot/task_engine.py`. That is not a bound on the complete blinded pilot plus artifact retention plus primary analysis, so it is insufficient by itself to select W.

Before W can be frozen, a synthetic-only timing study must establish conservative upper bounds for the exact frozen workflow covering:

1. reservation/authorization/consumption transparency operations;
2. P4-T-X secret generation and timelock encryption overhead on synthetic fixtures;
3. the full canonical blinded matrix execution path under its intended parallelism;
4. ciphertext/blinded-artifact publication and independent retention;
5. frozen primary-analysis runtime on a schema-valid synthetic matrix;
6. Sigstore/Rekor submission/verification latency under ordinary and degraded-but-accepted conditions;
7. a predeclared safety margin.

The timing study is engineering evidence, not efficacy evidence, and must use synthetic data only.

W must be fixed before the immutable freeze. It may not be extended after C because execution is slow or analysis is incomplete; failure to produce L before release invalidates the pilot rather than moving the release.

## Failure rules

- C transparency time unavailable or unverifiable → **STOP / NO SECRET**.
- Frozen W missing, zero, negative, or changed → **STOP / NO SECRET**.
- quicknet chain/genesis/period mismatch → **STOP / NO SECRET**.
- selected release round not exactly reproducible from C and W → **STOP / NO SECRET**.
- timelock client encrypts to a different chain or round → **PILOT INVALID**.
- L transparency time unavailable → **PILOT INVALID / NO PRIMARY INTERPRETATION**.
- `T_L >= release_time` → **PILOT INVALID / NO PRIMARY INTERPRETATION**.
- delayed/unavailable beacon publication does not retroactively make a late L valid; the ordering predicate remains against the frozen nominal round time unless a separately reviewed protocol rule says otherwise before freeze.

## Anti-manipulation properties

This rule prevents the analyst from:

- choosing the release round after seeing outcomes;
- extending the deadline because analysis is not finished;
- backdating L with a payload field;
- silently changing quicknet identity;
- treating a delayed beacon as permission for post-deadline primary analysis.

It does not prove the drand threshold-network security assumption or resolve the remaining live-runner-memory UNKNOWN.

## Current disposition

**Release-round algorithm specified; final numeric W remains OPEN pending synthetic timing evidence.**

No real timelock ciphertext, secret, empirical workload, freeze, authorization, unblinding, or empirical observation has been created by this draft.
