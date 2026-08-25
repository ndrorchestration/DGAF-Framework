# DGAF Comparative Hypotheses

**Status:** Pre-empirical research design  
**Date:** 2026-08-25

## Objective

Translate the candidate DGAF contribution into falsifiable comparisons rather than novelty assertions.

## H1 — Evidence-lifecycle coupling

A lifecycle coupling claim status, evidence requirements, governance gates, and repository artifacts may detect or prevent evidence-state violations that a governance-only baseline does not detect.

**Independent variable:** governance-only vs. governance + evidence-state coupling.

**Dependent variables:** seeded evidence-state violations detected, blocked, or incorrectly accepted.

**Required controls:** identical tasks, policies, seeds, and violation injections.

## H2 — Operational reproducibility

A versioned artifact/gate model may permit independent reconstruction of governance decisions with less ambiguity than a trace/log-only baseline.

**Dependent variables:** decision agreement, missing evidence, provenance ambiguity, reconstruction time.

**Protocol:** blind reviewers reconstruct decisions from archived evidence without access to implementation internals.

## H3 — Integration cost

Coupling governance and evidence state may improve auditability while imposing measurable implementation and execution costs.

**Dependent variables:** setup effort, runtime overhead, artifact volume, adjudication effort, failure-recovery effort.

## Falsification conditions

A hypothesis is not supported if the DGAF condition does not outperform or materially differ from the specified baseline in the preregistered direction, or if observed differences are attributable to confounds such as unequal policy coverage, unequal instrumentation, or implementation maturity.

## Current status

No hypothesis has empirical support yet. PDMAL remains pre-freeze / unauthorized with empirical N = 0.

## Prior-art boundary

The hypotheses deliberately do not test whether DGAF invented orchestration, runtime governance, provenance, trace assurance, or action mediation. Those capabilities are already represented in current literature. The research question is whether DGAF's particular coupling of claim/evidence state with governance and repository-operational controls yields measurable properties not obtained by the chosen baselines.
