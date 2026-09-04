# DGAF Instrument Identity Policy v1.0

**Status:** Audit control / non-authoritative until ratified
**Date:** 2026-09-04
**Purpose:** Prevent score, gate, metric, and rubric aliases from being treated as interchangeable evidence.

## 1. Core rule

A numerical or control result is not authoritative when it is identified only by a human-readable label such as `score`, `composite`, `AXIS`, `11Q`, `P-11`, `P-15`, or `harmonic_score`.

Authoritative evidence must bind, at minimum, to this identity tuple:

```text
instrument_id
instrument_version
instrument_type
canonical_source
formula_or_algorithm
parameter_set
score_range
thresholds_or_predicates
scope
authority
binding_strength
implementation_ref
source_commit
execution_run
execution_timestamp
upstream_dependencies
epistemic_status
```

## 2. Instrument classes

The following are distinct classes even when names overlap:

- **RUBRIC:** evaluates an artifact, agent, or process using defined dimensions and scoring rules.
- **GATE:** determines admissibility/continuation using predicates or quorum rules.
- **METRIC / SCORE:** computes a numerical measurement or control signal.
- **PROTOCOL:** defines an executable procedure.
- **ATTESTATION:** records a claimed verification result and its provenance.
- **EVIDENCE / REPORT:** records observations or conclusions without becoming the governing instrument.
- **HISTORICAL LINEAGE:** preserved prior-state material that must not silently become current authority.

## 3. Required lineage semantics

Every derivative instrument must explicitly declare one of:

1. `IMPLEMENTS` — materially implements the cited canonical model.
2. `EXTENDS` — preserves the canonical model and adds bounded semantics.
3. `ADAPTS` — intentionally changes semantics and therefore requires a new instrument identity.
4. `HISTORICAL` — preserved for traceability only.
5. `SUPERSEDES` — replaces a prior instrument by explicit authority decision.

A derivative may not claim `IMPLEMENTS` when score domain, dimensions, aggregation rule, or governing predicates materially differ from the cited source.

## 4. Mathematical integrity checks

Before an instrument can be marked executable canonical authority, its implementation or verifier must check, where applicable:

- weight sums;
- score-domain consistency;
- aggregation normalization;
- threshold reachability;
- boundary behavior;
- critical-fail precedence;
- parameter-set identity;
- deterministic replay inputs;
- derivative-to-canonical correspondence.

No check may silently normalize, rescale, substitute thresholds, or resolve aliases.

## 5. Evidence dependency rule

Derived evidence inherits the verification status of the instruments and artifacts it depends on. A derived result cannot be promoted above the epistemic status of an unresolved upstream algorithm, parameter set, or execution artifact.

This applies directly to historical attestation records and downstream metrics such as P-34.

## 6. Authority rule

When two artifacts disagree about a formula, threshold, identity, or scope, the disagreement is a **control defect** until an explicit authority decision resolves it. Newer prose, higher thresholds, successful CI, or directory presence does not by itself establish authority.

## 7. Current audit examples

The following remain explicitly unresolved as of 2026-09-04:

- `QA-11Q-ARTIFACT-v1`: published weights total 1.50 while its formula divides by 11.
- `GATE-11Q-v2`: distinct 11-gate deployment procedure; must not be conflated with P-11 scoring.
- `AXIS-v1.2` versus the seven-dimensional Apogee derivative.
- P-15 Reson coupling minimum versus Reson's internal QA seal floor.
- AHG Stability Index parameter lineage and divergence normalization.
- Harmonic Quintet matrix invariant versus printed matrix.
- NDR Markdown registry versus machine-readable JSON registry release identity.
- Agent A-ID mappings across roster, topology, and ecosystem sources.

## 8. State boundary

This policy is an audit/control artifact. It does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**DGAF scientific state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.

## References

- NIST AI RMF: Govern, Map, Measure, and Manage lifecycle functions; measurement should use rigorous testing, uncertainty, traceability, and documentation.
- SLSA Provenance 1.2: artifact provenance should make where, when, and how an artifact was produced verifiable.
- GitHub Actions secure-use guidance: pin third-party actions to full-length commit SHAs and minimize workflow permissions.
