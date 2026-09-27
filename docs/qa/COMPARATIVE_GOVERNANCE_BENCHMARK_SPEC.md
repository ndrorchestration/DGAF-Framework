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

## Mutation robustness layer

After the fixed seed suite is green, the benchmark SHOULD generate bounded
metamorphic mutations from legitimate seed cases.

The first mutation layer changes exactly one governance predicate at a time:

- delegated requester authorization;
- replay state;
- intent binding;
- workload attestation;
- delegation-width relation;
- evidence presence;
- evidence freshness;
- verification independence class;
- flow provenance;
- composed-flow authorization.

The purpose is to test local robustness and control attribution. It is not
randomized fuzzing and MUST NOT be described as broad adversarial robustness.

Acceptance requires:

1. every generated mutation has a declared seed and mutated field;
2. expected behavior is defined independently of observed DGAF output;
3. runtime-authority mutations are expected to be caught by the hardened policy
   comparator as well as DGAF;
4. epistemic/composed-authority mutations may count as DGAF incremental
   protection only where the hardened comparator is intentionally out of scope;
5. legitimate paired fixtures remain unblocked;
6. the mutation suite preserves all existing claim ceilings.

## Two-factor interaction layer

After the one-field mutation layer, the benchmark MAY combine two already
defined degradations in one deterministic case.

The initial interaction layer is limited to:

- authority + authority;
- epistemic + epistemic;
- flow + flow.

Acceptance requires:

1. each interaction identifies its legitimate seed and both mutated fields;
2. expected behavior remains defined before observing the tested decision;
3. authority-only failures are not credited uniquely to DGAF when the hardened
   policy comparator also blocks them;
4. DGAF incremental credit remains limited to controls absent from the hardened
   comparator by construction;
5. the suite is described as bounded two-factor engineering evidence, not proof
   of emergent, production, or general adversarial robustness;
6. all claim ceilings from the fixed and one-field suites remain unchanged.

## Cross-domain interaction layer

After same-domain two-factor interactions, the benchmark MAY combine degraded
conditions across distinct governance domains.

The initial cross-domain layer is limited to:

- authority + epistemic;
- authority + flow;
- epistemic + flow.

Acceptance requires:

1. each case identifies the seed and every mutated field;
2. expected decisions are fixed before observing tested outputs;
3. hardened runtime policy receives credit whenever authority controls already
   block the interaction;
4. DGAF incremental credit is limited to claim/flow controls absent from the
   hardened comparator by construction;
5. early denial by one domain does not count as evidence that later domains were
   independently exercised;
6. the layer is described as bounded synthetic engineering evidence, not general
   compositional robustness.

## Evidence-manifest reproducibility

Retained benchmark evidence SHOULD include a canonical manifest whose digest
scope excludes explicitly informational nondeterministic measurements such as
wall-clock or high-resolution runtime timing.

Acceptance requires:

1. canonicalization rules are explicit and tested;
2. two repeated executions of unchanged decision logic produce identical
   canonical digests;
3. excluded fields remain available as informational measurements where useful;
4. decision outputs, summaries, evidence classes, and claim ceilings remain in
   the canonical digest scope;
5. a stable digest is not interpreted as independent validation or scientific
   evidence.

## Evidence-envelope claim binding

Retained benchmark evidence SHOULD be wrapped in a machine-readable envelope
that binds the exact repository commit, verification class, canonical evidence
digests, supported statements, prohibited inferences, and current state
projection.

Acceptance requires:

1. the repository commit is exact and machine-verifiable;
2. same-system/local verification cannot be represented as independent review;
3. supported statements remain bounded to the synthetic fixtures actually run;
4. prohibited inferences include SOTA, generalized safety, efficacy,
   certification/compliance, independent validation, and scientific-N claims;
5. the state projection preserves all controlling fail-closed boundaries.

## Strong policy falsification layer

After the bounded C1/C2 comparison, a stronger conventional policy comparator
MUST be permitted equivalent access to declared claim, provenance, composition,
and authority inputs wherever ordinary policy-as-code can reasonably express
the same rule.

The first frozen implementation is `C3_STRONG_POLICY_AS_CODE_V1`.

Acceptance requires:

1. freeze the C3 machine-readable ruleset before inspecting its result;
2. run C3 and DGAF on the identical fixed fixture set;
3. record decision parity, task correctness, false blocks, rule count, and
   canonical policy size;
