# DGAF Capability Governance Design Track

> **Status:** PROSPECTIVE / NON-AUTHORIZING  
> **Primary rule:** Specify and test authority semantics before broad connector implementation.  
> **Companion:** `CAPABILITY_GOVERNANCE_PROTOCOL.md`

## Goal

Evolve DGAF from the current bounded local MCP adapter toward provider-neutral capability governance without prematurely building a general proxy or hosted control plane.

## Phase 0 — Authority and scope alignment

Deliverables:

- confirm canonical relationship between the Agent Governance Transition Specification and Capability Governance Protocol;
- map the existing functional role registry to runtime capability concepts without converting role descriptions into executable authority;
- define terminology for provider, capability, adapter, transport, effect, authorization, delegation, workflow, receipt, and postcondition;
- record explicit non-goals and scientific-state non-transfer boundaries;
- run the canonical Telescopic Lens against the design.

Exit criteria:

- no unresolved terminology collision;
- no transport-specific authority semantics;
- no implicit conversion of conceptual agents into runtime principals.

## Phase 1 — Machine-readable contracts

Deliverables:

- capability-manifest JSON Schema;
- authorization-object JSON Schema;
- delegation-chain schema;
- workflow-authorization schema;
- execution-receipt schema;
- postcondition/reconciliation schema;
- lifecycle and revocation schema;
- canonical JSON and digest rules.

Required properties:

- versioned and signed manifests;
- unknown fields handled by explicit compatibility policy;
- capability identity stable across adapter replacement;
- exact-action digest reproducible across implementations;
- tenant/security-domain identity explicit where applicable.

Exit criteria:

- positive and negative schema fixtures;
- deterministic canonicalization test vectors;
- version-compatibility rules documented.

## Phase 2 — Formal invariants and model checking

Model at minimum:

- non-widening delegation;
- authorization-before-execution;
- action-digest approval binding;
- revocation before commit;
- commit-time state revalidation;
- no self-broadening policy mutation;
- non-compositional authorization;
- partial execution preserving history;
- replay/idempotency behavior;
- unknown-outcome reconciliation.

Use a small finite model before selecting a production policy engine.

Exit criteria:

- model contains explicit counterexample tests;
- every core invariant has at least one illegal trace;
- implementation requirements link back to invariant identifiers;
- no claim of complete formal verification beyond modeled scope.

## Phase 3 — Conformance and adversarial harness

Build provider-neutral tests before expanding providers.

Test families:

- stale/replayed authorization;
- target substitution;
- delegation widening;
- confused deputy;
- approval laundering;
- prompt/tool injection;
- malicious capability metadata;
- sensitive-read to prohibited-write exfiltration;
- provider timeout with side effect completed;
- duplicate retry suppression;
- partial workflow failure and compensation;
- policy-version drift;
- revocation race;
- audit tampering and secret leakage.

Exit criteria:

- core profile conformance suite runnable without real credentials;
- synthetic/mocked provider adapter available;
- failures produce explicit governed states rather than exceptions alone.

## Phase 4 — Bounded reference implementation

Reuse the existing local MCP adapter as the first controlled integration surface.

Implement only:

- capability manifest loading;
- action canonicalization;
- PDP decision interface;
- PEP enforcement;
- scoped authorization object;
- exact-action digest binding;
- idempotency key handling;
- execution receipt capture;
- postcondition state;
- audit/provenance linkage.

**Bounded replay/idempotency slice implemented on draft PR #1041:** idempotency keys bind to exact action digests; completed results replay without a second dispatch; digest collisions and in-flight duplicates fail closed; unknown outcomes block retry until reconciliation; denied reservations can be released for a later authorized attempt. The original process-local ledger is now complemented by a SQLite-backed reference ledger using `BEGIN IMMEDIATE`, WAL mode, and bounded busy-timeout semantics. Completed results, unknown outcomes, digest binding, and denied-release state survive ledger re-instantiation; two local contenders cannot both reserve the same key. This remains a single-host reference mechanism, not distributed consensus or production-grade cross-region idempotency.

Do not yet implement:

- arbitrary provider proxying;
- broad OAuth brokerage;
- multi-tenant hosting;
- plugin marketplace;
- automatic policy synthesis;
- universal connector discovery.

Exit criteria:

- existing bounded adapter behavior preserved;
- unauthorized path demonstrably blocked at the enforcement point;
- no new scientific or primary-analysis authority introduced.

## Phase 5 — Second independent adapter path

