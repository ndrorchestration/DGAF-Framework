# DGAF / PDMAL Next-Stage Expert-Panel Execution Plan — 2026-09-05

**Status:** ACTIVE PLANNING CONTROL / PRE-FREEZE / NO EXPERIMENT AUTHORITY  
**Designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Empirical N:** `0`

## Panel perspectives

This plan reconciles six distinct expert perspectives against the current repository evidence:

1. **Experimental governance / methodology** — protects the P4 → P7 → P8 → P9 → authorization sequence and prevents engineering evidence from becoming efficacy evidence.
2. **Epistemic provenance / claims auditing** — requires exact identities, external digests, non-transferable evidence scope, and explicit UNKNOWN/OPEN states.
3. **Security / custody** — preserves genuinely distinct-human P4 key custody and rejects aliases, agents, bots, or inferred participation as substitutes.
4. **Independent verification / red team** — searches for circular identities, self-verification, mutable-ref dependence, verifier drift, substitution, and premature authorization paths.
5. **CI / reliability / release engineering** — requires exact-head validation, fail-closed workflow behavior, post-merge reproduction, deployment identity separation, and durable evidence handling.
6. **Repository / documentation governance** — keeps current-facing control surfaces synchronized while preserving historical records as scoped provenance.

## Panel consensus

The system has moved beyond broad implementation hardening. The critical path is now narrow, but the remaining steps are higher-consequence governance transitions.

The panel's principal new finding is Issue #280: the prior P7/P8/P9 model contained a circular dependency in which post-freeze verification evidence could be required inside the immutable freeze itself, and downstream P8/P9 outputs were incorrectly represented as P7 closure blockers. That must be corrected before P4 completion makes freeze execution actionable.

## Stage A — complete now: pre-P4 control-plane correctness

### A1. Remove P7/P8/P9 circularity

- Separate immutable freeze object F from post-freeze P8 verification record V.
- Restrict P7 closure blockers to pre-freeze inputs.
- Require final P9 to read candidate/P7/freeze state from exact F.
- Require final P9 to read V from exact descendant verification commit.
- Require external byte digests for both F and V.
- Require P9 verifier script/workflow identity equality between F and V.
- Maintain authorization `NOT_GRANTED` and empirical N `0` during P9.

**Exit:** exact-head CI passes adversarial tests and control-state checks; changes merge without changing scientific gate status.

### A2. Stabilize current-facing documentation

- Finish Issue #270 historical-boundary wording so verification records do not self-stale when later documentation merges advance `main`.
- Keep current-main operational state separate from historical exact verification boundaries.

**Exit:** one-file documentation correction merges cleanly.

### A3. Repository merge enforcement

Issue #277 remains a repository-administration control.

- Python quality workflow fail-closed behavior is already verified.
- Protected-branch/ruleset readback does not require the Python quality matrix before merge.
- Current connector cannot mutate branch protection/rulesets.

**Exit:** authorized repository administrator updates required checks/workflow policy, configuration is independently read back, and a controlled failing case demonstrates merge enforcement if practical.

This lane may remain externally blocked without blocking PDMAL scientific sequencing unless governance explicitly promotes it to a scientific prerequisite.

## Stage B — human operational gate: P4

No repository automation can complete this stage.

Required real-world events:

1. select a genuinely distinct human Key Custodian;
2. identify a distinct execution/analysis principal;
3. generate and privately retain the blinding key/nonces outside public control surfaces;
4. publish only nonce-hardened key/mapping commitments;
5. retain attributable custodian and no-access attestations;
6. complete independent custody review without exposing secret material.

**Stop condition:** any missing attributable human, commitment, access statement, or independent review keeps P4 OPEN.

## Stage C — P7 final exact binding

Execute only after P4 closes.

1. insert actual P4 custody evidence by digest/reference, never secret material;
2. select exact final protocol identity;
3. select exact accepted pre-freeze control-plane commit;
4. bind selected P9 verifier script/workflow SHA-256 values;
5. verify candidate/deployment/protocol/analysis/runner/schema/evidence tuple has no conflicts;
6. formally change P7 status from OPEN to CLOSED only when all pre-freeze blockers are resolved.

Downstream freeze/P8/P9/auth values may remain null at legitimate P7 closure.

## Stage D — P8 immutable freeze and independent verification

Execute only after P7 closes.

### D1. Construct F

- create `docs/experiment/PDMAL_IMMUTABLE_FREEZE.json` from exact closed P7 tuple;
- commit F at an exact immutable Git commit;
- compute F byte SHA-256 externally;
- ensure F contains no post-freeze verification evidence and no self-hash.

### D2. Independently verify F and create V

- independently retrieve exact F commit;
- recompute F byte digest;
- verify equality and frozen identity tuple;
- create separate `docs/experiment/PDMAL_P8_FREEZE_VERIFICATION.json` record V in a descendant commit;
- externally hash V;
- never modify F.

**Exit:** P8 can close only when V passes and the F/V identity chain is independently reviewable.

## Stage E — final P9

Execute only after P8 closes.

- dispatch from exact V commit;
- independently resolve F and frozen candidate/P7 identities;
- verify F and V external digests;
- verify P9 script/workflow definitions did not drift after F;
- reject any pilot authorization already granted, empirical N > 0, empirical execution, or unblinding;
- retain source P9 evidence and registry;
- move P9 evidence into durable custody and independently re-hash before final adjudication.

**Exit:** P9 CLOSED / VERIFIED for final frozen-chain integrity only.

## Stage F — separate pilot authorization

Only after P8 and P9 closure:

- create a separate explicit authorization record;
- bind it to exact F/V/P9 identities;
- confirm blinded execution remains unable to access the mapping;
- only then may empirical collection begin.

Authorization is not implied by green CI, P9 PASS, freeze construction, deployment readiness, or this plan.

## Parallel non-scientific lanes

These may progress without changing the PDMAL gate sequence:

- **Issue #144:** 82 safe-to-prune branch refs identified; mutation remains blocked because no branch-delete action is exposed.
- **Issue #277:** Python quality merge-enforcement configuration requires repository-admin capability not exposed here.
- **Issue #224:** agent identity implementation exists but sovereign ratifications remain human-authority decisions.
- **Issue #122:** P-38 source recovery remains blocked after GitHub/Notion/Gmail/file-library searches found no authoritative source copy.
- **Issue #36:** AOGA runtime is verified; Sentinel→AOGA integration is not implemented/evidenced; live staging circuit-breaker evidence remains pending.
- **Issue #32/#64:** evaluator mechanism is hardened, but provenance-controlled ground-truth corpus plus independently generated outputs are still needed for actual hallucination-rate evidence.

## Non-claims

This plan and its supporting control-plane work do not:

- execute P4;
- close P7, P8, or P9;
- create the real immutable freeze;
- grant pilot authorization;
- execute or unblind an empirical pilot;
- establish PDMAL efficacy;
- increase empirical N.

**Current scientific boundary remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
