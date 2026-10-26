# PDMAL-GR — Discrete communication-delay robustness proposal (2026-10-26)

**Status: PROPOSAL / EXPLORATORY / NON-ADMITTED / NOT A PROTOCOL FREEZE.**

Source lineage: [PDMAL exploratory phase-drift issue #1511](https://github.com/ndrorchestration/DGAF-Framework/issues/1511), [canonical pilot protocol](PDMAL_EXPERIMENT_PROTOCOL.md), [current mathematical correction](../formalism/PDMAL_MATH_CORRECTION_2026-08-15.md), [Notion formalization record](https://app.notion.com/p/3bcf5bad238b8123accfd4fd94f169b0).

**Hard boundaries:** SCIENTIFIC_N_INCREMENT=0; PILOT_AUTHORIZATION=NOT_GRANTED; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; DGAF_V1_RELEASE=HOLD. No protected experimental candidate, unblinding, custody, registry or production route is altered.

## Scientific question and identity

Does the dodecahedral **proxy topology** differ from matched graph controls in phase-coherence loss, recovery, or long-lived lag under heterogeneous link delays, holding oscillator model and coupling budget fixed?

PDMAL is **Phi-Driven Multi-Agent Lattice**, not Phi-Driven Pentagonal Multi-Agent Lattice. The dodecahedral topology remains a candidate structural intervention; **PDMAL-D is not activated**. Neither symmetry, the golden ratio, spectral gap nor plastic constant establishes delay robustness. Phi is not a parameter in this delay model.

## Sandbox equation and assumptions

For receiver i: d(theta_i)/dt = omega_i + K / deg(i) * Σ_{j neighbor i} sin(theta_j(t − tau_ij) − theta_i(t)).

**Implementation:** tools/pdmal/delay_sandbox.py, exercised by tests/test_pdmal_delay_sandbox.py.

- tau_ij denotes sender j to receiver i (directed), with tau_ij = integer_steps_ij × dt. Each graph edge can have different directional latencies.
- Fixed undirected simple graph, degree-normalized uniform coupling, fixed natural frequencies; initial negative-time history is constant.
- Explicit zero delay uses current RK4 stage; positive delay uses linearly interpolated **unwrapped** stored phase history.
- No noisy links, lost packets, dynamic tau, switched graphs, variable intrinsic frequency, real transport, task-success metric or safety control is implemented.
- This is an **uncertified numerical DDE approximation**. RK4 formal order can be reduced at delay/history discontinuities or by the interpolation; independently validate against a separate method-of-steps solver, including step-size convergence at fixed physical delays, before accepting transitions/bifurcation interpretations.

The code has **no benchmark runner, workflow, auto-generated scientific artifact, or dependency on experiments/pdmal_pilot**. Locally, 19 software contract checks were executed on 2026-10-26. They are not evidence of topology efficacy or authorized empirical observations. New-PR exact-head CI is a separate, currently unfulfilled check.

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
- [ ] Independently verify branch exact-head tests in CI; inspect scope and negative-case test adequacy.
- [ ] Independently cross-check the DDE solver on matched physical time/delay against a second implementation and documented numerical tolerances.
- [ ] Create independently reviewed prospective benchmark fixtures, graph and perturbation seed hierarchy, negative controls and primary-analysis/censoring protocol.
- [ ] Run any comparative synthetic experiment only under its explicit new exploratory authorization, never under the canonical PDMAL pilot identity or empirical N.
- [ ] Specify operational mapping for real agent phase, transport latency, queueing/retries, semantics, success/failure and governance boundaries before claiming real-world transfer.

**Slice A:** This sandbox + contract tests + proposal. **Slice B:** independent numerical oracle, sensitivity and fixture receipts. **Slice C:** external preregistration and equal-budget baseline generator/analysis lock. **Slice D:** isolated synthetic replication under separately approved scope. **Slice E:** real-world transport and agent-runtime mapping. No efficacy or pilot admission is inferred at any slice.

**Falsification priority:** seek matched parameters under which the dodecahedral graph fares *worse*; do not select only favorable recoveries.

## Peer-reviewed foundations (background only; no validation of this sandbox)

- Yeung & Strogatz (1999), *Time Delay in the Kuramoto Model of Coupled Oscillators*, Physical Review Letters: [DOI](https://doi.org/10.1103/PhysRevLett.82.648)
- Earl & Strogatz (2003), *Synchronization in Oscillator Networks with Delayed Coupling: A Stability Criterion*, Physical Review E: [DOI](https://doi.org/10.1103/PhysRevE.67.036204) . Its assumptions do not imply blanket stability for heterogeneous directed delays.
- Pecora & Carroll (1998), *Master Stability Functions for Synchronized Coupled Systems*, Physical Review Letters: [DOI](https://doi.org/10.1103/PhysRevLett.80.2109) . Applicability depends on the system and coupling assumptions.
