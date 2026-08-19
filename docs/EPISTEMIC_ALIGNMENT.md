# DGAF Epistemic Alignment

**Status:** Draft implementation policy
**Version:** 1.0
**Date:** 2026-08-17

## Purpose

DGAF already has a canonical epistemic vocabulary. This document extends that vocabulary into a reproducible evidence architecture and aligns it with external test, evaluation, verification, and validation practice without treating external frameworks as proof of DGAF claims.

## 1. Two separate dimensions

DGAF must distinguish **claim class** from **evidence maturity**.

### Claim class

The canonical taxonomy remains authoritative:

- `DEFINED` — project-defined term or proposition
- `IMPLEMENTED` — corresponding behavior exists in code
- `COMPUTED` — reproducible calculation or test produced a value
- `VERIFIED` — specified behavior has an identified verification method and evidence artifact
- `ATTESTED` — recorded by a reviewer or historical process without independent recomputation
- `HISTORICAL` — belongs to an earlier state
- `HYPOTHESIS` — proposed relationship requiring testing
- `METAPHOR` — conceptual analogy
- `UNSUPPORTED` — insufficient evidence
- `DEPRECATED` — no longer canonical

### Evidence maturity

Evidence maturity describes how far a particular claim has progressed through testing. It does **not** replace the claim class.

Recommended maturity stages:

1. `SPECIFIED` — claim and intended context are explicit.
2. `TESTED` — a defined test has been executed.
3. `REPRODUCIBLE` — the test can be rerun from preserved inputs, code, and procedure.
4. `VERIFIED` — results establish conformance to the stated specification.
5. `VALIDATED` — evidence supports fitness for the intended use/context.
6. `EMPIRICALLY_SUPPORTED` — repeated empirical evidence supports the claim under explicitly bounded conditions.

A claim may be `HYPOTHESIS` while a test is `REPRODUCIBLE`; reproducibility of a test does not make its hypothesis true.

## 2. Verification versus validation

**Verification:** Did we implement the specified behavior correctly?

Examples: schema conformance, deterministic replay, unit correctness, state-transition tests, graph-property tests.

**Validation:** Does the system or measurement support the intended real-world or operational claim?

Examples: controlled workload improvement, independent benchmark performance, physical acoustic measurement, or replicated deployment evidence.

A verification result MUST NOT automatically upgrade a claim to validation.

## 3. Measurement-tree model

Consequential claims should be traceable through:

`claim → construct → intended context → indicator/metric → test method → ground truth → observation → uncertainty → validity argument → evidence state`

The construct describes what is actually being measured. The metric is an observable operationalization of that construct. The validity argument explains why the observation supports the intended interpretation.

## 4. External alignment

External sources may provide:

- terminology and methodological guidance;
- benchmark definitions;
- measurement practices;
- known failure modes;
- independent reference implementations;
- evidence that a method is established elsewhere.

They do **not** establish that DGAF itself has achieved the corresponding result.

Initial external anchors include NIST AI TEVV, NIST AI RMF, NIST ARIA measurement/evaluation work, agent-evaluation research, and autonomous-agent evaluation methodology such as METR.

## 5. Evidence boundary

Every consequential DGAF claim should identify:

- exact claim text;
- scope and intended context;
- evidence class;
- measurement method;
- source data or ground truth;
- reproducibility information;
- uncertainty/limitations;
- provenance;
- external references, if any;
- last verification date.

Historical or attested evidence must retain its historical/attested status and must not be silently promoted to current verification.

## 6. Governance rule

The strongest supported statement is the permitted statement.

Do not transform:

`code exists → system works`

`unit test passes → real-world efficacy`

`external paper exists → DGAF result`

`historical PASS → current verification`

`mathematical identity → engineering guarantee`

## 7. Acceptance criterion

An external reviewer should be able to select a consequential DGAF claim and trace it from its exact wording through measurement and evidence to the bounded conclusion without relying on undocumented conventions.
