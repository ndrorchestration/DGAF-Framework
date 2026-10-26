# PDMAL-GR — Discrete communication-delay robustness proposal (2026-10-26)

**Status: PROPOSAL / EXPLORATORY / NON-ADMITTED / NOT A PROTOCOL FREEZE.**

Source lineage: [PDMAL exploratory phase-drift issue #1511](https://github.com/ndrorchestration/DGAF-Framework/issues/1511), [canonical pilot protocol](PDMAL_EXPERIMENT_PROTOCOL.md), [current mathematical correction](../formalism/PDMAL_MATH_CORRECTION_2026-08-15.md), [Notion formalization record](https://app.notion.com/p/3bcf5bad238b8123accfd4fd94f169b0).

**Hard boundaries:** SCIENTIFIC_N_INCREMENT=0; PILOT_AUTHORIZATION=NOT_GRANTED; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; DGAF_V1_RELEASE=HOLD. No protected experimental candidate, unblinding, custody, registry or production route is altered.

## Scientific question and identity

Does the dodecahedral **proxy topology** differ from matched graph controls in phase-coherence loss, recovery, or long-lived lag under heterogeneous link delays, holding oscillator model and coupling budget fixed?

PDMAL is **Phi-Driven Multi-Agent Lattice**, not Phi-Driven Pentagonal Multi-Agent Lattice. The dodecahedral topology remains a candidate structural intervention; **PDMAL-D is not activated**. Neither symmetry, the golden ratio, spectral gap nor plastic constant establishes delay robustness. Phi is not a parameter in this delay model.

## Sandbox equation and assumptions

For receiver i: d(theta_i)/dt = omega_i + K / deg(i) * Σ_{j neighbor i} sin(theta_j(t − tau_ij) − theta_i(t)).

**Implementation:** `tools/pdmal/delay_sandbox.py`, exercised by `tests/test_pdmal_delay_sandbox.py` and the separate test-only Euler method-of-steps cross-check in `tests/test_pdmal_delay_oracle.py`.

- tau_ij denotes sender j to receiver i (directed), with tau_ij = integer_steps_ij × dt. Each graph edge can have different directional latencies.
- Fixed undirected simple graph, degree-normalized uniform coupling, fixed natural frequencies; initial negative-time history is constant.
- Explicit zero delay uses current RK4 stage; positive delay uses linearly interpolated **unwrapped** stored phase history.
- No noisy links, lost packets, dynamic tau, switched graphs, variable intrinsic frequency, real transport, task-success metric or safety control is implemented.
- This is an **uncertified numerical DDE approximation**. RK4 formal order can be reduced at delay/history discontinuities or by the interpolation; independently validate against a separate method-of-steps solver, including step-size convergence at fixed physical delays, before accepting transitions/bifurcation interpretations.

The code has **no benchmark runner, workflow, auto-generated scientific artifact, or dependency on experiments/pdmal_pilot**. The initial 19 contract tests passed locally on 2026-10-26. Exact-head CI subsequently passed the three Python matrix test jobs on commit `dffe4fea4dda2b24fd6e2ba8fdbff23d333e5bd6`; the aggregate Python workflow still failed on existing CI dependency advisories. The new independent-code-path Euler checks are *pending fresh exact-head CI*. These tests are not evidence of topology efficacy or authorized empirical observations.

## Prospective, unapproved experimental design

**Primary equal-budget comparators:** 20-vertex, 30-edge, degree-3 NetworkX dodecahedral graph; 20-vertex circular ladder; connected uniform random cubic graphs sampled independently for each graph-realization seed. Mark the degree-2 cycle as a separate unequal-budget sensitivity case. A complete graph is **not** a resource-matched primary null.

**Pre-register before comparative runs:**

1. Grid for K, fixed physical tau, homogeneous versus heterogeneous directional delay distributions, observation horizon and integration resolution.
2. Common perturbation seed across graph comparisons; independently sampled graph seeds nested within perturbation draws. Do not treat multiple disturbances on the same graph as independent graph replicates.
3. Initial-phase impulse, temporary frequency detuning and persistent frequency differences as distinct disturbance families. Then, in separate prospective amendments, noise, time-varying delay, packet loss, asymmetric weights, and graph switching.
4. Primary endpoint (e.g. integrated post-release 1 minus circular order parameter), secondary peak decoherence and **censored** sustained recovery time. Record never-recovered trials and non-recovery fraction. Do not compare recovered-only survivors.
5. Negative controls, graph fingerprinting, randomization/seed derivation, predeclared analysis lock, multiplicity procedure, clustered uncertainty/bootstrap over independent graph draws and disturbances, and independent reproduction procedure.

Order parameter measures oscillator coherence only. It is **not** semantic correctness, governance approval, real-agent coordination, task completion or PDMAL effectiveness. Describe local phase-lag patterns as potential cluster phenomena, not validated chimera states, until cluster diagnostic, basin sensitivity and stability criteria are fixed.

## Verification gates and development slices

- [x] Pure-standard-library isolated numerical implementation and local tests.
- [x] Local replay, global-phase-shift, equilibrium, zero-K analytic, explicit zero-delay, directed-input validation, and fixed-physical-delay refinement tests (19 local checks).
- [x] Earlier exact-head Python 3.10/3.11/3.12 configured test jobs passed at `dffe4fea4d`; aggregate Python workflow remains FAIL on existing locked dependency vulnerabilities.
- [ ] Verify latest head including separate test-only Euler oracle, all security checks, and negative-case adequacy.
- [x] Implement a **same-system**, algorithmically separate explicit-Euler method-of-steps reference with physically fixed directed delays (0.04–0.12 s), constant negative-time history, 0.0005-s reference integration, 0.8-s endpoint, and <0.001-radian maximum terminal-phase agreement tolerance against RK4 (0.02-s step). These are prespecified numerical checks, not external validation.
- [ ] Obtain **external, non-author** independent DDE solver reproduction and tolerances, including convergence at the delay/history junctions.
- [ ] Create independently reviewed prospective benchmark fixtures, graph and perturbation seed hierarchy, negative controls and primary-analysis/censoring protocol.
- [ ] Run any comparative synthetic experiment only under its explicit new exploratory authorization, never under the canonical PDMAL pilot identity or empirical N.
- [ ] Specify operational mapping for real agent phase, transport latency, queueing/retries, semantics, success/failure and governance boundaries before claiming real-world transfer.

**Slice A:** This sandbox + contract tests + proposal. **Slice B:** independent numerical oracle, sensitivity and fixture receipts. **Slice C:** external preregistration and equal-budget baseline generator/analysis lock. **Slice D:** isolated synthetic replication under separately approved scope. **Slice E:** real-world transport and agent-runtime mapping. No efficacy or pilot admission is inferred at any slice.

**Falsification priority:** seek matched parameters under which the dodecahedral graph fares *worse*; do not select only favorable recoveries.

## Peer-reviewed foundations (background only; no validation of this sandbox)

- Yeung & Strogatz (1999), *Time Delay in the Kuramoto Model of Coupled Oscillators*, Physical Review Letters: [DOI](https://doi.org/10.1103/PhysRevLett.82.648)
- Earl & Strogatz (2003), *Synchronization in Oscillator Networks with Delayed Coupling: A Stability Criterion*, Physical Review E: [DOI](https://doi.org/10.1103/PhysRevE.67.036204) . Its assumptions do not imply blanket stability for heterogeneous directed delays.
- Pecora & Carroll (1998), *Master Stability Functions for Synchronized Coupled Systems*, Physical Review Letters: [DOI](https://doi.org/10.1103/PhysRevLett.80.2109) . Applicability depends on the system and coupling assumptions.

## Numerical-solver independent replication gate — source-backed update

**Same-author oracle limitation:** `tests/test_pdmal_delay_oracle.py` uses explicit Euler with a constant negative-time history and integer grid-aligned delays. Agreement with the RK4 sandbox at one 0.8-second endpoint cannot prove solution accuracy, correct propagation of history discontinuities, fourth-order RK accuracy, or absence of numerical bifurcations.

- [Shampine & Thompson (2001), Solving DDEs in Matlab](https://doi.org/10.1016/S0168-9274(00)00055-6) addresses DDE error estimation, short-delay handling and discontinuity tracking. Independent review must test those properties before scientific interpretation.
- [Bellen & Zennaro (2003), Numerical Methods for Delay Differential Equations](https://doi.org/10.1093/acprof:oso/9780198506546.001.0001) treats continuous extensions, delayed history and convergence. Simple RK4 plus linear history interpolation should not be assigned a global method order without analysis.
- [Fujii et al. (2026), Emergence of higher-order interactions in systems of coupled Kuramoto oscillators with time delay](https://doi.org/10.1103/s2n5-4ps2), peer-reviewed Physical Review E (2026-07-15), derives effective higher-order interactions under a particular expansion. For the proposed PDMAL comparison, delay-related behavior may not be attributable to topology alone; this is a **mechanistic hypothesis and possible confound**, not a finding about this sandbox.

**No-cost, independently maintained numerical cross-check candidates (NOT installed or executed here):**

- [Python JiTCDDE](https://jitcdde.readthedocs.io/en/latest/), open-source adaptive DDE solver with cubic-Hermite history reconstruction, or
- [Julia SciML DDEProblem + MethodOfSteps(Tsit5())](https://docs.sciml.ai/DiffEqDocs/dev/tutorials/dde_example/).

An eligible non-author should independently implement the fixed input fixture and verify recorded source/environment versions, directed lag orientation, historical phase inputs, sampled trajectory and full-trajectory error against an external solver. Include discontinuity-adjacent checkpoints and time-step refinement, predeclare acceptance bounds, and retain raw comparison failures. Do not promote the separately coded same-system Euler method to **independent scientific verification**.

## Structural comparator fixture implementation — NON-ADMITTED

**Source:** `tools/pdmal/comparator_fixtures.py`; `tests/test_pdmal_comparator_fixtures.py`. This module constructs and fingerprints candidate comparison graphs but does **not** simulate oscillators, sample phase/noise outcomes, select a winner, or increment empirical N. The work is software design and graph-structure validation; its tests require fresh CI after the new commit.

- The dodecahedral proxy reuses the repository-owned `DODECAHEDRAL_EDGES` constant, never a substituted or re-labeled topology.
- The 20-node circular ladder consists of two 10-cycles and ten rungs. Each comparator has exactly 20 labeled vertices, 30 distinct undirected edges, degree 3 at every vertex, no loops and connectedness.
- The random connected cubic control uses uniform randomly permuted degree-three stubs, rejecting loops, parallel edges, and disconnected graphs. Every *labeled simple 3-regular graph* has precisely `(3!)**20` corresponding stub matchings, so conditional rejection preserves uniformity over the *connected labeled simple cubic* sample space, assuming an unbiased PRNG shuffle. This does **not** produce a uniform distribution over unlabeled isomorphism classes. If `max_attempts` is exhausted, it raises rather than silently returning a biased fallback.
- Graph identifiers are SHA-256 of a versioned, sorted **labeled edge list**. These fingerprints track fixture identity, not structural graph-isomorphism class, spectral features, security authenticity or independent validation.
- `derive_seed(master_seed, domain, index)` uses domain-separated SHA-256 derivation for `graph` and `perturbation` pseudo-random seed namespaces. Distinct derived integers do not themselves prove statistical independence; independent graph realizations and perturbation sampling must still be prospectively reviewed before experiments.
- **No experimental configuration is admitted:** coupling/delay grids, graph seeds, perturbation seeds, outcome definitions, blinding and confidence intervals remain unapproved. A graph being degree-3/30-edge matched is *not* proof that all communication cost, distances or dynamical properties are matched.

**Gate:** review this structural generator and its sampling semantics independently before locking a prospective comparator manifest or running phase-drift trials. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.
