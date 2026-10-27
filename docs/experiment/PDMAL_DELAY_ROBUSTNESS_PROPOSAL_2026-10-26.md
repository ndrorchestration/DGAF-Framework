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

## 2026-10-26 — First executed maintained-DDE trajectory and bounded diagnostic plan

**Actual execution:** the public research-only workflow [run #40331892261](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40331892261) succeeded using JiTCDDE 1.8.3, SymEngine 0.14.1, SymPy 1.14.0, Python 3.11.17 and a single 4-node fixture. Artifact ID **12653344866** contains 41 unwrapped phase states, exact Git commit, source SHA-256 hashes, canonical fixed-fixture SHA-256 and a captured `pip freeze`. A prior run [#40331532525](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40331532525) failed with **ModuleNotFoundError: sympy** in JiTCDDE code generation/fallback; pinning SymPy in the isolated optional job resolved that dependency failure. Neither attempt touched production dependency locks or the canonical pilot.

**Measured numerical discrepancy, not accuracy proof:** the JiTCDDE trajectory versus isolated source RK4 at dt=0.02 has **maximum 2.04361646970e-4 rad at t=0.02** and **terminal 1.27856743452e-4 rad at t=0.8**. Against a separately author-coded SciPy DOP853 method-of-steps reference on the identical graph/physical delay fixture, the JiTCDDE run differs by **2.04361651648e-4 rad at t=0.02** and **1.26347482003e-4 rad at t=0.8**. Thus most of the discrepancy arises immediately in the first observation interval; it is **not explained by the sandbox's previous 4.400366e-6 rad maximum SciPy deviation alone**. It remains unknown which source of error dominates. JiTCDDE `integrate_blindly` deliberately ignores adaptive accuracy/error criteria around the initial derivative discontinuity. Its actual bootstrap behavior and initial-history representation require investigation before establishing a toleranced cross-solver acceptance criterion.

**Prospectively declared engineering sensitivity check (NOT experimental N):** run identical physical model and complete 41-state observation grid at three blind-bootstrap step sizes **0.001, 0.0005, 0.00025 s**, using adaptive integration only after the fixed 0.12-s bootstrap cutoff. Report the full per-time JiTCDDE trajectories, each variant's own canonical parameter hash (the numerical bootstrap step is an explicitly changed numerical control), largest / first / final discrepancy versus the fixed sandbox, and pairwise maximum variant divergence. Do not select a favorite or silently rewrite the frozen 0.001-s nominal fixture; no graph arm is compared, no pilot is run, no scientific sample is collected. Finer bootstrap steps are a bounded reproducibility diagnostic, not independent reviewer validation or a proof of convergence. Preserve failed configurations and exact environment/tool versions.

**Evidence ceiling:** this was an author-directed, GitHub-hosted maintained-DDE *library* run, not an independently designed non-author model reproduction. Independent issue [#1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521) remains open. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Executed numerical bootstrap sensitivity: first-order limitation observed

The separately specified, **author-operated and NON-ADMITTED** [GitHub sensitivity run #40332974545](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40332974545) **SUCCESSFULLY EXECUTED** the fixed four-node model using JiTCDDE 1.8.3 at blind-bootstrap step sizes 0.001, 0.0005 and 0.00025 s, holding physical directed delays, graph, frequencies, coupling, horizon, and observation grid identical. [Artifact #12656131084](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40332974545/artifacts/12656131084) includes each variant's own manifest SHA-256, complete 41-point unwrapped phase trajectory, actual runtime environment and exact source commit identity. No statistically independent graphs or scientific efficacy observations were generated.

**Full-trajectory maximum absolute difference against the unchanged dt=0.02 RK4 sandbox:**

- 0.001 s blind step: **0.0002043616469702969 radians**; first 0.02-s sample is the maximum; terminal discrepancy **0.00012785674345205944 rad**.
- 0.0005 s blind step: **0.00010217622798369685 radians**; first sample maximum; terminal **0.0000646814711569299 rad**.
- 0.00025 s blind step: **0.000051086965340840784 radians**; first sample maximum; terminal **0.00003309498316683701 rad**.

**Maximum full-trace intervariant differences:** 0.001 versus 0.0005 s = **0.00010218541898660005 rad**; 0.0005 versus 0.00025 s = **0.00005108926264285607 rad**; 0.001 versus 0.00025 s = **0.00015327468162945612 rad**. Halving the blind-bootstrap step approximately halves the dominant discrepancy, **compatible with first-order bootstrap discretization error on this one four-node fixture**. It is not a general theorem of order or an independently validated true-solution error bound. In particular, the comparison baseline itself has a previously measured small nonzero discrepancy from the author-coded SciPy/DOP853 reference. Neither source is to be declared ground truth.

**Engineering consequence:** a successful JiTCDDE job that merely checks receipt shape is insufficient for an accuracy claim. The 0.001-s blind-bootstrap reference must be labeled **numerically resolution-sensitive**, and any future accepted cross-solver tolerance must be defined only after independent DDE validation of initial-history/discontinuity behavior, more than one resolution and adverse cases. The test did not establish topology robustness, chimera states, runtime governance correctness or scientific efficacy. External non-author DDE replication remains open [#1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521), pilot authorization remains NOT_GRANTED, `SCIENTIFIC_N_INCREMENT=0`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, and `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Alternative discontinuity-aligned JiTCDDE on late common grid

The independent-maintainer JiTCDDE 1.8.3 library was executed a second way under the **same author-directed isolated research workflow**, using `step_on_discontinuities(propagations=1)` rather than the previous `integrate_blindly` startup. [Actual successful run #40358127422](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40358127422), source commit `28ebbb33e5d48bd8bb863e2a10d8e87f539a8215`, [artifact #12666278250](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40358127422/artifacts/12666278250) contains `discontinuity-alignment.json`, `bootstrap-sensitivity.json`, the original full 41-state nominal receipt, source SHA-256s and environment freeze. All use the same frozen four-node graph and input SHA-256 `9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15`. This is a numerical diagnostic, **NOT independent non-author review**.

**Important sampling ceiling:** `step_on_discontinuities(propagations=1)` first advanced the JiTCDDE integrator to **t = 0.40 s**. The implementation deliberately omitted, rather than interpolated or fabricated, the **20 observation grid states t = 0.02 through 0.40 s**. Only **20 paired late grid samples t = 0.42 through 0.80 s** are comparable. This does **not** constitute a complete 41-state DDE replication and cannot establish agreement near the initial derivative discontinuity.

On these late common samples, the **maximum phase deviation from the existing RK4(dt=0.02) sandbox was `4.4003696098582346e-6` radians**, occurring at the final t=0.80 s sample. The maximum deviation against JiTCDDE's same-run fine **0.00025-s blind-bootstrap** trajectory was **`4.0348920213276185e-5` radians**, at the first comparable t=0.42 s sample. The terminal difference to fine bootstrap was **`3.158567606684204e-5` radians**. For orientation, the separate author-coded SciPy/DOP853 method-of-steps check previously differed from RK4 by a similar ~`4.400366e-6` rad **on its own full grid**; these observations are consistent but do not identify which numerical method is correct.

**Interpretation:** the strong late-time agreement and previously measured ~2× blind-bootstrap error reduction for each bootstrap-step halving reinforce the **hypothesis** that initial-discontinuity/bootstrap treatment materially contributes to the cross-solver mismatch. No general convergence order, reliable early-time accuracy tolerance, physical system claim, topology superiority or governance efficacy follows. Prospective external validation must reproduce the derivative-history setup independently and provide an early-time method retaining all requested points, additional adverse/discontinuous fixtures, numerical convergence studies and non-author source provenance. See [external reviewer gate #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521).

The optional workflow was repaired after a malformed YAML source-guard edit and verified through the actual hosted GitHub Actions execution. The exact source-branch guard ensures current-workflow changes can run the numerical diagnostic; later documentation-only PR synchronizations skip package installation and integration. The separate signed-lock `pip-audit` CI failure remains unwaived. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## Research workflow scope correction

The optional solver workflow originally attempted to suppress documentation-only reruns with a `git show --name-only` + `grep` guard. A real follow-up [PR metadata/document run #40358647032](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40358647032) proved that guard did **not** suppress numerical work even though the [triggering source commit](https://github.com/ndrorchestration/DGAF-Framework/commit/183e82b9367b77f2f1a656025e49c7998a1dcf14) changed only the research document. Its duplicate JiTCDDE run must not be misrepresented as an independent replication or scientific N increment.

A subsequent workflow repair now limits the event sources to same-repository draft PR synchronization or explicit manual dispatch (with the existing branch-specific job condition); it enumerates `git diff-tree --no-commit-id --name-only -r HEAD` and compares each actual modified filename using an exact Bash `case` check. Only changes to the optional JiTCDDE workflow or source module should execute the numerical steps. Other PR updates should complete a lightweight scope check and skip optional package installation, compilation, trajectory generation, and artifact upload. The repaired code itself must be checked using a real documentation-only commit, not merely asserted from inspection.

Scientific custody unchanged: maintained DDE library results are author-directed; the comparative four-node fixture remains non-admitted; independent reviewer issue #1521 remains open; `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Analytic t=0 boundary and independent-code-path early ODE check

**New exploratory software fixtures:** `tools/pdmal/early_window_oracle.py`, `tests/test_pdmal_early_window_oracle.py`, and [frozen machine-readable analytic receipt](PDMAL_EARLY_WINDOW_ANALYTIC_RECEIPT_2026-10-26.json). These use only the frozen four-node physical model, Python standard-library mathematics, and a separately coded **bounded initial-interval** RK4 routine; no external dependency, graph comparator, pilot activation or new scientific observation is involved.

**Mathematically exact domain reduction:** the smallest positive directed delay is **0.04 s**. For every t in **[0,0.04]**, each delayed sender has t−τ≤0 and therefore contributes its prescribed constant history value `INITIAL[j]`. Only unspecified **zero-delay directed interactions** depend on current states. The DDE on this restricted interval consequently reduces to a finite-dimensional ODE. The formula is **not valid** for t>0.04 or as a general DDE history solver.

At t=0, the analytic *right* derivative `dθ/dt` in radians/second is **(-0.04382726981975876, 0.7374820637451177, -0.6852738109105043, 0.926169557350277)**. The right second derivative `d²θ/dt²` in radians/second² is **(-0.06327968042603098, 0.2413565892312074, -0.19689068074438454, -0.32457989538802645)**. These values follow directly from the fixed directed-lag Kuramoto right-hand side and the zero left derivative of the constant prescribed past, rather than from a DDE solver. The nonzero right slopes versus constant-history left slopes reveal a true **initial derivative discontinuity**; no JiTCDDE trajectory accuracy follows from this identity alone.

An author-coded 0.000625-s RK4 integration of this short-time ODE gives unwrapped phases at **t=0.02**: `(0.1991106323785867, -0.7852035448694009, 1.3862567400879844, -0.3815424149178949)`. At **t=0.04**: `(0.1981949660338344, -0.7703194101467735, 1.3724443172456253, -0.36321993736068886)`. Independently coded first-interval ODE software tests pin the analytic right slopes/accelerations, compare the short-window ODE with the existing full delayed RK4 on its first two steps, reject invalid grids, and check short-window RK4 substep sensitivity. **Same-author cross-check, not independent scientific validation.**

**Observed early-grid mismatch against preserved JiTCDDE artifact:** author-operated [run #40358127422](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40358127422) [artifact #12666278250](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40358127422/artifacts/12666278250) yields first-window (t=0.02) max phase differences from the short ODE of **0.0002043616516481661 / 0.00010217623266156606 / 0.00005108697001870999 rad** at blind-bootstrap steps **0.001 / 0.0005 / 0.00025 s**. At t=0.04 the respective differences are **0.00020283204588122938 / 0.00010141136424468566 / 0.000050704519419686456 rad**. Each approximate halving is consistent with previously observed first-order startup discretization sensitivity. This isolates a discrepancy *within the interval where true delayed history is mathematically constant*, but it does **not** determine why JiTCDDE's blind integrator differs or prove which full solver is correct.

**Scientific evidence ceiling:** the early derivative identities strengthen input/implementation falsifiability and local accuracy checks. A maintainer-independent, non-author model implementation is still required, especially a method retaining the unavailable t=0.02–0.40 s history samples; see [open issue #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521). First-window ODE results are **not** new network/topology efficacy data or an authorized experiment. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## 2026-10-26 — Executed early-window receipt audit: numerical success is not certification

A new source module, `tools/pdmal/early_window_receipt_audit.py`, enforces the **frozen 4-node fixture SHA-256**, nominal/sensitivity scientific-admission fields, 41 finite unwrapped phase vectors per solver variant, the prescribed initial phase vector, exactly three ordered blind-bootstrap steps, and cross-receipt nominal/0.001-s trajectory consistency. It independently computes the author-coded first-interval ODE on **[0,0.04] s** and compares JiTCDDE samples t=0.02 and t=0.04, recording observed residuals and ratios with **no unreviewed absolute-error acceptance threshold**. New `tests/test_pdmal_early_window_receipt_audit.py` covers malformed/truncated/NaN/changed-authorization receipts and undefined ratios for a zero-error reference. The auditor itself neither integrates a DDE nor certifies external validation.

The first **real optional GitHub-hosted audit** completed [run #40424843689](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689), code commit `43a37d928ba0d2e9209bb6f14fb7add52d1473d9`, full [artifact #12698429207](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689/artifacts/12698429207), including `early-window-audit.json`, `receipt.json`, `bootstrap-sensitivity.json`, `discontinuity-alignment.json`, source hashes and a pinned-package `pip freeze`. The audited status explicitly reads **`EXECUTION_RECEIPT_AUDITED_NUMERICAL_ACCURACY_NOT_CERTIFIED`** with disposition **`OBSERVED_EARLY_STARTUP_DISCREPANCY_REQUIRES_INDEPENDENT_REVIEW`**. The sole mechanical pipeline PASS means all **custody/shape checks passed**, not that numerical accuracy, full early-history correctness or scientific approval passed.

**Measured maximum absolute phase residuals from the same-author, bounded initial ODE:**

| Blind-bootstrap step | At t=0.02 s (rad) | At t=0.04 s (rad) |
| --- | ---: | ---: |
| 0.001 s | 0.0002043616516481661 | 0.00020283204588122938 |
| 0.0005 s | 0.00010217623266156606 | 0.00010141136424468566 |
| 0.00025 s | 0.00005108697001870999 | 0.000050704519419686456 |

Observed residual ratios for each bootstrap-step halving: at **t=0.02**: `2.0000899066719793`, `2.000044876886322`; at **t=0.04**: `2.000091877196678`, `2.000045861894351`. This is consistent with approximately first-order **startup-resolution sensitivity on one fixture**, not proof of general JiTCDDE convergence, validated accuracy tolerance, global DDE correctness, graph superiority or agent governance efficacy.

**Runner safety correction:** the optional workflow's exact-commit diff guard had silently skipped a changed-workflow numerical run due to a shallow `actions/checkout` (only one commit and no parent for `git diff-tree`). Research-only checkout now requests `fetch-depth: 2` and **fails closed if changed-file enumeration is empty**. The successful audited [run #40424843689](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689) specifically confirmed the repaired guard, installed the optional DDE library, executed the reference and all diagnostics and uploaded the receipt. The workflow continues to skip integration when the exact source commit changes unrelated documents/tests only; protected canonical pilot and dependency locks were not altered.

**Evidence boundaries:** this remains entirely **author-operated**; independent non-author DDE verification issue [#1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521) remains OPEN. `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`. CI for subsequent source cleanups is head-specific and must not inherit the earlier successful hosted run.
