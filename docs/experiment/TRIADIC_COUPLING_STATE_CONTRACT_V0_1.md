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

The commit model uses trusted fixture inputs, a single in-process lock,
frozen proposal and receipt objects, and in-memory operation deduplication.
It supports no real authority issuer, external effects, persistence, LLM
reasoning or adaptive mode. A separate experimental message boundary adds
fixture-key MAC checks but not production authentication or orchestration. Epoch invalidation is fault injection only.
Caller-provided time models a trusted clock; clock authentication is absent.

| Cases | Narrow modeled coverage | Remaining gap |
|---|---|---|
| C01, C03, C04, C05 | Synthetic commit, objection block, replay, conflicting operation identity | Full role/message/evidence protocol |
| C06, C07 | Revocation before commit; two concurrent candidates yield one transition | Distributed authority races |
| C08 | Old proposal rejected after injected epoch increment | Actual governed topology switch |
| C09, C11 | Incomplete check/deadline rejection; malformed fields and wrong identities | Peer timeout handling, authenticated digests |
| C14 | Replay after simulated ACK loss and revocation returns original receipt | Process crash and durable recovery |
| C02 | Frozen fixture oracle scores accepted false assertions independently of controller eligibility | Real semantic verifier, blinded external adjudication, real-agent comparison |
| C10 | Synthetic, pre-annotated message lineage tracks unsupported claim assertion, copying and challenge | Authenticated messages, observed rather than asserted provenance, live contamination experiments |
| C12, C13, C15, C16 | NOT IMPLEMENTED | Adaptive policy, durable recovery and role mapping |

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

## Bounded oracle-scoring extension — 2026-11-10

Modules: `scripts/triadic_oracle_scoring.py` and
`tests/test_triadic_oracle_scoring.py`. Run:

```bash
python -m unittest discover -s tests -p test_triadic_oracle_scoring.py -v
```

The offline fixture oracle holds predeclared exact-answer labels **outside the
commit controller's inputs**. After a synthetic commit or HOLD, it independently
scores whether the committed candidate matches that finite answer key; a
Governor's claimed correctness cannot change this score. An oracle-false
candidate may still be committed by the model. **C02 detects and records false
promotion; the scoring layer is not a semantic admission gate.**

C10 uses fixture-annotated claim IDs, stance (ASSERT, CHALLENGE, QUOTE),
message IDs and parent references. Ordered parent links identify attributable
transitive propagation from a declared injection root. An unsupported assertion
without known ancestry is reported separately as **unattributed**, not as proof
of non-propagation. Challenging or quoting a false claim is not counted as
endorsing it. Malformed, duplicate, forward-referencing or missing injection
records reject scoring instead of inventing certainty. The scorer preserves
event IDs as synthetic audit evidence but does not certify their authenticity.

Local Python 3.13.5: **15 targeted unittest cases passed** before upload,
using a faithful local copy of the unchanged commit controller. The exact
hosted code head must still be checked for formatting, typing, full-suite
regressions and dependency-security findings. No full C01-C16 acceptance
claim follows from these 15 tests.

The fixture author supplies both oracle labels and trace annotations: this is
**architectural separation of scoring**, not independently adjudicated truth,
peer independence, blind evaluation or empirical evidence. Synthetic role names
are not running agents; provenance is declared, not authenticated. There are no
LLM calls, real task sampling, external effects, adaptive switching or durable
recovery. The earlier security-scan and PDMAL infrastructure failures remain
separate blockers until verified otherwise.

DRAFT / NON-ADMITTING / UNMERGED. SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.

## Fixture-authenticated message boundary — 2026-11-10

Implementation: `scripts/triadic_message_boundary.py`.
Tests: `tests/test_triadic_message_boundary.py`.
Run: `python -m unittest discover -s tests -p test_triadic_message_boundary.py -v`.

This is a **separate research-only, in-memory message admission component**:
it is not attached to the synthetic commit controller or any repository,
deployment or external executor. A manifest pins one run ID, three distinct
fixture identities, explicit Generator/Critic/Governor roles, per-identity
32-byte-or-longer HMAC-SHA256 fixture keys, and candidate/evidence/policy
digests. The signed canonical JSON binds sender, role, recipient, message ID,
kind, epoch, predecessor, deadline and UTF-8 content digest. Message content
itself is also hashed and checked; signatures are checked with constant-time
MAC comparison against a key selected by the trusted fixture identity map.

The permitted independent-mode edges are **only to the synthetic controller**:
Generator may send CANDIDATE; Critic may send ASSESSMENT or OBJECTION; Governor
may send RESOLUTION. No signed role may independently authorize a commit or
an adaptive switch. Signed wrong-run/version messages are rejected before
operation-ID reservation. A message ID replay returns the original receipt
without another admission; conflicting, correctly signed bytes for an existing
ID return ID_CONFLICT. Unknown senders, bad MACs, revoked senders, role
spoofing, stale epochs/predecessors, altered run digests, expired deadlines and
unapproved message kinds all fail closed. A capacity limit bounds the
in-memory receipt ledger; exhaustion yields HOLD, not eviction.

