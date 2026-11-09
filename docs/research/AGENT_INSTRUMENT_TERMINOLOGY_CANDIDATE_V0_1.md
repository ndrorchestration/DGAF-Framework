# Agent Instrument — terminology and evaluation candidate v0.1

> **Status:** PROPOSED / `DEFINED` + `HYPOTHESIS`; not an accepted DGAF architecture primitive.
> **Scope:** Research terminology and prospective, non-authorizing experiments only.
> **Prepared:** 2026-11-09. **Repository baseline inspected:** protected `main` at `1a95b94332dffb404c5a3ce026d70781a8c10b90`. Check live Git identity again before using this as an implementation basis.
> **Scientific/authority effect:** NONE. `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`.

## Proposed definition

An **Agent Instrument** is a persistent, agent-operable interaction system exposing a small, coherent and composable vocabulary of controls over a shared, inspectable domain state. An agent can use the controls iteratively, observe consequential feedback, and construct, transform, branch, compare, and refine *multiple* valid trajectories without needing a bespoke endpoint for each desired outcome.

Its proposed *differentiator* is **playability**: a hypothesis that an agent can acquire **transferable operational proficiency** in using the controls through feedback and reusable action sequences. Measurable proficiency is a **research outcome**, not part of an automatically satisfied implementation claim.

**Plain-language translation:** A single-purpose button or canned procedure is useful, but an instrument resembles a piano or engineering workbench: a bounded set of controls supports many sequences, revisions, and outcomes. The musical analogy is `METAPHOR`; the testable properties below are the technical proposal.

**Descriptor, not a new acronym or established field label:** *stateful compositional agent interaction system*. Do not assign it an invented acronym to satisfy registry lint. The proper term remains **Agent Instrument (proposed)**.

## Minimal operational specification

An instrument candidate can be characterized as `I = (S, A, T, O, G, L)`:

| Symbol | Defined role | Required inspection |
| --- | --- | --- |
| `S` | Typed, versioned persistent *domain* state | State identity, provenance, explicit uncertainty, branch lineage |
| `A` | Small, coherent set of typed primitive controls | Preconditions, arguments, permitted effects, failure modes |
| `T` | Runtime-governed transition from state and action to next state | Explicit accepted/rejected/blocked outcome and delta, not an LLM assertion |
| `O` | Feedback/observation of state and consequences | What changed, failed, stayed unchanged, remains unknown, and at what cost |
| `G` | Externally enforced governance and effect boundary | Capability is not authority; policy admission distinct from execution |
| `L` | Retained sequence/lineage of actions and versions | Actor, source/context identity, replay limitations, custody and dependencies |

These symbols are a *descriptive contract proposal*, not a claim that DGAF currently implements this tuple as an API or mathematical formalism. Do not assume deterministic environment effects or reversibility.

### Terms to use consistently

| Term | Proposed definition | Not equivalent to |
| --- | --- | --- |
| **Instrument** | The persistent, composable agent interaction substrate | Any tool bundle, evaluation rubric, or governance authority |
| **Control / primitive action** | One typed admissible manipulation of the domain state | An autonomous authorization decision |
| **Domain object** | A typed, addressable item in the shared state | A verified real-world fact by default |
| **Feedback** | A bounded report of transition/observation, including uncertainty | A proof of correctness or empirical efficacy |
| **Phrase / reusable routine** | An inspectable, interruptible composition of controls | An opaque macro with inherited permissions |
| **Playability** | Ability to generate valid new trajectories using existing controls, with meaningful feedback | Aesthetic quality, agent sentience, or guaranteed superior performance |
| **Operational proficiency** | Measured improvement in correct, efficient and transferable control use on held-out tasks | Model-weight learning, unbounded autonomy, or a safety certificate |
| **Expressivity** | Reachable *valid* task/outcome diversity within the same control vocabulary | A high command count or unbounded capability |
| **Branch / fork** | Versioned divergence of internal workspace state | Reversal of already executed external effects |
| **Evaluation instrument** | A rubric, metric, gate or measurement protocol | **Agent Instrument** in this document |

