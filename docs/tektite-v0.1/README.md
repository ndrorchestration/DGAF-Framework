# Tektite v0.1 — Public Governance Console Seed

## Purpose

Tektite v0.1 is the minimum public release of the Tektite governance-console shell.

It is a static or semi-static public surface that explains:

- what happened;
- what evidence supports it;
- what claims are currently justified;
- what remains blocked;
- what is authorized next.

Tektite is not a second governance authority. DGAF remains the governance/admissibility authority. ACP remains the execution-boundary/control-plane authority. Tektite projects curated public status, evidence, limitations, and service translation.

## Required pages

1. **Home** — one-sentence definition, core question, status snapshot, what Tektite shows, what it does not claim.
2. **Governance Console** — current status, claim ceilings, authorization state, blocked transitions, latest milestone.
3. **Evidence Ledger** — curated public evidence rows with `claim_supported`, `claim_not_supported`, and `authorization_effect` fields.
4. **Case Studies** — ACP PR #145, DGAF claim discipline, AI Evidence Audit, optional Aetherwake orchestration.
5. **Services / About** — Andrew/NDR professional positioning, service cards, public/private boundary note.

## Required components

- `StatusCard`
- `EvidenceRow`
- `BlockedTransitionCard`
- `CaseStudyCard`
- `SystemCard`

## Concrete build order

1. Static shell and routing.
2. Static JSON/Markdown data seed for status, claim ceilings, latest milestone, active blockers, and evidence rows.
3. Reusable UI components.
4. Governance Console page.
5. Evidence Ledger page.
6. Case Studies page.
7. Services/About page.
8. Public/private boundary QA.
9. Claim QA: every claim must have source, status, scope, limitation, and authorization effect.
10. Release gate.

## Non-goals

Tektite v0.1 is not:

- a live agent-control system;
- a Notion mirror;
- a raw research archive;
- a live CI dashboard;
- a private project portal;
- a compliance claim;
- a production executor;
- proof of independent validation.

## Boundary

This package is documentation and static-data seeding only.

It does not authorize live executor promotion, rollback execution, production executor deployment, independent validation, canonical efficacy, or High-Assurance status.
