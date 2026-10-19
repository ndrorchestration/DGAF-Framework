# SBCF prior-art verification ledger — v0

Status: PARTIAL PRIMARY-SOURCE VERIFICATION / NO PERFORMANCE PARITY. Checkpoint C1 remains open.
Verification refresh: 2026-10-19. Primary-source inspection is not implementation reproduction.

## NVIDIA OpenShell — verified primary documentation

Sources:
- https://docs.nvidia.com/openshell/latest/how-it-works/policies/overview
- https://docs.nvidia.com/openshell/latest/how-it-works/policies/schema
- https://docs.nvidia.com/openshell/latest/how-it-works/policies/default-policy

Current documented release: latest v0.1.4. Policy schema v1 includes `filesystem_policy`, `landlock`, `process`, `network_policies`, and `network_middlewares`. Filesystem/Landlock/process controls are startup-scoped; network policy and middleware are live-updatable. OpenShell documents default-deny outbound network policy, Landlock kernel enforcement, non-root process identity, and restrictive default policy behavior.

Minimum SBCF comparator requirement: independently enforced resource boundary, explicit process/user identity, default-deny network egress, live policy-change semantics, effective-policy inspection, fail-closed error behavior where configured, and reproducible bypass/update-race testing.

Current SBCF result: NOT PARITY. The SBCF branch implements synthetic policy/evidence contracts and local SQLite witness behavior only. It does not implement an OpenShell-equivalent sandbox, kernel filesystem enforcement, process identity boundary, credential broker, or network proxy.

Reproduction still needed: pin exact OpenShell release/container/runtime; exercise filesystem/process/network controls, hot update, invalid policy, bypass attempts, crash/update races, evidence capture, and outside review.

## OWASP Agent Control Standard (ACS) — verified source and implementation availability

Sources:
- https://genai.owasp.org/resource/agent-control-standard-acs/
- https://github.com/GenAI-Security-Project/agent-control-standard

OWASP published ACS on 2026-09-01. The project describes ACS as a runtime control wire specification with lifecycle hooks, declarative policy enforcement, observability and an audit trail. The public repository exposes specification, tests, tools and a reference implementation. The current repository documentation identifies ACS v0.1.0 schemas and a Guardian pattern that can allow, deny, modify, ask or defer before an action.

Important published limitations of the reference implementation: its wire is documented as unauthenticated even though ACS-Core requires baseline HMAC-SHA256 envelope signing; the Guardian's default decision-failure posture is documented as `proceed` unless explicitly set to deny; only a bounded subset of hooks is live in the cited AGT reference implementation. These limitations are part of the baseline, not reasons to dismiss it.

Minimum SBCF comparator requirement: pre-action interception, deterministic policy-first decision path, authenticated control channel or explicit failure, reconstructable audit record, fail-closed decision-unavailability posture, and conformance tests over supported hooks.

Current SBCF result: PARTIAL CONTRACT OVERLAP / NO INTEROPERABILITY OR PERFORMANCE PARITY. SBCF has deterministic synthetic decisions, fail-closed local evidence checks and signed test envelopes, but no ACS wire interoperability, Guardian integration, conformance result, authenticated external control channel or independently managed audit service.

### ACS executable reproduction checkpoint — 2026-10-19

Pinned source: `GenAI-Security-Project/agent-control-standard` commit `9c05f0402d76dea6b67a12a93672c2131137e572`.

Hosted reproduction: DGAF research workflow run `39185127303`, job `117845841547`, mirrors the upstream reference workflow contract: Ubuntu latest, Bun `1.3.11`, frozen `bun.lock`, pinned `trash-cli@7.2.0`, typecheck, then full `bun test`. Result: **1231 passed / 4 skipped / 0 failed**, 3754 expectations, 1235 tests across 73 files in 37.07 seconds. Typecheck passed.

Windows bounded reproduction: NeonPC, same upstream source, Bun `1.3.11`, documented external `ACS_OPA_PATH`, no source edits. `bun test hosts\\claude-code` returned **50 passed / 0 failed**, 206 expectations, 50 tests across four files in 6.45 seconds. The suite includes the real subprocess test that sends a destructive `rm -rf /` tool call through the Claude host shim and expects a Guardian policy denial.

First failures are retained as reproduction evidence. Bun `1.4.3` produced **2 passed / 48 failed** in the Claude host subset because child shims exited successfully with empty stdout; the repository's own CI pins Bun `1.3.11`, and rerunning on that version resolved the behavior. Before nested tests could run, an earlier attempt also failed because locally installed Bun was not on the child-process `PATH`. Neither environment mismatch is counted as an ACS policy failure.

Disposition: ACS is now a **reproduced executable comparator** for its own pinned reference suite and bounded deny behavior. This does not establish SBCF parity, interoperability, comparative efficacy, or superiority. Published ACS reference limitations, including its documented unauthenticated wire and configurable/default decision-failure posture, remain part of the comparator.

## OWASP Top 10 for Agentic Applications 2026 — verified threat baseline

Source: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

