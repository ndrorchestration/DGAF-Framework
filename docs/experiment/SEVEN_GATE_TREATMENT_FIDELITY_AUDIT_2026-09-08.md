# Seven-Gate PDMAL Treatment Fidelity Audit — 2026-09-08

**Classification:** `POST_EMPIRICAL_SOURCE_AUDIT / NON_EMPIRICAL`  
**Controller:** Issue #392  
**Scientific N increment:** 0  
**Fresh empirical execution:** PROHIBITED pending adjudication

## Purpose

Epoch 004 executed the exact code and analysis it preregistered, and its negative primary result remains immutable evidence for that executed treatment. This audit asks a separate construct-validity question: did the seven constitutive TGL gates receive and preserve the historical/canonical substrate their own restored contracts require?

This audit does not change Epoch 004 data, rerun analysis, tune a threshold, or authorize a new experiment.

## Source identities

- Epoch 004 runner source blob: `eaedb40862684c33b3bff08d294338c74f7c9d92`
- Epoch 004 adapter blob: `95dc2f05196fe1df054fa9677bdfcd5d4d188081`
- Restored gate binding blob: `11677608141e53de0a963eb62d6c5fbfa70f211b`
- Mechanism diagnostic artifact: `10040466222`
- Mechanism artifact digest: `sha256:d150323e9cdd9ba641cf9aa7a2deb1a8cc5f29871fdff1821a50cf3a1a8e1b07`

## Integration fact

`CanonicalEpoch004Task._dgaf_update` constructs a new `ConsensusState` on every consensus iteration and does not explicitly pass any of the gate-state dataclasses. Their default factories therefore create fresh SCPE, convergence, Sentinel, KAPPA, DemiJoule, and Phi state each turn.

The restored binding module, by contrast, explicitly describes SCPE, P-33 convergence, Sentinel, KAPPA, and Phi state as substrate that is carried in `ConsensusState`, and its P-33/P-32 implementations rely on cross-turn state.

## Gate-by-gate fidelity matrix

| Gate | Required/restored substrate | Epoch 004 supplied substrate | Persistence | Diagnostic behavior | Fidelity |
|---|---|---|---|---|---|
| P-31 SCPE | token/tier store, insertion time, trust-edge state | default empty token store | fresh each iteration | PASS every traced turn | **NOT ESTABLISHED** |
| P-33 Convergence | current weighted graph, prior weights, divergence/stability counters/events | default empty weights/prev_weights/counters | fresh each iteration | PASS every traced turn | **NOT ESTABLISHED** |
| DemiJoule | semantic source payload for six-axis safety evaluation | no `payload` in PDMAL context; hook falls back to canonical serialized consensus state text | state fresh each iteration | PASS every traced turn | **NOT ESTABLISHED** |
| P-27 KAPPA | P-27/P-28 evaluation-record routing inputs and confidence pipeline | zero-default carried scalar fields; no evaluation score-vector consumer | fresh each iteration | WARN 9,000/9,000; drives CONSERVATIVE_MIX | **NOT ESTABLISHED — #390** |
| P-29 Sentinel | record category, KAPPA routing policy/confidence, hook point, deontic state | defaults `record_category=None`, `routing_policy=None`, permitted; no sentinel/risk decision in context | fresh each iteration | PASS every traced turn | **NOT ESTABLISHED** |
| P-32 Phi Closure | persistent stable/total/checkpoint/failure counters plus meaningful `is_stable` input | fresh zero counters; context omits `is_stable`, so hook defaults it to `True` | fresh each iteration | PASS every traced turn; checkpoints never accumulate | **NOT ESTABLISHED** |
| P-30 Apogee | source-bound external P-11/11Q qualification under the reconciled canonical definition | exact qualification bytes/digest/profile/source bound in Epoch 004 adapter | intentionally external qualification, not turn-state accumulation | PASS every traced turn | **ESTABLISHED — DEVELOPER SELF-ATTESTED / NON-INDEPENDENT** |

## Key negative findings

1. Hook implementation tests are not equivalent to end-to-end treatment-substrate tests.
2. The parity suite can prove a hook behaves correctly when manually supplied a substrate while the actual task never supplies that substrate.
3. Fresh construction of `ConsensusState` prevents the stateful P-33 and P-32 contracts from accumulating their historical turn state.
4. P-31's empty-token PASS is a no-op and does not establish execution of pruning semantics over a real context substrate.
5. DemiJoule is evaluating the canonicalized numeric state serialization because no semantic payload is supplied.
6. P-29's default state reduces to `risk_ok` in the absence of the historical routing/risk substrate.
7. P-27 is additionally version/provenance-misaligned and is governed separately by #390.
8. P-30's external 11Q qualification path is the one constitutive gate whose current Epoch 004 binding has already been explicitly reconciled and source-bound.

## Epoch 004 adjudication consequence

Epoch 004 remains a valid, reproducible negative result for the **exact executed restored-binding treatment**. It must not be deleted, rewritten, pooled away, or retrospectively reanalyzed to manufacture a different primary conclusion.

However, this audit does **not** support the stronger construct-validity claim that Epoch 004 exercised all seven constitutive canonical DGAF gate semantics faithfully. The broader claim `CANONICAL_DGAF_EFFICACY` therefore remains **NOT ESTABLISHED**.

Preferred wording for Epoch 004:

> Evidence against the preregistered directional hypothesis for the exact Epoch 004 restored-binding treatment under the Solo developer apparatus; seven-gate canonical treatment fidelity was subsequently found not established.

## Prospective consequence

Do not patch Epoch 004. Any corrected treatment requires:

1. explicit workload-specific treatment-profile specification;
2. source-bound gate-input mappings;
3. state-persistence contract for every stateful gate;
4. exclusion or explicit adaptation of gates whose historical substrate is absent;
5. new profile identity and 11Q qualification;
6. non-empirical multi-turn reachability/fidelity tests;
7. fresh preregistration and seeds;
8. separate empirical authorization.

No new canonical empirical epoch is authorized by this audit.

## Current boundary

`EPOCH_004_PRIMARY_RESULT = PRESERVED`  
`SEVEN_GATE_TREATMENT_FIDELITY = NOT_ESTABLISHED`  
`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`  
`FRESH_CANONICAL_EMPIRICAL_EPOCH = PROHIBITED`  
`HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`
