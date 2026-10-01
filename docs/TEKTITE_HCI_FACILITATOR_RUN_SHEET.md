# Tektite HCI Study — Facilitator Run Sheet

Canonical protocol: `docs/TEKTITE_HCI_VALIDATION_PACKET.md`  
Pattern Commons target: `PC-HCI-002`  
Transfer test: `TT-2026-10-01-023`  
Controller: issue #1224

## Frozen identities

Participant surface:

- URL: `https://dynamicgovernanceagenticformation-1ei0gb4sl-ndrorchestration.vercel.app`
- Vercel deployment: `dpl_EcDrRmUzFaWiGQf9nK6xzxw1LQLV`
- DGAF source SHA: `d172c1430c7d97fba74b182f4aedf0d6b374d96a`

Protocol packet:

- PR: #1227
- canonical packet commit: record the merged/canonical commit used for the session

If either the participant surface or protocol changes materially, do not reuse this sheet without rebinding the identities.

## Before the session

- [ ] Participant is unfamiliar with Tektite/DGAF design.
- [ ] Participant has not seen expected answers.
- [ ] Participant has not been coached on Understand → Verify → Inspect → Operate.
- [ ] Participant consents to an anonymized usability record.
- [ ] Assign a random participant ID.
- [ ] Record technical familiarity: low / medium / high.
- [ ] Record governance-tool familiarity: none / some / substantial.
- [ ] Confirm the pinned participant URL loads.
- [ ] Record the canonical protocol packet commit used for this session.
- [ ] Do not explain the four-stage pattern.

## During the session

Read only:

> Please use the interface and answer the questions in the participant brief in your own words. I am testing the interface, not you. I will not explain what the interface is intended to mean until the tasks are complete.

Allowed facilitator help:

- browser/network access;
- scrolling/navigation mechanics if the participant is physically unable to proceed;
- repeating a task verbatim.

Not allowed:

- explaining DGAF/Tektite terminology;
- pointing to the correct evidence or blocker;
- explaining readiness vs authorization;
- suggesting the correct action;
- telling the participant whether an answer is right.

Count every substantive intervention.

## Observation sheet

```text
TEKTITE_HCI_RUN_ID:
DATE_UTC:
PARTICIPANT_ID:
CONDITION: A_STAGED
TECHNICAL_FAMILIARITY:
GOVERNANCE_TOOL_FAMILIARITY:

REPOSITORY_SHA: d172c1430c7d97fba74b182f4aedf0d6b374d96a
VERCEL_DEPLOYMENT: dpl_EcDrRmUzFaWiGQf9nK6xzxw1LQLV
SURFACE_URL: https://dynamicgovernanceagenticformation-1ei0gb4sl-ndrorchestration.vercel.app
PROTOCOL_PACKET_COMMIT:

SYSTEM_PURPOSE_RAW:
CURRENT_STATE_RAW:
EVIDENCE_RAW:
BLOCKER_RAW:
READINESS_VS_AUTHORIZATION_RAW:
INSPECTION_PATH_RAW:
NEXT_ACTION_RAW:
ACTION_RESULT_RAW:
UNBLOCK_REQUIREMENTS_RAW:
FRICTION_RAW:

SYSTEM_PURPOSE_SCORE_0_2:
CURRENT_STATE_SCORE_0_2:
EVIDENCE_SCORE_0_2:
BLOCKER_SCORE_0_2:
READINESS_VS_AUTHORIZATION_SCORE_0_2:
BLOCKED_ACTION_EXPLANATION_SCORE_0_2:
TOTAL_COMPREHENSION_SCORE_0_12:

INSPECTED_BEFORE_OPERATION: YES / NO
PREMATURE_OPERATION_ATTEMPT: YES / NO
AUTHORITY_GATE_CORRECT: YES / NO
COMPLETION_TIME:
FACILITATOR_INTERVENTIONS:

CRITICAL_MISLEADING_AFFORDANCE: YES / NO
NOTES:

RESULT: PASS / FAIL / INCONCLUSIVE
BOUNDARY:
```

## Adjudication floor

A bounded receiver-transfer PASS requires:

- eligible unfamiliar participant;
- exact surface/protocol identity captured;
- state, evidence, blocker, and readiness/authorization each at least partially correct;
- no UI navigation stage itself grants authority;
- blocked actions remain blocked;
- no critical misleading affordance that reasonably implies evidence/readiness equals authorization.

One participant can support only a bounded receiver-transfer claim. It cannot support comparative HCI superiority or population-level usability.

## After the session

- [ ] Preserve the raw anonymized answers.
- [ ] Score only after the participant finishes.
- [ ] Record PASS / FAIL / INCONCLUSIVE without changing criteria.
- [ ] Attach the completed record to issue #1224.
- [ ] Bind exact run evidence into `TT-2026-10-01-023`.
- [ ] Promote `PC-HCI-002` only if the recorded evidence satisfies the frozen gate.
