# DGAF / PDMAL Next-Stage Expert-Panel Execution Plan — 2026-09-05

**Status:** ACTIVE PLANNING CONTROL / PRE-FREEZE / NO EXPERIMENT AUTHORITY  
**Designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Documentation reconciliation source boundary:** `a3bafa6fca8599df479a685828f5fdddb6bae589`  
**Empirical N:** `0`

## Panel perspectives

This plan reconciles six distinct expert perspectives against the repository evidence:

1. **Experimental governance / methodology** — protects the P4 → P7 → P8 → P9 → authorization sequence and prevents engineering evidence from becoming efficacy evidence.
2. **Epistemic provenance / claims auditing** — requires exact identities, external digests, non-transferable evidence scope, and explicit UNKNOWN/OPEN states.
3. **Security / custody** — protects effective separation of control over the blinding secret and rejects aliases, agents, bots, same-operator accounts, or analyst-recoverable infrastructure as substitutes for real independence.
4. **Independent verification / red team** — searches for circular identities, self-verification, mutable-ref dependence, verifier drift, hidden administrator/recovery paths, substitution, and premature authorization paths.
5. **CI / reliability / release engineering** — requires exact-head validation, fail-closed workflow behavior, post-merge reproduction, deployment identity separation, and durable evidence handling.
6. **Repository / documentation governance** — keeps current-facing control surfaces synchronized while preserving historical records as scoped provenance.

## Panel consensus

The system has moved beyond broad implementation hardening. The critical path is now narrow, but the remaining steps are higher-consequence governance transitions.

Issue #280 corrected the P7/P8/P9 circular dependency by separating immutable freeze object F from downstream verification record V. PR #284 integrated that correction. Issue #285 then corrected the earlier P4 model, which over-specified the mechanism of independence by requiring a distinct human in every case. PR #286 merged that P4 architecture correction as `a3bafa6fca8599df479a685828f5fdddb6bae589`.

The canonical P4 model preserves distinct-human custody as Mode H while permitting Mode I institutional/third-party custody and Mode T independently enforced technical custody. Every mode must establish the same invariant: before the predeclared release condition, the execution/analysis principal cannot unilaterally recover the protected blinding material through ordinary, administrative, recovery, backup, policy-edit, credential-reset, export, or break-glass paths.

No custody mode has been instantiated. Issue #287 is an OPEN design/threat-model lane for a possible zero-human Mode T lifecycle. It is not P4 evidence and does not yet change the canonical pre-freeze commitment lifecycle.

## Stage A — pre-P4 control-plane correctness

### A1. Remove P7/P8/P9 circularity

- Separate immutable freeze object F from post-freeze P8 verification record V.
- Restrict P7 closure blockers to pre-freeze inputs.
- Require final P9 to read candidate/P7/freeze state from exact F.
- Require final P9 to read V from exact descendant verification commit.
- Require external byte digests for both F and V.
- Require P9 verifier script/workflow identity equality between F and V.
- Maintain authorization `NOT_GRANTED` and empirical N `0` during P9.

**State:** IMPLEMENTED through PR #284 / merge `2d8a525b3f1717c5675907769615207e5aa59fd5`; later exact-scope validation remains evidence-bound to the runs that executed it.

### A2. Generalize P4 from human-only custody to independently enforceable custody

- Make `P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md` canonical.
- Preserve the historical human path as Mode H.
- Add Mode I institutional/third-party custody.
- Add Mode T independently enforced technical custody.
- Require a complete control-path inventory and evidence that the analyst lacks every unilateral path capable of defeating the blind.
- Reject same-operator accounts, AI agents/personas, repository secrets, analyst-recoverable vaults, analyst-administered KMS/HSM paths, and preregistration alone as P4 substitutes.
- Preserve P4-A pre-execution closure and P4-B post-unblinding continuity audit as distinct lifecycle stages.

**State:** COMPLETED as a governance-architecture correction through Issue #285 / PR #286 / merge `a3bafa6fca8599df479a685828f5fdddb6bae589`. This changed the admissible control architecture only; P4 itself remains OPEN / NOT EXECUTED.

### A2.1. Evaluate a solo zero-human Mode-T lifecycle

