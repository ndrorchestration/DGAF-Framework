# SBCF cross-layer contract v0

Status: PROPOSED / PRE-FREEZE / SYNTHETIC ONLY / NOT AUTHORIZED FOR LIVE USE.

Queue: [issue #1338](https://github.com/ndrorchestration/DGAF-Framework/issues/1338).
Parent implementation: draft [PR #1339](https://github.com/ndrorchestration/DGAF-Framework/pull/1339), inspected head `4756929bfe9fb2fa8d42c49a86708f3f1caa5229`.
Protected-main source: `aabf1163515af291dc564bd7564fd12762a898c8`.

## Purpose and ownership

Test one paired structural view: task meaning and parameter provenance versus scoped authority and observed state. Duotopology is an optional working name; the technical model is a typed multilayer graph with explicit cross-layer constraints. No new mathematical topology or novelty claim is established.

The executable specification in `experiments/sbcf/cross_layer.py` reuses the parent's `SimulatedGate` and quarantine predicate. It has no effect adapter, no grant issuance/restoration API and no production connection. It does not replace the parent's state controller, evidence admission or four-arm harness.

Proposed real-system owners: authority broker owns grants/revocations; provenance service owns parameter lineage; enforcement point owns actual effect and resource identity; worker/queue/network observers own field-specific observations; Structural Epistemics retains claims and contradictions; Tektite projects separately typed states. These are target integration responsibilities, not verified current implementations. Neither the observer nor the UI grants authority.

## Cross-layer relations

| Relation | Meaning | Authority consequence |
|---|---|---|
| SENDS_TO | An agent can receive a message | None |
| SUPPORTS / CONTRADICTS | Evidence bears on a claim | None by itself |
| PARAMETER_FROM | A tool parameter has an attributed source | Must satisfy source policy; no independent grant |
| SCOPED_GRANT | Issuer permits subject/action/resource in bound context | Necessary permission precondition |
| EFFECT_RECEIPT | An enforcement observer reports an attempted/committed effect | Outcome evidence; no future grant |
| QUARANTINE_OBSERVATION | Complete required state dimensions were observed | Can support a bounded containment predicate; cannot restore authority |

A graph path is not transitive delegation. This v0 has no delegation composition or grant expansion. Message text and local evidence labels are inert inputs. They cannot fill a missing grant or establish canonical validation.

## Closed synthetic input schema

`evaluate(case)` accepts exactly six fields: request, grant, context, quarantine, message, local_evidence_label. The last two are informational only. Outputs are effect_permitted, quarantine_predicate, canonical_validation_established=false and authority_effect=NONE. These are reference judgments, not execution receipts or permission tokens.

Request fields: subject, action, resource, policy, run, nonce, parameter_sources. Grant fields: issuer, subject, action, resource, policy, run, nonce, not_before, expires_at, revoked. Grant may be null; null never permits the action. Identifiers are nonempty strings. Times are nonnegative integer ticks; booleans do not count as integers. `revoked` is strictly boolean.

Context fields: current resource identity, policy, run, nonce, now, regime, trusted_issuers, parameter_policy, observable, revocation_checked. Regime is NORMAL, RESTRICTED or QUARANTINED. Issuers are a nonempty list of identifiers; parameter_policy is a nonempty map from critical parameter names to nonempty allowed-source lists. Observable and revocation_checked are strict booleans. Unexpected structural fields fail closed.

The fixture context is assumed to be supplied by a trusted control plane. This function does not authenticate its issuer list, source names, clock, revocation flag or observations. A caller who controls these facts can forge them. The same-process values do not establish independent custody, source identity or semantic correctness. Policy completeness and exact object identity acquisition require separate evidence.

## Permission predicate

Permit the reference action only when all conditions hold:

1. Request and grant have the exact schema and strict types; issuer is registered in the supplied context.
2. Subject/action/resource/policy/run/nonce match between request and grant. Resource/policy/run/nonce also match commit-time context.
3. `not_before <= now < expires_at`; current grant is not revoked, revocation was checked, and required observability is true.
4. Parameter names match the critical-parameter policy exactly; every attributed source is permitted for its parameter.
5. The existing simulator is in NORMAL and has the explicit matching action grant.

Any missing, mismatched, expired, wrongly typed or unresolved condition withholds the simulated effect. The real enforcement point must acquire identity/revocation facts and commit the effect atomically, or provide an evidenced bounded-staleness protocol. This reference predicate cannot eliminate a real race by receiving a boolean named revocation_checked.

## Quarantine predicate and claim ceiling

Quarantine observation has exactly: production_capabilities, uncontrolled_workers, pending_external_actions, unauthorized_destinations, observable and external_attestation. Counts are nonnegative integers, never booleans. Both flags are strictly boolean. Complete zero counts, observable state/context, restrictive QUARANTINED regime and attestation flag are necessary for the inherited synthetic predicate.

`quarantine_predicate=true` means the fixture satisfies that predicate. The external_attestation flag is caller-controlled and is not trusted attestation. It does not establish operational quarantine, independent validation, canonical efficacy or authority restoration. A surviving child worker or queued effect falsifies this predicate even when a regime label says QUARANTINED.

## Fixture packet

`experiments/sbcf/fixtures/cross_layer_v0.json` contains 24 explicit synthetic records in eight families: authorized controls, communication/authority mismatch, parameter-source substitution, namespace collision, revocation race, delegation escape, observer injection and ambiguous evidence. Each has a distinct ID, reference judgment, input and expected output. Eight are development; sixteen are reserved.

Reserved is an allocation label only. All cases are public and used in contract consistency checks; they are not concealed independent holdouts. Before any efficacy comparison, generate and freeze separate adversarial evaluation cases, reference judgments, rubric, system/model versions, prompts, policies and stopping rules. Repeated outputs from a case are dependent. This packet neither runs nor amends the parent's A/B/C/D design or an existing frozen benchmark.

The proposed paired-versus-single-view comparison must keep the enforcement boundary and policy constant. An intentionally weaker action-name-only simulator is useful for demonstrating a missing binding, but is not sufficient as a security baseline for parity/superiority claims. Independently reproduce appropriate prior art before such claims.

## Prior-art intake for C1

- [AuthGraph, arXiv:2605.26497v1](https://arxiv.org/html/2605.26497v1): close dual-graph comparator for provenance/authorization alignment and parameter-source checks. Its initial clean planner and runtime replanning trust boundary need separate comparison. Primary-source method inspected in the preceding research audit; implementation availability and matched reproduction remain unestablished here.
- [CaMeL, arXiv:2503.18813v2](https://arxiv.org/abs/2503.18813v2): compare control/data separation and capability enforcement. Do not combine different paper versions' scores. Not reproduced here.
- [Kivela et al., Multilayer Networks](https://arxiv.org/abs/1309.7233): established structural vocabulary. Not an agent-security effectiveness benchmark.

These references supplement C1 as candidates. They do not establish baseline admission, functional parity, novelty or independent reproduction.

## Completion receipt — 2026-10-11

Deliverable: additive executable cross-layer specification, 24-case JSON packet, focused tests and this contract. Source reconstruction used only the parent's SBCF Python modules; it was not a complete repository checkout. No AGENTS.md path existed in the complete returned parent tree. Existing PR work was preserved.

Verification environment: Linux scratch runtime, Python 3.12.14. Test-first probe of an action-name-only reference adapter produced 17 failed assertions/subtests and 2 setup/input errors: expiry, parameter source, grant binding, restriction and strict-type checks exposed missing behavior; the fixture file was not yet created. The probe was replaced with the scoped predicate, not retained as a benchmark arm.

Final focused command: `python3 -m unittest discover -s tests -p 'test_sbcf_cross_layer.py' -v` — 10 tests passed, including all 24 fixture reference judgments and negative mutations. These are deterministic contract checks, not 24 empirical observations. JSON parsing and changed-file whitespace verification passed before publication.

Broader suite: `python3 -m pytest` could not start because pytest is absent from this runtime; a complete repository checkout was also not present. Required hosted gates are not established by the local focused result. Existing parent rollback, coordinated rollback and crash-consistency expected-failure tests were not changed or rerun locally. Their documented gaps remain OPEN.

Checkpoint disposition: C1 intake extended, C3 executable predicate added, C7 contract drafted. C0–C9 are not completed by this packet. Full model comparison NOT_RUN; eligible independent review NOT_RUN; live enforcement NOT_IMPLEMENTED. Reviewable on an isolated stacked draft branch; no merge or release acceptance.

Next ready task: validate these bindings at a real or independently instrumented effect boundary, including revocation/identity changes between planning and commit. Prioritize external source authority and custody recovery obligations already tracked in PR #1339. Do not infer runtime behavior from this deterministic function.

Preserved ceiling: SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.

## Verification follow-up — 2026-10-11

All previously observed hosted checks at `61b6d986b919d0185b0916e7e98974cfe98ca177` completed successfully. None supplied a Python matrix for this stacked research base; the existing Python workflow only targets main/develop. The earlier local pytest limitation is preserved above as historical evidence.

Added `.github/workflows/sbcf-research-tests.yml`: pushes to and pull requests against `research/sbcf-*` run the complete SBCF synthetic test group, including the cross-layer cases. The workflow checks out the candidate head, uses the existing pinned actions and hash-locked Python 3.12 QA toolchain, and runs `python -m pytest tests/test_sbcf*.py -ra` without failure masking. Relevant source/test/toolchain/workflow paths trigger it; documentation-only updates do not. Main/develop continue using the existing broader Python workflow. This focused job is not added as a protected-main required context.

The cross-layer module and test file were formatted; predicate behavior was unchanged. Local verification used Python 3.12.14 with repository-pinned tool versions Black 26.5.1, isort 8.0.1 and pytest 9.1.1: 61 passed, 3 xfailed in the full SBCF test group. Black/isort checks passed. Workflow YAML parsing, branch filter, exact pytest invocation and absence of continue-on-error were checked. Local packages were installed separately for QA; the hosted workflow uses the repository's hash-locked dependency file.

The three strict expected failures remain open: evidence-store snapshot rollback, cross-store crash consistency and coordinated rollback of both host-local stores. They are counterexamples, not successful protections. The focused result does not establish the repository-wide pytest suite, live containment, independent validation or empirical efficacy. Hosted execution of the new job must be observed separately at its resulting exact head.

Final verification at code/workflow head `cab7ae109c13dd6130daf1e32dd8b9daf188333f`: hosted [run 38159355010, job 114528832325](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38159355010/job/114528832325) completed successfully; logs confirm 64 collected, 61 passed, 3 xfailed, and successful formatting checks. The matching pull-request-triggered job 114528842678 also succeeded.

A clean, complete-history checkout of that exact head was tested in an isolated virtual environment installed from the repository hash-locked Python 3.12 toolchain: `PYTHONPATH=$PWD python -m pytest tests/ -q` returned **2080 passed, 5 skipped, 3 xfailed, 7 warnings, 101 subtests passed** in 19.50 seconds. This is the repository `tests/` suite, not every separate experimental/PPTL suite. The first broader attempt had 12 provenance-related failures under a shallow clone; restoring historical Git objects resolved them without changing frozen records or product code. Earlier dependency/collection setup failures were resolved by the isolated locked environment. A final documentation receipt commit may follow this tested head; it changes no code, fixtures or workflow.

### Subsequent witnessed-admission candidate — 2026-10-11

The results above describe draft #1340's version. The stacked atomic-witness candidate changes the local witnessed admission path and adds failure-injection tests; it preserves the standalone rollback and coordinated rollback xfails. The former split-store fixture remains an xfail and is now explicitly identified as an evidence-only API bypass. Counter mismatch fences subsequent witnessed admissions. See [updated crash-consistency QA](SBCF_CRASH_CONSISTENCY_QA_V0.md) for the current protocol, results and remaining limitations. This does not upgrade the cross-layer predicate to live enforcement or independent validation.
