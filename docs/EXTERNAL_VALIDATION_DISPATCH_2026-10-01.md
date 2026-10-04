# External Validation Dispatch — 2026-10-01

This page is the public handoff for two bounded human-validation tasks that are technically ready and intentionally cannot be satisfied by the implementation author, same-owner automation, or ChatGPT.

Choose **one** lane. You do not need prior knowledge of DGAF, Tektite, or the NDR ecosystem.

## Lane A — Tektite unfamiliar-user HCI

**Controller:** [issue #1224](https://github.com/ndrorchestration/DGAF-Framework/issues/1224)  
**Protocol commit:** `c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91`  
**Status:** READY / NO RESULT YET

### Who qualifies

You qualify if you:

- did not design Tektite, DGAF, ACP, or this protocol;
- have not been coached on the intended Understand → Verify → Inspect → Operate pattern;
- have not seen the expected answers;
- are willing to provide an anonymized usability record.

Technical expertise is not required.

### Participant surface

Use the participant brief:

[Participant brief — pinned protocol commit](https://github.com/ndrorchestration/DGAF-Framework/blob/c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91/docs/TEKTITE_HCI_PARTICIPANT_BRIEF.md)

Participant-facing site:

`https://dynamicgovernanceagenticformation-kol94uquc-ndrorchestration.vercel.app/demo`

Surface identity:

- DGAF source: `d4d2387cc1f7466a127e57862acf79f7f0e1d9b8`
- Vercel deployment: `dpl_C1HM4r8nuSkzSK8nxxdL6uTKgXjs`
- facilitator-sheet rebind merge: `3f76c9a93168eed7b366f51ac16481ae53954e27`

The facilitator should separately use:

[Facilitator run sheet — current surface rebind](https://github.com/ndrorchestration/DGAF-Framework/blob/3f76c9a93168eed7b366f51ac16481ae53954e27/docs/TEKTITE_HCI_FACILITATOR_RUN_SHEET.md)

[Canonical validation protocol — facilitator only before the run](https://github.com/ndrorchestration/DGAF-Framework/blob/c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91/docs/TEKTITE_HCI_VALIDATION_PACKET.md)

For participant recruitment, share only the participant brief and neutral access instructions; keep the four-stage explanation and scoring material out of the pre-run handoff.

Do not expose facilitator scoring or expected answers before the participant finishes. The participant brief and canonical scoring protocol remain pinned to protocol commit `c4f8fda24d2d44c47d7de8c77fcbbd3d478f5a91`; only the participant surface identity and facilitator-sheet binding have been rebound to the current deployment.

### What the run tests

The participant attempts to determine, in their own words:

- what the interface is showing;
- current state;
- supporting evidence;
- current blocker;
- readiness versus authorization;
- where to inspect more detail;
- what action appears appropriate;
- why a blocked action remains blocked.

Navigation must never create authority.

### Evidence to preserve

Record:

- anonymous participant ID;
- protocol commit;
- exact participant surface/deployment;
- session timestamp and browser/device class;
- condition A or B (Condition A alone is single-condition evidence);
- coarse technical/governance familiarity;
- raw answers;
- intervention count;
- comprehension scores;
- operation-attempt behavior;
- friction/ambiguity;
- PASS / FAIL / INCONCLUSIVE under the frozen protocol.

A single passing run supports only bounded unfamiliar-user transfer evidence for that exact surface.

---

## Lane B — Governed Repo outside-operator trial

**Controller:** [issue #1210](https://github.com/ndrorchestration/DGAF-Framework/issues/1210)  
**Canonical Governed Repo source:** `c90c74c04583c5a3f23f6a261cf38cd6922c781c`  
**Validated integration head:** `77c818ecc5d57e5dd354bc86396dc9e7c5c6be9e`  
**Status:** READY_FOR_OUTSIDE_OPERATOR / USABILITY_NOT_ESTABLISHED

### Who qualifies

A technically capable developer, evaluator, DevOps engineer, or reviewer who:

- did not build Governed Repo;
- did not participate in its implementation;
- does not rely on private NDR context;
- can follow the public instructions without implementation-author coaching.

### Operator packet

Use:

[Package trial packet — pinned accepted-main documentation](https://github.com/ndrorchestration/DGAF-Framework/blob/3597852ddad746b29d024b8d19b6bfa83c8cbc30/docs/governance/GOVERNED_REPO_OUTSIDE_OPERATOR_TRIAL_V0.md)

Follow the published packet as written. If the packet is unclear, record the ambiguity rather than asking for hidden context.

### Required bounded tasks

Using only the public instructions:

1. install the package from the exact source named in the published packet;
2. run one eligible case;
3. run one expected denial case;
4. identify the returned reason semantics;
5. explain what the receipt does and does not authorize;
6. report every setup ambiguity, missing assumption, failure, workaround, or intervention.

### Evidence to preserve

Record:

- coarse operator background;
- exact tested source/version/SHA;
- environment and Python version when applicable;
- documented package path used;
- commands/config copied from docs;
- task outcomes;
- reason codes;
- operator explanation of non-effects;
- interventions;
- friction and defects;
- retest result if a blocking defect is repaired.

A successful trial supports only bounded outside-operator usability for that operator, path, and environment.

---

## Anti-contamination rules

For either lane:

- do not coach expected answers;
- do not supply unpublished/private implementation context;
- do not rewrite the participant/operator's raw observations after discussion;
- preserve failures and confusion as evidence;
- bind every result to exact source/protocol identity;
- do not infer broader scientific, security, product, or High-Assurance claims.

## Fixed claim ceilings

These human trials do **not** by themselves establish:

- scientific N increment;
- independent scientific validation;
- canonical DGAF efficacy;
- production safety;
- certification/compliance;
- High-Assurance authorization;
- real-project mutation authority;
- product-market fit.

## Returning results

For Tektite, attach the anonymized result record to issue #1224.

For Governed Repo, attach the operator record to issue #1210.

If a blocking defect is found, report the defect first. A failed or inconclusive trial is valid evidence and should be retained.
