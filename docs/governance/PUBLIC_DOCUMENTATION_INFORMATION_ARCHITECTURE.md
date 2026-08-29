# Public Documentation Information Architecture

## Purpose

This repository contains implementation, research, governance, and provenance material with different audiences and evidentiary roles. This document defines the preferred public information architecture so readers can find the right level of detail without confusing a landing page, a technical reference, and a forensic record.

## Documentation layers

### 1. Landing
For first-time visitors.

Answer: **What is this, why does it matter, and where should I start?**

Primary surface: `README.md`.

### 2. Project
For readers evaluating current direction and maturity.

Answer: **What is the current state and what is being worked on?**

Primary surfaces: `docs/CURRENT_STATE.md`, `docs/PROJECT_STATUS.md`.

### 3. Technical
For implementers and reviewers.

Answer: **How is this designed and how do the components fit together?**

Primary surfaces: technical references, module READMEs, specifications, and tests.

### 4. Research and experiment
For readers evaluating hypotheses and methods.

Answer: **What question is being investigated, under what protocol, and what evidence exists?**

Primary surfaces: experiment protocols, analysis plans, and evidence indexes.

### 5. Governance and evidence
For auditors and rigorous review.

Answer: **What authority, evidence, provenance, and controls support a specific claim?**

Primary surfaces: governance policies, manifests, verification records, and retained artifacts.

### 6. Historical
For provenance and project archaeology.

Answer: **What did the project previously contain or claim?**

Historical material should be retained where useful, but should not silently compete with current authorities in primary navigation.

## Navigation rules

- Link from a broad layer to a deeper layer when additional precision is needed.
- Prefer one current authority for each important status question.
- Do not duplicate a detailed forensic record on a landing page.
- Preserve historical material through explicit status and provenance rather than deletion for appearance.
- Do not use an internal working artifact as a default public navigation target unless it has been intentionally designated for that role.

## Claim placement

Claims should appear where their evidence can be understood at the same level of detail. Broad project descriptions should avoid implying that a component-level result proves repository-wide efficacy. Detailed evidence records may contain exact identifiers, runs, environments, and predicates where those details are necessary for reproducibility.

## Maintenance test

Before adding a prominent document link, ask:

1. Who is expected to use this?
2. What question does it answer?
3. Is it current, historical, or evidence-scoped?
4. Is there already a more authoritative entry point?
5. Does this placement reduce or increase reader friction?

---

This architecture complements the Public Surface QA Standard and Documentation Style Guide. It does not replace experimental evidence or governance controls.
