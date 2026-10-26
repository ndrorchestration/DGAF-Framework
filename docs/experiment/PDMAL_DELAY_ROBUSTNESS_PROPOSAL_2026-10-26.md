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

The code has **no benchmark runner, workflow, auto-generated scientific artifact, or dependency on experiments/pdmal_pilot**. The initial 19 contract tests passed locally on 2026-10-26. Exact-head CI subsequently passed the three Python matrix test jobs on commit `dffe4fea4dda2b24fd6e2ba8fdbff23d333e5bd6`; the aggregate Python workflow still failed on existing CI dependency advisories. The separate same-author Euler checks were pending at this historical early checkpoint; later exact-head CI evidence is recorded in the addenda below. These tests are not evidence of topology efficacy or authorized empirical observations.

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

## Labeling and disturbance-placement guard — structural implementation only

The exploratory branch adds `label_permutation(master_seed, arm, replicate)`, `relabel_cubic_graph`, `relabel_vertex_values` and `relabel_directed_delays` to `tools/pdmal/comparator_fixtures.py`. This implements the previously identified risk that equal-node/equal-edge baselines can still be biased by node labeling and unequal perturbation locations.

- Per-arm, per-replicate **old-to-new** vertex label maps are generated from a separate `label` pseudo-random seed domain. Label maps are required to be exact bijections over 0–19, and normalized graphs are rechecked for degree, edge budget, loops, duplicates and connectedness.
- For the same physical system, `relabel_vertex_values` carries phase and frequency inputs to the new node indices; `relabel_directed_delays` maps each *(receiver,sender)* delay pair without silently swapping direction.
- `tests/test_pdmal_comparator_fixtures.py` adds bijection/inverse tests, invalid-map and invalid-domain failures, directed-delay orientation tests and a **metamorphic test**: identical delayed-oscillator dynamics must be reconstructed after a permutation on a *single dodecahedral graph*, provided every node attribute and directed lag is transformed consistently. This is an invariance check, not a comparative trajectory run or evidence that the dodecahedron is more robust.
- A shuffled label is **not** a structurally comparable node location between non-isomorphic graphs; randomizing labels alone cannot control betweenness, graph distance, intervention exposure or disturbance placement. A future scientific protocol must preregister how target nodes/edges are drawn or stratified, and report mapping receipts, conditioning rules and nested uncertainty.
- Python's `random.Random` shuffle is a deterministic PRNG convenience, not a cryptographically secure draw nor a cross-version immutable sampling guarantee. Any *authorized* prospective work should freeze interpreter version, seed derivation, graph fingerprints and exact maps before evaluating any outcome.
- **No experimental seeds, participant data, oscillator efficacy outcomes or primary analysis were collected** by the fixture helpers. New exact-head CI verification is pending at the moment this section is authored. `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `PILOT_AUTHORIZATION=NOT_GRANTED`; `DGAF_V1_RELEASE=HOLD`.

## Separating reindexing invariance and randomized disturbance placement

**Scientific correction:** A simultaneous node-label permutation of the graph, phase states, natural frequencies and directed delay keys leaves the *same physical graph intervention at the same structural vertex*. It is useful as a **metamorphic software test**, but it is **not** a randomization of disturbance exposure or a fairness adjustment among non-isomorphic graph arms. The earlier draft's description of distinct arm streams as *preventing reuse of a chosen source vertex* overclaimed what distinct PRNG seeds guarantee: equal-site or equal-number collisions remain possible.

An isolated `prospective_perturbation_vertex(master_seed, arm, replicate)` helper now selects a **source-label index uniformly from 0–19**, using a domain-separated `placement` pseudorandom stream independent in *derivation* from the existing `label` stream. A selected source vertex `v` maps to new index `label_permutation(...)[v]` when the graph and all attributes are simultaneously relabeled; that transformation is still the **same graph location**. These functions create only deterministic test fixtures and do **not** dispatch delayed oscillators or generate scientific observations.

**Before any synthetic experiment may be authorized**, reviewers must specify whether intervention sites will be sampled uniformly over physical vertices, stratified by structural features, exhaustively blocked by vertex (possible for twenty nodes), or modeled hierarchically. For each arm, predeclare and retain: source graph fingerprint, original site, node relabeling map, mapped site, relevant shortest-path/centrality descriptors, pairing and seed hierarchy, and a non-pseudoreplicated uncertainty plan. Different seeded streams do not prove statistically independent realizations; do not equate equal-degree graphs with equal latency distances or disruption exposure. The unit checks of this helper establish neither selection fairness nor any outcome advantage.

**Status:** source-level correction implemented on draft #1518; exact-head CI for the placement addition still required. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## Structural site exposure: topology-only shortest-path profile

To make site-allocation designs reviewable before any dynamical study, `structural_distance_profile(edges, source_vertex)` constructs the sorted multiset of 20 **unweighted shortest-path distances from a source vertex**. This is a graph-geometric descriptor, **not** an outcome measure, experimental observation, confidence interval, transport latency, spectral gap, causal effect or scientific N increment.

- `tests/test_pdmal_comparator_fixtures.py` uses the source vertex sampled by the separate placement domain, maps it through the arm's bijective label permutation, and asserts the profile is **identical after simultaneously relabeling the same graph and its site**. Tests also reject boolean, out-of-range and noninteger vertex references. These are input/invariance correctness checks.
- The descriptor can later support external review of within-graph vertex blocking or structural site stratification, but equality of graph-distance distributions does not by itself match queueing delays, network congestion, local clustering, dynamic influence, or physical communications cost.
- When producing an **authorized and separately preregistered** experiment, record both the source and mapped site and the associated exact **graph** fingerprint. Retain the unrelabeled source vertex rather than mistaking a new label for a new physical intervention.
- No comparative phase-drift runs, benchmarks, scientific statistics or pilot data are generated by this helper. The exact source branch requires fresh CI on the new head. `SCIENTIFIC_N_INCREMENT=0`; `PILOT_AUTHORIZATION=NOT_GRANTED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `DGAF_V1_RELEASE=HOLD`.

