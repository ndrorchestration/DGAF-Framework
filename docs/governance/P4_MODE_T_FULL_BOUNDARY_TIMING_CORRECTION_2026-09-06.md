# P4 Mode T Full-Boundary Timing Correction — 2026-09-06

**Status:** CURRENT-LINEAGE CORRECTION / PREDECLARATION / NONCANONICAL / NO NUMERIC W  
**Issues:** #293, #296  
**Historical provenance:** draft PR #306; reconstructed after merged current-lineage timing PR #547  
**Scientific boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Why this correction exists

Expert-panel review found a material scope mismatch in the component synthetic timing evidence.

Canonical `experiments/pdmal_pilot/run_pilot.py` executes root seeds sequentially. For each seed it executes all 5 topologies × 4 conditions × 9 failure counts = 180 trials before advancing to the next seed. The planned full pilot uses 50 paired root seeds, so the complete canonical task-execution shape is:

```text
50 seeds × 180 trials/seed = 9,000 trial executions
```

The current component `mode_t_timing_study.py`, restored on current lineage by #547, times one 180-trial seed-shaped matrix per repetition. Its evidence is valid bounded one-seed engineering timing, not complete-pilot timing evidence.

This distinction is load-bearing because Mode T requires an analysis lock before the frozen timelock release. Underestimating the pre-release workload can produce an unsafe `W` even when every measured component is individually correct.

## Additional full-boundary gaps

The component lanes do not yet establish one contiguous monotonic timing interval from the authorization-consumption-equivalent boundary through independently verified analysis lock.

Before any numeric `W` proposal, the accepted correction must include all work that occurs after the C-equivalent boundary and before the L-equivalent boundary, including:

1. any runtime identity/prerequisite re-verification required after C;
2. protected-material generation and timelock encryption using synthetic non-protected fixtures only;
3. all 50 sequential seed executions using the exact canonical task path, unless canonical execution semantics are separately changed and frozen;
4. creation of the complete synthetic blinded artifact set and summary with sizes representative of the canonical runner;
5. publication and accepted independent retention of the relevant complete artifact set, not only a ciphertext-sized proxy;
6. locked primary analysis over 50 schema-valid synthetic seeds with the frozen bootstrap configuration;
7. L-equivalent transparency/retention submission, retrieval, and verification;
8. one contiguous monotonic full-boundary duration spanning the entire accepted sequence.

Component timings remain useful diagnostics, but they cannot substitute for the controlling contiguous full-boundary measurement.

## Required correction invariants

The corrected apparatus must fail closed unless all of the following are true:

- synthetic pilot seed count is exactly 50;
- trial count per seed is exactly 180;
- total trial executions per full-pilot repetition are exactly 9,000;
- seed execution order matches the canonical sequential `run_pilot.py` semantics unless a later canonical change explicitly supersedes this requirement;
- no real empirical observation is executed or serialized;
- no real blinding key, mapping, nonce, or protected ciphertext is instantiated;
- synthetic scientific outcomes are not promoted into timing evidence beyond the minimum schema-shaped fixtures necessary to exercise the path;
- exact repository/helper/workflow/dependency identities are recorded;
- full-boundary timing uses a monotonic clock;
- publication/retention evidence is exact-run/head/tool bound and independently retrievable/re-hashable under the accepted mechanism;
- failed or partial retention/transparency work cannot become PASS;
- retries cannot hide a slow or failed post-C-equivalent attempt;
- `coverage_complete=false`, `w_proposal_eligible=false`, `numeric_w_selected=false`, and `proposed_w_seconds=null` remain controlling until every required stage and review condition is satisfied.

## Treatment of component evidence

Existing component timing artifacts are **not discarded**. Their interpretation is bounded:

- one-seed synthetic matrix timing: valid for that one-seed component only;
- locked-analysis timing: valid for the exercised synthetic analysis component only;
- synthetic tlock-encryption timing: valid for that component only;
- ciphertext-sized GitHub publication timing: valid for that specific transport fixture only;
- none of these individually or by naïve summation is accepted as the complete `C → L` Mode-T timing bound.

The #547 current-lineage artifact remains valid within those component scopes. No one-seed timing artifact may be relabeled as complete-pilot or W-eligible evidence.

## Repetition and degraded-condition discipline

This correction deliberately does not choose a numeric `W` or a final statistical bound.

Before a numeric W may be proposed:

1. the corrected full-boundary apparatus must pass exact-head engineering validation;
2. normal-condition full-boundary repetitions must be completed under a predeclared count;
3. degraded-but-accepted conditions must be defined before their timing is observed and then repeated under the same exact apparatus identity;
4. the final bound/quantile and safety-margin rule must be documented before adjudicating a numeric W;
5. an independent review must confirm that the rule is conservative and was not outcome- or convenience-selected;
6. any material helper/toolchain/execution-semantics change invalidates transfer of the prior timing distribution unless explicitly revalidated.

The design should prefer a deliberately conservative policy over optimizing W tightly. A late analysis lock invalidates the pilot; it must never cause the release round to be moved after C.

## Anti-drift rules

Future documentation and automation must not say that:

- 180 trials represent the complete 50-seed pilot;
- a one-seed timing artifact measured the complete pilot;
- GitHub publication transport establishes durable custody or full blinded-artifact retention timing;
- component timing sums are a measured contiguous C→L duration;
- a numeric W has been selected;
- Mode T custody is accepted;
- freeze or pilot authorization exists;
- empirical N is greater than zero.

Any such claim is a status error and must fail review.

## Promotion boundary

The restored 50-seed task-shape timing is still only bounded engineering evidence. Even successful 9,000-trial timing does not establish the complete C→L boundary, Mode-T custody sufficiency, W, freeze, authorization, or efficacy.

Only after Mode T is admitted, complete full-boundary timing is accepted, W is independently reviewed and frozen, and the separate verification/authorization sequence completes may empirical execution occur.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
