# Epistemic Vocabulary Standard

**Status:** Canonical policy for taxonomy and vocabulary artifacts
**Effective:** 2026-09-02 reconciliation extension
**Scope:** `docs/NDR_INTERNAL_VOCABULARY_MASTER.md`, `docs/taxonomy/**`, agent role vocabularies, external-equivalent mappings, benchmark language, generated taxonomy documents, and transversal candidate-state terminology.

## Purpose

Taxonomy is not evidence. A useful vocabulary mapping must distinguish what a term is called, what it resembles externally, what is implemented, and what has actually been demonstrated.

This standard prevents internal names, metaphors, mathematical constants, qualitative judgments, and historical benchmark claims from acquiring evidentiary status merely through repetition in vocabulary files.

## Required Epistemic Classes

Every substantive taxonomy claim should be interpretable as one of these classes:

| Class | Meaning | Allowed wording |
|---|---|---|
| `DEFINED` | Internal term or role is explicitly defined by the project | "is defined as", "the project calls this" |
| `IMPLEMENTED` | Corresponding behavior exists in code and can be inspected | "implemented by", "the code performs" |
| `COMPUTED` | Value is produced by a reproducible calculation or test | "computed", "measured", "test result" |
| `VERIFIED` | Claim has an identified verification method and evidence artifact | "verified by [test/artifact]" |
| `ATTESTED` | A reviewer or historical record records the claim, without independent recomputation | "attested", "recorded as PASS" |
| `HISTORICAL` | Claim belongs to an earlier state and is not necessarily current | "historical result" |
| `HYPOTHESIS` | Proposed relationship requiring empirical or formal validation | "hypothesized", "to be tested" |
| `METAPHOR` | Internal analogy used for conceptual communication | "metaphor", "analogy", "inspired by" |
| `UNSUPPORTED` | Claim currently lacks sufficient evidence | "unsupported", "not established" |
| `DEPRECATED` | Term or claim should no longer be used as current canonical language | "deprecated" |

## External-Equivalent Rule

"External Equivalent" means the closest recognized concept, not proof of equivalence.

Use:

> Internal term → closest external analogue → explicit difference

Do not use:

> Internal term = established external standard

unless the implementation and semantics have actually been demonstrated to be equivalent.

## Mathematics and Named Operators

A correct mathematical identity does not validate an unrelated engineering conclusion.

A taxonomy entry must separate:

1. **mathematical fact** — e.g. a ratio identity or theorem;
2. **implementation** — what the software actually computes;
3. **engineering interpretation** — why the project chooses to use it;
4. **empirical consequence** — what testing demonstrates.

Named mathematical operators, algorithms, protocols, or standards must not be used as labels for merely metaphorical or superficially similar mechanisms. If a mechanism is a random threshold, call it a random threshold. If it is a heuristic inspired by an operator, call it an inspiration/analogy.

## Quantitative Claims

Percentages, multipliers, scores, ratios, resilience figures, and benchmark values require:

`defined metric → defined denominator/baseline → source telemetry → calculation → reproducible test → reported result`

A number hard-coded into a dictionary, dataframe, README, or taxonomy table is **not** independently verified merely because an assertion succeeds.

Unspecified `Nx` claims are prohibited. The `1x` baseline must be defined before `150x`, `200x`, etc. can be called ratios.

Qualitative judgments must not be expressed as percentages unless a measurement protocol exists.

## Certification and Attestation

Words such as `verified`, `certified`, `production-ready`, `proven`, `validated`, and `PASS` must identify the scope and evidence basis.

Preferred:

- `PASS — historical attestation`
- `verified — test suite X, commit Y`
- `computed — source telemetry Z`
- `experimental — not independently validated`

Avoid unqualified:

- `proven stable`
- `production certified`
- `100% verified`
- `mathematically guaranteed`

## Role and Persona Vocabulary

Agent role descriptions are design specifications unless supported by executable behavior or evaluation evidence. Words such as `authority`, `arbiter`, `certifier`, `security monitor`, and `formal verifier` describe intended role boundaries unless implementation evidence establishes those capabilities.

`External Equivalent` should therefore describe the nearest functional category, not confer credentials or standards compliance on the internal agent.

## Historical Preservation

Historical claims should not be silently deleted when they are useful provenance. Instead, preserve them with an epistemic label and evidence boundary.

Canonical pattern:

> **Historical claim:** X. **Evidence status:** attested/unreproduced. **Current status:** not independently established.

This preserves the audit trail without laundering historical assertions into current facts.

## Cross-Project Vocabulary

A term shared by two projects does not establish architectural identity. Shared mathematical motifs, names, metaphors, or control patterns must be recorded as similarity only until an explicit bridge is implemented and documented.

## Transversal Agreement Vocabulary — 2026-09-02

A live governance state is **transversally coherent** only when the independently maintained projections of that state resolve to the same scoped identity and compatible status.

Required identity tuple:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Use the following distinct terms:

| Term | Meaning |
|---|---|
| `ROLE DIFFERENCE` | Two identifiers intentionally describe different semantic roles in the same candidate cycle. |
| `HISTORICAL DIFFERENCE` | A prior candidate/run/deployment is retained for provenance and explicitly marked historical/non-closing. |
| `TRANSVERSAL DRIFT` | Independent live projections can reasonably be read as describing different current states. |
| `BLOCKING CONTRADICTION` | A projection would permit invalid evidence transfer, downstream closure, freeze, or authorization. |
| `CANDIDATE-BOUND` | Evidence explicitly names the exact candidate identity that produced it. |
| `CURRENT-CYCLE` | Evidence belongs to the selected candidate cycle and its upstream dependencies. |

Transversal agreement is a **consistency property**, not an evidence class. A successful consistency check cannot upgrade `DEFINED`, `IMPLEMENTED`, `VERIFIED`, or historical material by itself.

### P-35 / P-42 namespace rule

`P-35` is **Procluding Premise Gate**.

`P-42` is **Adaptive Harmonic Governance (AHG)**.

The current P-35 engineering remediation enforces an explicit premise-check dependency at the DGAF/TGL/ConsensusTask boundary. That wiring rule is not a PDMAL-specific constitutional premise policy. A PDMAL-specific checker remains an explicit scientific-control dependency and must be approved separately before pilot execution.

### Evidence transition vocabulary

Keep these transitions distinct:

`DEFINED → IMPLEMENTED → TESTED → CANDIDATE-BOUND → VERIFIED → FROZEN → AUTHORIZED → EMPIRICAL`

No transition is implied by naming, ancestry, deployment readiness, or shared workflow identity.

## Minimum Review Checklist

Before merging a taxonomy/vocabulary change:

- [ ] Internal name is clearly distinguished from external equivalent.
- [ ] Implementation claim is backed by code when labeled `IMPLEMENTED`.
- [ ] Numeric claims have a defined metric and baseline.
- [ ] Mathematical facts are separated from engineering conclusions.
- [ ] Named operators/protocols are technically accurate or explicitly marked metaphorical.
- [ ] Historical attestations are not presented as current verification.
- [ ] Certification language identifies scope and evidence.
- [ ] Cross-project similarities are not presented as identity.
- [ ] Deprecated terminology is explicitly marked.
- [ ] Candidate, apparatus, deployment, workflow, artifact, freeze, and authorization identities are role-qualified.
- [ ] Cross-system live projections are checked for transversal agreement.
- [ ] New dependencies are identified and their downstream invalidation scope is recorded.

**Canonical rule:** Vocabulary organizes claims; it does not upgrade their epistemic status. Transversal agreement organizes state projections; it does not create authorization.
