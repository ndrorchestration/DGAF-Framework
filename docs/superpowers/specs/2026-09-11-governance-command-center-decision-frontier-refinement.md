# DGAF Governance Command Center — Decision Frontier Refinement

**Date:** 2026-09-11  
**Applies to:** `docs/superpowers/specs/2026-09-11-governance-command-center-ui-design.md`  
**Scientific-state effect:** NONE  
**Authority effect:** NONE

## Purpose

Refine the accepted Governance Command Center architecture without replacing it. The first implementation correctly separated Overview, Control Room, Governance, Agents & Formations, Evidence & Research, and Tools, but visual review showed that repeated cards could still make repository truth, runtime health, evidence, blockers, and permission feel like peer dashboard metrics.

DGAF's interface should instead make the **current admissible decision frontier** the primary control object.

## Expert-lens synthesis

The refinement was reviewed from six complementary perspectives:

1. product and portfolio comprehension;
2. governance and epistemic semantics;
3. operator workflow;
4. external technical-review comprehension;
5. visual-system and accessibility behavior;
6. frontend information architecture.

The common conclusion is to retain the #631 architecture while reducing generic dashboard repetition and making ordered control flow visually dominant.

## Design decisions

### 1. Decision Frontier is the primary control object

Overview, Governance, and Control Room consume one presentation component that answers, in order:

`Evidence → Blocker → Action Permitted Now`

The component consumes `NEXT_TRANSITION`; it does not define or infer a second governance state model.

The current frontier remains repository custody acceptance. Bounded operator-local recovery evidence exists, repository custody acceptance remains NOT ESTABLISHED, and the admissible action is limited to admission and validation of the exact existing non-secret public artifacts.

### 2. Repository truth becomes a compact beacon

The persistent truth surface remains visible across views but no longer occupies a multi-row dashboard grid.

Collapsed state exposes the minimum orientation set:

- PRE-FREEZE;
- NOT AUTHORIZED;
- N=0.

Expanded state exposes:

- FAIL-CLOSED;
- canonical efficacy NOT ESTABLISHED;
- repository presentation-authority provenance.

This preserves truth salience while preventing the governance boundary from consuming the mobile viewport.

### 3. Authorization prohibition is not visualized as execution failure

`NOT AUTHORIZED` receives a dedicated authority/lock tone rather than the destructive failure tone.

This is a semantic correction in presentation only. A correctly enforced governance prohibition is expected system behavior and must remain visually distinct from `FAILED`.

### 4. Overview uses DGAF's actual control grammar

The decorative orbit is replaced by the control chain:

`Evidence → Verification → Authority → Permission`

The visual boundary explicitly states that no implication occurs across stages. This makes DGAF's governing distinction a recognizable interface primitive rather than decorative branding.

### 5. Governance is rendered as semantic lanes

The ordered lifecycle remains unchanged, but presentation groups it into four lanes:

1. **Pre-authorization control** — custody, preflight, freeze, closure, verification, collection authorization;
2. **Empirical execution** — collection, quality control, dataset lock;
3. **Controlled disclosure** — unblinding decision, controlled materialization;
4. **Primary analysis** — analysis authorization, locked analysis.

The current repository-custody stage is marked as the frontier. Prepared tooling remains separately labeled and never promotes the predicate state.

### 6. Operator detail uses progressive disclosure

Overview and Governance remain comprehension-first. Control Room may expand an operator handoff containing the exact safe branch, helper command, and staged-scope verification command already defined by repository tooling.

The operator handoff must never request, expose, stage, or describe secret material as an input to the UI. Private keys, passphrases, encrypted backups, and blinding secrets remain outside the presentation and repository boundary.

## Responsive hierarchy

Desktop prioritizes the control chain and horizontal Evidence → Blocker → Action flow.

At narrower widths:

- the Decision Frontier becomes a vertical sequence;
- governance lanes stack without changing order;
- the truth beacon compresses to essential state;
- operator details remain collapsed by default;
- exact artifact paths wrap rather than overflow.

## Non-effects

This refinement does not:

- change `TRUTH_BOUNDARY`, governance-stage ordering, or predicate meaning;
- establish custody, freeze, closure, verification, collection authorization, empirical collection, dataset lock, unblinding, materialization, analysis authorization, or efficacy;
- infer repository state from runtime health;
- add backend capability;
- change empirical N;
- weaken fail-closed behavior.

Controlling state remains:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

Canonical DGAF efficacy remains `NOT ESTABLISHED`.

## Follow-up boundary

Route-level addressability for the six major views is a separate information-architecture improvement. It should be handled independently after this presentation refinement is accepted so a navigation refactor does not obscure review of governance semantics and visual hierarchy.
