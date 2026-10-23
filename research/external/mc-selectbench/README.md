# MC-SelectBench — Channel Selection Evaluation (proposal v0.1)

**Status:** Research design only · NOT_RUN · No measured outcome · Not an MC Chat integration · Not independent validation.

**Inspired by:** Jean Charbonneau's October 8, 2026 article, *MC Chat: weaving several perspectives into one AI answer*. The article describes explicit perspective channels, word-interleaved streaming, logged corrections, and two-pass synthesis. We appreciate the idea and aim to evaluate it without assuming that visible channels are independent reasoning processes.

**Authorship and boundaries:** This is a separately scoped research proposal prepared within the [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) ecosystem. It is not affiliated with or endorsed by Jean Charbonneau or MC Chat. Original MC Chat repository cited in the article: https://github.com/TheLightFramework/MC-Chat — access was not verified on 2026-10-22 (GitHub returned 404). Channel names, API signatures, and implementations therefore remain provisional.

## Research question

Does a **preregistered task-matched selection of visible response channels** improve final answer quality over random-channel selection under matched token budgets, and beyond single-pass and two-pass controls?

The project is deliberately falsifiable: a random-channel tie, a failure against budget-matched baselines, degraded channel-to-answer fidelity, or unacceptable cost/reliability tradeoffs must be reported as such.

## Experiment at a glance

- **Exploratory pilot:** 40 development tasks, excluded from confirmatory inference.
- **Candidate confirmatory dataset:** 200 held-out tasks (40 each: technical correctness, code review, beginner explanation, creative work, evidence conflicts).
- **Conditions:** 8 arms (A–H); 3 generation attempts per held-out task and arm, per model (4,800 model-task-condition runs per model).
- **Primary comparison:** G (matched channels) versus F (random channels), paired by task.
- **Primary outcome:** blinded 0–100 answer-quality rubric; reliability, latency, costs, and channel-fidelity metrics reported alongside it.
- **Important:** 200 tasks is a planning number, not a power-validated sample size; simulate power after pilot.

## Arms

| Arm | Intervention | Why |
|---|---|---|
| A | Ordinary single-pass response | Minimal-overhead reference |
| B | Single-pass with matched output budget | Additional token-budget control |
| C | Two-pass response without perspective channels | Extra-call control |
| D | Two-pass with one channel | Channel-count control |
| E | Two-pass with 3 duplicate/equivalent channel instructions | Diversity ablation |
| F | Two-pass with 3 randomly sampled channels | **Primary control** |
| G | Two-pass with 3 preregistered task-matched channels | **Primary treatment** |
| H | Two-pass with 3 preregistered deliberately mismatched channels | Relevance sensitivity |

B–H must share total-output-token caps. Record actual usage, including provider caching and input tokens; avoid assuming comparable realized cost. Lock provider/model version, settings, context and source materials per comparison. Distinguish models' optional self-corrections from injected parser replay fixtures.

## Primary falsification rules

1. If G fails to outperform F by a statistically reliable, practically meaningful margin, **task-matched channel selection has not demonstrated benefit**.
2. If G exceeds A but not B/C, gains may be attributable to budget or an additional pass rather than channel selection.
3. If gains hold only in one category or model, claims must be limited to that setting.
4. If protocol-invalid or truncated runs disproportionately affect G, count and report them; do not silently exclude failures.
5. If synthesis omits critical caveats or contradictory findings, report fidelity failures even when average quality improves.
6. A nonsignificant superiority test does **not** establish equivalence.

Proposed initial meaningful-effect threshold: 5/100 quality points (must be fixed after pilot but before confirmatory testing). Predeclare two-sided alpha 0.05 for the primary paired comparison, with task-clustered bootstrap CIs and multiple-testing adjustment for any additional confirmatory endpoints. A favorable point estimate alone is not success. Run pilot-informed power simulations.

## Evidence and safeguards

Keep raw stream and SHA-256, parser corrections separately from model-authored edits, selected channel text, synthesis input, final answer, scorer identities/agreements, errors, timeouts, output tokens, cache information and latency. Preserve source integrity; do not infer independent cognition from visible perspectives. Include all assigned runs in intention-to-treat analyses.

**DGAF scientific ceilings remain unchanged:** independently validated DGAF efficacy is NOT_ESTABLISHED; HIGH_ASSURANCE is NOT_AUTHORIZED; this benchmark has not run and increments no scientific N.

## Collaboration invitation

We welcome feedback from the MC Chat maintainer on protocol compatibility, the appropriate benchmark task domains, channel naming, and whether a standalone, optional evaluation harness would be useful. Our intended first contribution is a small, reversible protocol-conformance fixture and scoring harness, **not** an architectural rewrite.

See [protocol](PROTOCOL.md), [proposed evidence schema](schema/run-record.example.json), and [example task](fixtures/evidence-example.json).
