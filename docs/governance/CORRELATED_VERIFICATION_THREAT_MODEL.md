# Correlated Verification Threat Model

> **Status:** EXPLORATORY GOVERNANCE RESEARCH / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Established:** 2026-09-17

## Purpose

Multi-agent systems can produce multiple agreeing outputs without producing multiple independent checks. This threat model treats **verification dependence** as a first-class governance risk.

The governing distinction is:

```text
number of verifier outputs != number of independent verification paths
```

Agreement is evidence only to the extent that the paths producing it add materially distinct information, reasoning, or observations.

## Protected assets

This threat model is intended to protect:

- factual claim integrity;
- claim-to-source provenance;
- authorization decisions;
- reviewer independence;
- tool/action integrity;
- confidence calibration;
- audit-log interpretability;
- the distinction between corroboration and repetition.

## Dependency model

For each verifier `v_i`, record a dependency signature where observable:

```text
d_i = {
  model_identifier,
  provider_or_family,
  system_and_policy_lineage,
  prompt_template_lineage,
  retrieved_source_ids,
  upstream_agent_output_ids,
  tool_output_ids,
  shared_memory_or_context_ids,
  adjudicator_or_judge_dependencies
}
```

The signature is an audit artifact, not proof of independence. Unknown fields remain `UNKNOWN`; they must not be silently interpreted as distinct.

## Threat classes

### CV-01 — Shared-source monoculture

**Trigger:** Multiple verifiers rely on the same source or a small set of mutually dependent sources.

**Failure:** Repetition across agents is mistaken for independent corroboration.

**Detection signals:**

- high claim agreement;
- low unique-source count;
- high source-concentration index;
- common critical provenance root.

**Controls:** independent retrieval where feasible, source-lineage tracking, primary-source preference, explicit source-diversity measurement, and counterevidence search.

### CV-02 — Inherited-output contamination

**Trigger:** A verifier can see earlier verifier conclusions before forming its own initial judgment.

**Failure:** Later verifiers anchor on prior outputs, reducing epistemic independence while preserving the appearance of a panel.

**Controls:** hidden first-pass judgments, delayed reveal, independent evidence acquisition, and post-reveal change logging.

### CV-03 — Model-family or provider correlation

**Trigger:** Verifiers use closely related model families, checkpoints, providers, or training lineages.

**Failure:** Shared systematic errors survive majority voting.

**Controls:** record model lineage where knowable; do not equate model-name diversity with independence; test heterogeneous panels prospectively.

### CV-04 — Judge/verifier correlation

**Trigger:** The same model, prompt lineage, evidence context, or provider architecture influences both candidate outputs and their judge.

**Failure:** A judge inherits the same blind spot as the outputs being judged.

**Controls:** distinct adjudication role, evidence-visible rejection authority, adversarial counter-checks, and explicit judge dependency metadata.

### CV-05 — Provenance aliasing

**Trigger:** Different URLs, summaries, mirrors, or agent messages derive from the same underlying primary source.

**Failure:** Source count is inflated by aliases.

**Controls:** canonical source identity where feasible, content hashes, citation-chain tracing, and provenance-root collapsing.

### CV-06 — Synthetic consensus amplification

**Trigger:** Repeated agent discussion increases claim prevalence or confidence without adding materially new evidence.

**Failure:** Confidence rises faster than evidential support.

**Prospective signal:**

```text
A_c = post_interaction_prevalence_or_confidence(c)
      / max(pre_interaction_prevalence_or_confidence(c), epsilon)
```

Track independent evidence gain `DeltaE_c` separately. A candidate danger pattern is `A_c >> 1` while `DeltaE_c ~= 0`.

### CV-07 — Counterevidence suppression

**Trigger:** A minority verifier has relevant contradictory evidence but majority or conversation dynamics suppress it.

**Failure:** Consensus mechanics eliminate the strongest correction signal.

**Controls:** protected dissent channel, required contradiction ledger, adjudicator obligation to inspect minority evidence, and no majority-only dismissal rule.

### CV-08 — Verification-path collapse after tool failure

**Trigger:** Distinct verifiers silently fall back to the same cached context, search result, or tool output after failures.

**Failure:** A nominally diverse workflow becomes operationally monocultural.

**Controls:** tool-call receipts, fallback-path logging, failure-mode labeling, and fail-closed independence claims.

## Adjacent control-envelope threat: specification gaming

