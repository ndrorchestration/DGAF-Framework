# Deliberative Operational Policies

> **Epistemic Boundary:** N=0, NOT GRANTED, PRE-FREEZE — throughout this document.

> **Current candidate:** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

> **Status:** Proposed. These policies require formal adoption by governance authority before they are binding. They do not authorize execution. They do not close any predicate. They are designed to prevent false closure, not to accelerate it.

---

## Purpose

This document defines operational policies governing the DGAF-Framework pilot experiment. It serves as a reference for what must hold, what evidence is required, and what constitutes violation, for each policy domain. All policies are stated as proposed — none are adopted or binding until explicitly recorded as such by the governance authority.

The document draws exclusively on the P7 Adjudication Record (panel-ready 2026-08-23), the P8 Analysis Lock and Verification Checklist, the PDMAL Protocol Matrix (amendment v0.7.5), the P3/P4/P5/P6 Freeze Readiness assessment (2026-08-21), and the current PDMAL Control State. No additional sources are incorporated.

---

## Policy 1: Parameter Boundary

### Purpose

To prevent ambiguity between scientific decisions (subject to formal adjudication and resistant to silent change) and implementation constants (subject to operational documentation). The boundary ensures that any post-freeze change to an analysis parameter either goes through formal re-adjudication (if it is a P7 scientific decision) or is documented with justification that preserves or transparently limits reproducibility (if it is a P8 implementation constant).

### P7 Scientific Decisions (adjudication-required)

The following are classified as P7 scientific decisions. They were adjudicated in the P7 Adjudication Record (11 open decisions, pending authority adoption) and cannot be changed after freeze without formal re-adjudication:

- **Reference condition:** null
- **Estimand:** E[FFCR_dgaf(S) − FFCR_null(S)]
- **Unit:** root seed; 180 trials per seed = 4×5×9
- **Direction:** higher FFCR better; two-sided 95%; directional support
- **Aggregation:** FFCR = successful/complete cells; equal weighting
- **CI convention:** two-sided 95% percentile paired bootstrap
- **Directional support criterion:** estimate > 0 AND CI lower bound > 0
- **Exclusion rules:** no outcome-aware exclusion; matrix completeness/pairability required; no 10% threshold
- **Multiplicity treatment:** none for primary; Holm if secondary confirmatory
- **RNG domain separation:** analysis seed 20260823; bootstrap domains separated from execution domains
- **Success criterion:** positive estimate + CI wholly above zero; 0.15 = planning MDE only (not a success threshold)
- **Falsification criterion:** CI wholly below zero = evidence against; overlap = inconclusive; non-support ≠ falsification

### P8 Implementation Constants

The following are classified as P8 implementation constants:

- **Bootstrap resample count:** 10,000
- **Analysis bootstrap seed:** 20260823
- **CI alpha level:** 0.05 (inherent in the two-sided 95% CI decision — the alpha level is not independently chosen; it derives from the CI convention, which is a P7 scientific decision)

The CI alpha level occupies a boundary position: it is stated here as an implementation constant because it is the numeric instantiation of a P7 scientific decision (the 95% CI convention). Changing the alpha level independently of the CI convention would constitute a substantive change to the analysis and would require re-adjudication.

### Required Behavior

1. Every analysis parameter in use by the candidate must be classifiable as either a P7 scientific decision or a P8 implementation constant.
2. The classification must be recorded in both the P7 traceability matrix and the P8 analysis lock.
3. Changing a P7 scientific decision after freeze requires formal re-adjudication under the closure requirements recorded in the P7 Adjudication Record: (1) explicit adoption by authority, (2) verification treatment/reference match candidate apparatus, (3) reconciliation with protocol + P8 analysis spec, (4) record of authority/date/adopted identity, (5) binding to exact freeze candidate without silently changing any decision.
4. Changing a P8 implementation constant after freeze requires documented justification and may invalidate reproducibility claims. The justification must state what was changed, why, and what reproducibility implications follow.

### Evidence Standard

- The P7 traceability matrix must enumerate each P7 decision with its current value and the adjudication status (open/pending adoption).
- The P8 analysis lock must record the implementation constants in use by the candidate.
- Any post-freeze change to a parameter must be traceable to either a re-adjudication record or a documented justification with reproducibility impact assessment.

### What Violates This Policy

- A parameter used in analysis that is not classified as either P7 or P8.
- A P7 decision changed without re-adjudication.
- A P8 constant changed without documented justification.
- Silent changes to any parameter that alter the analysis result, the estimand, or the evidentiary claim.

---

## Policy 2: Blinding Operational

### Purpose

To ensure that condition identities are withheld from the executor and from artifacts until governance-authorized unblinding, and that the blinding custody chain is independently verifiable. The blinding policy protects against outcome-aware analysis decisions and against post-hoc reinterpretation of blinded results.