The final row is essential for DGAF. Existing numerical and evaluation instruments such as 11Q/AXIS have their *own* identity and authority conventions; this concept must not reuse their identifiers, thresholds, scores, or promotion language. See the [DGAF canonical instrument reconciliation matrix](https://app.notion.com/p/3d1f5bad238b81c5a3bfe41ddaa112ad).

### Necessary characteristics vs testable hypothesis

A candidate interface must demonstrate **persistent shared state**, **coherent compositional controls**, **observable incremental feedback**, **multiple valid task trajectories**, and **explicit runtime permission/effect boundaries**. A tool or workflow may qualify; categories are not mutually exclusive.

**Separate hypothesis:** after exposure to prior tasks or reusable reviewed routines, the same agent solves held-out task structures more accurately or efficiently than matched alternatives without new bespoke endpoints. Failure of this hypothesis does not make the implemented controls imaginary; it *does* undermine the proposed incremental value.

## Nearest established terminology — not interchangeable

| Existing term | Alignment | Meaningful difference or uncertainty |
| --- | --- | --- |
| **Instrumental Interaction** (Beaudouin-Lafon, CHI 2000) | Domain objects manipulated through interaction instruments | Established human-computer interaction model, not by itself a theory of agent proficiency, persistent agent research state, or DGAF authorization |
| **Agent–Computer Interface** (SWE-agent / NeurIPS 2024) | Specialized commands and feedback for agents | General agent interface category; does not mandate the proposed persistent compositional substrate |
| **Compositional skills / hierarchical options** | Reusable sequences or temporally extended actions | Usually specifies behaviors; not necessarily the persistent shared domain instrument |
| **Stateful workflow runtime / experiment workspace** | Checkpoints, branches, replay, stateful execution | May completely implement the proposal; do not claim novelty when equivalent capabilities already exist |
| **Claim/evidence graph or argumentation system** | Persistent claims, supports, defeaters, and dependencies | A possible *domain substrate* for an evidence instrument, not the whole interaction architecture |
| **Self-verifying Agent Instrument** (Arjmandi, arXiv:2608.04066, 2026) | Same words, typed proposals and verification discipline | Distinct published use of the name for a specific self-verifying architecture; no entitlement to exclusive term, identity, or novelty is established |

Primary prior-art starting points: [Instrumental Interaction (2000)](https://perso.lisn.upsaclay.fr/mbl/papers/CHI2000/), [SWE-agent paper (2024)](https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html), [SWE-agent interface documentation](https://github.com/SWE-agent/SWE-agent/blob/main/docs/background/aci.md), [Arjmandi (2026)](https://arxiv.org/abs/2608.04066).

**Novelty status:** overlap with prior art is established by the cited definitions; uniqueness, novelty, market significance, patentability, and performance benefits **are not established**. A broad assertion that “there is no other name for it” is not a verified finding. The narrower observation is that none of the examined terms has yet been shown to be fully synonymous with this working definition.

## DGAF architectural fit and anti-duplication rule

**Do not promote this into the governance kernel.** Consider only a non-authorizing, optional *research/interface profile* after checking that no simpler existing interface already offers the same behavior.

| Existing owner / substrate | Proposed relationship; no new authority |
| --- | --- |
| **Structural Epistemics / ClaimGraph v0** | Reuse existing claim, evidence-root, support, contradiction, defeater, staleness and supersession representation; no second claim graph |
| **Evidence Gate v0** | Reuse evidence intake/receipts/claim ceiling; evidence admission remains non-authorizing |
| **DGAF** | Owns governance, admissibility and claim/action authority transitions; instrument requests may be denied |
| **Agent Control Plane (ACP)** | Owns bounded execution and effect admission only through existing governed contracts |
| **Agent Observation and Safety System (AOSS)** | Observes and assures at exact scope; reported observation does not itself grant authority |
| **Tektite/operator presentation** | May display state and blockers; visual affordances do not grant permission |
| **Existing Experiment 1 (#1275)** | Characterize extant queryable ecosystem state first; no competing single source of truth |

Source anchors: [ClaimGraph extraction #1173](https://github.com/ndrorchestration/DGAF-Framework/issues/1173), [Evidence Gate extraction #1170](https://github.com/ndrorchestration/DGAF-Framework/issues/1170), [queryable state Experiment 1 #1275](https://github.com/ndrorchestration/DGAF-Framework/issues/1275), [assurance profile and ownership #1183](https://github.com/ndrorchestration/DGAF-Framework/issues/1183), [comparator falsification #1061](https://github.com/ndrorchestration/DGAF-Framework/issues/1061), [architecture/current-state authority](../CURRENT_STATE.md). These source records establish *existing relevant machinery*, not the new instrument's implementation.

## First falsifiable experiment (not preregistered)

**Scope:** one isolated, non-authorizing *evidence instrument* using existing claim/evidence graph and evidence-intake semantics. Candidate controls: `add_claim`, `attach_evidence`, `challenge`, `fork`, `inspect`, `compare`. These are interface *proposals*, not asserted existing executable endpoints.

Compare three matched interfaces over the same underlying evidence corpus, graph validator, model, prompts and permissions: (A) direct existing controls, (B) fixed research workflow with equivalent capabilities, and (C) composable instrument presentation. Predeclare scenarios, randomization unit, held-out task structures, time/compute budgets, evidence snapshot hashes, stopping criteria and analysis before outcome inspection. Human review must be separately eligible and blinded where practical; same-owner model grading is internal engineering evidence only.

**Primary discriminating endpoints to preregister:** source-span-to-claim accuracy; unsupported-claim rate; correct recognition of correlated source roots and defeaters; recovery after inserted contradictory/stale evidence; false authorization/false block; retained trace reconstruction; human review effort; cost and latency. Normalize by legitimate task success and do not reward citation counts alone.

**Negative controls:** poisoned source text or instruction-in-evidence; two citations from one underlying source; superseded evidence; unverifiable support span; invalid claim-evidence edge; stale branch; replayed action; revoked authorization; interrupting a macro; attempted external effect without approval; evaluator using the same model/context to certify its own success.

**Falsification:** If a fixed workflow or existing controls achieve comparable legitimate/attack-case accuracy, reviewability, recovery and cost under fair budgets, then the proposed extra instrument layer is **not justified** by these data. If errors increase, authority separation weakens or a new state-of-truth emerges, reject the implementation candidate. Do not infer independent scientific validation or increment canonical DGAF N from this study.

## Admission and publication boundaries

- **Now:** terminology is `DEFINED`; transferable-playability value is `HYPOTHESIS`; the piano analogy is `METAPHOR`. Neither a DGAF core feature nor an established external category.
- **Next:** inspect exact source and tests for existing ClaimGraph, Evidence Gate and ACP/AOSS contracts; make a deduplicated interface-to-existing-operation map before any code.
- **Only then:** freeze a fair comparator and acceptance oracle prospectively; implement a disposable read-only or internal-state-only prototype with typed negative controls.
- **Before promotion:** prove scope, tests, source binding, security and reviewer eligibility under current repo gates. A passing test is bounded internal evidence, not independent review.
- **Never by documentation alone:** merge, release, production authorization, empirical effectiveness, claimed standards compliance, external validation, canonical scientific-N increment or High-Assurance authorization.

**Disposition:** candidate *adjacent research/interface profile*. No architecture promotion or release-gate change is proposed by this document. This document can be withdrawn without altering existing DGAF implementation, current-state predicates, or historical records.
