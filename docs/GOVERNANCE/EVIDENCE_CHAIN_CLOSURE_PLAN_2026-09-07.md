# Evidence-Chain Closure Plan — 2026-09-07

> **Document class:** Operational closure plan; not an evidence artifact and not an authority source.  
> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.  
> **Final v0.7.6 candidate:** NOT DESIGNATED under Issue #309.  
> **P4:** OPEN / FAIL-CLOSED.  
> **P7 final binding:** OPEN.  
> **P8:** OPEN / FAIL-CLOSED.  
> **Final P9:** NOT EXECUTED.

This plan defines the order in which the remaining evidence and governance boundaries must be closed. It deliberately does **not** embed a volatile `live main` SHA as authority. Repository tips change; immutable evidence identities, issue acceptance predicates, exact PR heads, and designated candidate/freeze artifacts are the relevant identities.

The direct `main` commit `741f2c1a92297a7b2c08cfa8df6635f42e579b11` is retained as an incident boundary, not a governance promotion. Main Push Provenance Audit run `34086327869` failed for that push. Any semantically valid content from that commit must be carried forward through normal reviewed PRs before it is treated as accepted repository state.

---

## 1. Authority model

Use the following precedence when claims conflict:

1. immutable accepted evidence and explicit gate/freeze/authorization artifacts;
2. current issue acceptance predicates and source-bound governance contracts;
3. merged, verified repository implementation;
4. operational planning documents such as this file;
5. dashboards, summaries, portfolio records, and public-facing prose.

A lower layer must never strengthen a claim beyond the layer above it.

Passing CI proves only what the corresponding tests/checks actually establish. A successful synthetic contract, deployment, documentation check, or dry run is not evidence of independent custody, real Confidential Space admission, freeze, authorization, or empirical execution.

---

## 2. Gate 0 — repository integrity and mutation control (#277)

**State:** BLOCKED ON REPOSITORY-ADMIN CONFIGURATION.

The repository currently has a detective Main Push Provenance Audit, but detective controls are not equivalent to preventive enforcement. The connected automation surface can read rulesets/branch protection but cannot modify repository-administration rules safely.

Required closure evidence:

- default branch is protected by a rule that actually requires pull requests before merge;
- no rule condition accidentally excludes `main`;
- force pushes and deletion remain prohibited;
- deliberately selected merge-critical checks are required by their exact live check-context names;
- bypass actors are explicitly understood and minimized;
- conversation resolution is required where compatible;
- a controlled failing required check is proven to block merge;
- an ordinary direct contents write to `main` is proven to be rejected;
- a normal fully green PR is proven to merge through the intended path;
- live ruleset/protection readback is retained as evidence.

Do **not** import older ready-to-apply ruleset JSON from this repository without fresh validation. Earlier draft material had unsafe condition/check assumptions and is not authority.

Until this gate closes, Main Push Provenance Audit is a compensating detective control only.

---

## 3. Gate 1 — correct and qualify the real Confidential Space path (#310)

**Current engineering state:** corrected Stage-A procedure is being carried through PR #349.  
**Execution state:** NOT EXECUTED.  
**Scientific effect:** none; empirical N remains 0.

Stage-A must be one coherent real-cloud engineering path:

1. authenticated GCP project and explicitly supported Intel TDX machine/zone;
2. production Google Confidential Space VM image;
3. separate digest-pinned DGAF workload container;
4. reviewed launch contract and exact launch metadata;
5. workload service account with least-privilege roles, including the attestation-token role required by Google Confidential Space;
6. PRE token requested from inside the workload through the Confidential Space launcher socket;
7. Google signature/JWKS verification through the repository production verifier;
8. DGAF claim verification against frozen audience, subject, service accounts, image digest, args/env, hardware/security state, and PRE nonce;
9. only successful PRE admission may gate operational-key generation;
10. synthetic Stage-A workload executes without empirical observations;
11. POST token binds the same runtime identity to the final engineering-output/evidence manifest;
12. evidence is retained, retrieved, and cryptographically reverified under the declared custody model;
13. teardown is recorded.

