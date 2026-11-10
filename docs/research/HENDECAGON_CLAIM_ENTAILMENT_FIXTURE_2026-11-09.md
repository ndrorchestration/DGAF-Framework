# Hendecagon claim-entailment fixture — research protocol v0.1

> **Status:** DESIGN ONLY / SAME-SYSTEM PROVISIONAL LABELS / NON-COLLECTING / NON-AUTHORIZING  
> **Date:** 2026-11-09  
> **Owner/routing:** Existing DGAF Structural Epistemics / Research, Evidence & Audits / Claim & Evidence Registry procedures; no new canonical subsystem  
> **Issue:** [#1572](https://github.com/ndrorchestration/DGAF-Framework/issues/1572)  
> **Dependent numeric-documentation correction:** [#1571](https://github.com/ndrorchestration/DGAF-Framework/issues/1571) and its draft [PR #1574](https://github.com/ndrorchestration/DGAF-Framework/pull/1574)

## R0 — Decision and research question

The bounded question is whether a future evidence-bound assessor can distinguish **correct mathematical premises** from **invalid or unjustified conclusions**, particularly when a cited research theorem lends an unrelated conjecture apparent authority.

No performance claim is being evaluated in this candidate. The current deliverable is a source-bound *test-design artifact* and executable checks for elementary reference arithmetic. It neither measures an LLM's reliability nor supplies new empirical data for DGAF.

## R1–R2 — Locked candidate scope and source hierarchy

1. **Published primary abstract:** [Benjamin & Snyder (2014)](https://doi.org/10.1017/S0305004113000753) explicitly establishes that a regular hendecagon is constructible by marked ruler and compass. The accessible publisher abstract suffices for the existence claim, **not** for independently asserting the paper's complete proof mechanism or all auxiliary equations.
2. **Conjecture/source of disputed inference:** [Oscar Lanzi's public proposal](https://math.stackexchange.com/questions/4714174/what-are-some-conjectures-of-your-own/4715207) proposes uniqueness among non-Pierpont prime side counts, gives a finite-field factorization, and reports unsuccessful construction attempts for 31, 41 and 61. These are source claims; the universal uniqueness conclusion is **not proved** by this record.
3. **Deterministic same-system reference mathematics:** `tests/test_hendecagon_claim_entailment_fixture.py` checks elementary algebra using the Python standard library. These checks do not constitute independent mathematical review, and tests of fixture labels do not establish that an evaluator correctly adjudicates them.

The provisional input and disposition set is [`fixtures/hendecagon_claim_entailment.v0.1.json`](fixtures/hendecagon_claim_entailment.v0.1.json). Its source IDs are defined within that file. There are ten fixed candidate claims, not a benchmark sample drawn from a broader task distribution.

## R3 — Mathematical facts within scope

For unit side length, `R = 1/(2sin(pi/11)) = 1.77473276644211166...`. This is a geometric radius, not the conjecture's cubic variable.

For `f(r) = 25r^3 - 40r^2 + 21r - 2`, the factorization `f(r) = 3(r+1)^2(r+3) (mod 11)` is correct. But its characteristic-zero discriminant is `-44000 != 0`, so `f` does *not* have a repeated root in characteristic zero. Numerically `f(R) ≈ 49.02817983`, demonstrating that the radius is not a root of this cubic.

The distinct auxiliary polynomial `g(u)=u^3+2u^2+2u+2` has discriminant `-44`. The relation of its parameter to the complete geometric construction requires precise primary-paper mechanism review before stronger claims; the numerical test only validates the displayed discriminant. Cubing is bijective over `F_11` because `gcd(3, 10) = 1`, without explaining the repeated root of `f` modulo 11.

**Known invalid transitions for test design:**

- repeated factor after reducing modulo 11 ⇒ repeated factor over the reals;
- verified geometric radius ⇒ root of the conjecture's unrelated cubic;
- one attempted construction method failing ⇒ impossibility of every construction;
- credible published existence theorem ⇒ verified uniqueness theorem;
- mathematical constructibility ⇒ evidenced improvement in cryptographic security.

## R4 — Proposed labels, not independent gold

The fixture declares `RETAIN` for scoped, verified premises; `REJECT` for falsified claims or logically invalid entailment; and `WITHHOLD` when the conclusion lacks the necessary evidence. Missing evidence is not automatically falsity.

The ten proposed labels are **same-system analyst prelabels awaiting independent gold-label QA**. The tests assert the labels have not silently changed and that elementary supporting calculations are reproducible. A passing suite does not prove all labels independently adjudicated.

## R5 — Controlled next-step protocol (not executed)

Before any model or DGAF comparison:

1. Version and hash the input set and independently adjudicate each gold label with mathematical sources appropriate to the claim type.
2. Define baseline/comparator and DGAF-assisted review condition, model/tool/version identities, prompts, seeds, allowed sources, review procedure and exact outputs to collect.
3. Hold inputs and allowed source context constant across conditions, blind adjudication where feasible, and record all false acceptances, false rejections, abstentions, provenance failures and domain-transfer mistakes.
4. Separate formal-reference correctness, claim entailment, reviewer independence, and system-level performance.
5. Preregister the comparison and its limits with the existing research controller before collecting evidence; document conflicts and negative results.
6. Do not generalize from a ten-item synthetic case or count same-system testing as independent evaluation.

**No model invocations, randomized trials, comparative runs, scientific-N increments, or downstream promotion are part of this PR.**

## R6–R7 — Acceptance and claim ceiling

For *research-fixture engineering acceptance only*:

- [ ] Source URLs resolve to the intended work; full-paper mechanisms remain explicitly bounded.
- [ ] Ten fixture records, case IDs, source references, labels and rationale are schema-checked.
- [ ] All deterministic arithmetic checks pass on the exact PR head.
- [ ] The fixture and code are pinned to exact content identities in review evidence.
- [ ] The existing GitHub quality, security, governance and branch-protection conditions are respected.
- [ ] Independent review is still required before treating provisional labels as accepted reference truth.

The existing #1571 numeric-documentation correction is a separate draft; this proposal does not merge, override, or backfill it. Historical experiments, custody artifacts, immutable evidence and canonical current-state files must not be rewritten.

```text
EVIDENCE_CLASS=INTERNAL_SYNTHETIC_RESEARCH_FIXTURE_DESIGN
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
EXTERNAL_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```
