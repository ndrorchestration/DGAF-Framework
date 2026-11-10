# Triadic coupling-state contract v0.1 — proposed research specification

Status: PROPOSED CONTRACT / PARTIAL SYNTHETIC MODEL / NOT EXPERIMENTALLY VALIDATED.
Date: 2026-11-10.
Baseline inspected: DGAF main `1a95b94332dffb404c5a3ce026d70781a8c10b90`.
Authority effect: NONE. SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.

## Placement and evidence boundary

This prospective contract extends the questions in
[Triadic Orchestration Patterns](../patterns/TRIADIC_ORCHESTRATION_PATTERNS.md).
It does not supersede its consensus/conducted definitions, amend a frozen
experiment, activate PDMAL-D, or integrate adjacent research into DGAF.

The pattern document defines three peer contributors or a conductor with two
augmenters. Generator/Critic/Governor below is a proposed role specialization,
not a recovered universal implementation contract. Its embedded mesh/conducted
functions are illustrative placeholders; trace flags do not establish isolation
or rollback. The baseline pages/api/triad.ts contains verification stubs.
[PR 1553](https://github.com/ndrorchestration/DGAF-Framework/pull/1553)
is a separate unmerged non-authorizing route repair; no result transfers here.

The [Notion formalization record](https://app.notion.com/p/3bcf5bad238b8123accfd4fd94f169b0)
separates topology, choreography, constraints and effect hypotheses.
The [topology protocol](https://app.notion.com/p/3bff5bad238b810399b3d384646094e5)
treats dodecahedral topology as a candidate research factor. This local triad
contract does not establish lattice-scale utility, convergence or independence.

## Research question

Does a specified communication policy improve correctness and reduce false
promotion relative to independent aggregation at matched resources, while
retaining dissent and containing injected failures?

Treat role assignment, communication graph, scheduling, shared mutable state,
execution isolation, model dependence and commit authority as separate factors.
Three agents do not imply independent judgments. Agreement does not imply truth.

## Actors and authority

| Actor | May do | Must not do |
|---|---|---|
| Generator | Submit candidate plus cited evidence | Commit accepted state or rewrite reviews |
| Critic | Submit checks, counterexamples and blocking objections | Treat candidate rationale as verified evidence |
| Governor | Propose reconciliation and record unresolved dissent | Grant itself permissions or dismiss objections without policy evidence |
| Commit controller | Evaluate frozen policy and atomically record eligible synthetic transition | Infer authority from role labels, confidence, transport ACK or majority agreement |

The controller is an enforcement component, not a fourth reasoning vote.
For the first implementation it may affect only disposable in-memory synthetic
state. No filesystem, repository, deployment or external-action executor is
authorized by this document.

## Required run manifest

Reject missing or ambiguous mandatory fields before accepting messages:

- contract_version, run_id, source_commit, policy_digest, fixture_digest;
- model/version identifiers, prompt digests, decoding settings and seeds where
  available; note nondeterminism that seeds cannot eliminate;
- role-to-agent mapping, tool allowlist and shared evidence snapshot digest;
- mode, topology_epoch, expected predecessor version, monotonic deadline;
- required checks and objection disposition rules, commit-controller identity;
- budget for tokens, calls, wall time and maximum reconciliation rounds;
- predeclared switching triggers, thresholds, hysteresis and maximum switches.

No default uncertainty threshold, phi constant or uncalibrated confidence score
may authorize promotion or switching. Missing calibration disables adaptive mode.

## Modes and allowed edges

| Mode | Allowed information flow | Private state | Exit condition |
|---|---|---|---|
| INDEPENDENT | Versioned task/evidence to each role; each sealed assessment to controller | Initial assessments hidden from peers until all required submissions are frozen | Complete submissions or deadline |
| CONDUCTED | After initial freeze, role submissions to Governor; Governor requests to Generator/Critic; replies to Governor/controller | Initial assessments remain immutable; private scratch state is not shared | Proposed resolution, round limit or deadline |
| ADAPTIVE | Only a reviewed transition between the preceding edge sets | Same immutable initial assessments and state ownership | Triggered transition, budget exhaustion or HOLD |

Independent mode means communication separation, not statistical or external
independence. Initial Critic criteria should be frozen before candidate rationale
is visible; later candidate evaluation must be separately timestamped.
A missing peer at the deadline yields HOLD, never implicit agreement.

Shared mutable storage is not permitted in v0.1. Published evidence snapshots
are read-only. Changes to evidence require a new digest and new evaluation;
they cannot silently modify a proposal already under review.
Adapter synchronization and shared model updates are explicitly outside v0.1.

## Message contract

Each message carries run_id, message_id, sender identity/role, topology_epoch,
predecessor version, candidate digest, evidence digest, policy digest, type and
payload digest. Authenticate sender identity through the selected test harness
boundary; hashes alone provide neither identity nor authorization.

Allowed types: CANDIDATE, ASSESSMENT, OBJECTION, RESOLUTION, SWITCH_REQUEST,
SWITCH_RECEIPT, COMMIT_RECEIPT and HOLD_RECEIPT.
Reject malformed, stale-epoch, wrong-run, unauthorized-edge, wrong-policy or
digest-mismatched messages. Record the rejected message identity and reason.
A transport ACK records delivery only. Deduplicate by run_id/message_id and
reject reuse of an identifier with different bytes.

## Promotion and dissent

Commit eligibility requires ALL of:

1. Current explicitly scoped authority at the instant of commit.
2. Exact candidate/evidence/policy identity match and complete required checks.
3. Every blocking objection resolved according to the frozen policy, with
   linked evidence; a vote cannot erase a counterexample.
4. Unchanged predecessor version and current topology epoch.
5. Unexpired deadline and sufficient remaining budget.

Commit uses one atomic compare-and-set against predecessor and epoch, with a
unique operation identifier. Retries return the existing receipt without a
second state transition. If authority storage cannot support the required
atomic check, implementation readiness is BLOCKED.

Outcomes are COMMITTED_SYNTHETIC, REJECT, HOLD or INCONCLUSIVE.
An accepted synthetic transition is not a scientific admission.
Retain initial assessments, dissent, revisions, disposition rationale and
evidence lineage even after agreement. Correctness is scored against an
external-to-the-orchestration oracle, not by the Governor's self-rating.

## Reconfiguration protocol

1. Stop new candidate admission for the current epoch.
2. Capture immutable predecessor, evidence and outstanding-message identities.
3. Evaluate a predeclared trigger; uncertainty alone is insufficient.
4. Cancel or disposition outstanding messages explicitly.
5. Atomically advance epoch and allowed-edge policy under current authority.
6. Emit a switch receipt binding both epochs and state digests.
7. Re-evaluate affected proposals under the new epoch; old approvals cannot
   authorize a new-epoch commit.

A failed or timed-out switch leaves the last accepted state unchanged and enters
HOLD. Restrict information propagation when contamination is suspected.
Missing shared context may justify a new evidence snapshot; conflicting
interpretations justify retaining independent assessments before reconciliation.
Scheduling failure may justify coordination changes without exposing judgments.
These are candidate policies to test, not validated control rules.

Rollback means discarding uncommitted synthetic state only. Reversing an
external effect would require a distinct authorization and compensating action;
no such executor is specified here.

## Falsification and acceptance matrix

The full cases below remain planned at system scope. The partial synthetic model
coverage described at the end does not establish full-case acceptance.

| ID | Intervention | Required observation |
|---|---|---|
| C01 | Complete valid evidence, current authority, no blocking objections | Exactly one synthetic commit and a verifiable receipt |
| C02 | Three agents agree on an oracle-false assertion | Oracle marks false promotion if committed; agreement never counts as correctness |
| C03 | Critic supplies unresolved decisive counterexample | HOLD/REJECT, dissent preserved |
| C04 | Duplicate a valid commit message | Same receipt; zero additional transitions |
| C05 | Reuse message ID with changed payload | Reject and retain conflict evidence |
| C06 | Revoke authority after review, before commit | No commit |
| C07 | Change predecessor concurrently | No commit against stale predecessor |
| C08 | Replay old approval after topology switch | Reject stale epoch |
| C09 | Required Critic times out | HOLD; no fabricated assent |
| C10 | Inject unsupported premise into a peer message | Preserve unverified provenance; measure downstream propagation |
| C11 | Corrupt evidence/policy digest or omit required field | Reject before evaluation/commit |
| C12 | Oscillating trigger values | Respect hysteresis/switch budget; terminate boundedly |
| C13 | Crash during switch before atomic epoch update | Retain prior accepted state; recovery does not mint authority |
| C14 | Crash after commit before ACK | Replay returns original receipt, no duplicate effect |
| C15 | Permute role names without changing permissions | Authority follows explicit mapping, not persona names |
| C16 | Supply an uncalibrated adaptive trigger | Adaptive mode refused; no silent fallback that claims equivalent evidence |

For control acceptance, C01 must pass and C03–C09/C11–C16 must have zero forbidden
transitions in the declared finite test matrix. This establishes only tested
engineering behavior, not universal safety. C02 and C10 measure scientific
failure modes; do not turn an observed error into a passing correctness result.

## Prospective comparison

Compare independent aggregation, conducted discussion after initial assessment
freeze, and adaptive switching. Hold roles, fixtures, model configurations,
available evidence, tools and resource ceilings constant. Record actual usage.
Include a resource-matched single-agent/checklist comparator. Vary roles in a
separate ablation; the first comparison estimates coupling-policy effects only.

Pre-register task families, sampling unit, minimum meaningful effect, sample-size
rationale, exclusions, oracle adjudication, stopping rules and analysis before
confirmatory execution. Split tuning/calibration from held-out evaluation;
cluster repeated runs by task rather than counting agents or messages as
independent samples. Report uncertainty intervals, failures and inconclusive
results. Do not choose thresholds from held-out outcomes.

Primary outcomes: oracle correctness and false-promotion rate.
Secondary outcomes: false rejection, dissent retention, correlated error,
containment breaches, communication volume, latency, cost and recovery success.
Independent non-author replication is a separate gate.

## Implementation order and open decisions

1. Review this contract and decide scope without changing scientific authority.
2. Implement a deterministic synthetic state machine and the control matrix.
3. Verify receipt replay, revocation race and stale-epoch behavior.
4. Review oracle design and the independent baseline.
5. Define/calibrate adaptive triggers using separate data.
6. Freeze an authorized experiment before any confirmatory collection.

Still unresolved: eligible authority issuer, authenticated message mechanism,
storage transaction semantics, empirical trigger calibration, oracle ownership,
sampling/power parameters and independent reviewer. Until resolved, this is a
reviewable specification, not an implementation-ready production system.

## External rationale (not evidence for DGAF efficacy)

- [Du et al., ICML 2024](https://proceedings.mlr.press/v235/du24e.html):
  structured debate improved evaluated tasks; supports testing interaction.
- [Choi et al., NeurIPS 2025](https://papers.nips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html):
  voting explained much of the observed gain; motivates independent aggregation.
- [Kaesberg et al., ACL 2025](https://aclanthology.org/2025.findings-acl.606/):
  protocol and discussion effects differ by task; measure more than agreement.
- [Redis Streams documentation](https://redis.io/docs/latest/develop/data-types/streams/):
  delivery/acknowledgment/recovery semantics do not provide epistemic acceptance.

## Partial synthetic model checkpoint — 2026-11-10

Implementation: `scripts/triadic_commit_model.py`.
Tests: `tests/test_triadic_commit_model.py`.
Run: `python -m unittest discover -s tests -p test_triadic_commit_model.py -v`.
Local Python 3.12.14: **9 tests passed**. No LLM calls or scientific samples.
Local Black/flake8 are unavailable; hosted quality and full-repository checks
must be assessed at the resulting PR head before claiming wider verification.

The model uses trusted fixture inputs, a single in-process lock, frozen proposal
and receipt objects, and in-memory operation deduplication. It supports no real
authority issuer, authenticated peer messages, external effects, persistence,
LLM reasoning or adaptive mode. Epoch invalidation is fault injection only.
Caller-provided time models a trusted clock; clock authentication is absent.

| Cases | Narrow modeled coverage | Remaining gap |
|---|---|---|
| C01, C03, C04, C05 | Synthetic commit, objection block, replay, conflicting operation identity | Full role/message/evidence protocol |
| C06, C07 | Revocation before commit; two concurrent candidates yield one transition | Distributed authority races |
| C08 | Old proposal rejected after injected epoch increment | Actual governed topology switch |
| C09, C11 | Incomplete check/deadline rejection; malformed fields and wrong identities | Peer timeout handling, authenticated digests |
| C14 | Replay after simulated ACK loss and revocation returns original receipt | Process crash and durable recovery |
| C02 | Oracle-false candidate accepted when supplied check flag is true | Semantic verifier and real-agent comparison |
| C10, C12, C13, C15, C16 | NOT IMPLEMENTED | Propagation, adaptive policy, recovery and role mapping |

C02 is a deliberate negative scientific finding for this toy mechanism: passing
control tests does not make its accepted answer correct. It must not be reported
as a successful correctness or multi-agent efficacy trial. Denied operation IDs
are retained; revisions require a new operation ID. Replayed receipts report the
original result and do not imply renewed authority or another state change.

Prior documentation-only head `30f52b542670eeebf5ae340d95b7599ba9d87932`
had passing documentation, governance and Python 3.10/3.11/3.12 test jobs.
Required security-scan failed at pip-audit (run 42827378914); three PDMAL
workflows failed at Python setup (runs 42827378794, 42827378466, 42827378670).
These failures are retained, not waived, and those results do not verify the
new model source. DRAFT / UNMERGED; all scientific and authorization ceilings
remain unchanged.
