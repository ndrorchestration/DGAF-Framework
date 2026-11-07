# DGAF — Dynamic Governance Agentic Formation

**Evidence-bound governance and assurance for agentic AI systems**

DGAF is an **experimental research and engineering framework** for controlling what AI agents may do, what evidence supports their decisions, and which conclusions that evidence can legitimately support.

**An agent's ability to act is not permission to act. A successful action is not, by itself, proof of system-wide reliability, security, or efficacy.** DGAF explores how to represent and enforce those distinctions through explicit, inspectable software controls.

DGAF is **not** currently a certified, independently validated, production-assurance product. Its **v1 release remains on HOLD** under [Gate 0 controller #1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421).

## Why DGAF exists

An AI coding assistant may know how to edit files, have access to a repository, and pass its unit tests. Those facts do not, by themselves, answer whether a particular edit is authorized or whether its result supports a broad claim about the system.

DGAF separates five questions that are often conflated:

| Question | Meaning |
| --- | --- |
| **Can it do this?** | Technical capability |
| **May it do this?** | Current authority, delegated scope, and policy |
| **Is the evidence sufficient?** | Validity, provenance, freshness, and applicable verification |
| **What actually happened?** | Execution evidence and verified postconditions |
| **What may we conclude?** | The bounded claims supported by that evidence |

The goal is not merely another allow/deny decision. The research question is whether explicit **evidence and authorization lifecycles** can offer measurable assurance beyond well-designed conventional controls. That additional value is **not yet established**.

## A practical example

Consider an AI coding agent requesting a change to a repository.

1. **Request:** The agent proposes an exact action, target, and parameter set.
2. **Adjudication:** The system checks current delegated authority, applicable policy, and required evidence. A technically feasible action can still be denied.
3. **Execution:** An admitted action may perform only its bounded effect.
4. **Receipt and verification:** A receipt records what occurred and whether the defined postcondition was verified. The receipt is **evidence, not permission**.
5. **Next action:** The agent cannot reuse the prior receipt as authority. A subsequent consequential action requires **fresh adjudication and applicable authority**.

If the scope is revoked before admission, the action is denied without executing the effect. The public demonstration illustrates both cases in a constrained setting.

## How the governed-action lifecycle works

    REQUEST (exact action, target, parameters)
       |
       v
    CHECK CURRENT AUTHORITY + EVIDENCE + POLICY
       |
       +---- missing / stale / revoked / invalid ---> DENY (no effect)
       |
       v
    ADMIT (bounded authorization)
       |
       v
    BOUNDED EXECUTION
       |
       v
    EXECUTION RECEIPT + VERIFIED POSTCONDITION
       |
       v
    CLAIM BOUNDARY (what this evidence can support)
       |
       v
    NEXT CONSEQUENTIAL ACTION? --> FRESH ADJUDICATION REQUIRED

The **intended fail-closed rule** is that missing, conflicting, malformed, stale, or unverifiable required inputs block the relevant transition. This diagram explains the control model, **not a guarantee that every prototype or integration enforces every invariant**. Scope and actual enforcement must be checked against implementation-specific evidence.

A related idea is **epistemic transition control**: governing when the available evidence is sufficient to strengthen a *claim*, separately from governing whether software may perform an *action*.

## See or evaluate the implementation

| Path | Best for | Evidentiary meaning |
| --- | --- | --- |
| **[Public bounded demonstration](https://project-7ybao.vercel.app/demo)** | A first look without setup | A bounded, same-system allowed/denied action demonstration |
| [Demo walkthrough and proof identity](docs/DEMO_WALKTHROUGH.md) | Understanding the receipt, denial codes, and replay-only trace | Explains the scope and precise proof identity; not new validation |
| [Local operator self-test](docs/qa/DGAF_OPERATOR_SELFTEST.md) | Developers testing a clean checkout | Internal engineering evidence for the exact tested setup |
| [Outside-operator trial protocol](docs/governance/GOVERNED_REPO_OUTSIDE_OPERATOR_TRIAL_V0.md) | A qualifying uninvolved technical operator | A proposed bounded usability check; [#1210](https://github.com/ndrorchestration/DGAF-Framework/issues/1210) remains unsatisfied |

In the live demonstration, valid scoped authority admits a bounded **ephemeral audit-counter effect** and produces an execution receipt with `postcondition=VERIFIED`, `authority_effect=NONE`, and `follow_on_authority=FRESH_ADJUDICATION_REQUIRED`. Revoked authority produces `AUTHORIZATION_REVOKED` **without an execution receipt**.

The accompanying **DGAF-to-ACP cross-system trace is replay-only**. It explains the proposed responsibility boundary; it is **not** a second live cross-system execution or proof of general authorization enforcement. See the [walkthrough](docs/DEMO_WALKTHROUGH.md).

## What is implemented, and what has been established?

The repository contains governance and orchestration components, provenance and source-binding machinery, deterministic validation and negative controls, CI, experimental and blinded-data infrastructure, bounded capability-governance reference implementations, an operator-facing Governance Command Center, and a partial assurance catalog.

These artifacts have **different maturity and evidence classes**. A passing source test, a runnable demonstration, a simulated or replayed trace, an executed local experiment, and independent verification are not interchangeable. Consult the [prototype maturity map](docs/PROTOTYPE_MATURITY_MAP.md) before interpreting a capability as production-ready.

### The conventional-policy comparison

A stronger conventional policy-as-code comparator matched the bounded DGAF allow/deny model on **13 of 13 fixed fixtures** and across **112,200 systematically enumerated bounded input states**, with zero decision differences in that declared space.

Those 112,200 states are **not 112,200 independent real-world experiments**. This parity result does **not** demonstrate superior policy decisions or unique policy-engine capability. It narrows the research question to surrounding controls: evidence admissibility, provenance continuity, authority binding, transition/recovery integrity, reconstructability, and justified downstream actions or claims. Whether these provide incremental measurable assurance remains unproven.

See [comparative controller #1061](https://github.com/ndrorchestration/DGAF-Framework/issues/1061) and [independent reproduction gate #1067](https://github.com/ndrorchestration/DGAF-Framework/issues/1067).

### Research progress is not release readiness

The successor **Track A Epoch 002** completed a governed prospective collection and local locked primary analysis. Its interpretation and post-interpretation disposition are accepted **only for the exact preregistered, same-system/nonindependent scope**. This does not establish independent validation or canonical DGAF efficacy. An earlier Epoch 001 collected blinded data but could not complete its primary analysis because its protected treatment mapping became cryptographically unrecoverable. The successor made recoverable custody an explicit prerequisite.

Detailed experimental units, the custody failure, the successor lifecycle, other tracks, and DGAF-on-DGAF self-testing are explained in the [research program explainer](docs/RESEARCH_PROGRAM_EXPLAINER.md). The **50 paired seeds** and **2,250 observations** in Track A are not a promotion of the separately governed canonical High-Assurance **empirical N**.

## Current research, validation, and release boundaries

| Dimension | Status / interpretation |
| --- | --- |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Independent validation | **NOT ESTABLISHED** |
| Canonical High-Assurance empirical N | **0** |
| High-Assurance authorization | **NOT AUTHORIZED** · PRE-FREEZE · FAIL-CLOSED |
| Track A Epoch 002 | **CLOSED FOR EXACT PREREGISTERED SCOPE**; same-system/nonindependent |
| AOSS Stage-A external review | Handoff prepared; review **NOT EXECUTED** ([#929](https://github.com/ndrorchestration/DGAF-Framework/issues/929)) |
| Outside-operator usability gate | Trial packet prepared; qualifying trial **NOT SATISFIED** ([#1210](https://github.com/ndrorchestration/DGAF-Framework/issues/1210)) |
| DGAF v1 release | **HOLD**; Gate 0 and independent acceptance unresolved ([#1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421)) |

The [current state record](docs/CURRENT_STATE.md) and linked issue controllers remain the authority for exact evidence identities and permitted transitions. Its `last_verified` metadata is a **whole-record reconciliation marker**, not a claim that later issue updates have all been incorporated; inspect controlling live GitHub issues and the exact source SHA for consequential use.

## Known limitations and ongoing engineering

The following are documented **open engineering findings**, not proof of a system-wide exploit or proof that every DGAF component fails:

- [#1548](https://github.com/ndrorchestration/DGAF-Framework/issues/1548): repeated task expansion can leak control-plane concurrency accounting slots. [PR #1563](https://github.com/ndrorchestration/DGAF-Framework/pull/1563) proposes a fix; do not count an unmerged candidate as accepted protection.
- [PR #1561](https://github.com/ndrorchestration/DGAF-Framework/pull/1561): negative-test work characterizes an insufficient semantic check for sealed `PASS` evidence. [PR #1562](https://github.com/ndrorchestration/DGAF-Framework/pull/1562) proposes a correction; validation and admission remain separate.
- [#1551](https://github.com/ndrorchestration/DGAF-Framework/issues/1551): a legacy API prototype can emit misleading approval-like output and a non-cryptographic token labeled as a seal. Its deployment reachability has **not** been established. [PR #1553](https://github.com/ndrorchestration/DGAF-Framework/pull/1553) proposes fail-closed handling.
- [Gate 0 #1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421): v1 release criteria, independent sign-off, scope and security/reproducibility evidence remain outstanding. Passing tests do **not** automatically clear this hold.

For distinctions among **implemented**, **tested**, **simulated**, **replayed**, **locally executed**, and **independently accepted**, use the [prototype maturity map](docs/PROTOTYPE_MATURITY_MAP.md).

## Read deeper, by purpose

| If you want to… | Start here |
| --- | --- |
| Inspect architecture, components, execution contracts and test surfaces | [Technical reference](README.technical.md) |
| Audit evidence/authority contracts and conceptual standards mappings | [Governance reference](README.governance.md) |
| Understand experiments, comparator methodology, custody, scientific N and non-claims | [Research program explainer](docs/RESEARCH_PROGRAM_EXPLAINER.md) |
| Compare what runs against what is simulated, replay-only, or independently unverified | [Prototype maturity map](docs/PROTOTYPE_MATURITY_MAP.md) |
| Check exact current scientific/evidence state and authorization boundaries | [Current state](docs/CURRENT_STATE.md) |
| Trace superseded proposals, PR chronology, and historic engineering milestones | [Historical records index](docs/HISTORICAL_RECORDS_INDEX.md) |
| Translate DGAF vocabulary into public terminology | [Public translation layer](docs/PUBLIC_TRANSLATION_LAYER.md) |

DGAF's technical positioning is **experimental agentic-AI assurance / evidence-bound Governance-as-Code**, not independently established superiority, certification, compliance, commercial readiness, or production security. Familiar terms like **policy decision point (PDP)**, **policy enforcement point (PEP)**, and **assurance control plane** describe responsibilities; they do not confer verified security on a particular implementation.

---

**DGAF research rule:** A green test, merged pull request, authored assurance record, local research result, demonstration receipt, or UI display cannot silently become independent evidence, scientific-N promotion, generalized efficacy, continuing authority, or release approval.
