# Evidence Graph Draft — DGAF/PDMAL Completion Journey

**Established:** 2026-08-21  
**Status:** DRAFT — MOST NODES EMPTY (N=0)  
**Step:** 28 prep (Evidence Graph)

---

## Intent

This document drafts the evidence graph that SHOULD exist after pilot completion. Most nodes are empty today because N=0 — no pilot has run, no artifacts exist, no analysis has been performed.

The graph shows what WILL exist after a successful pilot, not what exists now. Nodes marked "EMPTY" require actual pilot execution to populate.

---

## The Evidence Chain (Target State)

```
CLAIM
  ↓
PRIMARY RESULT
  ↓
LOCKED ANALYSIS
  ↓
PILOT ARTIFACT
  ↓
PILOT RUN
  ↓
FREEZE MANIFEST
  ↓
CANDIDATE SHA
  ↓
SOURCE
```

A reviewer starts with a claim and walks backward to its underlying evidence. Every link must be traceable.

---

## Node-by-Node Status

### 1. CLAIM

**What exists today:** The claim is defined in the estimand chain:
- Construct: FFCR (Failure-Free Completion Rate) — proportion of trials completing without failure per condition per seed
- Estimand: E[FFCR(T) - FFCR(R)] — mean of seed-level paired differences
- Primary endpoint: FFCR per condition, per seed, 180 trials/seed, higher is better

**What's missing:** The claim is NOT yet fully specified:
- Primary contrast NOT adjudicated (4 candidates, none selected)
- Direction NOT defined
- Success criterion NOT defined
- Falsification criterion NOT defined
- Multiplicity strategy NOT defined

**Evidence:** `estimand_chain.json`, `PDMAL_EXPERIMENT_PROTOCOL.md`, `PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`

**Status:** PARTIALLY DEFINED — construct + estimand + endpoint exist; contrast + direction + success + falsification + multiplicity are OPEN.

---

### 2. PRIMARY RESULT

**What exists today:** EMPTY. No pilot has run. No primary result exists.

**What's missing:** The actual FFCR values from a blinded pilot execution. 50 seeds × 180 trials = 9,000 observations (or 180 observations per seed × 50 seeds).

**What's needed:** A blinded pilot execution (Step 24) with N > 0.

**Status:** EMPTY — requires empirical execution.

---

### 3. LOCKED ANALYSIS