**Security and evidence boundary:** HMAC authenticates only relative to
fixture-held shared secrets. It does not verify an agent's real-world identity,
proof of possession on a secure device, independence, permission issuer,
key lifecycle or message transport. A fixture actor able to sign arbitrary
content can still submit a false claim; C02 oracle scoring remains external
and post hoc. Role mapping and clock are trusted configuration. This module
has no persistent receipts, authenticated peer execution, restart recovery,
governed topology switch, real agent communication or scientific sample.
An ACK for admission does not establish evidential validity or permission
to act.

These tests cover a **narrow message-layer subset** of the planned C04/C05,
C08 and C11 mechanisms. They do not satisfy full system acceptance for those
cases, C14 durable recovery, C15 persona-permutation authorization, or the
C01-C16 suite. Hosted quality and repository CI results must be bound to the
resulting exact PR head before assigning any PASS checkpoint.

DRAFT / NON-ADMITTING / UNMERGED. SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.

## Durable synthetic receipt recovery — 2026-11-10

Research implementation:
`scripts/triadic_durable_receipts.py` and
`tests/test_triadic_durable_receipts.py`.

Local command (POSIX filesystem only):

```bash
python -m unittest discover -s tests -p test_triadic_durable_receipts.py -v
```

**Scope:** a separate, deliberately limited commit-state/receipt research
model that mirrors the in-memory controller's bounded eligibility checks.
It owns only a disposable journal in a test-created temporary directory,
not DGAF governance, the authenticated-message module, deployment,
filesystem actions on behalf of users, or external-effect authority.
It does not retrofit persistence into the existing controller or prove an
atomic transaction with the separately developed HMAC message boundary.

The initial fixture creates a new, exclusive journal on POSIX only. For
each synthetic operation it serializes the next state and corresponding
receipt into a single HMAC-sealed JSON snapshot, fsyncs a sibling
temporary file, atomically replaces the journal path and fsyncs its parent
directory **before returning the receipt**. Both committed and denied
operation IDs are retained. An exact replay returns the historical receipt;
reuse of the same identifier with different proposal bytes yields HOLD.
A terminal write exception poisons the writer, preventing subsequent new
transitions within that process.

Reopening an existing journal checks manifest binding, seal, schema,
receipt sequencing, state consistency, missing/truncated records and
duplicate operation IDs. It enters **RECOVERY_ONLY** mode: historical
receipts can be replayed; new operations, revocation changes and epoch
changes cannot be admitted by the recovered object. The original in-process
writer is a fixture-only authority assumption; restart never creates a
replacement writer or new authority. Revocation and simulated epoch
invalidation persist as state changes, without implementing real governance.

**Bounded crash injection:** interruption before atomic replacement leaves
the prior journal state; interruption after directory fsync but before
the receipt ACK recovers the new state and original receipt without a
duplicate synthetic transition. This tests simulated interruption points,
not actual power-failure, storage-hardware durability or cross-process
linearizability.

**Important falsification:** saving a previously valid journal snapshot,
recording a later accepted transition, and restoring the earlier
HMAC-authenticated snapshot **passes current verification**. The model
therefore cannot detect valid-prefix rollback. External monotonic custody,
hardware-backed anchors or independently retained receipts would need
separate research and authorization. Likewise, one-writer ownership is an
assumption; the code does not establish cross-process exclusive leasing,
distributed transactions, secure key lifecycle, real authenticated agent
identity or an authenticated monotonic clock.

A false answer can still be durably committed when trusted synthetic
eligibility checks say yes. Durable recovery preserves such an error;
the controller-external oracle can identify false promotion but does not
turn it into legitimate epistemic acceptance. The journal is not an
external-effect executor and does not establish scientific correctness.

Local Python 3.13.5: **22 bounded tests passed** before GitHub upload.
Hosted source-quality and test evidence must be bound to the resulting
exact PR head. The existing C14 full-case acceptance (real process crash
and end-to-end authenticated/durable effect recovery) remains
NOT_ESTABLISHED. C13 switch-crash recovery likewise remains unimplemented;
these disk fault points are not a governed topology switch.

DRAFT / NON-ADMITTING / UNMERGED.
SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.

## Monotonic custody witness fixture — 2026-11-10

Research modules: `scripts/triadic_monotonic_custody.py` and
`tests/test_triadic_monotonic_custody.py`. The separate fixture holds
a (run ID, monotonic sequence, journal SHA-256 digest) witness in a
thread-safe in-memory object **outside the journal file**, not in an
external durable service. Each recorded journal change, including denial,
revocation or epoch fault injection, requires a compare-and-swap advance
of the witness from the preceding sequence and digest.

Prospective state-machine behavior:

- Genesis may initialize an **empty** witness only when creating a new
  exclusive disposable journal. Reopening an existing journal without
  an independently retained witness fails closed; no authority is
  reconstructed from journal data.
