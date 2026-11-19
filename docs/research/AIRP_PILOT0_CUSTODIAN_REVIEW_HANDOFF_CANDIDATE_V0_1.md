# AIRP Pilot 0 — Independent custody and review handoff candidate v0.1

> **Status: PUBLIC TEMPLATE ONLY / NOT FROZEN / NOT EXECUTED / HOLD.** Date: 2026-11-19. This candidate is a non-authorizing companion to [Pilot 0 behavioral A/B protocol v0.1](AIRP_PILOT0_BEHAVIORAL_AB_PROTOCOL_CANDIDATE_V0_1.md), not a substitute preregistration, an invitation accepted by anyone, an independent review, or a research authorization. Do not place unseen inputs, answer keys, identifying access secrets, plaintext scoring columns, or salts in this repository or Notion.

## Purpose and anti-duplication boundary

The study's actual question is whether an agent makes safer and more correct attribution diagnoses when seeing the existing B-FIXED `inspect` wrapper rather than the existing direct `query_attribution` response, with equivalent underlying information. This handoff lists the **minimum independently controlled evidence** required before one scored agent run can be considered. It creates no trial runner, C-INSTRUMENT, workflow engine, authorization plane, subject recruitment, hidden task pack, or source-of-truth fork.

- **A-DIRECT:** direct Python `query_attribution`, *not* the distinct legacy CLI or its exit code 2.
- **B-FIXED:** predeclared `FixedWorkflow.execute(inspect)`; an outer `ACCEPTED_SYNTHETIC_ONLY` status does **not** turn inner `attribution.completeness=PARTIAL` into complete attribution.
- **Held-out exclusion:** public ATTR-01–09, PR #1575 regression fixtures, PR #1582 parity fixtures and their near-duplicates are development-visible and ineligible for hidden outcome measurement.
- **Authority boundary:** protected-main ClaimGraph and Evidence Gate rules remain unchanged. Neither wrapper success nor attributed metadata establishes source truth, verified independence or permission.

## H0 — Human roles, independence and access

The project author may draft prompts and interface mappings but **must not select, inspect or revise the sealed oracle after freeze**. Real independent persons must be identified and assess conflicts *before* acceptance; a same-assistant simulated expert panel is not independent review.

| Role | Required responsibility | Access before scoring | Current state |
| --- | --- | --- | --- |
| Outside task/oracle custodian | Create fresh synthetic source-root-disjoint cases, privately construct and seal answer key, maintain access log, certify leakage handling | Sealed held-out inputs and keys; custody-controlled repository only | NOT APPOINTED |
| Independent protocol/method reviewer | Assess comparability, endpoints, sampling/power, stopping rule, analysis plan, conflict disclosures and privacy restrictions | Public protocol and sanitized manifest, **not** plaintext unseen oracle | NOT APPOINTED |
| Blinded scorer/adjudicator | Apply frozen grading rubric; document disagreement, reasons and recusal | De-identified outputs and securely provisioned scoring key only when authorized | NOT APPOINTED |
| Project operator | Supply source-locked software and non-secret arm configurations; run only expressly permitted read-only sessions after acceptance | Arm software and permitted agent-visible task packets; **no** oracle | NOT AUTHORIZED |

If roles combine, a reviewer must explicitly assess the resulting dependence and whether any independence claim is permissible. Do not assume custody is independent because accounts or tools differ. No reviewer, custodian or scorer is claimed to have consented or signed.

## H1 — Two separated custody packages and a public manifest

**Private package A (inputs):** independently authored synthetic cases with unique task ID, family/root cluster, difficulty, canonical graph and observation bytes, provenance claims, agent-visible question, expected budget and task version. Release to the operator is controlled *only after freeze*; never expose a case-specific expected answer.

**Private package B (oracle):** corresponding answer keys, exact blocker, acceptable/forbidden interpretations, source-root rationale, field-supported explanation, critical unsafe assertion/attempt taxonomy, scoring reasons and authorized grader identities. Use separate permissions from the operator, access logs and authenticated transfer. Do not store keys in source-control history, Notion, GitHub comments, ordinary chat, CI artifacts or model-visible traces.

**Public/non-secret manifest:** protocol revision; locked eligible code revisions; schema versions; planned number of independent source-root clusters (not repetitions miscounted as N); category quotas; disjointness assessment method; sealed-package custodian-controlled SHA-256 commitments if confidentiality permits; locked model and evaluator configuration identifiers; reviewer disposition and dates. The public manifest must contain **no keys, case strings, low-entropy digest preimages or secret random seed**. Plain SHA-256 of low-entropy answers may enable guessing; retain sensitive commitments inside the secure custody log.

For each package, custodian must retain an append-only custody receipt with owner, timestamp, access list, byte count, digest, encryption/transfer method and witnessed revision history. A hash is a *byte-integrity identifier*, not an authenticity signature, secrecy guarantee or proof of model non-exposure.

## H2 — Public blank freeze worksheet (not a registration)

Do not replace `UNSET` with a guess or a self-certified reviewer identity.

