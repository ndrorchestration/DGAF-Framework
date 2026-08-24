# Adversarial Expert Panel Review — 2026-08-21

## Purpose

Stress-test the current DGAF/PDMAL freeze apparatus for weaknesses before any new freeze or empirical authorization. This is an adversarial engineering/methodology review, not an independent P9 certification.

## Panel roles

1. Principal Software Architect — state coupling, stale bindings, architecture.
2. Experimental Methodologist — estimand, contrast, statistical validity.
3. Epistemic/Provenance Auditor — claim status, historical/current contamination.
4. Security/Blinding Reviewer — leakage, secrets, authorization boundaries.
5. Reproducibility Engineer — determinism, environment, artifacts, custody.
6. Adversarial Release Engineer — CI/CD, deployment identity, race/false-green paths.

## Findings

### A1 — Candidate drift

**Risk: HIGH.** Documentation commits repeatedly advance `main` after deployment. A previously READY deployment can therefore become stale relative to the repository.

**Required control:** every candidate evidence record must bind an immutable Git SHA to an exact deployment ID and reject missing/mismatched identity.

### A2 — Deployment readiness is not runtime evidence

**Risk: HIGH.** A Vercel deployment reaching READY proves successful build/deployment, not application behavior. Current `/api/health` access redirects to Vercel SSO, and no runtime logs were observed for the candidate deployment.

**Required control:** P2/P6a remain unverified until candidate-bound runtime assertions execute and produce retained evidence.

### A3 — Historical evidence promotion

**Risk: HIGH.** Historical P6a/PDMAL evidence is legitimate evidence of prior states but could be accidentally consumed by current predicate tooling.

**Required control:** evidence must carry source SHA, deployment ID, protocol identity, and temporal classification; historical records cannot satisfy current predicates.

### A4 — Audit self-staleness

**Risk: MEDIUM/HIGH.** An exhaustive audit workflow can itself become stale or run against a different SHA than the repository state being evaluated.

**Required control:** audit output must record the exact checked-out SHA and fail if the expected candidate identity is absent or inconsistent.

### A5 — Semantic namespace migration

**Risk: HIGH.** FLAG-02 has historical and current meanings. Human-readable documentation alone is insufficient to prevent accidental semantic reuse.

**Required control:** current terminology must be machine-distinguishable from historical references; new documents must not introduce FLAG-02 as a current evaluation-mode label.

### A6 — P7 decision leakage

**Risk: HIGH.** Leaving the primary contrast open is methodologically correct pre-freeze, but selecting it after observing results would create outcome-dependent analysis.

**Required control:** primary contrast, estimand, direction, multiplicity, exclusions, and analysis authority must be locked before unblinding/empirical interpretation.

### A7 — Blinding verification gap

**Risk: HIGH.** Presence of a blinding primitive or synthetic procedure does not establish operational separation of labels and secrets in the actual execution path.

**Required control:** synthetic operational verification must pass before freeze; production-secret access must remain prohibited during verification.

### A8 — Custody gap

**Risk: HIGH.** Repository persistence and SHA sidecars do not by themselves establish durable research custody.

**Required control:** actual archive → retrieve → recompute → compare → record round-trip event is required.

### A9 — P9 independence

**Risk: HIGH.** A checklist run by the same authoring environment cannot constitute meaningful independent verification.

**Required control:** P9 must be performed through an independent verification path against the immutable frozen candidate.

### A10 — False-green CI possibility

**Risk: MEDIUM/HIGH.** Candidate-bound workflows can still produce misleading green results if required inputs are defaulted, deployment identity is not validated, or artifacts are not linked to the tested SHA.

**Required control:** fail closed on absent candidate SHA/deployment identity; retain the identity in the artifact; reject artifacts whose identity does not match the requested candidate.

## Required adversarial pre-flight

Before freeze authorization, all of the following must be true:

```text
candidate SHA immutable
AND exact deployment identity verified
AND runtime reachable
AND P2 assertions passed
AND P6a assertions passed
AND artifact candidate-bound
AND historical evidence excluded
AND blinding operationally verified
AND custody round-trip verified
AND P7 contrast locked
AND P8 analysis lock established
AND P9 independently executed
```

Any `NO`, `UNKNOWN`, or `STALE` state blocks progression.

## Disposition

The panel finds the current apparatus substantially stronger than the historical state but **not freeze-ready**. The dominant remaining weaknesses are execution/evidence boundaries, not missing prose.

No empirical result is established. Empirical N remains 0. Pilot authorization remains not granted.