## Free SciPy numerical cross-check — author-operated, non-admitted

**New optional probe:** `python -m tools.pdmal.scipy_reference_probe`, requiring SciPy only if explicitly invoked. It imports the actual `tools.pdmal.delay_sandbox.simulate_delayed_kuramoto`, segments the fixed four-node case into 0.02-second method-of-steps intervals shorter than its shortest nonzero delay (0.04 seconds), and uses SciPy's **maintained DOP853 ODE integrator** for each interval. The delay-history orchestration is **locally authored**, NOT an independently maintained DDE solver, independent scientist, scientific review or production implementation. No mandatory dependency or signed lock was edited.

**Pre-commit local reference experiment (2026-10-26):** In an isolated analysis container running Python 3.13.5 and SciPy 1.17.0, a separately transcribed copy of the repository's numerical RK4 algorithm was compared against this type of DOP853 method-of-steps reference on the fixed four-node `tests/test_pdmal_delay_oracle.py` fixture: K=1.1, directed delays of 0.04–0.12 s, history equal to initial state before t=0, horizon 0.8 s. DOP853 controls: relative tolerance 1e-11, absolute tolerance 1e-13, segments 0.02 s. A second reference with 0.01-s segments and tighter tolerances (1e-12, 1e-14) differed by at most ~1.33e-15 rad across the shared output grid in this short fixture.

| Sandbox step (s) | Maximum sampled-trajectory absolute phase discrepancy to SciPy reference (rad) |
| --- | ---: |
| 0.0200 | 4.400366e-6 |
| 0.0100 | 1.100079e-6 |
| 0.0050 | 2.750189e-7 |
| 0.0025 | 6.875467e-8 |

All reported values are from the **local source-algorithm transcription**, not yet from a successfully executed checkout of the repository's new opt-in probe. **Do not label the new module itself verified until an exact-source run is captured.** The approximately fourfold decrease on halving dt is **compatible with second-order leading error** on this fixture; despite RK4 staging, linear historical interpolation and propagated delay/history nonsmoothness can lower the overall order. This is **not** a proof of global order, stability, accuracy under other parameter sets, or delayed-network bifurcation behavior. The original fixture only crosses a short set of directed positive delays; failures near more complex discontinuity structures remain untested.