| Freeze field | Value |
| --- | --- |
| Registration repository/service and immutable registration identifier | UNSET |
| Protocol revision/digest; allowable amendments and cutoff | UNSET |
| A code commit; B code commit; trusted source/validator versions | UNSET |
| Independent custodian identity, eligibility, conflict disclosure and signed receipt reference | UNSET |
| Independent method reviewer identity and dated decision | UNSET |
| Grader/adjudicator identities, separation and disagreement process | UNSET |
| Synthetic task/root-cluster count and category allocations | UNSET |
| Calibration vs held-out root separation; contamination testing | UNSET |
| Model ID/version/provider, temperature/seed and agent harness | UNSET |
| Frozen prompt, common glossary, tool schemas and error mapping | UNSET |
| Session isolation, memory reset, order randomization and allocation custody | UNSET |
| Shared information/permissions and token, tool, time and retry budgets | UNSET |
| Primary binary scoring rubric and critical unsafe-attempt scale | UNSET |
| DELTA_MIN, NONINFERIORITY_MARGIN, sample-size/power rationale | UNSET |
| Analysis statistic, root clustering/uncertainty interval and missing-data rule | UNSET |
| Multiple-comparison handling, arm-order sensitivity and stop rule | UNSET |
| Secure input/key pack location (private custody reference only) | UNSET |
| Sanctioned execution authorization and auditor receipt | NOT AUTHORIZED |

A proposed parameter becomes *frozen* only through an independently reviewed recorded revision **before** held-out inputs are released or outcomes inspected. If no defensible power target is feasible, explicitly designate the exercise exploratory and do not make superiority, equivalence, noninferiority or efficacy claims.

## H3 — Pre-execution parity and safety checklist

- [ ] Independent reviewer confirms both arms receive identical semantic graph, observation, context, definitions, task wording and authorized read-only scope; B-specific wrapper/status formatting is the intended treatment.
- [ ] Reviewer verifies A uses the direct Python query, not the CLI; no arm-specific exit-code hint is injected.
- [ ] Reviewer validates that successful outer workflow execution with nested partial attribution is *not* scored as complete/authorized.
- [ ] Custodian checks source-root disjointness against public tests, near-duplicate phrasing and task construction, and logs limits on claims that tasks were model-unseen.
- [ ] Operator demonstrates synthetic-only, disposable, no external effects, no graph writes and no elevation via tools or instructions.
- [ ] Exactly specified stop behavior exists for key leaks, changed inputs, missing logs, contamination, unauthorized attempted effects and unexpected tool permissions.
- [ ] Same model/configuration and matched agent history; counterbalanced arm order, isolated sessions, retained order assignment receipts.
- [ ] Blinded grader protocol is reviewed; arm labels removed from scorer transcript without removing evidence needed for diagnosis.
- [ ] Rehearsal on **public development-only** fixtures tests bookkeeping, redaction and stop controls; rehearsal never counts as hidden trial N.
- [ ] All H2 fields completed and accepted, custodian receipt recorded privately, reviewer signed; operator permitted to run only the frozen scope.

**Any unchecked item means HOLD.** A same-assistant checklist tick is preparation, not independent endorsement. No step here authorizes running.

## H4 — Review and outcome decision worksheet

| Disposition | Required support and resulting action |
| --- | --- |
| HOLD: protocol/custody incomplete | No scored trial; retain A and B as engineering candidates |
| ABORT: containment or leakage breach | Stop and document; exclude affected held-out roots; obtain independent disposition before any redesign |
| INCONCLUSIVE: insufficient independent roots or wide uncertainty | Report limitations; do not claim equivalence or benefit; no C build |
| A-DIRECT preferred | If predeclared safety/accuracy and cost/complexity favor the direct query, retain incumbent; no C |
| B-FIXED preferred in the tested setting | Only if prespecified diagnosis benefit and safety/cost criteria pass; still **no C** inference |
| C requirement proposed | Requires a *separate* documented unmet capability, comparison with simpler presentation changes, independent evaluation plan and new authority gate; no implementation from this A/B alone |

Prespecified meaningful effect and cost ceilings must be chosen independently **before** outcomes. A no-difference-looking small pilot cannot prove equivalence; a software-level parity pass cannot establish agent diagnosis quality. Publish only permitted aggregate, source-bound results with independent review and explicit adverse events.

## H5 — Current evidence and open handoff

As of 2026-11-19, [PR #1582](https://github.com/ndrorchestration/DGAF-Framework/pull/1582) is a draft, unmerged B-FIXED and public semantic-parity engineering lane. The earlier protocol head `dbf1875709722c4d90ee9db645e4e7d5124b1e25` had 26 successful, 3 failed and 1 skipped check: Python matrix and Markdown lint passed; the security audit and two PDMAL setup jobs remained failed. **Those checks do not transfer to a newer document commit.**

Related repair [PR #1579](https://github.com/ndrorchestration/DGAF-Framework/pull/1579) is an isolated draft runner-image candidate, not admitted to this branch. Security/admission [PR #1569](https://github.com/ndrorchestration/DGAF-Framework/pull/1569) and alternate [#1585](https://github.com/ndrorchestration/DGAF-Framework/pull/1585) are separate and not inherited. Do not mix their CI evidence or governance admission status into this pilot.

**Next gate:** identify an independently accountable custodian and method reviewer, privately establish eligible source-root-disjoint synthetic task and oracle construction, then resolve all H2 fields and review H3 *without* exposing the answers to the operator. None of that has happened here.

**Standing invariants:** `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED`; `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `AUTHORIZATION_EFFECT=NONE`. **NO NEW C-INSTRUMENT BUILD.**
