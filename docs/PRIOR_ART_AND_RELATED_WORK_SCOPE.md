# DGAF Prior-Art and Related-Work Scope

**Status:** Active research map and comparison protocol; no absolute novelty conclusion  
**Updated:** 2026-09-01

## Purpose

This document defines how DGAF's related-work and prior-art review is conducted before public claims about novelty, distinctiveness, or priority are strengthened.

The purpose is not to search for evidence that confirms originality. The purpose is to identify relevant overlap, distinguish terminology from mechanism, and compare the **governed object and lifecycle** of candidate predecessors.

## 1. Review question

The primary question is:

> Which elements of DGAF are established techniques, adaptations, combinations, or potentially distinct formulations when compared with relevant work in multi-agent systems, organizational MAS, agent governance, runtime assurance, evaluation, provenance, distributed systems, and research workflow governance?

The architecture-level question is:

> Even where individual components are established, did DGAF independently couple formation state, formation authority, veto/conflict/escalation, formation-transition idempotency, provenance, exact candidate identity, verification, and authorization into one continuous governed lifecycle?

Neither question is answered by terminology alone.

## 2. Required comparison dimensions

Each candidate prior work should be compared across:

| Dimension | Question |
|---|---|
| Governed object | Action, agent, task, workflow, organization/formation, artifact, or candidate? |
| Formation | Are groups/organizations explicit and dynamically changeable? |
| Membership/roles | Are role and membership changes represented as governed state? |
| Topology | Does structure affect coordination, authority, or policy? |
| Authority | Where are decision rights, delegation, and override rules represented? |
| Transitions | Are creation, reconfiguration, handoff, escalation, suspension, or dissolution explicit? |
| Veto/conflict | Can one authority block, pause, or resolve another authority? |
| Idempotency | Is repeat behavior controlled at the relevant state/formation transition boundary? |
| Evidence/provenance | What evidence is attached to state or transitions, and how is it reconstructed? |
| Candidate identity | Is evidence bound to an exact source/artifact/candidate identity? |
| Verification | Can an independent party verify the evidence/object relationship? |
| Authorization | Does promotion or execution authorization resolve against the same identity/evidence? |
| Experimental status | Are design, implementation, verification, and empirical claims explicitly separated? |

A feature match without a governed-object and lifecycle match is not architectural equivalence.

## 3. Required research domains

The review must cover at minimum:

1. Organizational multi-agent systems and dynamic reorganization.
2. Agent orchestration and control planes.
3. AI governance and runtime assurance.
4. Agent evaluation, testing, and benchmarking.
5. Provenance, attestation, traceability, and reproducibility.
6. Distributed reconfiguration, recovery, and idempotent state transitions.
7. Software supply-chain security and candidate/release governance.
8. Research workflow provenance and experiment-version management.
9. Formal methods where DGAF makes bounded formal claims.

Additional domains should be added when a DGAF component depends materially on them.

## 4. Established prior-art baseline

The current review establishes the following broad prior art:

- Dynamic organizational reorganization and authority over organizational structure predate DGAF.
- Organizational MAS frameworks treat roles, groups, assignments, policies, and adaptive organizational state as explicit concepts.
- Modern agentic systems provide runtime governance, supervision, constraint graphs, authority resolution, audit/replay, veto, and escalation.
- SLSA and in-toto establish exact artifact/source identity and evidence-subject matching as verification principles.
- Idempotency and reconfiguration safety are established distributed-systems techniques.

Therefore DGAF must not claim firstness for these primitives individually.

## 5. Architecture-level comparison target

The principal historical hypothesis is represented as:

`Q = <GF, AF, VF, IF, PC, XC, L>`

where:

- `GF` = formation is an explicit governed state;
- `AF` = authority is attached to formation state;
- `VF` = veto/conflict/escalation constrains formation governance;
- `IF` = formation transitions are explicitly idempotent;
- `PC` = experimental evidence is bound to an exact candidate identity;
- `XC` = verification/authorization resolves against that candidate;
- `L` = the controls participate in one continuous lifecycle.

A candidate source with only a subset of these dimensions is a **near-composition prior**.

## 6. Evidence hierarchy for historical comparison

Prefer, in order:

1. dated primary implementation or repository commits;
2. versioned specifications/ADRs and formal papers;
3. archival documentation attributable to the system maintainers;
4. secondary descriptions only when primary evidence is inaccessible and the limitation is recorded.

A source must be dated to the relevant historical cutoff. Post-cutoff implementations cannot be used to establish earlier priority without contemporaneous evidence.

## 7. DGAF chronology that must remain separate from priority

The current repository record shows:

- **2026-04-29:** `bb5c8f19d393cf04eacac66ba3a58df97671bfdb` changes the public framework expansion to **Dynamic Governance Agentic Formation**.
- **2026-05-01:** `edc9f93da03747cfab3a6610d3349a122ba5f128` adds explicit authority-conflict resolution, sovereign veto, timeout escalation/blocking, and formation idempotency semantics to the Harmonic Quintet.
- **2026-08-21:** development/candidate separation and candidate-bound execution path are explicitly documented.

These dates establish repository provenance for successive DGAF formulations. They do not establish historical firstness.

## 8. Candidate/evidence discipline

The following are established external principles, not DGAF inventions:

- evidence must apply to the exact artifact/source revision under verification;
- attestations can be rejected when subject/digest identity does not match;
- immutable or content-derived revision identifiers can anchor provenance;
- stale evidence must not silently qualify a changed object;
- release candidates can be kept distinct from moving development state.

The narrower DGAF hypothesis is about **governance placement**: whether these established principles were explicitly integrated into an experimental authorization lifecycle so that a moving development branch cannot silently redefine the evaluated candidate.

## 9. Novelty language rules

Use:

- “DGAF presents a documented synthesis…”
- “DGAF combines…”
- “DGAF proposes…”
- “The repository documents…”
- “Potentially distinctive integration…”
- “No equivalent predecessor was located in the bounded review…”

Avoid:

- “first ever”;
- “unique” without a defined comparison universe;
- “unprecedented”;
- “invented” for established primitives;
- “solves” where evidence supports only implementation or bounded testing.

Publication timestamp establishes public existence of a formulation at a time; it does not by itself establish conceptual priority.

## 10. Deliverables

The review should maintain:

- a primary-source bibliography;
- a feature/claim comparison matrix;
- an architecture-level predecessor table;
- explicit contradictions and downgraded claims;
- a list of unresolved historical questions;
- a narrowly scoped contribution statement.

## 11. Current conclusion

**No absolute novelty conclusion has been reached.** The current public record supports describing DGAF as an open research and implementation framework with an evidence-aware governance formulation.

The strongest remaining historical question is whether an earlier public system implemented an equivalent **cross-domain lifecycle** connecting formation governance to candidate-bound experimental verification and authorization. This is an architecture-level comparison, not a primitive-level novelty claim.

## Cross-references

- [`research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`](research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md)
- [`research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md`](research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md)
- [`DGAF_RELATED_WORK_MATRIX.md`](DGAF_RELATED_WORK_MATRIX.md)
- [`PUBLICATION_AND_PROVENANCE_SPINE.md`](PUBLICATION_AND_PROVENANCE_SPINE.md)
- [`CLAIM_EVIDENCE_INDEX.md`](CLAIM_EVIDENCE_INDEX.md)
- [`CURRENT_STATE.md`](CURRENT_STATE.md)
- [`experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md`](experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md)