### Required Behavior

1. **Key storage:** The unblinding key is held in the environment variable `PDMAL_BLINDING_KEY`. It is not hardcoded, not stored in source control, and not recoverable from the binary, the execution environment, or the source.
2. **Executor isolation:** The executor process has no access path to the key under any execution mode.
3. **Blinded artifact IDs:** Artifacts use blinded condition IDs (e.g., `blind_A`, `blind_B`) rather than raw condition names. The mapping between blinded IDs and raw conditions is known only to the custodian.
4. **Custody separation:** The unblinding map is stored separately from both the artifacts and the executor. Custody is not combined with execution or analysis custody.
5. **Governance authorization required:** Unblinding can only occur after governance authorization is recorded.
6. **Operational dry-run:** An operational dry-run exercise of the unblinding procedure is required before pilot. The dry-run must exercise the procedure without compromising pilot integrity — it uses surrogate or synthetic material, not pilot data.
7. **Key distribution documentation:** The key distribution mechanism must be documented and reviewed before pilot.
8. **Operational proof:** Blinding custody evidence must demonstrate operational proof, not merely synthetic or demo evidence.

### Evidence Standard

Blinding custody evidence must demonstrate all four of the following:

- **(a) Executor cannot access key:** Evidence that the executor process, under any execution mode, cannot recover the unblinding key from the binary, environment, or source.
- **(b) Blinded IDs consistently applied:** Evidence that artifacts consistently use blinded condition IDs and that the blinding map is applied at artifact generation time, not retrospectively.
- **(c) Custody separated:** Evidence that the unblinding map custody is separated from executor custody and from analysis custody.
- **(d) Dry-run exercises procedure:** Evidence that an operational dry-run of the unblinding procedure was conducted and its results recorded.

### What Violates This Policy

- The unblinding key appearing in source control, hardcoded in the binary, or recoverable from the execution environment.
- The executor having any access path to the key.
- Artifacts containing raw condition names rather than blinded IDs.
- Unblinding occurring before governance authorization is recorded.
- Custody of the unblinding map being combined with executor or analysis custody.
- Blinding evidence being synthetic or demonstrative rather than operational.

---

## Policy 3: Infrastructure-Unavailable (P2/P6a)

### Purpose

To define the admissible responses when candidate runtime verification is unavailable, and to prevent the misclassification of "unavailable" as "N/A" followed by premature closure. This policy applies to P2 and P6a predicates where candidate-scoped evidence is required but the candidate runtime is not currently available for verification.

### Current State

Per the current PDMAL Control State: P2/P6a are PARTIAL/APPLICABILITY REQUIRED — candidate-scoped evidence or a justified applicability decision is required.

### Required Behavior

When candidate runtime verification is unavailable, exactly one of the following options must be chosen and recorded:

- **Option A — Defer:** Execute candidate runtime verification when the environment becomes available. The predicate remains open with a defined condition for closure (environment availability + verification execution). The expected availability date or trigger must be recorded.
- **Option B — Alternative verification:** Perform an explicitly justified alternative verification with limitations recorded. This option is only admissible when the alternative provides meaningful evidence toward the predicate and the limitations are fully disclosed.
- **Option C — Retain OPEN:** Retain the predicate in OPEN status with defined conditions for closure. This is the default when neither Option A nor Option B is currently actionable.

### Prohibited Action

- **Cannot convert "unavailable" → "N/A" → closed.** The sequence of reclassifying unavailable evidence as not-applicable and then closing the predicate is prohibited. "Unavailable" is a state of the evidence, not a determination that the predicate is inapplicable.

### Required Recording

- The choice of option (A, B, or C) and the rationale must be recorded in the evidence matrix.
- If Option B is chosen, the limitations must include:
  - **What was not verified:** the specific verification that the candidate runtime would have provided but did not.
  - **Why the alternative is acceptable:** the reasoning that the alternative evidence is sufficient for the predicate's intent, or at least sufficient to bound the risk.
  - **What risk remains:** the residual risk from the unverified component, stated explicitly.

### Evidence Standard

- The evidence matrix entry for the predicate must state which option was chosen and the supporting rationale.
- For Option B, the three required limitation components must be present and explicit.
- For Option A or C, the defined conditions for closure must be stated.

### What Violates This Policy

- Reclassifying "unavailable" as "N/A" and closing the predicate.
- Selecting Option B without recording all three limitation components.
- Selecting an option without recording the rationale.
- Closing a P2/P6a predicate without candidate-scoped evidence or a justified applicability decision.

---

## Policy 4: Documentation-Only Post-Freeze Change

### Purpose