**What exists today:** 
- `PDMAL_ANALYSIS_CONTROL_PLAN.md` (blob `3e556882` at PR #77) — records partial estimand chain and planning basis.
- `sample_size.py` — implements paired-difference normal approximation power calculation.

**What's missing:**
- `PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` — NOT FOUND at any path. This would bind the analysis implementation + configuration to an exact SHA.
- The analysis procedure is NOT locked: what will be calculated, how, what counts as success/failure — none of this is finalized because the primary contrast is not adjudicated.

**What's needed:**
- Adjudicate primary contrast (Step 1)
- Create analysis plan certificate (Step 19)
- Lock analysis before unblinding (Step 25)

**Status:** NOT LOCKED — analysis specification is incomplete. The control plan is a planning record, not a locked specification.

---

### 4. PILOT ARTIFACT

**What exists today:** EMPTY. No pilot artifacts exist.

**What's missing:**
- Per-seed artifact JSON files with blinded_condition_id, trial outcomes, SHA-256, sidecars
- 180 records per seed × 50 seeds = 9,000 trial records
- Each artifact validated by `pilot_artifact_schema.py:validate_artifact()` and `verify_sidecar()`

**What's needed:** A blinded pilot execution (Step 24) that produces artifacts.

**Status:** EMPTY — requires empirical execution. The schema for artifacts exists (`pilot_artifact_schema.py`, blob `2918a9d`), but no artifacts have been produced.

**Pre-existing evidence (NOT pilot data):**
- 360 observations from executor acceptance run (2 seeds × 180 trials, all SUCCESS) — classified as executor acceptance evidence, N=0, NOT pilot data.

---

### 5. PILOT RUN

**What exists today:** EMPTY. No pilot run has occurred.

**What's missing:**
- A `run_pilot.py` execution in pilot mode (not contract mode)
- Requires: protocol freeze + explicit authorization + candidate SHA + blinding key
- Produces: artifacts, sidecars, logs, environment fingerprint

**What's needed:**
- Protocol freeze (Step 22)
- Pilot authorization (Step 23)
- Blinded execution (Step 24)

**Status:** EMPTY — requires authorization and freeze, neither of which exists.

**Pre-existing evidence:**
- `run_pilot.py` in contract mode: 360 observations (2 seeds × 180 trials, all SUCCESS) — executor acceptance test, N=0.

---

### 6. FREEZE MANIFEST

**What exists today:**

At PR #77 (`94fb6fd`, blob `1a143b29`):
- Status: FROZEN
- State: FROZEN — post-freeze verification in progress
- Freeze target SHA: `915e454e27eb2770e7f40a067a881b0783feaae4`
- Freeze commit SHA: PLACEHOLDER (Git freeze commit to be created)
- Primary contrast: OPEN
- N = 0
- Pilot authorization: NOT GRANTED
- Total observations: 360 (executor acceptance, not pilot)
- All success: YES

At local HEAD (`3510b86889`):
- Status: FROZEN (frontmatter)
- Body text: PRE-FREEZE (preconditions listed as OPEN/IN PROGRESS)
- Primary contrast: OPEN
- N = 0
- Pilot authorization: NOT GRANTED

**What's missing:**
- Actual freeze commit SHA (PLACEHOLDER — needs a real git commit that freezes the candidate)
- Primary contrast adjudication (OPEN — must be closed before freeze)
- All gates closed (currently BLOCKED/OPEN/NOT GRANTED)

**What's needed:**
- Close all gates (Steps 1-21)
- Create freeze commit (Step 22)
- Replace PLACEHOLDER with actual SHA

**Status:** PARTIALLY PRESENT — the FROZEN document exists at PR #77, but it's a placeholder (freeze_commit_sha = PLACEHOLDER, primary_contrast = OPEN). The real freeze requires a commit that binds the candidate to an exact SHA.

**Note on two versions:** The local HEAD version and the PR #77 version are DIFFERENT documents with DIFFERENT content. The local HEAD version has PRE-FREEZE body text (preconditions OPEN). The PR #77 version has FROZEN status but acknowledges verification is in progress. Both correctly state N=0 and NOT GRANTED.

---

### 7. CANDIDATE SHA

**What exists today:**

- Local candidate SHA: `94fb6fdff64f2919d35938c5b1cb506625cf1139` (PR #77, `pr-77-head`)
- GitHub candidate SHA: `b25a914c0e86333a9af4b216a9acdfaec28e42b0` (PR #77 head, diverged from local)
- Candidate manifest: `CANDIDATE_MANIFEST_2026-08-21.json` (written by hand, NOT YET COMMITTED)

**What's missing:**
- Candidate manifest committed to repository (currently on disk only)
- Development/candidate separation (not established)
- Protected candidate reference (tag or branch)
- The manifest identifies the candidate but does NOT make it immutable

**What's needed:**
- Commit candidate manifest (Step 3)
- Create protected candidate reference (Step 4)
- Separate development from candidate (Step 4)

**Status:** IDENTIFIED BUT NOT IMMUTABLE. The candidate SHA exists (94fb6fd locally, b25a914c on GitHub), and the manifest identifies the components. But the candidate is not yet an immutable reference — the manifest is not committed, and there's no separation between development and candidate.

---

### 8. SOURCE

**What exists today:**

Local HEAD (`3510b86889cd341f7a7cf9ab684fd37b2fafd758`):
- `run_pilot.py`: blob `1e6ba2e0` — uses `ScriptedTask`, contract mode only
- `artifact_schema.py`: blob `41a9048` — PRE-FREEZE contract validation
- No `pilot_artifact_schema.py`, no `test_security_controls.py`, no `durable_retention.py` (only on disk, not committed)

PR #77 (`94fb6fd`):
- `run_pilot.py`: blob `184f4aa7` — uses `ConsensusTask`, pilot mode with gating
- `artifact_schema.py`: blob `41a9048` (unchanged)
- `pilot_artifact_schema.py`: blob `2918a9d` — FROZEN pilot validation
- `test_security_controls.py`: blob `ddc59571` — 6 adversarial tests
- `test_artifact_schema.py`: blob not individually verified
- `durable_retention.py`: NOT FOUND at PR #77 (only on disk)
- `.github/workflows/pdmal-preauth-security.yml`: blob `9cff92a5`
- `.github/workflows/pdmal-blinding-operational-test.yml`: blob `7506f412`
- 7 documentation files (see PR #77 audit)

**What's missing:**
- The source is the current state of the repository. The candidate is the PR #77 state. The source for a future pilot is the frozen candidate (after Step 22).
- `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` — not found at any path
- `PDMAL_PIPELINE_SPEC.md` — not found at any path
- `PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` — not found at any path

**Status:** SOURCE EXISTS. The repository has code, configuration, and documentation. The candidate is identified (PR #77). But the source for the empirical experiment is not yet frozen — the candidate is not yet immutable.

---

## Graph Visualization (Current State)

```
CLAIM ── [PARTIAL] ── Construct + estimand + endpoint defined
         │                  Contrast + direction + success + falsification OPEN
         │
PRIMARY RESULT ── [EMPTY] ── No pilot run. N=0.
         │
LOCKED ANALYSIS ── [NOT LOCKED] ── Control plan exists (planning record)
         │                       Analysis plan certificate NOT FOUND
         │                       Analysis NOT locked (contrast not adjudicated)
         │
PILOT ARTIFACT ── [EMPTY] ── No artifacts. Schema exists but un-used.
         │
PILOT RUN ── [EMPTY] ── No execution. Contract-mode run exists (360 obs, N=0).
         │
FREEZE MANIFEST ── [PLACEHOLDER] ── FROZEN document exists at PR #77
         │                            freeze_commit_sha = PLACEHOLDER
         │                            primary_contrast = OPEN
         │
CANDIDATE SHA ── [IDENTIFIED] ── 94fb6fd (local) / b25a914c (GitHub)
         │                         Manifest exists but NOT committed
         │                         No dev/candidate separation
         │
SOURCE ── [EXISTS] ── Repository at 3510b86889 (main) + PR #77 at 94fb6fd
```

---

## What Needs to Happen to Complete the Graph

| Node | Required For | Step(s) | Current Status |
|---|---|---|---|
| CLAIM (complete) | Everything | Step 1 (Gate 1) | PARTIAL — contrast + direction + success + falsification + multiplicity OPEN |
| PRIMARY RESULT | Empirical evidence | Step 24 | EMPTY — no pilot run |
| LOCKED ANALYSIS | Scientific lock | Steps 1, 19, 25 | NOT LOCKED — control plan exists, certificate missing, analysis not locked |
| PILOT ARTIFACT | Evidence | Step 24 | EMPTY — no artifacts |
| PILOT RUN | Evidence | Steps 22, 23, 24 | EMPTY — no execution (contract-mode run exists, N=0) |
| FREEZE MANIFEST (complete) | Formal freeze | Steps 1-22 | PLACEHOLDER — FROZEN document exists but freeze_commit_sha is placeholder, contrast is OPEN |
| CANDIDATE SHA (immutable) | Gate 2 | Steps 2-4 | IDENTIFIED — manifest exists but not committed, no separation |
| SOURCE (frozen) | Everything | Step 22 | EXISTS — but candidate not yet frozen (PLACEHOLDER) |

---

## Pre-Existing Evidence (N=0, NOT Pilot Data)

The following exists today but is NOT pilot data — it is executor acceptance or characterization evidence:

1. **360 observations** (2 seeds × 180 trials, all SUCCESS) — executor acceptance run in contract mode. Classified as "Executor acceptance evidence only; not pilot data; N = 0" in FREEZE_MANIFEST.md.

2. **Executor implementation** — `ConsensusTask` implemented at `75a7f18` (PR #77 corrected runner uses this). The executor works, but this is implementation evidence, not empirical evidence.

3. **Artifact schema** — `artifact_schema.py` (PRE-FREEZE) and `pilot_artifact_schema.py` (FROZEN) exist and are correct. This is implementation evidence, not empirical evidence.

4. **Security controls** — `test_security_controls.py` (6 adversarial tests) exists. This is implementation evidence, not empirical evidence.

5. **Blinding function** — `blind_condition()` exists in `run_pilot.py`. This is implementation evidence, not empirical evidence.

6. **Topology definitions** — 4 conditions × 5 topologies × 9 failure counts frozen at `915e454e`. This is design evidence, not empirical evidence.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This evidence graph draft shows what WILL exist after a successful pilot. Most nodes are empty today because N=0. The graph does NOT claim any empirical evidence exists. It does NOT substitute for actual pilot execution.

The graph is a specification for evidence that must be produced, not evidence that has been produced.
