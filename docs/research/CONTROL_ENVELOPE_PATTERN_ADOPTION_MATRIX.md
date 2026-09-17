# Control-Envelope Pattern Adoption Matrix

> **Status:** DESIGN TRACEABILITY / NON-AUTHORIZING  
> **Established:** 2026-09-17  
> **Purpose:** prevent duplicate governance subsystems by recording what is reused, adapted, or genuinely new.

## Adoption classes

- `REUSE_EXISTING_DGAF_PRIMITIVE` — preserve an existing DGAF semantic boundary; do not create a parallel concept.
- `ADAPT_ECOSYSTEM_PATTERN` — reuse a pattern already developed elsewhere in the NDR ecosystem, but establish DGAF-native evidence before claiming implementation.
- `NEW_IMPLEMENTATION_REQUIRED` — no sufficient enforced primitive has been established for the target behavior.
- `RESEARCH_ONLY` — retain as hypothesis/methodology; do not place on the authority path.

## Matrix

| Design element | Pattern lineage | Adoption class | Control-envelope treatment | Present status |
|---|---|---|---|---|
| Fail-closed prerequisite evaluation | DGAF guarded transitions / truth-layer discipline | `REUSE_EXISTING_DGAF_PRIMITIVE` | Missing, false, stale, unknown, or identity-mismatched required predicates do not satisfy a protected transition. | Semantic reuse; ledger enforcement not yet implemented. |
| Exact identity binding | DGAF candidate/source/artifact/runtime identity discipline | `REUSE_EXISTING_DGAF_PRIMITIVE` | Bind action, policy, target, evidence, executor, and receipt identities to exact scope. | Semantic reuse. |
| Proposal / authorization / commit separation | DGAF recursive control-plane pattern | `REUSE_EXISTING_DGAF_PRIMITIVE` | Add action canonicalization and commit-time revalidation without collapsing authorization into execution. | Formalized prospectively. |
| Verification != authorization != execution | DGAF evidence/governance discipline | `REUSE_EXISTING_DGAF_PRIMITIVE` | Preserve as separate state dimensions and receipts. | Already a DGAF semantic rule. |
| Evidence Card relationship | DGAF Evidence Card schema and consistency rules | `REUSE_EXISTING_DGAF_PRIMITIVE` | Link material admission predicates to evidence objects; do not invent a second evidence-maturity ladder. | Relationship specified; no schema coupling yet. |
| Append-only validity / invalidation | Dynamic Assurance Lab pattern | `ADAPT_ECOSYSTEM_PATTERN` | `ACTIVE / SUPERSEDED / INVALIDATED`; preserve history and compute affected descendants where dependency data exists. | Research/design lineage only in this tranche. |
| Explicit defeaters | Dynamic Assurance Lab pattern | `ADAPT_ECOSYSTEM_PATTERN` | Store supporting controls separately from facts that defeat admissibility. | Newly specified. |
| Digest-bound action approval | Collabration/Intellectro governed action pattern | `ADAPT_ECOSYSTEM_PATTERN` | Approval binds the exact canonical action digest; substitution fails closed. | Newly specified for DGAF generic control envelope. |
| Single-use execution authorization | Collabration/Intellectro governed action pattern | `ADAPT_ECOSYSTEM_PATTERN` | Prefer single-use action-specific authorization for high-impact actions; reusable grants require explicit policy. | Newly specified. |
| Attenuated delegation | Collabration/Intellectro delegation pattern | `ADAPT_ECOSYSTEM_PATTERN` | Child authority is a subset of parent authority; delegation cannot mint capabilities. | Newly specified. |
| Revision-aware staleness | Collabration/Intellectro provenance pattern | `ADAPT_ECOSYSTEM_PATTERN` | Preserve historical validity for exact inputs while marking currentness affected when inputs change. | Newly specified. |
| Action Receipt separation | Collabration/Intellectro accountability fabric | `ADAPT_ECOSYSTEM_PATTERN` | Keep provenance/action receipt distinct from verification result and truth claim. | Newly specified. |
| Trust-anchored lineage | ecosystem review-package hardening pattern | `ADAPT_ECOSYSTEM_PATTERN` | Digest chain + admission authority + source identity + attestation/signature + supersession/revocation; fork is explicit. | Newly specified. |
| Failure -> regression-control loop | ecosystem correction/appeal pattern | `ADAPT_ECOSYSTEM_PATTERN` | Escaped failure becomes classified regression fixture and control/test improvement without rewriting history. | Design requirement for later operations. |
| Verifier independence measurement | Structural Epistemics / triadic research | `RESEARCH_ONLY` | Do not equate multiple agents with independent verification; independence requirements are policy inputs. | Research hypothesis/measurement program. |
| Evidence-bound stabilization / unresolved state | triadic epistemic research | `ADAPT_ECOSYSTEM_PATTERN` | Permit `INCONCLUSIVE` / unresolved rather than forcing an answer or authorization. | Specified as fail-closed operational state. |
| Governance mutation testing | DGAF Discovery Harness | `ADAPT_ECOSYSTEM_PATTERN` | Mutate authority, provenance, ordering, policy, time, and error handling; dangerous mutants should be killed. | Verification method for future implementation. |
| Metamorphic monotonicity | DGAF Discovery Harness | `ADAPT_ECOSYSTEM_PATTERN` | Weaker/staler evidence and de-independence cannot increase authority. | Verification method for future implementation. |
| Verifier/property mutation | DGAF Discovery Harness | `ADAPT_ECOSYSTEM_PATTERN` | Corrupt the checker/property deliberately and require detection of the corruption. | Verification method for future implementation. |
| Consequential-action registry | no sufficiently established generic runtime registry found | `NEW_IMPLEMENTATION_REQUIRED` | Versioned denominator for coverage and enforcement scope. | Not implemented in this tranche. |
| Machine-readable Action Admission Record schema | synthesis of DGAF + ecosystem patterns | `NEW_IMPLEMENTATION_REQUIRED` | Typed record for exact action admissibility and execution binding. | Markdown specification only. |
| Gateway-level mandatory AAR enforcement | target normative control | `NEW_IMPLEMENTATION_REQUIRED` | Consequential actions lacking a valid required record cannot execute. | Not implemented. |
| Commit-time volatile revalidation | synthesis of revoked-authority-race and DGAF commit barrier | `NEW_IMPLEMENTATION_REQUIRED` | Recheck revocation, digest, target, policy, environment, limits, and defeaters immediately before side effect. | Specified only. |
| Composition/Saga coordinator | distributed transaction recovery precedent | `NEW_IMPLEMENTATION_REQUIRED` | Composition requires own identity/policy; support forward recovery, compensation, containment, or explicit partial-state handling. | Specified only. |
| Reversibility classification | control-envelope synthesis | `NEW_IMPLEMENTATION_REQUIRED` | `REVERSIBLE / COMPENSATABLE / IRREVERSIBLE`; never call compensation rollback. | Specified only. |
| Postcondition closure state machine | transition-spec extension | `NEW_IMPLEMENTATION_REQUIRED` | Execution remains historical even when postcondition is failed/inconclusive; block closure/dependents as policy requires. | Specified only. |
| Coverage audit | panel recommendation corrected by registry denominator | `NEW_IMPLEMENTATION_REQUIRED` | Report coverage only against a versioned action registry and disclose known registry gaps. | Specified only. |
| Dependency circuit breaker | reliability pattern | `NEW_IMPLEMENTATION_REQUIRED` | Block repeated failing dependency calls; breaker state never creates governance permission. | Optional future runtime mechanism. |