A Stage-A PASS is an apparatus-qualification result only. It does not close P4, designate the final candidate, freeze the protocol, authorize the pilot, execute final P9, or move N above zero.

---

## 4. Gate 2 — independent security review (#320)

**State:** NOT EXECUTED / OPEN / FAIL-CLOSED.

PR #350 prepares the review package. The review source boundary is intentionally immutable even if `main` later advances:

- repository: `ndrorchestration/DGAF-Framework`;
- source commit: `1f0a7f1e99787777d18b1bd62fe41dce5286a102`;
- source tree: `ace8fce9a51b97e43e883795748ff07896292e22`;
- exact artifact blob identities: defined in `docs/GOVERNANCE/review_packages/320_mode_t_oidc_security/SOURCE_IDENTITIES.json` once PR #350 is accepted.

The reviewer must be organizationally independent from DGAF/PDMAL contribution. Repository authors, this assistant, and CI may prepare evidence but cannot satisfy that independence requirement by reviewing their own work.

Review scope includes at minimum:

- exact Confidential Space discovery/JWKS trust root and issuer consistency;
- TLS, redirect, parser, cache/rotation, JWK/RSA and algorithm restrictions;
- signed-token time handling;
- audience/subject/service-account and Confidential Space claim interpretation;
- PRE/POST nonce and runtime-identity continuity;
- admission-policy binding and caller-substitution resistance;
- operational-key release/lifetime/failure cleanup;
- integrated lifecycle ordering and retry/crash boundaries;
- Sigstore/TrustedRoot assumptions;
- retention/custody claims and synthetic-vs-production separation.

The reviewed repository contract uses the Confidential Space issuer `https://confidentialcomputing.googleapis.com`, not generic Google/Firebase identity issuers. The independent reviewer must verify that trust model against authoritative Google documentation and report any mismatch rather than inheriting DGAF's assertion.

Closure requires a report that is identity-bound, independently attributable, hash-identified, and has no unresolved `BLOCKED` findings. `UNKNOWN` is fail-closed for gate purposes.

---

## 5. Gate 3 — production trust authority and independently retained R/A/C (#316)

**State:** OPEN / FAIL-CLOSED.

The synthetic/read-only engineering path is not the production authority boundary. Production key acquisition must remain disabled/fail-closed until the retained authorization capability exists and is independently re-verifiable.

Required closure evidence:

- one canonical admission-policy identity covering the security-critical expectation fields;
- policy digest bound into reservation/freeze R before execution;
- exact digest carried through authorization A and single-use consumption C;
- production R/A/C retained outside the caller-controlled assertion path;
- retained C independently retrieved and cryptographically reverified;
- production key acquisition consumes that authenticated retained capability before entropy generation;
- caller-provided digests, booleans, expectations, or synthetic retention records cannot substitute for the retained authority;
- final signing/retention authority is instantiated;
- exact production TrustedRoot material and digest are frozen and independently approved;
- TUF/bootstrap, expiry, rotation, and update semantics are defined and verified;
- PRE binds to the consumed C and POST/output lineage cannot silently switch policies;
- #320 independent review has no unresolved blocking findings;
- real Stage-A PRE/POST evidence has been independently reverified.

P4 does not close merely because hashes exist. The required property is independently checkable custody and authority lineage.

---

## 6. Gate 4 — final v0.7.6 candidate designation (#309)

**State:** NOT DESIGNATED.

Do not designate a final candidate while security-critical apparatus or authority boundaries are still being repaired.

Candidate designation becomes appropriate only after:

- repository mutation controls are established or an explicitly accepted residual governance risk is recorded;
- Stage-A real-cloud qualification has a resolved evidence disposition;
- #320 independent review is complete and blocking findings are remediated/re-reviewed;
- #316 production R/A/C, signer/root, retention and production key-consumption boundary is resolved;
- candidate-relevant CI is clean;
- documentation no longer carries contradictory candidate/security authority claims.

Designation must produce one exact candidate commit/tree identity. Routine development must not silently redefine it.

