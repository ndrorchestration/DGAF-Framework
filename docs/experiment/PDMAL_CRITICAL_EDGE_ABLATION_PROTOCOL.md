# PDMAL Critical-Edge / Communication-Ablation Protocol

> **Status:** PROSPECTIVE FUTURE EXPERIMENT / NOT EXECUTED / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Current Track A Epoch 002 primary-analysis effect:** NONE  
> **Established:** 2026-09-17

## Quarantine from current experiment

This protocol is a **future-work design**. It is not an amendment, addendum, endpoint, secondary analysis authorization, or interpretation rule for the locked Track A Epoch 002 experiment.

It must not be executed on current protected/locked outcome material unless a future governance action explicitly establishes a permitted analysis scope. Preferred use is a separately preregistered new experiment with fresh prospective seeds/data.

## Objective

Estimate which communication edges are causally important to agent-system outcomes under controlled, paired interventions and determine whether graph-theoretic measures can prospectively predict that importance.

Primary conceptual distinction:

```text
structural importance != empirical causal importance
```

The experiment tests the relationship rather than presuming it.

## Graph intervention

For baseline communication graph:

```text
G = (V, E)
```

and edge `e in E`, define an ablated graph:

```text
G_-e = (V, E \ {e})
```

For outcome `Y`, define paired edge effect:

```text
Delta_e(Y) = Y(G) - Y(G_-e)
```

The sign convention must be interpreted according to the outcome. For failure rate or cost, lower may be better; for success rate, higher may be better.

## Experimental unit

The inferential unit must be declared before execution. A preferred design uses paired prospective seeds/tasks so the same controlled unit is evaluated under baseline and intervention conditions.

The protocol MUST define:

- task corpus/version;
- model/provider/version;
- prompt/policy versions;
- topology identity;
- edge identity;
- failure intervention, if any;
- RNG/seeding scheme;
- stopping rules;
- outcome definitions;
- allowed retries;
- tool/environment versions.

## Primary research questions

### E-RQ1

Which individual communication edges materially change task or robustness outcomes when removed?

### E-RQ2

Do graph-theoretic predictors such as edge betweenness, cut membership, local redundancy, or curvature predict measured `Delta_e` out of sample?

### E-RQ3

Do edges that matter for task performance also matter for epistemic outcomes such as false consensus, correction, or evidence diversity?

### E-RQ4

Are single-edge effects stable across tasks, seeds, failure levels, and model configurations?

## Conditions

At minimum, a future preregistration SHOULD include:

1. **Baseline:** intact graph `G`.
2. **Single-edge ablation:** each eligible `G_-e` or a prospectively sampled subset.
3. **Matched random-edge baseline:** ablate an equal number of randomly selected eligible edges under a frozen sampling rule.
4. **Optional targeted baseline:** ablate edges selected by a preregistered structural measure.

Multi-edge ablations are secondary unless separately powered and preregistered, because higher-order interactions can invalidate simple additivity assumptions.

## Eligibility rules

Before outcome access, define whether the following edges are eligible:

- mandatory control-plane edges;
- human-approval edges;
- tool-execution edges;
- self-loops;
- bidirectional pairs;
- topology-specific edges with no counterpart in another graph.

Safety-critical or authorization-control edges SHOULD NOT be experimentally removed in a live system with real external side effects. Use simulation/sandbox environments.

## Outcome registry

### Task outcomes

- task success / exact endpoint appropriate to task;
- failure/recovery rate;
- quality score under a frozen rubric;
- time/turns to completion.

### Epistemic outcomes

- unsupported-claim rate;
- false-consensus rate;
- minority-correction rate;
- contradiction survival;
- unique provenance-root count;
- evidence-source concentration;
- epistemic amplification statistic.

### Operational outcomes

- token/message cost;
- tool-call count;
- latency;
- retries;
- escalation frequency.

## Pairing and randomization

Where the system is stochastic, pair baseline and ablated runs by the strongest defensible common randomization unit while avoiding accidental state leakage between conditions.

A future preregistration must state whether model sampling seeds are reproducible for the selected provider/runtime. If exact reproducibility is unavailable, record the limitation and increase replication rather than pretending deterministic pairing exists.

Order effects SHOULD be randomized or counterbalanced when stateful infrastructure could bias results.

## Blinding

Where practical:

- use blinded topology/edge labels during human scoring;
- hide structural predictor ranks from outcome adjudicators;
- calculate locked primary outcomes before revealing predictor-based interpretations;
- keep hypothesis-generating visualizations out of confirmatory decision paths.

## Structural predictor comparison

Candidate edge-level predictors may include:

- edge betweenness;
- bridge/cut membership;
- endpoint degrees;
- local alternate-path count;
- shortest-path participation;
- local clustering effects;
- exact declared curvature measure;
- change in algebraic connectivity after edge removal;
- change in global efficiency after edge removal.

Predictors must be computed without outcome information.

## Analysis plan requirements

Before execution, declare:

- primary outcome;
- primary edge-effect estimand;
- aggregation across seeds/tasks;
- confidence-interval procedure;
- treatment of failed/invalid runs;
- multiple-testing strategy for many edges;
- minimum effect of interest where possible;
- confirmatory predictor(s), if any;
- held-out strategy for predictive claims;
- robustness/sensitivity analyses;
- criteria for classifying an edge as empirically important.

Raw per-edge ranking without multiplicity or uncertainty treatment is exploratory.

## Non-additivity check

Single-edge effects may interact. If future resources permit, a separately declared secondary design may compare:

```text
Delta_{e1,e2}(Y)
```

against the sum of single-edge effects to detect synergy/antagonism. This must not be inferred from single-edge results alone.

## Safety and authorization constraints

The protocol MUST run in a sandbox or simulation unless a separate authority explicitly permits real-world effects.

Default constraints:

- no financial/payment actions;
- no destructive production operations;
- no uncontrolled publication;
- no privilege escalation;
- no removal of mandatory human approval in a live environment;
- no use of protected secrets in prompts/logs;
- no scientific-state transition without the appropriate evidence and authorization record.

## Stop conditions

A future execution SHOULD stop/fail closed if:

- topology identity or code hash drifts;
- task set changes after freeze;
- an ablation unexpectedly enables a prohibited external path;
- scoring or logging provenance fails;
- a required artifact is missing;
- a protected secret enters logs;
- the planned paired design cannot be maintained and no preregistered fallback applies.

## Interpretation rules

An edge with large measured `Delta_e` is empirically influential **within the tested scope**. It is not automatically a universal bottleneck or mechanistic explanation.

A structural measure that correlates with edge effects in the discovery data is not a predictive result until tested prospectively or out of sample.

A null result is retained. Failure of structural metrics to predict edge importance is a valid research outcome.

## External methodological precedent

Li et al. (2026), *Discovering Efficient and Explainable Communication Topologies for LLM-based Multi-Agent Systems via Causal Inference*, arXiv:2608.12921, uses communication-edge interventions as part of a causal-topology analysis. This protocol treats that work as methodological precedent only; its results do not establish PDMAL behavior.

https://arxiv.org/abs/2608.12921

## Gate to execution

Before this document can become an executable experimental protocol, it requires at minimum:

1. exact experiment identity/version;
2. fresh prospective seed/data plan or explicit lawful analysis scope;
3. endpoint/estimand freeze;
4. power/sample-size rationale appropriate to the final design;
5. code/environment freeze;
6. custody/blinding plan where applicable;
7. explicit authorization to execute;
8. retained raw data and reproducible analysis artifacts.

Until those conditions exist, this document remains **NOT EXECUTED / EXPLORATORY**.