Published 2025-12-09. OWASP describes it as a peer-reviewed risk framework for autonomous/agentic systems, developed with more than 100 experts, researchers and practitioners. It is a threat/mitigation baseline, not a containment implementation or efficacy benchmark.

Use in SBCF: map the C2 adversarial threat model and negative test catalog to the relevant agentic risk categories. Do not claim benchmark parity from taxonomy coverage alone.

## Cisco Zero Trust for Agentic AI — verified architecture baseline

Source: https://www.cisco.com/c/en/us/solutions/collateral/artificial-intelligence/security/zero-trust-agentic-ai-wp.html
Document updated 2026-03-23.

Cisco frames the architecture around three continuous pillars: know every agent, authorize every action, and adapt to risk in real time. The published design includes NHI discovery/ownership, least-privilege and time-bound authorization, runtime behavioral/semantic inspection, and inline blocking, privilege revocation or isolation across identity, network and application layers.

Minimum SBCF comparator requirement: explicit agent identity/ownership, authorization per action, runtime behavioral inspection that cannot itself grant authority, and enforceable block/revoke/isolate outcomes outside the agent's own reasoning loop.

Current SBCF result: NOT PRODUCT/DEPLOYMENT PARITY. SBCF currently tests synthetic authority and evidence contracts; it has no enterprise NHI lifecycle, network enforcement, integrated identity provider, or deployed real-time isolation plane.

## LLM Agent Honeypot — verified monitoring precedent, not containment baseline

Source: https://arxiv.org/abs/2410.13919
Reworr and Dmitrii Volkov, first submitted 2024-10-17.

The paper augments an SSH honeypot with prompt injection and time-based analysis to identify potential autonomous AI hacking agents in public attack traffic. It reports a roughly three-month deployment with 8,130,731 hacking attempts and 8 potential AI agents.

Relevance to SBCF: semantic/behavioral observation precedent and adversarial monitoring evidence. It does not establish agent recapture, quarantine, capability revocation, safe-continuation efficacy, or containment convergence.

## BRaVeS / LBCF — verified peer-reviewed bounded-safety comparator

Sources:
- https://link.springer.com/article/10.1007/s10846-026-02467-w
- https://arxiv.org/abs/2610.08815

Published in Journal of Intelligent & Robotic Systems in September 2026. The work describes bounded autonomy with invariant anchors, a state hierarchy that reduces autonomy as epistemic risk rises, and the Lyapunov-Bounded Consensus Framework (LBCF). The authors explicitly bound the formal convergence result to a finite abstraction under fixed thresholds and feasible-shield assumptions; they do not claim proof over the full continuous neural activation space. Evaluation is discrete-event Monte Carlo simulation using industrial-control-system time-series data with synthetic noise/degradation.

Minimum SBCF comparator requirement: explicit safety-state abstraction, stated convergence assumptions, shield feasibility, finite-step or terminal escalation conditions, and matched simulation/adversarial tests if SBCF makes a comparable convergence claim.

Current SBCF result: NO FORMAL PARITY. SBCF finite-state enumeration verifies implementation properties only and is not a Lyapunov convergence proof.

## MARIS-TRA — verified temporal runtime-assurance comparator

Source: https://www.mdpi.com/2504-4990/8/9/293

The 2026 publication describes hierarchical temporal runtime assurance using a quantitative Signal Temporal Logic fragment, bounded predictive monitoring, deterministic repair over an explicit candidate library and hash-chained assurance certificates. Reported results are simulator/episode measurements, with explicit sensitivity to numerical semantics, model mismatch, hysteresis and safety/recovery conflicts.

Minimum SBCF comparator requirement: explicit temporal properties, monitor semantics, repair/escalation rules, reproducible scenario generation, matched baseline semantics, and sensitivity analysis before any comparative superiority claim.

Current SBCF result: NO TEMPORAL-RUNTIME PARITY. SBCF does not yet implement matched STL monitoring, predictive safety shielding, or an equivalent empirical benchmark.

## C1 disposition

Primary-source identity is now verified for OpenShell, OWASP ACS, OWASP Agentic Top 10, Cisco Zero Trust for Agentic AI, LLM Agent Honeypot, BRaVeS/LBCF and MARIS-TRA.

C1 remains OPEN. ACS has advanced from source verification to executable reproduction, but the other candidate baselines have not yet received matched implementation reproduction, and no cross-system SBCF comparison has been run. Before promoting any candidate to an empirical minimum benchmark:
1. pin exact version/commit/artifact;
2. identify executable implementation and license/access constraints;
3. define matching threat model and control surface;
4. reproduce its relevant reported behavior where feasible;
5. record first failure, environment, raw outputs and artifact hashes;
6. use equivalent semantics and workloads for SBCF;
7. obtain non-author review before comparative claims.

## Negative QA gate

Do not promote a benchmark candidate on title/abstract similarity, vendor language, source inspection, or taxonomy overlap. Primary-source inspection without implementation reproduction is only source verification. Inaccessible code, unmatched semantics, missing artifacts, or infeasible reproduction must remain explicitly NOT ESTABLISHED.

SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.