---

## 7. Gate 5 — final P7 / P8 / P9 closure on the designated candidate

After candidate designation, rebuild the final gate packet against that exact identity.

Requirements:

- P7 final binding references the designated candidate without circular prerequisites;
- P8 evidence is evaluated under its actual acceptance predicate and remains fail-closed if evidence is incomplete;
- final P9 is genuinely independent and is executed only against the final designated candidate/evidence packet;
- historical P7/P8/P9 passes remain historical and are not promoted to the final candidate unless their identity contract explicitly permits it.

No final P9 claim may be inferred from earlier independent-verification prototypes or pre-candidate runs.

---

## 8. Gate 6 — protocol freeze

Freeze occurs only after the final candidate and candidate-bound evidence package are stable.

Freeze must bind at minimum:

- candidate source/tree;
- protocol and analysis code;
- topology/condition/failure-level design;
- seed plan and deterministic analysis seed;
- exclusion and QC rules;
- bootstrap/statistical procedure;
- evidence schemas and artifact naming/retention rules;
- dependency/environment identities;
- blinding/unblinding procedure;
- authorized execution boundaries.

Substantive post-freeze changes require an explicit amendment. A green build or candidate designation is not itself freeze.

---

## 9. Gate 7 — explicit pilot authorization

Authorization is separate from freeze.

A pilot authorization artifact must consume the frozen identities and state exactly what may execute, by whom/what, under which evidence and custody constraints, and what terminates authorization.

Until that artifact exists and validates, the system remains **NOT AUTHORIZED** and any empirical execution is prohibited by governance.

---

## 10. Gate 8 — bounded pilot, QC and sample-size decision

Only after valid authorization may empirical N move above zero.

The bounded pilot must:

- execute the frozen path rather than a development substitute;
- preserve blinding and provenance;
- produce retained evidence under the accepted custody model;
- run preregistered QC;
- feed the predefined sample-size/final-experiment decision without retrospective outcome-driven rule changes.

Pilot output is not automatically the final experiment.

---

## 11. Gate 9 — final experiment, unblinding and baselines

After the QC/sample-size decision authorizes the final run:

1. execute the final blinded experiment;
2. close evidence retention and completeness checks;
3. unblind only at the authorized point;
4. run the frozen analysis;
5. classify results according to the preregistered support criteria;
6. establish the relevant P4/PDMAL baselines;
7. propagate only evidence-supported claims to documentation, portfolio, resume and public materials.

Synthetic results, engineering dry runs and apparatus checks remain excluded from empirical claims.

---

## 12. Current critical path

The operational sequence is:

**prevent direct mutation → finish current documentation/security repairs → real Stage-A qualification → independent #320 review → #316 production custody/authority closure → designate one final candidate → final P7/P8/P9 → freeze → explicit authorization → bounded pilot → QC/sample-size decision → final experiment → unblind/analyze → publish evidence-bounded claims.**

The project should not add unrelated capabilities while these boundaries remain unresolved unless a new feature is strictly necessary to close one of them.

---

## 13. Immediate actions from this plan

1. Let PR #349 complete fresh exact-head verification; merge only if all returned checks are successful and review/thread state is clear.
2. Let PR #350 complete fresh exact-head verification; merge only under the same rule. Its immutable review-source anchor remains `1f0a7f1e...` even if the package itself merges later.
3. Merge this closure-plan correction only after its own exact-head verification passes.
4. Re-read `main` and Main Push Provenance Audit after every merge; any new direct-main write interrupts the sequence and reopens repository-integrity handling.
5. Apply and verify #277 repository-admin enforcement through an authorized administration surface.
6. Issue #320 to a genuinely independent reviewer using the frozen package.
7. Prepare #310 real Stage-A execution inputs without executing empirical work.
8. Close #316 only with real independently retained and reverified production authority evidence.
9. Keep #309 open until all candidate prerequisites are evidenced.

---

*Corrected operational plan: 2026-09-07.*  
*No scientific-state transition is claimed by this document.*