- The synthetic journal is fsynced and atomically replaced **before**
  the fixture witness advances. Once the witness advances, the
  synthetic method may return its receipt.
- If a crash is injected before journal replacement, the old journal
  and witness still match; an opened recovery reader remains replay-only.
- If a crash or injected witness refusal occurs after journal
  replacement but **before** witness advancement, recovery detects a
  journal/witness mismatch and enters a blocking state. It cannot
  silently infer a missing witness receipt or automatically adopt the
  new journal state.
- If a crash occurs **after** witness advancement but before ACK, a
  reopened reader can return the original stored synthetic receipt
  without a second transition. The writer that experienced an
  uncertain completion is quarantined.
- Restoring an older valid HMAC-sealed journal while the same
  trusted witness survives produces JOURNAL_WITNESS_DIVERGENCE.
  An older valid journal alone is not sufficient to recover.

**Known negative and trust boundary:** restoring an old signed journal
**and replacing or resetting the witness** can make this toy checker
accept the older state. The fixture witness is an ordinary in-memory
Python object; it is neither durable across process restart nor an
independent, authenticated monotonic authority. It has no secure
bootstrap provenance, hardware-backed counter, external write quorum,
key custody, cross-process lease, authenticated transport, independently
verified timestamp or production failure isolation. A malicious actor
with control over both witnesses and journal can defeat this model.
The journal and witness are not committed in one transaction; a
between-store failure is detected and blocks recovery, rather than
recovering automatically. This is a deliberate fail-closed choice.

The test module defines **23 synthetic research tests** (full hosted
quality and execution status must be checked at the final PR head).
No real power-loss or adversarial storage tests have been performed.
The previous standalone durable-journal model continues to lack
rollback detection; this optional wrapper does not change that
baseline's API or production-readiness classification.

These tests inform a **narrow, partial C14 research mechanism** only.
C13 crash-during-switch, C15 real authorization mapping, the
end-to-end C01-C16 acceptance matrix, scientific validity and
independent external validation all remain NOT_ESTABLISHED.
A false answer remains eligible for synthetic commit when caller
check flags say yes: custody is not correctness.

DRAFT / NON-ADMITTING / UNMERGED.
SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.

## POSIX file-backed monotonic witness fixture — 2026-11-10

Implementation: `scripts/triadic_posix_witness.py`.
Tests: `tests/test_triadic_posix_witness.py`.
Run: `python -m unittest discover -s tests -p test_triadic_posix_witness.py -v`.

This **separate research fixture** replaces the earlier in-memory witness
object with an HMAC-sealed, append-only, fsynced record file in a separate
test directory. The file and lock path are independent of the journal path,
but remain on the **same untrusted host and filesystem failure domain**.
The witness retains a run ID, sequence, current journal digest and
prior-record digest for a bounded chain. It refuses missing, duplicate,
truncated, non-sequential, wrong-run, tampered, or incomplete records.
A distinct fixture HMAC key protects these entries. A POSIX `flock`
guard on a sidecar file serializes compare-and-swap witness updates
between cooperating processes. A stale expected state cannot append
a second transition at the same sequence.

The existing synthetic `WitnessedSyntheticController` now accepts
a subtype of its fixture witness, so the adapter can create an exclusive
journal and witness, persist the journal first, then append and fsync
the witness before acknowledging a synthetic operation. Reopen reads
the persistent witness rather than reconstructing it from the journal.
Recovered durable-journal readers remain **RECOVERY_ONLY** and cannot
mint new commit authority. The prior in-memory witness and baseline
durable-journal models remain available, unchanged in their documented
research status.

Positive and negative scenarios include restart with a new witness
object, a signed older-journal rollback detected by a surviving witness,
competing independent Python processes attempting the same witness
sequence, tampered/truncated witness rejection, and crash-injection
windows both before and after witness advancement. The design **blocks**
when the journal is durable but the witness update is missing; it does
not silently reconcile or automatically advance the witness.

**Critical negative control:** restoring the older journal **and**
its earlier valid signed witness file succeeds in this toy model,
including after process restart. This is evidence that local append-only
files, HMAC chaining and filesystem locks do **not** establish secure
monotonic anchoring. Any actor able to replace or roll back both files,
reuse a fixture key, remove/recreate the lock path, or compromise the host
can defeat the intended custody property. No independent operator,
remote trusted witness service, trusted hardware counter, anti-rollback
platform, cross-host attestation, secure key lifecycle or Byzantine
failure model has been exercised. An OS `flock` is advisory, not a
permission issuer or comprehensive production cross-process lease.

The module has **22 bounded test cases** defined; exact-head hosted
format/type/execution results must be observed before claiming PASS.
This is a software design exercise, not live multi-agent experimental
data, independent validation, production reliability, scientific
superiority or a full C14 acceptance result. A wrong semantic answer
can still be accepted and signed, because custody does not check truth.

DRAFT / NON-ADMITTING / UNMERGED.
SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.
