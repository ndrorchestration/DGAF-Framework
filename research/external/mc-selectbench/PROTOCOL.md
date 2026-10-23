# MC-SelectBench v0.1 — preregistration draft

**Registration state: DRAFT / NOT_REGISTERED. Execution state: NOT_RUN.**

## Frozen design prerequisites

1. Confirm MC Chat repository and license, authoritative channel names, output parser rules, maximum channel count, correction replay semantics, and exact synthesis behavior. Record immutable source commit. Until then no compatibility claims.
2. Build 40 development and 200 separate held-out tasks; enforce category stratification and hash fixture corpus. Avoid data leakage and scoring prompt contamination.
3. Freeze eight arm prompts, channel mappings, randomization seed, generation budgets, model snapshots, evaluator rubrics, exclusion rules, thresholds, and preplanned analysis. No held-out outcome may influence these choices.
4. Use 3 generation attempts per task/arm/model, shuffled in blocks. Task is statistical sampling unit, not each replicate. Preserve completed and failed runs, including invalid streams.
5. For G, a deterministic mapping from task category to three channels must be preregistered. F samples three distinct channels at random from that same eligible pool without task access; H uses a fixed rotated mapping. D has one channel. E represents nominally distinct slots with identical semantic instructions if literal duplicates are forbidden.
6. Cost-equivalent conditions must receive fixed maximum total output tokens. Record realized input/output tokens and API calls; analyze efficiency separately. If token budgets cannot be meaningfully matched, disclose this and downgrade budget-controlled claims.

## Outcomes and grading

**Primary endpoint:** blinded mean answer quality on 0–100 scale, combining correctness (40), requirements coverage (25), usefulness (20), and clarity (15). Freeze task-specific anchors and weighting before launch. Two independent blinded human graders for subjective dimensions, adjudication by preregistered policy; automatic checks where available.

**Secondary:** claim correctness, requirement coverage, channel-to-synthesis finding retention, contradiction/uncertainty disclosure, protocol validity, end-to-end task success, latency and monetary cost. Critical-finding retention candidate threshold 95% on predefined tasks. Where corrections are naturally emitted, measure their effect descriptively; synthetic correction traces only test parser/replay.

**Primary estimand:** mean difference in task-aggregated quality, G − F. Compute task-wise mean over 3 replicates, stratified paired bootstrap confidence intervals, 2-sided 0.05 test. Preregister a practical 5-point improvement threshold; report estimate and interval in addition to p value. Require prespecified absence of unacceptable reliability regression. If confirming several other hypotheses, adjust within declared family by Holm.

## Interpretation / falsification

- G ≤ F or imprecise confidence interval: no demonstrated benefit.
- G > A, but ≈ B or C: extra computation or second pass plausible explanation.
- D/E match G: selected channel diversity mechanism unsupported.
- H matches G: task relevance mechanism unsupported.
- Significant protocol failure, missing safety caveats, or cost blowout: qualified or adverse finding even if quality improves.
- One model or category drives result: restrict claim to model/category; no blanket superiority.
- No equivalence claim from absence of significance; preregister equivalence margin and TOST separately if needed.

## Evidence custody

For each run, store raw bytes, stream integrity hash, decoded events, parser repairs, model-authored corrections, discarded invalid events, selected channel outputs, synthesis input, answer and scorer IDs, scoring rationales and error metadata. Never relabel synthetic tests as independent external replication. Publication must include caveats and a frozen evidence manifest.

## Explicit nonclaims

No outcome is reported. No claim of separate internal agents, independent reasoning, higher correctness, external validation, safety proof, or DGAF high assurance. This is a protocol designed to *test* hypotheses, not evidence for them.
