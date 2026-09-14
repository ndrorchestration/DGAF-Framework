# DGAF Agents + Evidence System UI Refinement

**Date:** 2026-09-11  
**Depends on:** `ui/governance-clarity-refinement-2026-09-11` / PR #636  
**Scientific-state effect:** NONE  
**Authority effect:** NONE  
**Runtime API effect:** NONE

## Purpose

The Governance Command Center now has a strong Overview, Decision Frontier, truth boundary, and governance lifecycle grammar. The remaining Agents & Formations and Evidence & Research views still read primarily as collections of generic cards. This refinement gives those views DGAF-specific information architecture without changing their underlying data or claim semantics.

## Design decision: formation before identity

The runtime roster is easier to understand when the coordination context is visible before individual codenames. The Agents view therefore uses this hierarchy:

1. validated runtime snapshot and provenance;
2. runtime formation topology;
3. searchable agent directory;
4. ontology boundary.

The topology is derived only from the existing validated roster response. It does not infer hidden relationships, authority, capability, or scientific meaning from names or visual proximity.

Agent labels continue to use the public translation layer so function is presented before project-local identity. Runtime codenames remain available for exact lookup.

## Design decision: evidence lineage before glossary

The Evidence view now presents the current evidence boundary as four separate objects:

1. bounded operator-local recovery evidence;
2. repository custody predicate;
3. successor collection permission;
4. canonical efficacy claim ceiling.

These are visually connected to help a reader understand the current state, but the UI explicitly states that movement at one layer does not promote the next. The sequence is explanatory, not a new governance engine.

The existing repository truth sources, epoch summaries, and epistemic vocabulary remain the data authorities. The glossary is retained as reference material, but it is no longer the primary explanatory object.

## Visual grammar

- Formation topology uses restrained rails and bounded member nodes rather than a social-network graph. This avoids implying quantitative edge weights, hierarchy, or communication telemetry that the backend does not provide.
- Runtime snapshot metrics are descriptive only: agents, formations, registered NDR-pattern count, and version.
- Evidence lineage uses the existing semantic status system, including the dedicated authority/lock treatment for `NOT AUTHORIZED`.
- Epoch 001 and Epoch 002 remain visibly separate records.
- Mobile collapses topology and evidence rails into ordered vertical flows without hiding claim/status text.

## Non-goals

This refinement does not:

- create or modify `/api/roster`;
- infer live inter-agent messages or edge traffic;
- calculate topology metrics not returned by the runtime;
- claim that roster health establishes governance state;
- create new evidence, verification, or independence classifications;
- establish repository custody, freeze, closure, authorization, empirical results, or efficacy;
- change the controlling `PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0` posture.

## Acceptance

The stacked PR must pass the existing UI semantic/contract tests and production Next.js build. It must also preserve the existing repository-wide truth and governance gates. Under the standing merge policy, it remains unmergeable to `main` until its parent PR is admitted and all required checks/statuses for the eventual exact merge head pass.
