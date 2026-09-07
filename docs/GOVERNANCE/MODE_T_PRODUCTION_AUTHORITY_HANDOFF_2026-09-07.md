# Mode-T Production Authority Handoff — Issue #316

> **Status:** READY FOR EXTERNAL AUTHORITY DECISIONS / PRODUCTION AUTHORITY NOT ESTABLISHED  
> **Prepared-against checkpoint:** `d01fa13d40b60a1e0bd661756fd60e8550107d9d`  
> **Controlling scientific state:** P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0

## Purpose

Translate #316's remaining production trust boundary into a compact external decision and evidence checklist. This document does not choose the authority, root, signer, custodian, or reviewer. Those choices must originate outside the synthetic engineering path and remain independently attributable/reverifiable.

## Production decisions that must be made explicitly

### 1. Authorization / R-A-C authority

Record:

- who or what creates reservation R;
- who or what authorizes A;
- who or what performs single-use C consumption;
- why the execution principal cannot silently rewrite or substitute the accepted R/A/C chain;
- exact storage/retention system and access boundary;
- exact cryptographic identity of retained records;
- failure/retry semantics after C is consumed.

Production key acquisition must consume authenticated retained C (or an equivalently verifiable capability) and must not accept caller booleans, caller-selected digests, synthetic C, or a self-asserted policy identity as production authority.

### 2. Admission-policy identity

The accepted policy must bind the canonical security-critical fields already enforced by the repository, including audience, execution subject, exact service-account set, workload image digest, args, command/environment policy, Confidential Space security profile, restart policy, clock-skew rule, and maximum signed token lifetime.

Required evidence:

- canonical serialized policy bytes or equivalent deterministic representation;
- exact policy SHA-256;
- proof that R, A, and C carry the same policy identity;
- proof that the production key path recomputes and exactly matches the accepted policy before entropy generation;
- negative evidence showing a valid token for a different policy is rejected.

### 3. Production signer / transparency authority

Decide and record:

- exact signer identity permitted for the accepted retained evidence;
- certificate/identity constraints;
- transparency/inclusion requirements, if used;
- rotation/revocation procedure;
- which actor may approve a new signer identity;
- whether signer authority can be changed by the solo workload operator during an accepted run.

Existing synthetic Sigstore mechanics are supporting engineering evidence only.

### 4. TrustedRoot and TUF policy

Record and independently approve:

- exact production TrustedRoot bytes;
- TrustedRoot SHA-256;
- bootstrap origin and authenticity evidence;
- validity/expiry policy;
- TUF update/rotation procedure;
- rollback/freeze-attack handling;
- recovery/break-glass authority;
- what happens when fresh trusted metadata cannot be obtained.

Any missing, mismatched, stale, or unapproved root must fail closed.

### 5. Retention and independent retrieval

Record:

- exact external retention location/object identity;
- retaining actor/system;
- retrieval actor/system;
- whether independence is claimed and the concrete basis for that claim;
- original object digests;
- independently retrieved object digests;
- fresh cryptographic verification results;
- evidence that local/GitHub existence alone is not being called independent retention.

### 6. Real Confidential Space dependency

Issue #316 cannot close solely from retained authorization records. The accepted production authority must compose with:

- completed independent #320 security review;
- real authenticated Stage-A evidence under #310;
- independently reverified PRE/POST attestation;
- accepted workload/policy identities;
- production key acquisition occurring only after the accepted authorization and PRE boundaries.

## Required final evidence record

A production-authority acceptance record should include at minimum:

- authority record version;
- exact repository/source identities under evaluation;
- R/A/C scheme and actor identities;
- policy identity + SHA-256;
- signer identity;
- TrustedRoot SHA-256 and TUF policy identity;
- retention location and object digests;
- independent retrieval/reverification evidence;
- #320 review identity/result;
- #310 Stage-A evidence identity/result;
- unresolved findings;
- explicit adjudication: `PASS`, `BLOCKED`, or `UNKNOWN`.

`PASS` here means the production authority boundary is accepted for candidate construction. It does not itself designate the candidate, establish P4 final candidate-bound acceptance, freeze the experiment, authorize the pilot, or create empirical observations.

## Fail-closed defaults

Until the evidence above exists and is independently adjudicated:

- production authority: **NOT ESTABLISHED**;
- production key acquisition authority: **DISABLED**;
- #316: **OPEN**;
- P4: **OPEN / FAIL-CLOSED**;
- final candidate: **NOT DESIGNATED**;
- freeze: **NOT ESTABLISHED**;
- pilot authorization: **NOT GRANTED**;
- empirical N: **0**.