**Source evidence needed next:** execute the new opt-in probe from the exact `PR #1518` checkout, preserve its JSON output, numerical tool versions, SHA-256 of `delay_sandbox.py`, code commit, exact source hashes and negative findings. Seek a **non-author maintained DDE implementation and independently controlled reviewer** via [#1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521) before claiming independent solver validation. Never silently promote SciPy-maintained ODE integration to an independent DDE solver, nor numerical consistency to empirical PDMAL advantage.

**No comparative oscillator topology trial or governed pilot execution:** `SCIENTIFIC_N_INCREMENT=0`; `PILOT_AUTHORIZATION=NOT_GRANTED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Executed exact-source SciPy probe + fail-closed reproducibility gate

**Source provenance:** the Python source for `tools/pdmal/delay_sandbox.py` and the original `tools/pdmal/scipy_reference_probe.py` was retrieved from draft [PR #1518](https://github.com/ndrorchestration/DGAF-Framework/pull/1518) head `e748aba9690a2ed8fadd46ddaec312bfa214f9ec`, reconstructed in an isolated execution directory, and independently compared **byte-for-byte through each original Git blob SHA-1** (`7a0bc7d0ad69dd5d81cf1d1ac51ea021034a051d`, `09eedf832d79ae8b8d2848fb4849073ff2a7d75f`). No source algorithm had to be retyped or approximated for this latest run.

**Execution:** `python -m tools.pdmal.scipy_reference_probe` ran successfully in a no-cost isolated Python 3.13.5 / SciPy 1.17.0 environment. The DOP853 integration core is SciPy-maintained; the *method-of-steps DDE history, directed-delay lookup, segmentation and comparison logic remain author-coded*. **This does not meet the independent DDE solver or non-author review gates.** No oscillator graph comparisons or scientific outcomes were produced.

- Reference: fixed 4-node graph, directed positive delays 0.04–0.12 s, coupling 1.1, constant negative-time phase, horizon 0.8 s, segments of 0.02 s versus 0.01 s; DOP853 tolerance pair 1e-11/1e-13 (and tighter 1e-12/1e-14 refinement).
- Local reference-segment refinement max phase difference: **1.33226762955e-15 radians** on matched sample points, only a narrow numerical self-consistency indicator.
- Sandbox RK4 versus SciPy-author-history full-trace max unwrapped phase errors: `dt=0.02: 4.40036605115e-6`; `0.01: 1.10007862555e-6`; `0.005: 2.75018869372e-7`; `0.0025: 6.87546688749e-8` radians. Observed consecutive halving ratios approximately **4.000047, 4.000011 and 4.000003**, *compatible* with second-order leading global error on this specific fixture (likely limited by linearly interpolated history), **not a proof of solver order or physical robustness**.

**Evidence-integrity defect corrected:** the original optional probe rounded `HORIZON / segment` without checking exact divisibility and used `zip` when comparing phase vectors without validating equal dimensions. This could silently accept an unintended terminal time or truncated vector comparison if manually modified. The new `validate_reference_grid` rejects non-finite, nonpositive or bool-valued settings, segments longer than the shortest positive delay, and segments that do not evenly divide the horizon and all positive physical delays. `_max_phase_difference` fails closed for mismatched, empty or nonfinite vectors. The run receipt now includes SHA-256s of the sandbox file, probe file and canonical serialized fixture, along with segment metadata and measured error ratios.

**New test gate:** `tests/test_pdmal_scipy_reference_probe.py` runs **20 standard-library-only/pytest parameter checks**, passed locally before commit; the file is designed to run without SciPy in Python 3.10/3.11/3.12 CI. This does not cause CI to execute SciPy or assert DDE scientific validation. After this documentation commit, **fresh exact-head CI must be checked independently** before reporting a passing repository gate.

External, independently maintained DDE code and non-author reproduction remain requested by [issue #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521). Do not merge the exploratory PR, change the canonical pilot, unblind, run an efficacy comparison, or reinterpret any software numerical receipt as permission for scientific N. **SCIENTIFIC_N_INCREMENT=0 · PILOT_AUTHORIZATION=NOT_GRANTED · INDEPENDENT_VALIDATION=NOT_ESTABLISHED · DGAF_V1_RELEASE=HOLD.**

## 2026-10-26 — Optional JiTCDDE handoff adapter (unexecuted, external DDE library)

**New source:** `tools/pdmal/jitcdde_reference_probe.py` plus `tests/test_pdmal_jitcdde_reference_probe.py`. This is an **author-built adapter** for an independently maintained **DDE** solver library, not a non-author implementation or external reviewer. It is opt-in only: `python -m tools.pdmal.jitcdde_reference_probe`. No dependency lock, CI workflow, governed pilot, registry or production runtime imports the optional JiTCDDE package.

**What is fixed and what is not:** the adapter reuses the registered 4-node 5-edge, 5-directed-delay fixture from `scipy_reference_probe.py`, with K=1.1, constant pre-zero history, 0.8-s horizon and 0.02-s output grid. All oriented keys are explicitly *(receiver, sender)*; an unspecified direction means zero delay. The equation is assembled symbolically using JiTCDDE's `y(index, t-lag)` and `sin`, while zero-lag edges use `y(index)`. Its initial derivative-history discontinuity needs special handling.

**Documented discontinuity approach:** JiTCDDE's `step_on_discontinuities` can advance the solver past early requested checkpoints; this would prevent a complete t=0 through 0.8-s sampled trace. Instead the adapter retains constant negative-time history, uses `integrate_blindly` at 0.001-s fixed steps for each requested sample up to the maximum 0.12-s positive delay, then invokes adaptive `integrate` thereafter. The fixed blind integration may introduce its own early-history discretization error; the 0.001-s bootstrap resolution is a **proposed initial choice, not validated accuracy**. A prospective independent reviewer must repeat it with finer bootstrap resolutions and report discontinuity-adjacent discrepancies, not silently discard early samples. Source references: [JiTCDDE documentation](https://jitcdde.readthedocs.io/en/latest/) (constant past, initial derivative discontinuities, blind integration).

**Receipt/QA behavior:** `fixture_manifest()` yields a canonical machine-readable input description; `validate_fixture()` fails closed on the wrong graph, nonpositive/misaligned positive link delays or a non-divisible observation grid. `build_symbolic_rhs` has a solver-free numerical substitution test to check sender/receiver orientation and zero-delay default. Only successful execution with the maintained external package should yield a JSON receipt including package versions, input/source SHA-256 hashes, a complete 41-state unwrapped trajectory, per-sample and maximum phase discrepancies against the sandbox, and explicit scientific custody limits.

**Actual execution blocker at this checkpoint:** JiTCDDE and SymEngine were not installed in the isolated local runtime. Installing from the package index failed because DNS resolution was unavailable, and the previously paired remote Windows desktop remains at its Desktop Commander remote-call usage limit. **No maintained-DDE solver run and no external-replication result exist yet.** The optional adapter and its Python-only tests require exact-head GitHub static and regression checks before claiming software verification.

The issue [#1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521) retains its requirement for a **non-author**, independently controlled DDE reproduction, with input custody, solver versions, trajectory and discontinuity-adjacent failures. A future successful author-run JiTCDDE execution would verify only the bridge's bounded numerical behavior, **not** fulfill that independence requirement. No comparative topology data or empirical N; `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Runtime fixture custody and fake-solver scheduling checks

The opt-in JiTCDDE bridge now enforces a fixed **canonical JSON fixture SHA-256** (`9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15`) **before** importing or running the optional external solver. The earlier test-only pinned hash did not constrain the executable command: modifying model inputs could have created a newly hashed, superficially legitimate receipt. `validate_fixture()` now checks finite phase/frequency/coupling values, strictly positive and finite grid/horizon/bootstrap/adaptive stepping settings, exact delay/horizon alignment, and the pinned digest. Prospective fixture changes require a reviewed protocol version rather than silently changing the reference.

Sampling logic has been moved into `collect_reference_trajectory(solver, n_samples)`, which can be exercised using a fake, in-process solver. New contract tests verify **exactly 41 states** at t=0…0.8 s in 0.02-s increments, six `integrate_blindly` calls at t=0.02…0.12 s, and 34 `integrate` calls at t=0.14…0.8 s. The fake-solver test also rejects non-finite and wrong-dimension outputs, invalid sample counts, out-of-range parameters and an altered canonical fixture. It provides **no information about actual JiTCDDE numerical integration, delayed-history correctness, convergence, runtime package compatibility, independent scientific validation or topology performance**.

The CI status of this source change must be established against its final exact Git commit, not copied from the earlier `dcc76583` tests. A successful fake-solver test establishes a narrow *API-call sequence contract only*. The maintained solver remains **unexecuted here** because the local JiTCDDE dependency is absent and the RDC remote-command quota is exhausted. This work does not change the signed CI locks, protected canonical pilot, statistical N, scientific claims, or admission controls: `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