4. treat parity as a valid falsification outcome rather than tuning the
   comparator until DGAF wins;
5. interpret parity only as evidence about the bounded fixtures, not
   architectural equivalence;
6. preserve scientific N=0 and every existing claim ceiling.

If C3 reproduces DGAF decisions on the fixed fixtures, the benchmark MUST NOT
describe those fixtures as evidence of unique DGAF protection. Future
comparative work should instead test scaling, configuration/update burden,
cross-workflow composition, evidence-state semantics, recovery/reconciliation,
and operator burden.

## Exhaustive bounded semantic-equivalence layer

After fixed-fixture parity, the comparator SHOULD be evaluated across the
complete currently declared Boolean/categorical input schema rather than only
hand-selected cases.

The first bounded enumeration covers action, authority context, claim state,
and flow state, including absent optional domains.

Acceptance requires:

1. enumerate the declared finite schema without sampling;
2. evaluate identical generated states under C3 and DGAF;
3. retain total state count, parity count, difference count, and allow counts;
4. treat zero differences as decision-function equivalence only for the
   enumerated schema;
5. do not infer architectural equivalence from decision equivalence;
6. move subsequent research toward scaling, evidence lifecycle,
   composition/recovery, provenance custody, and operator burden;
7. preserve all scientific and assurance claim ceilings.

## Configuration-scaling falsification layer

After semantic-equivalence testing, configuration-growth claims MUST be tested
without forcing the conventional comparator to duplicate rules per governed
scope.

The neutral reuse model grants both architectures:

1. shared semantic modules;
2. one binding per governed scope;
3. a central semantic version;
4. one shared-module edit for the modeled semantic change.

Initial scale points are 1, 8, 64, and 512 governed scopes.

Acceptance requires:

1. report shared semantic-module count and scope-binding count for both;
2. report semantic-update artifacts touched for both;
3. allow reusable abstractions equally;
4. treat linear binding growth and constant-time shared semantic updates as
   parity where observed;
5. report serialized configuration size descriptively only;
6. do not interpret representation byte counts as operator burden or
   superiority scores;
7. preserve every existing scientific and assurance claim ceiling.

If both architectures show the same structural growth under fair reuse, the
benchmark MUST NOT claim an inherent DGAF configuration-scaling advantage from
this model alone.

## Matched composition and recovery falsification layer

After static decision and configuration parity, composition/recovery claims MUST
be tested against a conventional comparator that is permitted ordinary stateful
engineering mechanisms rather than a stateless policy stub.

The comparator may use:

1. workflow context and composition authorization;
2. sensitivity propagation;
3. idempotency state;
4. unknown-outcome state;
5. reconciliation state;
6. structured recovery modes.

DGAF MUST NOT receive hidden inputs unavailable to the comparator.

The first paired implementation binds DGAF to the merged capability workflow and
idempotency reference APIs on protected main.

Acceptance requires:

1. paired composition and recovery scenarios;
2. explicit unknown-outcome and retry-blocking behavior;
3. rollback, compensation, and contain/escalate cases;
4. protected-egress composition cases;
5. wrong-authority and stale-retry continuation counts;
6. parity and conventional-policy advantage treated as valid outcomes;
7. no inference from synthetic parity to architectural equivalence;
8. unchanged scientific and assurance claim ceilings.

If both implementations produce the same outcomes under matched semantics, the
benchmark MUST NOT claim unique DGAF composition or recovery protection from
those cases alone.

## Provenance-custody falsification layer

After semantic, scaling, and recovery/composition parity, provenance claims MUST
be tested against a comparator permitted ordinary schema validation and
cross-link custody checks.

The first bounded mutation layer uses the merged reference transaction to emit
a receipt/audit pair and mutates:

1. action digest;
2. authorization ID;
3. workflow ID;
4. invocation ID;
5. capability ID;
6. adapter identity;
7. executor identity;
8. provider-receipt evidence ID.

Acceptance requires:

1. validate the unmodified base artifacts first;
2. apply one mutation at a time;
3. compare detection on identical mutated artifacts;
4. report operator-review counts for both;
5. treat parity and conventional-policy advantage as valid outcomes;
6. do not interpret equal mutation detection as architectural equivalence;
7. preserve all scientific and assurance claim ceilings.

If both implementations detect the same mutations and require the same review
count, the benchmark MUST NOT claim unique DGAF provenance-custody protection
from those checks alone.

