# AOSS v0.6 Stage-A external reviewer quickstart

Status: **NAVIGATION AID ONLY — NON-AUTHORITATIVE**

Controller: #929

Authoritative handoff:
`docs/research/AOSS_V0_6_STAGE_A_INDEPENDENT_VALIDATION_HANDOFF.md`

Accepted handoff commit:
`92bc930bdd84f6c4258852e764d3e42019e41342`

Frozen ACP target:
`ndrorchestration/agent-control-plane@dbab7c1afafec524ce7c18157de2089cafe79c87`

This page reduces navigation burden for an external reviewer. It does not amend,
replace, summarize away, or widen the accepted handoff. If this page conflicts
with the accepted handoff, the accepted handoff controls.

## Minimal review path

1. **Retrieve independently.** Clone the DGAF Framework and agent-control-plane
   repositories from sources you control. Do not rely on an archive or evidence
   bundle supplied only by the project owner.
2. **Open the accepted handoff first.** Read the full independent-validation
   handoff before inspecting any claimed result or conclusion.
3. **Record independence/conflict information before substantive review.**
   Preserve reviewer identity, affiliation/role, relationship to the project,
   prior contribution or access, outcome exposure, and commercial or
   collaborative relationships.
4. **Verify identities and required predicates.** Follow the handoff's complete
   verification procedure for DGAF/ACP identities, frozen contracts, installed
   environment, source-driver/executable, destination/attempt, freshness,
   custody, five read-only replay passes, and no-retry-after-inspection.
5. **Retain your own evidence.** Keep consequential outputs outside the DGAF
   repository or in another independently controlled location where
   practicable. Recompute hashes yourself.
6. **Return a finding without a required conclusion.** ACCEPT, REJECT, or
   BLOCKED are all valid outcomes. Use the handoff's required evidence fields
   or a stricter equivalent.

## What not to use as independence evidence

The following may help diagnose engineering behavior but cannot substitute for
the independent review required by #929:

- DGAF CI results;
- the project owner's operator self-test packet;
- synthetic fixtures;
- same-system replay;
- owner-authored positive conclusions;
- a model or agent operating solely inside the project owner's retained
  execution context.

## Reviewer stop conditions

Stop and report **BLOCKED** rather than silently repairing or substituting when
a required identity is unresolved, an artifact is missing, the class set
drifts, freshness/skew rules fail, replay mismatches, custody is incomplete, or
a retry would occur after outcome inspection.

## Where to return evidence

Return the independently retained record and consequential evidence through a
durable channel you control. Content-addressed or immutable references are
preferred. The DGAF maintainer will locally reverify returned bytes and
adjudicate reviewer attribution, independence, and each acceptance predicate
separately.

## Claim ceiling

Completing these steps does not by itself establish general DGAF efficacy,
production certification, High-Assurance authorization, or a scientific-N
increment. Those remain separate governance and evidence questions.

Current controller boundary remains defined by #929 and #901.
