# Tektite HCI Validation Packet

**Pattern Commons target:** `PC-HCI-002 — Understand → Verify → Inspect → Operate`  
**Transfer test:** `TT-2026-10-01-023`  
**Controller:** issue #1224  
**Protocol status:** READY FOR UNFAMILIAR-PARTICIPANT EXECUTION / NO RESULT YET

## 1. Purpose

Test whether Tektite's staged operator flow:

`Understand → Verify → Inspect → Operate`

helps an unfamiliar participant correctly understand governed system state, locate and interpret evidence, identify blockers, distinguish readiness from authorization, and avoid premature operation attempts.

This protocol evaluates **human comprehension and interaction behavior only**. It does not establish runtime safety, system efficacy, independent scientific validation, certification, or authorization.

## 2. Participant eligibility

An eligible participant:

- did not design Tektite, DGAF, ACP, or this protocol;
- has not been coached on the four-stage pattern;
- has not previously been shown the expected answers;
- may be technical or nontechnical, but prior experience must be recorded;
- must consent to an anonymized usability record.

The author/operator must not answer task questions during the run. Clarifications are limited to mechanical access problems.

## 3. Exact surface binding

Before each run record:

- repository: `ndrorchestration/DGAF-Framework`;
- exact commit SHA;
- exact deployment URL or local build identity;
- timestamp;
- browser/device class;
- whether the participant is viewing the staged or control condition.

Do not transfer a result to a later revision without a new binding or explicit equivalence argument.

## 4. Conditions

### A — staged condition

Use the Tektite surface as implemented with the intended progression:

1. Understand
2. Verify
3. Inspect
4. Operate

### B — control condition

Use an otherwise equivalent presentation where the same information and controls are available without the staged progression. Do not intentionally degrade wording, evidence quality, or runtime authorization behavior.

If a valid control surface is unavailable, run Condition A only and classify the result as **single-condition usability evidence**, not comparative evidence.

## 5. Participant tasks

Give these tasks without explaining the intended answers.

1. In your own words, what is this system showing you?
2. What is the current state of the selected item?
3. What evidence supports that state?
4. What is the most important current blocker or unmet predicate?
5. Is the system ready, authorized, both, or neither for the visible next operation? Explain.
6. Show where you would inspect more detail before acting.
7. Attempt the next action you believe is appropriate.
8. Explain what happened and why.
9. If an operation is unavailable or blocked, explain what would have to change before it should become available.
10. Identify anything that felt misleading, hidden, redundant, or unnecessarily difficult.

Do not reveal correctness until the participant has completed the tasks.

## 6. Required observations

Record for each participant:

- participant ID: random/non-identifying code;
- condition: A or B;
- technical familiarity: low / medium / high;
- prior governance-tool familiarity: none / some / substantial;
- completion time;
- correct system-purpose description: yes / partial / no;
- correct current-state identification: yes / partial / no;
- correct evidence identification: yes / partial / no;
- correct blocker identification: yes / partial / no;
- correct readiness-vs-authorization distinction: yes / partial / no;
- inspected evidence/details before operation attempt: yes / no;
- premature operation attempt: yes / no;
- correctly explained blocked/unavailable action: yes / partial / no;
- authority gate behaved correctly: yes / no;
- participant friction notes;
- observed ambiguity or misleading affordance;
- unexpected behavior;
- facilitator intervention count.

## 7. Scoring

Use the following bounded comprehension score:

- system purpose: 0–2
- current state: 0–2
- evidence: 0–2
- blocker: 0–2
- readiness vs authorization: 0–2
- blocked-action explanation: 0–2

Maximum: **12**.

Behavioral measures are kept separate:

- inspected before operation: 0/1
- premature operation attempt: 0/1
- authority gate correct: 0/1
- completion time
- facilitator interventions

Do not collapse these dimensions into one opaque usability score.

## 8. Pass / fail interpretation

A single participant does not establish a general comparative HCI effect.

For **receiver-transfer PASS**, the minimum acceptable evidence is:

- at least one eligible unfamiliar participant;
- exact surface binding recorded;
- participant correctly identifies the current state, evidence, blocker, and readiness/authorization distinction at least partially;
- no runtime authority is granted merely because the participant reaches the Operate stage;
- blocked actions remain blocked;
- no critical misleading affordance is observed that would cause a reasonable participant to mistake evidence/readiness for authorization.

For a **comparative claim** that the staged flow improves comprehension or reduces premature action, run both conditions with multiple unfamiliar participants and report the raw outcomes. Do not claim superiority from a single participant or an uncontrolled observation.

## 9. Failure conditions

Classify the run as FAIL or INCONCLUSIVE as appropriate if:

- critical state or blocker cannot be found;
- the participant consistently treats evidence as authorization;
- the staged flow makes a blocked operation appear authorized;
- reaching Operate changes runtime authorization;
- the participant requires substantive coaching;
- exact surface identity was not captured;
- the surface changes materially during the run;
- the control condition differs in more than presentation/order;
- data are incomplete or contradictory.

## 10. Protected invariant

**Navigation order never creates authority.**

The Operate stage may expose an available control only when the separate runtime/governance admission state permits it. If the interface order itself is sufficient to cause execution, this protocol fails regardless of comprehension results.

## 11. Result record template

```text
TEKTITE_HCI_RUN_ID:
DATE_UTC:
PARTICIPANT_ID:
CONDITION:
TECHNICAL_FAMILIARITY:
GOVERNANCE_TOOL_FAMILIARITY:

REPOSITORY_SHA:
DEPLOYMENT_OR_BUILD_ID:
SURFACE_URL_OR_ROUTE:

SYSTEM_PURPOSE_SCORE_0_2:
CURRENT_STATE_SCORE_0_2:
EVIDENCE_SCORE_0_2:
BLOCKER_SCORE_0_2:
READINESS_VS_AUTHORIZATION_SCORE_0_2:
BLOCKED_ACTION_EXPLANATION_SCORE_0_2:
TOTAL_COMPREHENSION_SCORE_0_12:

INSPECTED_BEFORE_OPERATION:
PREMATURE_OPERATION_ATTEMPT:
AUTHORITY_GATE_CORRECT:
COMPLETION_TIME:
FACILITATOR_INTERVENTIONS:

FRICTION_NOTES:
AMBIGUITIES:
UNEXPECTED_BEHAVIOR:

RESULT: PASS / FAIL / INCONCLUSIVE
BOUNDARY:
```

## 12. Claim ceiling

A passing unfamiliar-participant run may support:

> This exact Tektite surface demonstrated bounded receiver usability for the Understand → Verify → Inspect → Operate progression with an unfamiliar participant while preserving separate authority gating.

It does **not** establish:

- universal HCI superiority;
- population-level usability;
- production safety;
- DGAF efficacy;
- independent scientific validation;
- compliance/certification;
- High-Assurance authorization;
- authority to execute any blocked action.

## 13. Promotion rule

Do not promote `PC-HCI-002` from its current hold until an eligible unfamiliar-participant record is complete and reviewed against this packet.

If the result is PASS, bind the exact run record to `TT-2026-10-01-023`.  
If FAIL, preserve the result and revise the interface before retesting.  
If INCONCLUSIVE, preserve the result and repeat without weakening the criteria.
