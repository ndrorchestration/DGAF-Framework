# External Acceptance Readiness — 2026-09-07

> **Status:** INTERNAL PREPARATION COMPLETE FOR CURRENT NON-EMPIRICAL REHEARSAL / EXTERNAL GATES NOT EXECUTED  
> **Prepared-against repository checkpoint:** `7e356d412a7653039c89bf818173f9d60e07b744` (merged PR #360)  
> **Controlling scientific state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0  
> **Final v0.7.6 candidate:** NOT DESIGNATED under Issue #309

This document is a dated readiness checkpoint. It is not a moving `main` pointer and must not be promoted into candidate, freeze, authorization, P4, P9, or empirical evidence.

## What can be tested now

The current PDMAL v0.7.6 apparatus can be exercised immediately through the merged **PDMAL v0.7.6 Contract Rehearsal** workflow introduced by PR #360.

That lane is deliberately non-empirical. It:

- checks out and verifies the exact source identity;
- installs the hash-locked v0.7.6 pilot dependencies;
- proves freeze, pilot authorization, blinding-key, frozen-SHA, and archive inputs are absent;
- runs the current schema, security, and blinding adversarial controls;
- executes the fixed two-seed `PDMAL_MODE=contract` rehearsal;
- requires the rehearsal to emit no empirical artifact; and
- verifies by negative control that `PDMAL_MODE=pilot` fails closed without the required authorization boundary.

A successful contract rehearsal establishes only that the current apparatus satisfies that bounded test contract. It does not designate the final candidate, satisfy P4, establish freeze, grant pilot authorization, execute final P9, or increase empirical N.

## Internal readiness now established

- PR #343: source-bound Mode-T external-acceptance handoff merged.
- PR #344: fail-closed external-result intake merged.
- PR #346: immutable #343 handoff binding restored after direct-main identity regression.
- PR #352: authority-aware evidence-chain closure plan merged.
- PR #353: corrected Google Confidential Space Stage-A qualification procedure merged.
- PR #354: exact-identity #320 independent security-review package merged.
- PR #357: inert external-acceptance templates, handoffs, fail-closed validator, and dedicated readiness CI merged.
- PR #358: sendable #320 independent-review outreach handoff merged without altering the frozen review scope.
- PR #360: current v0.7.6 non-empirical contract rehearsal merged after its exact-head workflow set completed without failure.

## Remaining external or administrative gates

| Track | Internal state | External fact still required |
|---|---|---|
| #277 repository enforcement | Detective/pre-merge controls verified; admin handoff prepared | Repository administrator applies and proves preventive PR/required-check enforcement |
| #320 independent security review | Frozen exact source/review package and reviewer handoff ready | Organizationally independent reviewer returns attributable, identity-bound report and findings are dispositioned |
| #310 Stage-A Confidential Space | Corrected procedure, inert input/evidence templates, and synthetic engineering coverage ready | Authenticated real GCP Confidential Space PRE/POST qualification run and independent reverification |
| #316 production authority | Engineering/synthetic policy binding verified; decision handoff and acceptance template ready | Independently retained production R/A/C, signer/root/TUF authority, retrieval and cryptographic reverification |
| #295 protected continuity | Engineering, reproducibility, structural binding, and acceptance template ready | Final candidate-bound protected ciphertext/commitment, accepted retention/retrieval, and independent final adjudication |
| #309 final candidate | Designation template and current-apparatus rehearsal ready | Candidate-relevant external/P4 prerequisites resolved, followed by explicit exact candidate designation |

## Current boundary between rehearsal and pilot

**Rehearsal-ready:** current v0.7.6 apparatus can be repeatedly tested in contract mode with empirical N remaining zero.

**Pilot-not-authorized:** the empirical pilot must remain unavailable until the external/administrative predicates above are actually evidenced and adjudicated, the final candidate is explicitly designated, candidate-dependent evidence is regenerated or classified, immutable freeze is established and independently verified, final P9 is completed, and a separate pilot authorization is granted.

## Downstream sequence after external readiness closes

`external/admin acceptance → #309 final candidate designation → classify/regenerate candidate-dependent evidence → final candidate-bound P4/#295 acceptance → P7 final binding → construct and independently verify immutable P8 freeze → final independent P9 → separate explicit pilot authorization → blinded pilot → QC/sample-size decision → final experiment → dataset lock → authorized unblinding/analysis → evidence-bounded publication`

## Non-promotion rule

The templates introduced with the readiness packet are deliberately inert. Null identities, `TEMPLATE`, `NOT_EXECUTED`, `NOT_DESIGNATED`, and `NOT_AUTHORIZED` values are safety properties. Filling them is not sufficient for acceptance; the applicable external attribution, retrieval, cryptographic verification, and governance adjudication must also occur.

No repository preparation or rehearsal step may increase empirical N or convert CI/synthetic evidence into real P4 custody, independent review, cloud admission, freeze, or authorization.