## Transfer rule

Pattern transfer does not transfer evidence.

A pattern developed in Collabration, Dynamic Assurance Lab, Discovery Harness, or another repository can inform DGAF design. It does not establish that DGAF has implemented or validated the pattern. DGAF-native implementation, exact-scope tests, runtime evidence, and authorization remain separately required.

## Vocabulary protection

This design MUST preserve established DGAF distinctions rather than creating new overloaded labels:

- workflow lifecycle state is not claim class;
- claim class is not evidence maturity;
- evidence maturity is not validation status;
- verification is not authorization;
- authorization is not execution;
- provenance is not truth;
- implementation is not efficacy;
- historical validity is not current admissibility.

## Explicit non-adoptions

The following are deliberately not imported as generic authority rules:

- Byzantine quorum thresholds such as `3f+1` without a formally matching fault model;
- majority consensus as a substitute for evidence-bound verification;
- agent persona count as verifier independence count;
- Merkle/hash chaining as proof of authority, completeness, truth, or trustworthy time;
- automatic P1-P9 predicate mapping from generic ledger fields;
- a single linear evidence ladder replacing DGAF's separate claim/evidence/validation dimensions;
- mandatory rollback language for irreversible actions;
- model-generated confidence as an authorization predicate without a separately validated calibration policy.

## Implementation sequencing

The safest later implementation order is:

1. consequential-action registry;
2. machine-readable AAR schema and static validator;
3. authority/delegation attenuation checks;
4. exact action canonicalization/digest binding;
5. commit-time revalidation;
6. gateway enforcement for one narrowly selected action class;
7. receipts, replay/idempotency, and lineage handling;
8. postcondition/recovery state machine;
9. coverage reporting;
10. mutation/metamorphic/adversarial verification;
11. expansion to additional action classes only after exact-scope evidence supports it.

No implementation step automatically changes scientific or High-Assurance authority state.
