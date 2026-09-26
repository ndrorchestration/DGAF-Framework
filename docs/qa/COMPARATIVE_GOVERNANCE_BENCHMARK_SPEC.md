# Comparative Governance Benchmark — Prospective Specification

> **Status:** PROSPECTIVE / NON-COLLECTING UNTIL SEPARATELY AUTHORIZED  
> **Purpose:** Determine whether DGAF prevents failure classes that simpler governance approaches miss, while measuring operational cost.

## Research question

Under identical tasks and injected failures, does DGAF improve governance outcomes relative to simpler baselines without unacceptable false blocking, latency, policy complexity, or operator burden?

This question is not answered by this specification.

## Baselines

| ID | Baseline | Minimum definition |
|---|---|---|
| A | Prompt-only | Behavioral instructions with no external authority enforcement. |
| B | RBAC/ACL | Identity-to-permission checks without DGAF evidence/claim-state semantics. |
| C | Policy-as-code | External runtime allow/deny policy over proposed actions. |
| D | DGAF | Evidence-, provenance-, verification-, and authority-conditioned admission using the bounded implementation under test. |

Implementations must be frozen and recorded before result inspection.

## Failure families

### Operational authority

- prompt-injection escalation;
- confused deputy;
- unauthorized delegation;
- credential/token replay;
- compromised sub-agent;
- replayed consequential action.

### Evidence and provenance

- stale evidence;
- fake evidence;
- provenance substitution;
- alias-derived false corroboration;
- evidence unavailable/conflicted.

### Epistemic authority

- engineering PASS promoted to efficacy;
- same-system verification promoted to independence;
- execution promoted to validation;
- unsupported claim asserted instead of UNDETERMINED;
- stale evidence used beyond its admitted scope.

### Composition

- sensitive read -> agent transfer -> external write;
- individually authorized operations producing an unauthorized combined effect;
- authority laundering across delegation chains.

### Presentation/control-plane

- UI-state spoofing;
- presentation-only state treated as runtime authority;
- catalog membership treated as requiredness or empirical evidence.

## Required outcomes

For each trial record:

- task success/failure;
- unsafe action attempted;
- unsafe action admitted;
- unsupported claim attempted;
- unsupported claim admitted;
- legitimate action blocked;
- decision latency;
- end-to-end latency;
- operator interventions;
- policy/configuration count and size;
- recovery steps;
- evidence/provenance record identifiers;
- final decision reason.

## Primary engineering metrics

```text
unsafe_action_acceptance_rate
unsupported_claim_acceptance_rate
legitimate_task_completion_rate
false_block_rate
median_governance_latency
p95_governance_latency
operator_interventions_per_task
policy_complexity
median_recovery_time
```

No single metric is a sufficient superiority criterion.

## Fair-comparison constraints

1. identical task fixture and injected failure per paired comparison;
2. same external tools and data where possible;
3. same consequence boundary;
4. no baseline-specific hidden information;
5. retain all negative and blocked outcomes;
6. record configuration effort separately from runtime effort;
7. do not tune a baseline after inspecting its result unless all systems are re-frozen and rerun;
8. preserve same-system versus independent evaluation status.

## Claim ceiling

Permitted result language before independent validation:

- “under this bounded benchmark...”
- “in these retained fixtures...”
- “DGAF blocked X/Y injected failures while baseline B blocked ...”

Not permitted from this benchmark alone:

- “DGAF is state of the art”;
- “DGAF is safer in general”;
- “DGAF is production-certified”;
- “DGAF is independently validated.”

## Falsification criteria

The hypothesis that DGAF's added complexity is justified is weakened if:

- it does not materially reduce unsafe-action or unsupported-claim acceptance relative to simpler controls;
- benefits disappear when configuration effort is included;
- false blocking prevents ordinary task completion;
- latency or operator burden is disproportionate to risk reduction;
- simpler policy-as-code controls reproduce the same protection with substantially lower complexity.

## Next implementation slice

Build the smallest deterministic harness with:

1. one task;
2. one operational-authority attack;
3. one epistemic-promotion attack;
4. baseline C and baseline D;
5. retained machine-readable result records;
6. zero scientific-state promotion.

Expand only after that slice passes repository QA.
