# External Harness Integration Boundary

## Purpose

DGAF may be developed with, embedded beside, or adapted to external agent-development and orchestration systems without transferring governance authority to those systems.

This document defines the boundary between:

1. **development assistance** — tools that help plan, implement, test, review, document, or operate DGAF;
2. **execution/orchestration infrastructure** — runtimes that schedule agents, tools, workflows, persistence, or handoffs; and
3. **DGAF governance authority** — machine-relevant evidence, provenance, admissibility, authorization, and transition semantics owned by DGAF records and validators.

The distinction is architectural. It does not establish production readiness, empirical efficacy, independent validation, runtime authority, or High-Assurance authorization.

## Three-layer model

```text
┌──────────────────────────────────────────────┐
│ Development / ecosystem layer               │
│ coding agents · skills · review · docs · CLI │
├──────────────────────────────────────────────┤
│ Execution / orchestration layer              │
│ agents · tools · workflows · persistence     │
├──────────────────────────────────────────────┤
│ DGAF governance control plane                │
│ evidence · provenance · epistemic state      │
│ authority · admissibility · transitions      │
│ authorization · revocation · claim control   │
└──────────────────────────────────────────────┘
```

An external harness may occupy one or both upper layers. It does not become an authoritative DGAF verifier merely because it generated code, executed a test, returned a success status, or produced a recommendation.

## Default trust classification

External development and orchestration systems are treated as:

`DEVELOPMENT_ASSISTANCE / NON_AUTHORITATIVE / UNTRUSTED_UNTIL_VALIDATED`

Their outputs may become candidate inputs to DGAF-controlled validation. They do not directly establish DGAF state.

## Required separation

The following substitutions are prohibited unless a future governed specification explicitly admits them:

- external harness success → DGAF verification;
- framework-native approval → DGAF authorization;
- model confidence → evidence quality;
- orchestration completion → admissible completion;
- trace existence → provenance validity;
- provider identity → independent verification;
- tool capability → permission to execute;
- development-agent review → empirical support.

The permitted pattern is:

```text
external tool proposes / implements / executes
                  ↓
        candidate artifact or evidence
                  ↓
      DGAF-native validation boundary
                  ↓
 provenance + identity + evidence checks
                  ↓
 governed state-transition evaluation
                  ↓
       accepted state or fail-closed
```

## Adapter principle

DGAF should prefer provider-neutral governance semantics with thin adapters rather than embedding one orchestration framework into the governance kernel.

A future adapter MAY translate external runtime events into DGAF candidate records, for example:

```text
runtime event
  → normalized identity
  → evidence envelope
  → provenance binding
  → requested transition
  → DGAF admissibility evaluation
  → authorization / rejection record
```

The adapter MUST NOT silently upgrade the evidentiary or authority class of the source event.

## Development-harness use

Agent-development systems may be useful for:

- planning implementation work;
- parallel code review;
- test generation and TDD assistance;
- security review;
- CI diagnosis;
- documentation maintenance;
- refactoring and dead-code analysis;
- cross-framework adapter prototyping.

These uses are operational assistance only. Acceptance remains controlled by repository tests, exact-bound evidence, governance checks, review policy, and the relevant DGAF state owner.

## Landmark comparisons

External projects are useful as architectural landmarks, not as authorities or templates to copy wholesale.

| Landmark category | Useful comparison surface | DGAF distinction |
|---|---|---|
| Agent-development harnesses | skills, specialist agents, hooks, developer UX, packaging | DGAF does not delegate governance authority to the development harness |
| Stateful orchestration frameworks | graphs, durable execution, persistence, recovery, HITL | DGAF focuses on evidence/authority/admissibility constraints over transitions |
| Agent SDKs | minimal agent/tool/handoff primitives, tracing | DGAF can govern such primitives without needing to replace their runtime |
| Guard/validation frameworks | input/output validation and policy checks | DGAF treats validation as one evidence class rather than the whole authority model |
| DGAF | provenance-bound evidence, epistemic state, admissibility, authorization, non-claims | intended governance/control-plane layer |

Named third-party integrations require separate technical evaluation before admission. This document does not claim compatibility with any specific external framework.

## Candidate governance primitive interface

A reusable DGAF governance primitive should eventually make at least the following explicit:

```text
inputs
preconditions
required authority
evidence classes
provenance requirements
admissible transition
postconditions
invalidators
reversibility / revocation behavior
failure state
```

This is a design target, not a claim that every existing DGAF gate already conforms to a single generalized interface.

## Cross-system state dimensions

For future formalization, DGAF should preserve the ability to model independent dimensions rather than collapsing them into a scalar confidence value. Candidate dimensions include:

- evidence quality;
- provenance integrity;
- uncertainty;
- authority;
- consequence;
- reversibility;
- verification class;
- transition admissibility.

`UNKNOWN` may therefore represent more than low confidence. In some states it may mean **no admissible transition has yet been established**.

These dimensions remain subjects for formalization and testing. They do not alter current authoritative project state.

## Non-effects

Adopting or evaluating an external harness does **not** by itself change:

- scientific N;
- experimental freeze state;
- empirical efficacy;
- independent-validation status;
- authorization state;
- action-class scope;
- production certification;
- High-Assurance status.

All current state remains owned by the canonical DGAF evidence and governance records.
