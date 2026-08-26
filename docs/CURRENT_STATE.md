---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: 83e1678f55d16f32b5ce363e091ac74479cbfe1f
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **What this document does NOT claim (2026-08-26 update):** This revision records the *corrected live candidate basis* after the CI/doc-hygiene PRs merged on 2026-08-26. It does **not** constitute a freeze, a P8 closure, pilot authorization, or empirical validation. P8 remains OPEN / FAIL-CLOSED. Empirical **N = 0**. No efficacy claim is authorized. Merge ≠ freeze; execution ≠ empirical validation.

## Authoritative current state

|| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only for the corrected apparatus |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Panel-ready record (`P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`) presents 11 proposed decisions all OPEN / PENDING AUTHORITY ADOPTION; primary contrast (DGAF vs null) selected but formal adoption not evidenced; see `P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation and controls exist, but executed candidate-scoped verification is incomplete |
| Exact verification candidate | IDENTIFIED (corrected basis) | `83e1678f55d16f32b5ce363e091ac74479cbfe1f` is the corrected live candidate basis (post-#95/#96/#98 main). Prior immutable apparatus reference `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is retained as HISTORICAL PROVENANCE for the pre-correction apparatus. Because #95 altered `test_execution_contract.py` / `test_orchestration_firewall.py` (verification-apparatus components), the corrected tree is a NEW candidate identity requiring re-verification before any P8 closure claim — it is not a silent rebind of the immutable `2a80f819`. |
| New immutable freeze | NOT CREATED | Candidate has not yet crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | Durable retention, candidate-scoped runtime evidence, and remaining custody/provenance checks require closure |
| P9 independent verification | NOT EXECUTED | Downstream of candidate evidence closure |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Candidate identity boundary

