# Experimental Mapping for H1–H3

**Status:** Design instrument — authorization not granted  
**Date:** 2026-08-25

## Purpose

Map the publication hypotheses to measurable apparatus without initiating the PDMAL empirical pilot. This document defines what would have to be true before an authorized experiment could test the hypotheses.

## Hypotheses

### H1 — Evidence-lifecycle coupling

**Question:** Does coupling claim/evidence state to governance gates detect or prevent unsupported operational decisions that governance-only controls miss?

**Primary outcome:** rate of unsupported decisions reaching execution.

**Secondary outcomes:** blocked-invalid decisions, false blocks, evidence completeness, policy violations, and recovery/revision events.

**Minimum comparison:** governance-only baseline vs governance + evidence-state coupling.

### H2 — Independent reconstruction

**Question:** Can an evaluator reconstruct why a decision was permitted, blocked, revised, or escalated from DGAF evidence artifacts more reliably than from conventional execution logs?

**Primary outcome:** reconstruction accuracy against a blinded adjudication key.

**Secondary outcomes:** time-to-reconstruction, missing causal links, ambiguity rate, and inter-rater agreement.

**Minimum comparison:** DGAF evidence package vs conventional log package containing equivalent execution events but without the explicit claim/evidence model.

### H3 — Cost/benefit

**Question:** What auditability or detection benefit is obtained, and what latency, complexity, and maintenance cost does the coupling impose?

**Outcomes:** execution latency, artifact volume, validation cost, implementation complexity, operator effort, and detection/reconstruction benefit.

**Requirement:** benefit must be reported together with cost; no one-sided optimization claim.

## Apparatus mapping

| Requirement | Existing DGAF capability | Gap before experiment |
|---|---|---|
| Versioned governance rules | CI/repository governance | Verify exact experimental snapshot |
| Evidence artifacts | Evidence schemas/validators | Freeze canonical artifact schema |
| Claim status | Publication/evidence model | Define machine-testable status vocabulary |
| Decision gates | CI and governance gates | Define experimental gate semantics |
| Blinded evaluation | PDMAL blinding design | Verify custody and unblinding procedure |
| Reproducible runs | Seeded experiment infrastructure | Complete freeze and environment fingerprint |
| Baseline comparison | Candidate baseline matrix | Implement and validate baseline |
| Independent reconstruction | Not yet established as outcome protocol | Create adjudication rubric + blinded reviewers |
| Statistical analysis | PDMAL protocol work | Finalize endpoint/SAP before authorization |

## Negative controls

At minimum, the experiment should include:

1. A governance-only condition.
2. A deliberately incomplete-evidence condition.
3. A valid-evidence condition.
4. A policy-conflict condition.
5. A revision/recovery condition.

The exact conditions must be frozen before pilot authorization.

## Authorization boundary

This document does **not** authorize the PDMAL pilot. It is apparatus planning only.

Current state remains:

- PDMAL: PRE-FREEZE.
- Pilot authorization: NOT GRANTED.
- Empirical N: 0.
- Historical freeze artifacts are not treated as current empirical evidence.
- No publication claim of efficacy may be derived from the design itself.

## Decision gate before empirical work

The experiment may proceed only after the repository contains a frozen protocol covering topology, endpoints, failure model, recovery semantics, RNG separation, trial ordering, exclusions, stopping rules, blinding, unblinding, statistical analysis, baselines, artifact schema, SHA binding, and environment fingerprinting.
