# Propagation Checking Specification

**Established:** 2026-08-21  
**Status:** SPECIFICATION — NOT YET IMPLEMENTED  
**Step:** 9 of 28 (Gate 3: Engineering and Evidence Closure)

---

## Problem

A governance decision is only useful if it propagates to every place that depends on it. Without propagation checking, a governance decision can be made in one place (e.g., the freeze manifest) but silently bypassed in another (e.g., the runner, the analysis, or the evidence graph).

Example of the failure mode:

```
Primary configuration says: "Use topology X"
       ↓
Runner uses: topology Y (different from config)
       ↓
Artifact records: topology Y
       ↓
Analysis analyzes: topology Y
       ↓
Evidence shows: "topology Y was tested"
       ↓
Reviewer asks: "Was topology X the intended candidate?"
       ↓
Answer: "No one checked."
```

The propagation failure is silent — everything looks consistent within itself, but nothing is consistent with the governance decision.

---

## What Propagation Checking Must Detect

A propagation check should detect when any link in the chain carries a value that doesn't match the upstream governance decision.

### Chain links

```
Primary configuration
       ↓
Runner (code + configuration)
       ↓
Artifact (what was produced)
       ↓
Analysis (what was computed)
       ↓
Evidence (what was recorded)
```

At each link, the downstream item should carry a reference to the upstream item it depends on. A mismatch at any link is a propagation failure.

### Specific checks

1. **Configuration → Runner:** The runner should carry the protocol SHA and configuration version it was built against. If the runner was built against protocol v1 but the governance decision was made against protocol v2, that's a propagation failure.

2. **Runner → Artifact:** Each artifact should carry the runner SHA that produced it. If an artifact claims to be produced by runner SHA A but was actually produced by runner SHA B, that's a propagation failure.

3. **Artifact → Analysis:** The analysis should reference the specific artifacts it analyzed. If the analysis uses artifacts from candidate A but the governance decision was about candidate B, that's a propagation failure.

4. **Analysis → Evidence:** The evidence should reference the analysis that produced it. If the evidence cites an analysis that doesn't match the locked analysis specification, that's a propagation failure.

5. **Evidence → Governance decision:** The evidence should be traceable back to the governance decision (freeze manifest, candidate manifest, primary contrast adjudication) that authorized it.

---

## Recommended Implementation: SHA Chaining Through Metadata

Each artifact, analysis output, and evidence record should carry SHA references that chain back to the governance decision:

```
artifact.json:
  - experiment_commit_sha: "<candidate SHA>"
  - runner_sha: "<runner blob SHA>"
  - schema_sha: "<schema blob SHA>"
  - artifact_sha256: "<self-hash>"

analysis_output.json:
  - input_artifact_sha256: "<hash of input artifact>"
  - analysis_commit_sha: "<analysis code SHA>"
  - analysis_config_sha: "<analysis config SHA>"
  - result: {...}

evidence_record.json:
  - source_analysis_sha: "<analysis output SHA>"
  - frozen_commit_sha: "<freeze manifest SHA>"
  - candidate_sha: "<candidate manifest SHA>"
  - primary_contrast_sha: "<contrast adjudication document SHA>"
```

With this chaining:

1. A reviewer can start at any evidence record and walk backward through analysis → artifact → runner → candidate → governance decision.
2. Any break in the chain (missing reference, wrong reference, SHA that doesn't resolve) is detectable.
3. A mismatch (artifact claims runner SHA A but runner SHA A doesn't match the candidate) is detectable.

---

## Detection Logic

For each link, the check is:

```
Is the upstream SHA referenced by the downstream item?
    → If no: propagation failure (missing reference)
    → If yes: Does the upstream SHA resolve to the expected item?
        → If no: propagation failure (wrong reference)
        → If yes: Does the resolved item match the governance decision?
            → If no: propagation failure (governance bypass)
            → If yes: propagation OK
```

---

## Example Propagation Failure

Suppose:

- Candidate manifest says runner SHA = `184f4aa7`
- Artifact says runner SHA = `184f4aa7` (matches manifest)
- But the actual runner code on disk has been modified (git diff shows changes)
- The artifact was produced by the modified runner, not the candidate runner

The SHA in the artifact matches the manifest, but the artifact was not actually produced by the candidate runner. This is a propagation failure that SHA chaining alone would not detect — it requires verifying that the artifact's claimed runner SHA actually produced it (i.e., the artifact's hash matches what the candidate runner would produce for that input).

This is the deeper propagation problem: **matching SHAs is necessary but not sufficient.** You also need to verify that the artifact is consistent with what the referenced code would produce.

---

## Gap from PR #77

PR #77 provides:

- `artifact_sha256` field in artifact records (the artifact's self-hash)
- `experiment_commit_sha` field (the candidate SHA at time of run)
- `environment_fingerprint` field (runtime environment info)

PR #77 does NOT provide:

- `runner_sha` field (which blob produced the artifact)
- `schema_sha` field (which schema validated the artifact)
- `analysis_commit_sha` field (which analysis code produced the result)
- `analysis_config_sha` field (which analysis configuration was used)
- Propagation checking logic (code that verifies the chain)

The `experiment_commit_sha` in artifacts points to the candidate, but the chain from artifact → runner → candidate is incomplete because the runner SHA and schema SHA are not recorded in the artifact.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This is a specification for a control that does NOT yet exist. No artifacts have been produced (N=0), so no propagation can be checked.