The P8 verification checklist previously identified `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` as the exact candidate tree for verification. After the 2026-08-26 CI/doc-hygiene merges (#89 claim-hygiene fix, #90/#91/#92 clean rebuilds, #93 markdownlint auto-fix 1692→567, #95 test-contract repair, #96 P7 status reconciliation, #98 tzdata `--require-hashes` fix), the corrected live candidate basis is `83e1678f55d16f32b5ce363e091ac74479cbfe1f`. `2a80f819` is retained as HISTORICAL PROVENANCE for the pre-correction apparatus; it is not silently redefined. Because #95 altered verification-apparatus test contracts, the corrected tree is a NEW candidate identity requiring re-verification before any P8 closure claim. Later documentation-only commits do not redefine that apparatus. Any further substantive apparatus change requires a new candidate identity and re-verification.

Historical SHA references, including earlier PR #77 and pre-correction P8 bindings, remain provenance where they describe what was actually examined; they are not current-state assertions.

## Canonical predicate state

- **P1 Candidate integrity:** PARTIAL — candidate exists; executed candidate evidence still required.
- **P2 Execution contract:** PARTIAL — implementation controls exist; current runtime evidence remains incomplete.
- **P3 Artifact contract:** PARTIAL — executable contract is strengthened; candidate-scoped verification remains required.
- **P4 Security / blinding integrity:** PARTIAL — controls and synthetic evidence exist; operational custody boundary remains to be fully evidenced.
- **P5 Provenance / reproducibility:** PARTIAL — bindings exist; candidate-scoped reproduction and environment evidence remain incomplete.
- **P6 Durable evidence custody:** OPEN — durable archive plus independent retrieval/hash evidence remains required.
- **P7 Scientific target specification:** TECHNICALLY ADJUDICATED / FORMALLY OPEN — the panel-ready record presents all 11 scientific decisions as OPEN / PENDING AUTHORITY ADOPTION; the primary contrast (DGAF vs null) has been selected but formal authority adoption is not evidenced; must remain traceable to the authoritative adjudication record and protocol before P8 closure claims scientific closure.
- **P8 Analysis lock:** OPEN / FAIL-CLOSED — no closure by implementation presence alone.
- **P9 Independent verification:** NOT EXECUTED.

Authorization is separate from predicate status. Freeze is separate from authorization. Merge is not freeze, and execution is not empirical validation.

## Current documentation and hygiene rules

1. Current-state assertions must identify the current candidate or explicitly say that a SHA is historical.
2. Historical evidence must retain the SHA/run/deployment actually examined.
3. Status documents cannot create closure by assertion; closure requires the evidence specified by the relevant predicate.
4. A frozen candidate tree is immutable. Later documentation corrections may clarify the record but do not rewrite the frozen apparatus.
5. P7 adoption, P8 implementation, freeze, authorization, execution, and empirical efficacy are distinct state transitions.
6. The current empirical boundary remains **N = 0** and no efficacy claim is authorized.

## Required next evidence events

1. Execute the applicable CI/test hierarchy against exact candidate `2a80f819...` and retain run IDs, logs, artifacts, and executed-tree identity.
2. Complete candidate-scoped P8 verification, including analysis, artifact, schema/security, compilation, provenance, determinism, and environment checks as applicable.
3. Establish durable evidence retention and independently verify retrieval and integrity.
4. Complete remaining operational blinding custody and runtime-dependent verification according to explicit applicability/fallback rules.
5. Derive and evidence P1–P8 from the exact candidate; do not infer closure from configuration alone.
6. Create an immutable freeze only after required pre-freeze predicates are satisfied.
7. Execute independent/adversarial verification against the frozen candidate.
8. Make a separate authorization decision.
9. Only then execute the blinded empirical pilot and proceed to formal unblinding and locked analysis.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**

## Corrected candidate basis — 2026-08-26

This section records the post-merge live state and the explicitly accepted/deferred
items. It is a documentation correction only; it does not create a freeze, close P8,
grant pilot authorization, or validate anything empirically.

### Merged on 2026-08-26 (all verified live)
| PR | Content | Effect on gates |
|----|---------|-----------------|
| #89 | Claim-hygiene / registry gate crash fix | `IP & Claim Hygiene Check` ✅, `scan` ✅, `Claim Hygiene Audit` ✅, `IP Hygiene Sweep` ✅ |
| #90 / #91 / #92 | Clean rebuilds of #85 / #74 / #42 (additive docs + pip lockfiles) | additive; no gate regression |
| #93 | markdownlint auto-fix (repo debt 1692 → 567) | mechanical only; 567 judgment-required violations remain |
| #95 | Test-contract repair (`test_execution_contract.py`, `tests/test_orchestration_firewall.py`) | `test (3.10/3.11/3.12)` matrix ✅ (was red on prior base) |
| #96 | P7 project-status reconciliation (`docs/PROJECT_STATUS.md`) | P7 now consistently recorded as FORMALLY OPEN / PENDING AUTHORITY ADOPTION |
| #98 | tzdata pin added to `requirements-full-lock.txt` | `security-and-schema` ✅ (was failing on `--require-hashes` install) |

Corrected live candidate basis: **`83e1678f55d16f32b5ce363e091ac74479cbfe1f`**.
Prior immutable apparatus reference **`2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`** retained as historical provenance.

### Explicitly accepted / deferred items
1. **Markdown Lint debt (567 violations, 268 files).** Breakdown: 360 MD040 (fenced-code-language), 165 MD036 (emphasis-as-heading), plus MD025/MD022/MD032/MD029/MD028/MD052/MD056/MD055/MD003. These are overwhelmingly **intentional content** (agent PROTOCOL specs, formalism/theory math derivations, ASCII flow diagrams such as "DEFINED → IMPLEMENTED → COMPUTED", multi-H1 templates, CHANGELOG). They are **separate from the P7 reconciliation** and are **not** auto-fixed, because blind `--fix` would corrupt intentional structure. Recorded here as accepted debt; resolve via human review, not mechanical edit. Markdown Lint is **not** a required status check (only `PPTL CI` is required), so it does not block merges.
2. **PR #77 (pre-authorization / pilot boundaries) — NOT MERGED.** It adds `pilot_artifact_schema.py`, modifies `run_pilot.py`, and adds `test_security_controls.py` / `test_artifact_schema.py` / modifies `test_execution_contract.py` — pre-auth/pilot scope whose base (`695ba3ad`) predates and conflicts with already-merged #95. Per standing governance (pilot NOT granted, PRE-FREEZE, no irreversible merges without explicit authorization), #77 is held for explicit human authorization.
3. **PR #97 (P-42 registry reconciliation) — already CLOSED** (not merged; added `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md`). No action required.

### Verification basis (what this update rests on)
- GitHub API check-runs on `83e1678`: `IP & Claim Hygiene Check`, `scan`, `Governance CI`, `PPTL CI`, `security-and-schema`, `test` matrix, `Fail-closed runner` all green; only `Markdown Lint` fails (accepted debt above).
- Branch protection requires only `PPTL CI` (verified live); repo Ruleset "Main" enforces deletion + non-fast-forward only.

### What this does NOT claim
No freeze created. P8 remains OPEN / FAIL-CLOSED. Pilot authorization NOT GRANTED. Empirical **N = 0**. Implementation/hygiene presence is not empirical validation. The corrected candidate basis requires candidate-scoped re-verification before any P8 closure claim.