**Bounded slice implemented on draft PR #1041:** an in-process mock HTTP/OpenAPI-style adapter exposes only `GET /v1/status`, opens no listener, and maps to the same `dgaf.local.status` governed capability as the MCP path.

Add one adapter with meaningfully different mechanics from local MCP, such as a mock REST/OpenAPI service or isolated GitHub read/write test fixture.

Purpose:

- prove capability identity is independent of transport;
- test adapter replacement;
- validate provider receipts and postconditions;
- expose hidden MCP-specific assumptions.

Exit criteria:

- same governed capability can be represented across two adapter types;
- policy remains capability-oriented;
- transport-specific trust properties are expressed without changing authority semantics.

A general provider proxy remains deferred until this phase passes.

## Phase 6 — Credential and data-flow profiles

Only after core enforcement is stable, add optional profiles for:

- short-lived/audience-bound credential exchange;
- proof-of-possession;
- workload identity;
- taint/data classification;
- egress policy;
- redaction/DLP;
- model-context contamination controls.

Exit criteria:

- agent does not receive raw provider credentials in the brokered path;
- cross-boundary data flow has explicit policy decisions;
- secrets are excluded from audit/evidence records.

These profiles should remain optional until deployment requirements justify them.

## Phase 7 — Operability and recovery

Add:

- provider health/attestation;
- revocation propagation;
- rate/cost budgets;
- failure-policy matrix;
- reconciliation workers;
- rollback/compensation orchestration;
- incident evidence;
- deterministic replay of decisions where possible;
- observability that distinguishes policy denial from provider/runtime failure.

Exit criteria:

- EXECUTION_OUTCOME_UNKNOWN can be reconciled;
- partial execution has explicit recovery semantics;
- degraded modes cannot widen authority;
- operator can trace a decision from request through postcondition.

## Phase 8 — Multi-tenant, federation, and productization research

Research before commitment:

- tenant isolation;
- cross-domain delegation;
- DGAF-to-DGAF federation;
- embedded library vs sidecar vs gateway vs hosted control plane;
- policy distribution and trust roots;
- extension registries;
- conformance/certification profiles;
- upgrade and compatibility governance.

Do not treat these as core requirements for the initial reference implementation.

## Minimal trusted computing base

Core TCB candidates:

- canonicalizer/digest logic;
- policy decision interface;
- authorization verifier;
- commit-time revalidator;
- PEP/tool gateway;
- revocation check;
- receipt/postcondition state;
- integrity-protected policy/manifest loading.

Keep orchestration planners, model prompts, UI, provider metadata, and retrieved content outside the trusted base where possible.

## Expert-panel review lanes

Each major revision SHOULD be reviewed from at least these perspectives:

1. distributed systems and reliability;
2. zero-trust security / IAM;
3. AI-agent and multi-agent architecture;
4. API/MCP/plugin/connector integration;
5. formal methods and authorization logic;
6. privacy/data governance;
7. adversarial security and supply chain;
8. developer experience, operability, and adoption.

Disagreements should be recorded as design tensions with explicit disposition, not collapsed into a single consensus score.

## Canonical Telescopic Lens application

For every phase, review all eight canonical dimensions at:

- Macro;
- Mid;
- Tactical;
- Quantum.

Dimensions:
Intent Alignment; Provenance Integrity; Boundary Clarity; Coherence; Coverage; Calibration; Sovereignty; Evolvability.

A Telescopic Lens PASS is structural evidence only and must not be represented as production security assurance.

## Do now / validate next / defer

### Do now

- finish protocol terminology and invariants;
- create schemas and canonicalization test vectors;
- map current local MCP operations into draft capability manifests;
- write threat model and abuse-case corpus;
- build core conformance tests;
- run Telescopic Lens review.

### Validate next

- extend the implemented bounded small-state/model-checking analysis beyond the current composition, recovery, and competing-idempotency interleavings toward larger state spaces, persistent storage, and stronger concurrency models;
- extend the implemented SQLite-backed single-host persistent/concurrent idempotency slice toward multi-process crash recovery, lease/owner semantics, and stronger distributed-storage models;
- credential-broker trust-root and token-boundary profile;
- postcondition verification classes beyond the bounded mock/local paths;
- minimal policy-engine comparison;
- adversarial adapter/runtime substitution tests.

### Defer

- general MCP/API proxy;
- hosted multi-tenant service;
- marketplace/plugin ecosystem;
- automatic policy generation;
- federation;
- broad credential brokerage;
- certification claims.

The design track advances only when each prior phase produces evidence sufficient for the next commitment.