To allow non-substantive corrections to documentation after freeze without invalidating the frozen candidate, while maintaining a clear boundary that any substantive change — to code, protocol, analysis, evidence semantics, or experimental apparatus — invalidates the candidate and requires a new freeze cycle.

### Required Behavior

1. **Permitted post-freeze changes:** Non-substantive documentation corrections may be applied after freeze. These include:
   - Typographical corrections
   - Clarifications that do not change meaning
   - Formatting changes
   - Broken link fixes
2. **Recording requirement:** Each documentation-only correction must be recorded with date, author, and description. The record must be visible in the repository history or an equivalent auditable log.
3. **Prohibited post-freeze changes:** The following invalidate the frozen candidate:
   - Changes to executable code
   - Changes to the protocol specification
   - Changes to the analysis specification or analysis parameters
   - Changes to evidence semantics (what counts as evidence, how it is evaluated)
   - Changes to the experimental apparatus
4. **Substantive change procedure:** A substantive change requires a new candidate cycle:
   - New candidate SHA
   - New verification against the full P8 checklist
   - New freeze
   - The prior frozen candidate is superseded, not amended.

### Definition of "Non-Substantive"

A change is non-substantive if and only if it does not change any of the following:

- Any executable behavior
- Any analysis result
- Any experimental outcome
- Any evidentiary claim

If a change alters any of these four, it is substantive regardless of intent.

### Disputed Classification

If the classification of a proposed post-freeze change as documentation-only or substantive is disputed, the matter escalates to governance review. The governance review decision is recorded and is binding for that change.

### Evidence Standard

- The repository history or equivalent auditable log must show each documentation-only correction with date, author, and description.
- No substantive change may be applied to a frozen candidate without a new candidate SHA, new verification, and new freeze.

### What Violates This Policy

- Applying a substantive change to a frozen candidate without initiating a new candidate cycle.
- Failing to record a documentation-only correction with the required metadata.
- Claiming a change is documentation-only when it alters executable behavior, analysis results, experimental outcomes, or evidentiary claims.
- Failing to escalate a disputed classification to governance review.

---

## Policy 5: Adversarial Preflight

### Purpose

To require resistance-to-error testing before an independent audit of a frozen candidate. Preflight is not authorization and does not close any predicate; it verifies that the candidate can withstand the specific failure modes that an independent audit would test.

### Required Behavior

Before an independent audit of a frozen candidate, the following preflight checks must be performed and their findings resolved or explicitly bounded:

1. **Candidate SHA verification:** Verify that the exact candidate SHA matches the deployment verification. The SHA in the analysis lock must match the SHA of the deployed artifact. A mismatch means the candidate under audit is not the candidate that was frozen.
2. **Artifact-substitution detection:** Test whether artifact substitution can be detected. The check asks: if an artifact were replaced with a different artifact, would the substitution be detectable by the verification mechanism? If the answer is no, the substitution vector must be bounded or closed before audit proceeds.
3. **Blinding-key leakage testing:** Test whether the executor can recover the blinding key through side channels. This includes environment introspection, memory inspection, binary analysis, and any other plausible leakage path. If any leakage path is found, it must be closed or explicitly bounded with residual risk recorded.
4. **Runtime ceiling enforcement:** Verify that the runtime ceiling (300s) actually triggers. The check is operational: run the executor under conditions that should hit the ceiling and confirm that it is enforced. If the ceiling does not trigger, the enforcement mechanism must be corrected or the non-enforcement must be recorded as a finding that bounds the audit scope.

### Required Recording

- Preflight findings must be recorded with: check performed, result (passed/failed/bounded), and any bounding conditions or residual risk.
- Findings that are not resolved must be explicitly bounded before the audit proceeds. "Bounded" means the scope of the audit is limited to account for the unresolved finding, and the limitation is stated.

### Evidence Standard

- All four preflight checks must have a recorded result.
- A failed check without explicit bounding blocks the audit from proceeding on the affected scope.

### What Violates This Policy

- Proceeding to independent audit without completing all four preflight checks.
- Proceeding with an unresolved finding that is not explicitly bounded.
- Treating preflight as authorization — preflight is resistance-to-error testing, not closure of any predicate.

---

## Policy 6: Formal Unblinding Procedure

### Purpose

To define the controlled procedure by which blinded condition identities are revealed to the analysis process after the dataset and artifact freeze are complete and verified, and after governance authorization is recorded. The procedure exists to prevent premature or unauthorized unblinding that could compromise the pilot's integrity.

### Roles (TBD at Authorization Time)

- **Unblinding mapping custodian:** The party that holds the unblinding map. Designated by governance at authorization time. [TBD]
- **Unblinding authorizing authority:** The governance authority that authorizes unblinding. Designated at authorization time. [TBD]

### Required Sequence

Unblinding occurs only after all of the following preconditions are met:

