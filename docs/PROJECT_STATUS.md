# DGAF / PDMAL Project Status

**Status date:** 2026-08-29  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Engineering lane:** PR #139 — governed control-plane integration and TGL hardening  
**Experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

DGAF is actively advancing its governed control-plane engineering work. The current engineering lane is PR #139. Its substantive implementation checkpoint `a728ce3ee8a024646c0971c9d4f392abaa3d691a` completed dedicated control-plane/TGL/adversarial/capability-boundary verification with **41/41 tests passing** in run `33247361730`. Later PR #139 commits are documented as documentation, governance, CI, and provenance-hardening changes; the 41/41 result remains scoped to that exact checkpoint.

The PDMAL research track is separately governed. It remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**. The current candidate boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`; no new immutable freeze exists and no pilot has been authorized or executed.

Historical implementation freezes and verification runs remain valid only for the exact source, environment, deployment, workflow, and artifact that produced them. They are not automatically transferable to the current candidate or later documentation lineage.

## Current gate board

| Area | Status | Interpretation |
|---|---|---|
| Governed control-plane engineering | ACTIVE | PR #139 is the current engineering lane |
| TGL contract hardening | ACTIVE | Hardened contract work is integrated in the current engineering candidate; exact-head CI remains authoritative |
| Current `main` | CURRENT LINEAGE | Documentation/evidence lineage; not automatically the experimental apparatus identity |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267…` |
| E2b | CLOSED / VERIFIED (exact historical tree) | `d299dd152…`; run `33047380487` |
| M6 | CLOSED / VERIFIED (exact candidate scope) | `ac8ea267…`; run `33050398324` |
| Current-boundary E2b | OPEN | Exact executing workflow boundary still requires verification for freeze admissibility |
| P2 runtime verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| P6a CORS verification | NOT EXECUTED | Authenticated exact deployment matrix required |
| P4 security / blinding | OPEN | Current operational custody verification required |
| P5 provenance / reproducibility | OPEN | Current execution packet required |
| P6 durable evidence custody | OPEN | Current archive/retrieval/hash proof required |
| P7 scientific specification | ADOPTED IN SUBSTANCE / FORMALLY OPEN | Exact freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Candidate-scoped closure remains required |
| P9 independent verification | NOT EXECUTED | Independent review remains required |
| New immutable freeze | NOT CREATED | No current candidate has crossed the freeze boundary |
| Pilot authorization | NOT GRANTED | Separate explicit governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## TGL / P-35 review

A prior remediation sequence exposed a substantive TGL → P-35 contract regression. The associated **41-pass / 2-fail** result remains a diagnostic finding scoped to that historical candidate; it is not a current system-wide failure rate or efficacy measurement.

The review identified contract incompatibility, premise-hook wiring, exception containment, deterministic `PASS / WARN / SKIP / ESCALATE / KILL` reduction, required-versus-conditional `SKIP` semantics, and audit-seal sequencing as areas requiring hardening. PRs #132 and #133 are historical remediation records. The current engineering lane is PR #139.

See [`docs/governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md`](governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md) for the detailed forensic record.

## Evidence boundaries

The repository uses the following evidence vocabulary:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

A result is interpreted at the scope at which it was produced. A component test establishes the tested component result; it does not establish repository-wide validation. A deployment establishes deployment state; it does not establish experimental authorization or efficacy. A historical result does not become current evidence merely because the underlying concept remains relevant.

## Historical verification retained

- E2b run `33047380487` remains exact-tree evidence for `d299dd152fb82d48a066d66a64bf0917e20d6167`.
- M6 run `33050398324` remains candidate-scoped evidence for `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`.
- Historical freeze `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only.

These records are not invalidated by later documentation changes, but neither are they promoted to evidence for a later candidate without explicit re-verification.

## Research boundaries

### PDMAL

PDMAL is an experimental research track. Its topology and mathematical structures remain research objects until the protocol, candidate identity, verification boundary, and evidence establish stronger claims. In particular, topology alone does not establish a complete Byzantine Fault Tolerance protocol or another externally defined property.

### Mathematical notation

`φ` denotes the Golden Ratio. `ρ` denotes the mathematical plastic number. `pP` / **Platinum Mean** is intentional DGAF-specific notation for `1/(2 sin(π/11)) ≈ 1.774732842`; it is not presented as a universal mathematical symbol or as a member of the quadratic metallic-means family.

See [`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md) for the canonical notation policy.

## Operational issues

- **Issue #117:** unweighted dodecahedral Forman–Ricci output is constant (`Ric_F(e) = -2`) and therefore represents `NO_DISCRIMINATING_SIGNAL`; implementation/output semantics remain open.
- **Issue #122:** P-38 source-integrity record has an incomplete historical tail; provenance-controlled reconstruction remains open.
- **Issue #137:** deployment/source-provenance gate remains part of the current engineering closure path.

## Public documentation rule

Public documentation should explain the project before exposing internal process. High-level surfaces summarize and route; technical, research, evidence, and historical records preserve the detail required for reproducibility and auditability.

See [`docs/governance/DOCUMENTATION_STYLE_GUIDE.md`](governance/DOCUMENTATION_STYLE_GUIDE.md) and [`docs/governance/PUBLIC_SURFACE_QA_STANDARD.md`](governance/PUBLIC_SURFACE_QA_STANDARD.md).

## Required closure path

1. Complete exact-head validation of the current engineering/TGL state.
2. Complete current-boundary E2b verification where required for freeze admissibility.
3. Complete authenticated P2/P6a deployment verification.
4. Complete P4/P5/P6 evidence and custody requirements.
5. Complete P7 exact freeze binding and P8 closure.
6. Execute P9 independent verification.
7. Create and independently verify a new immutable freeze.
8. Obtain explicit pilot authorization.
9. Only then execute the authorized blinded pilot.

**Current conclusion: engineering is active; the PDMAL experiment remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N = 0.**