Issue #287 is the active design/threat-model lane.

Candidate design concept:

- exact frozen workflow/helper identity;
- transient hosted execution environment;
- secret/mapping generation only inside the separately authorized empirical runner;
- blinded dataset emitted without plaintext mapping;
- future-time/timelock release bundle;
- primary analysis lock server-timestamped before the release condition;
- fail-closed invalidation if analysis is not locked before release;
- post-release P4-B continuity/reveal audit.

**Critical caveat:** this design conflicts with the current universal P4-A requirement that real key/mapping commitments already exist before P7/freeze. Therefore the candidate architecture cannot be promoted merely by implementing tooling. It requires a separate threat model, mode-specific lifecycle decision, P7/P8/P9 schema changes where justified, adversarial tests, and independent review before it can become an accepted Mode-T path.

**State:** OPEN / DESIGN ONLY / NOT P4 EVIDENCE.

### A3. Repository merge enforcement

Issue #277 remains a repository-administration control.

- Python quality workflow fail-closed behavior is verified.
- Protected-branch/ruleset readback does not require the Python quality matrix before merge.
- Current connector cannot mutate branch protection/rulesets.

**Exit:** authorized repository administrator updates required checks/workflow policy, configuration is independently read back, and a controlled failing case demonstrates merge enforcement if practical.

This lane may remain externally blocked without blocking PDMAL scientific sequencing unless governance explicitly promotes it to a scientific prerequisite.

## Stage B — real P4-A custody gate

Repository automation can prepare and test the control model, but it cannot truthfully declare real custody without evidence from the selected external/enforced mechanism.

Required events under the current canonical lifecycle for any mode:

1. select exactly one custody mode: H, I, or T;
2. identify the execution/analysis principal and custody authority/system;
3. generate and protect the blinding key, mapping, and commitment nonces outside analyst access;
4. publish only nonce-hardened key/mapping commitments;
5. predeclare the release rule;
6. inventory every ordinary/admin/recovery/backup/export/break-glass path;
7. retain evidence that the execution/analysis principal cannot use any path alone to recover protected material before release;
8. complete independent review appropriate to the selected custody mode without exposing secret material.

Mode H additionally requires genuinely distinct humans and attributable role/no-access attestations. Mode I requires external custody/release-policy evidence and lack of unilateral analyst administration/recovery. Mode T requires independently inspectable or machine-verifiable enforcement evidence and absence of analyst-controlled recovery or override capability.

**Stop condition:** any unexamined control path, analyst-controlled override, missing commitment, missing release rule, contradictory access evidence, unsupported independence claim, or unmerged alternate lifecycle keeps P4-A OPEN.

## Stage C — P7 final exact binding

Execute only after P4-A closes.

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
- confirm blinded execution remains unable to access the mapping under the accepted custody lifecycle;
- only then may empirical collection begin.

Authorization is not implied by green CI, P9 PASS, freeze construction, deployment readiness, preregistration, custody setup, a proposed timelock design, or this plan.

## Parallel non-scientific lanes

These may progress without changing the PDMAL gate sequence:

- **Issue #144:** safe-to-prune branch refs remain a repository-hygiene lane.
- **Issue #277:** Python quality merge-enforcement configuration requires repository-admin capability.
- **Issue #224:** agent identity implementation exists but sovereign ratifications remain human-authority decisions.
- **Issue #122:** P-38 source recovery remains blocked after prior source searches found no authoritative copy.
- **Issue #36:** AOGA runtime is verified; Sentinel→AOGA integration and live staging circuit-breaker evidence remain separate work.
- **Issue #32/#64:** evaluator mechanism is hardened, but provenance-controlled ground-truth corpus plus independently generated outputs are still needed for actual hallucination-rate evidence.
- **Issue #287:** zero-human Mode-T custody architecture remains a design/threat-model lane until independently accepted.

## Non-claims

This plan and its supporting control-plane work do not:

- execute P4-A;
- close P7, P8, or P9;
- create the real immutable freeze;
- grant pilot authorization;
- execute or unblind an empirical pilot;
- establish PDMAL efficacy;
- establish the sufficiency of a proposed zero-human Mode-T mechanism;
- increase empirical N.

**Current scientific boundary remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