1. **Pilot dataset collected:** The pilot dataset must be collected. Unblinding cannot occur before data collection is complete.
2. **Artifact freeze verified:** The artifact freeze must be verified. The candidate SHA must be confirmed and the P8 verification checklist must show the required evidence for the frozen candidate.
3. **Governance authorization recorded:** Governance authorization for unblinding must be recorded. The authorization must state the authorizing party, the date, and the scope of the unblinding.

### Unblinding Execution

When the preconditions are met and authorization is recorded:

- The unblinding mapping is released to the analysis process under controlled conditions.
- The release is recorded with: timestamp, authorizing party, receiving party, and mapping hash (not the key itself).
- The mapping hash provides a verifiable record that the released mapping matches the custodian's map without revealing the map to the record.

### Prohibited Actions

- Unblinding cannot occur before any of the three preconditions (dataset collected, freeze verified, authorization recorded) are met.
- Emergency early unblinding requires explicit governance escalation and is not routine. It is an exception path, not a standard procedure.

### Evidence Standard

- The unblinding record must include timestamp, authorizing party, receiving party, and mapping hash.
- The preconditions must be verifiable from the recorded evidence (dataset collection complete, freeze verified, authorization recorded).

### What Violates This Policy

- Unblinding before any precondition is met.
- Unblinding without recorded governance authorization.
- Unblinding without a recorded timestamp, authorizing party, receiving party, or mapping hash.
- Routine use of the emergency early-unblinding path without governance escalation.

---

## Policy 7: Comparative Baseline Scheduling

### Purpose

To ensure that post-pilot comparisons against alternative baselines are scheduled explicitly rather than allowed to drift indefinitely, and that they are not retroactively imposed as prerequisites to the already-specified primary pilot. Comparative baselines are planned extensions, not gatekeepers for the primary DGAF-vs-null hypothesis.

### Planned Comparisons

The following comparisons are planned for post-pilot analysis, where defined by the protocol:

- null
- simple
- static
- DGAF
- DGAF+PDMAL

### Required Behavior

1. **Explicit scheduling:** Each comparison must be scheduled explicitly with a target timeframe. Comparisons are not allowed to drift indefinitely without a schedule.
2. **No retroactive preclusion:** Comparisons are NOT retroactively imposed as a prerequisite to the already-specified pilot. The primary pilot (DGAF-vs-null) proceeds on its own schedule and its own protocol. A comparison that was not specified before the pilot must not be used to delay, invalidate, or reframe the primary results.
3. **Protocol before data collection:** Each comparison must have its own protocol specification before data collection for that comparison begins. A comparison without a protocol specification is not authorized.
4. **Independence from primary hypothesis:** Comparative baseline results do not validate or invalidate the primary DGAF-vs-null hypothesis. The primary hypothesis stands or falls on its own evidence. Comparative results are supplementary and must not be treated as confirmatory or falsifying of the primary result.

### Evidence Standard

- Each comparison must have a protocol specification on record before data collection.
- The schedule for each comparison must be recorded.
- The primary pilot's protocol and schedule must not reference comparative baselines as prerequisites.

### What Violates This Policy

- Allowing a comparison to drift without a schedule indefinitely.
- Imposing a comparison as a prerequisite to the primary pilot after the pilot protocol was already specified.
- Starting data collection for a comparison without a protocol specification.
- Treating comparative baseline results as validating or invalidating the primary DGAF-vs-null hypothesis.

---

## Governance Notes

These policies are **proposed**. They require formal adoption by the governance authority before they are binding. Until adopted, they serve as a reference for the intended operating discipline but do not carry binding force.

- These policies **do not authorize execution.** Execution is governed by the execution contract and the current control state.
- These policies **do not close any predicate.** P2, P4, P6, and P6a remain in their current states (PARTIAL, OPEN, APPLICABILITY REQUIRED) as recorded in the PDMAL Current Control State.
- These policies are **designed to prevent false closure, not to accelerate it.** They establish what must hold, what evidence is required, and what constitutes violation, so that closure decisions are grounded in verified evidence rather than assumption or convenience.

### Formal Adoption Requirements

For any policy in this document to become binding, the governance authority must:

1. Explicitly adopt the policy by identity (name or role) and date.
2. Record the adoption in the governance record.
3. Bind the adoption to the current candidate SHA (`2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`) without silently changing any decision in the P7 Adjudication Record.

Adoption of a subset of policies is permissible; adoption of all is not required for any single policy to be binding. Each policy's adoption status must be individually recorded.

---

*Document drafted from: P7 Adjudication Record (panel-ready 2026-08-23), P8 Analysis Lock, P8 Verification Checklist, PDMAL Protocol Matrix amendment v0.7.5, P3/P4/P5/P6 Freeze Readiness assessment (2026-08-21), PDMAL Current Control State.*