Specification gaming is not a correlated-verification class, so it is not assigned a `CV-*` identifier. It is an adjacent threat that must be integrated into the action-admission design rather than hidden in a cross-reference.

**Failure chain:**

```text
proxy specification
  -> literal predicate compliance
  -> omitted case exploited
  -> formally compliant but harmful/unintended result
  -> false assurance
```

The prospective control is an action-specific specification-gaming analysis recording what the verifier actually checks, the intended norm, known omissions, exploit scenarios, mitigations, and residual risk.

See `ALIGNMENT_CONSTRAINT_LEDGER.md`.

## Dependence measurements

No single metric establishes true statistical independence. The following are **audit features** for prospective evaluation.

### Source-overlap Jaccard

For source sets `S_i` and `S_j`:

```text
J_ij = |S_i intersection S_j| / |S_i union S_j|
```

High `J_ij` indicates source overlap. It does not establish error correlation by itself.

### Source concentration

A Herfindahl-style concentration statistic may be calculated over the fraction of material claims supported by each provenance root:

```text
H = sum_k p_k^2
```

Higher `H` means support is concentrated in fewer roots.

### Novel-evidence contribution

For verifier `i`:

```text
NE_i = count(material evidence nodes first introduced by i)
```

A verifier with `NE_i = 0` may still contribute reasoning, contradiction detection, or validation; it should simply not be counted as a novel evidence source.

### Provenance-root minimum

For a material claim, collapse known aliases and derived copies into critical provenance roots. The count of roots is a conservative descriptive quantity, not a statistical effective sample size.

## Governance requirements

A high-assurance verification workflow SHOULD:

1. record verifier dependency signatures where observable;
2. preserve each verifier's initial judgment before peer-output exposure when independence matters;
3. record claim-to-source lineage, not only final citations;
4. distinguish primary sources from mirrors, summaries, and agent-derived restatements;
5. record contradictory evidence even when the final decision rejects it;
6. permit a final adjudicator to reject apparent consensus for inadequate provenance;
7. prevent an agent from self-approving a policy exception it requested;
8. label unknown dependency information explicitly;
9. avoid representing agent count as an independence count;
10. fail closed when an action requires independent verification but independence cannot be established to the required policy threshold;
11. permit `INCONCLUSIVE` or unresolved outcomes rather than forcing consensus where evidence is insufficient.

These are prospective design requirements. Existing DGAF artifacts retain their exact accepted scope.

## Experimental matrix

A future controlled evaluation can separate model diversity from evidence diversity:

| Condition | Models | Evidence acquisition | Peer outputs visible before first judgment |
|---|---|---|---|
| A | homogeneous | shared | yes |
| B | homogeneous | independent | no |
| C | heterogeneous | shared | no |
| D | heterogeneous | independent | no |

A controlled misleading-source intervention can test whether apparent consensus remains predictive after provenance dependence is considered.

### Candidate outcomes

- unsupported-claim acceptance rate;
- false acceptance conditional on majority/unanimous consensus;
- minority correction rate;
- contradiction survival rate;
- claim amplification;
- unique provenance-root count;
- source concentration;
- pairwise evidence overlap;
- judge reversal rate after provenance disclosure;
- cost, latency, and escalation rate.

No current Track A Epoch 002 data may be repurposed for this new hypothesis without separate governed authority.

## Abuse and benign-failure cases

This threat model applies both to adversarial attacks and ordinary correlated mistakes. A malicious source can exploit consensus amplification, but no attacker is required: stale documentation, a wrong API response, a widely copied secondary source, or a shared retrieval failure can create the same structure.

## Evidence boundary

External literature supports the plausibility and importance of correlated model/agent errors; it does not establish a DGAF-specific effect size.

Methodology/context references:

- Garg et al. (2025), *Correlated Errors in Large Language Models*, arXiv:2506.07962. [arXiv:2506.07962](https://arxiv.org/abs/2506.07962)
- Wu, Li & Li (2025), *Can LLM Agents Really Debate?*, arXiv:2511.07784. [arXiv:2511.07784](https://arxiv.org/abs/2511.07784)
- NIST, *Building Evaluation Probes into Agentic AI*. [NIST project page](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai)

## Falsification criteria

The DGAF-specific threat hypothesis would be weakened if, under controlled prospective testing, provenance overlap fails to predict false consensus, independent evidence collection provides no correction benefit, or raw agreement performs equally well out of sample after cost and task difficulty are controlled.
