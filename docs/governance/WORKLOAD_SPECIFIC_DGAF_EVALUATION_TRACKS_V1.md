# Workload-Specific DGAF Evaluation Tracks v1

**Status:** NONEMPIRICAL CANDIDATE ARCHITECTURE  
**Controller:** Issue #394  
**Scientific N increment:** 0  
**Empirical authorization:** FALSE

## Decision

Future DGAF/PDMAL evaluation SHALL use workload-specific treatment profiles. A gate may only be included when the workload supplies the gate's actual source-bound substrate and, for stateful gates, the required state persists for the declared lifetime.

The prior `DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1` remains preserved as the exact historical Epoch 004 profile. It is not rewritten, deleted, or pooled into future profiles, but it is not eligible for future canonical use because the seven-gate fidelity audit established that six constitutive gate bindings were not semantically established in that workload.

## Global rules

1. No gate without a source-bound workload substrate.
2. No numeric proxy for a semantic gate input.
3. No semantic proxy for weighted graph state.
4. Stateful gates declare state lifetime and reset semantics.
5. Excluded gates are explicitly out of scope, not represented as default PASS.
6. P-30/11Q is an external profile qualification control, not a per-turn efficacy signal.
7. Any empirical track requires a new profile identity, new qualification, fresh preregistration, fresh seeds, and separate execution authorization.

## Track A — PDMAL topology robustness

**Profile:** `PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1`

Purpose: characterize topology and failure-recovery behavior in the numeric distributed-consensus apparatus.

The workload contains numeric agent state, topology, neighbor relations, deterministic failure/recovery schedules, iteration, and seed. It does **not** claim to be a semantic DGAF governance workload.

### Gate disposition

| Component | Disposition |
|---|---|
| P-31 SCPE | Out of scope: no token/tier context |
| P-33 Convergence | Evaluated separately under B3, not used as a consensus-update proxy |
| DemiJoule | Out of scope: no semantic payload |
| P-27 KAPPA | Out of scope: no evaluation-record weight consumer |
| P-29 Sentinel | Out of scope: no routing/risk/deontic record |
| P-32 Phi Closure | Out of scope unless separately specified with persistent closure state |
| P-30 | External profile qualification only |

The labels `dgaf`, `full_dgaf`, and `canonical_dgaf` are prohibited for Track A treatment conditions.

**Claim ceiling:** topology/failure robustness only; no DGAF efficacy claim.

## Track B1 — semantic routing and safety

**Profile:** `DGAF_SEMANTIC_ROUTING_SAFETY_PROFILE_V1`

Purpose: evaluate gates whose historical semantics operate directly on structured semantic/evaluation records.

Required workload fields include content, entropy/kappa signals, the five KAPPA score dimensions, and deontic/risk context.

Included:
- DemiJoule semantic safety;
- P-27 KAPPA v3.6;
- P-28 evaluation pipeline;
- P-29 Sentinel;
- external P-30 profile qualification.

Excluded:
- P-31 and P-32, which require persistent multi-turn context under B2;
- P-33, which requires persistent weighted-graph state under B3.

**Claim ceiling:** record-level routing and safety behavior only.

## Track B2 — stateful context and closure

**Profile:** `DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1`

Purpose: evaluate P-31 SCPE and P-32 Phi Closure on a true multi-turn semantic session.

Required state must persist for one complete session and reset only at the session boundary:
- SCPE token/tier store;
- token insertion timestamps and trust edges;
- Phi stable/total counters;
- Phi consecutive-failure state;
- explicit `is_stable` input.

Included:
- P-31 SCPE;
- P-32 Phi Closure;
- external P-30 profile qualification.

**Claim ceiling:** state persistence, pruning and closure behavior only.

## Track B3 — graph convergence monitor

**Profile:** `DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1`

Purpose: evaluate P-33 on a sequence of persistent weighted-graph snapshots.

Required state:
- `W_t`;
- `W_{t-1}`;
- consecutive stable/divergent counters;
- event history.

P-33 status must not be mapped to a consensus mixing alpha or efficacy effect without a separately governed specification.

**Claim ceiling:** monitor fidelity and alert behavior only.

## Track C — integrated DGAF system

**Profile:** `DGAF_INTEGRATED_WORKLOAD_PROFILE_V1`

Deferred. It may be specified only after A, B1, B2 and B3 have each passed their own source-bound qualification and non-empirical validation, and only with an explicit cross-track interface that introduces no proxy inputs.

## Epoch 004 boundary

Epoch 004 remains immutable evidence for the exact restored-binding treatment that actually ran.

Preferred wording:

> Evidence against the preregistered directional hypothesis for the exact Epoch 004 restored-binding treatment under the Solo developer apparatus; subsequent source audit found seven-gate canonical treatment fidelity not established.

This architecture does not reanalyze or rescue that result.

## Next sequence

1. Merge this architecture only after exact-head validation.
2. Adjudicate #390 as a PDMAL mapping issue, not a KAPPA component defect.
3. Build non-empirical Track A contract tests.
4. Build B1 semantic fixtures against the actual KAPPA/evaluation/Sentinel pipeline.
5. Build B2 persistent-session harness.
6. Build B3 persistent weighted-graph harness.
7. Run source-bound P-30/11Q qualification for each profile.
8. Only then preregister any fresh empirical epoch.

## Current boundary

`EPOCH_004_PRIMARY_RESULT = PRESERVED`  
`SEVEN_GATE_TREATMENT_FIDELITY = NOT_ESTABLISHED`  
`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`  
`FRESH_CANONICAL_EMPIRICAL_EPOCH = PROHIBITED`  
`HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`
