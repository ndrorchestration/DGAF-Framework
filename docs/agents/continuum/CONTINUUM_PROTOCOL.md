# Continuum — Protocol v1.0

**Agent:** Continuum
**Agent ID:** A-29
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-09-04

---

## Procedure 1 — Evidence Lineage Tracing

**Trigger:** Orchestrator provides an evidence artifact (artifact ID, file path, or sidecar) and asks Continuum to trace its lineage.

```
Step 1: Identify the artifact
         — artifact ID (GitHub Actions artifact identifier)
         — OR file path (local or repository path to the evidence file)
         — OR sidecar path (the .sha256 companion file)

Step 2: Retrieve the artifact's metadata
         — For GitHub Actions artifacts: the workflow run ID that produced it,
           the workflow name, the triggering candidate SHA, and the artifact digest
         — For local files: the file's current SHA-256, its sidecar (if present),
           and any metadata headers or manifest entries that reference it

Step 3: Trace the lineage chain:
         candidate_sha → workflow_name → workflow_run_id → artifact_id → artifact_digest

Step 4: Verify each link:
         — Does the candidate SHA match the SHA the evidence is claimed for?
         — Does the workflow run ID match the exact run that triggered on that SHA?
         — Does the artifact ID match the artifact that holds the evidence?
         — Does the artifact digest match the actual file content?

Step 5: Report the lineage:
         — Each link in the chain, with the actual identifier found
         — Any link that cannot be verified, with the reason
         — Any mismatch at any link, with both the claimed and actual values
```

---

## Procedure 2 — Anti-Transfer Risk Scanning

**Trigger:** Orchestrator asks Continuum to scan for transfer risks in a document, manifest, or evidence set.

```
Step 1: Identify the scope of the scan
         — A single document (path or content)
         — A manifest file (JSON/YAML with candidate_sha, deployment_id, run_id fields)
         — A set of evidence artifacts

Step 2: For each item in scope, extract the identifiers:
         — candidate_sha (if present)
         — workflow_run_id (if present)
         — artifact_id (if present)
         — deployment_id (if present)
         — any other identity fields (run ID, trigger SHA, etc.)

Step 3: Compare each identifier against the current state:
         — Is the candidate_sha the current candidate, or a superseded candidate?
         — Is the workflow_run_id the current triggering run, or a historical run?
         — Is the deployment_id the current deployment, or a superseded deployment?
         — Is the artifact digest still valid for the current file content?

Step 4: Flag each transfer risk:
         — The identifier found
         — The identifier it should be (if known)
         — The nature of the risk (superseded candidate, historical run, wrong deployment, etc.)
         — The severity: high (likely to be misread as current), medium (ambiguous), low (clearly historical context)

Step 5: Report the transfer risks:
         — Each risk as a structured finding
         — No transfer risks found, if applicable
```

---

## Procedure 3 — Staleness Detection

**Trigger:** Orchestrator asks Continuum to scan for stale references in documents, manifests, or sidecars.

```
Step 1: For each file in scope:
         — Read the file content
         — Identify all SHA references (40-character hex strings)
         — Identify all deployment ID references (dpl_... identifiers)
         — Identify all workflow run ID references (numeric identifiers)
         — Identify all sidecar references (.sha256 companion files)

Step 2: For each SHA reference:
         — Determine whether the SHA is the current candidate, a historical candidate,
           or an unknown SHA
         — Flag any SHA that is superseded or historical as a stale reference

Step 3: For each deployment ID reference:
         — Determine whether the deployment is the current deployment or superseded
         — Flag any superseded deployment ID as a stale reference

Step 4: For each sidecar:
         — Read the sidecar's expected checksum
         — Compute the actual checksum of the accompanying file
         — Flag any mismatch as a stale sidecar

Step 5: Report the staleness findings:
         — Each stale reference with file path, field, stale value, and current value (if known)
         — Each stale sidecar with expected and actual checksum
```

---

## Procedure 4 — Evidence-State Labeling

**Trigger:** Orchestrator provides an evidence artifact or assessment and asks Continuum to apply an evidence-state label.

```
Step 1: Identify what has been established about the evidence:
         — Does the artifact exist? → IMPLEMENTED (at minimum)
         — Has the artifact passed a test or CI check? → TESTED (if no further verification)
         — Has the artifact been independently verified against its claims? → VERIFIED
         — Has the artifact been produced by authorized empirical execution? → EXPERIMENTALLY DEMONSTRATED
         — Is the artifact proposed but not established? → PROPOSED
         — Is the artifact theoretical or planned? → HYPOTHETICAL
         — Is the artifact valid for a past candidate but not current? → HISTORICAL
         — Has the artifact not been established by any evidence? → NOT ESTABLISHED

Step 2: Apply the most specific label that the evidence supports:
         — Do not upgrade a label without the corresponding evidence
         — HISTORICAL evidence is not VERIFIED current evidence
         — TESTED is not EXPERIMENTALLY DEMONSTRATED
         — NOT ESTABLISHED is not VERIFIED

Step 3: Report the label and the evidence that supports it:
         — The label applied
         — The specific evidence, run ID, SHA, or verification that supports the label
         — Any ambiguity or uncertainty in the labeling
```

---

## Procedure 5 — Sidecar Integrity Verification

**Trigger:** Orchestrator asks Continuum to verify one or more `.sha256` sidecar files.

```
Step 1: For each sidecar:
         — Read the sidecar content
         — Extract the expected SHA-256 checksum
         — Identify the accompanying file (same path with .sha256 extension replaced, or
           explicitly referenced in the sidecar)

Step 2: Compute the actual SHA-256 of the accompanying file

Step 3: Compare:
         — Expected checksum vs actual checksum
         — Match → sidecar is current
         — Mismatch → sidecar is stale

Step 4: Report:
         — Each sidecar: path, expected checksum, actual checksum, match/mismatch
         — Any mismatch flagged as a stale sidecar with both values
```

---

## Procedure 6 — Historical-vs-Current Overlay Assessment

**Trigger:** Orchestrator asks Continuum to assess whether a historical record should be overlaid with a current interpretation.

```
Step 1: Identify the historical record and its content
         — What candidate SHA, run ID, deployment ID, or state it references
         — Whether the record is clearly historical or ambiguously current

Step 2: Identify the current state
         — The current candidate SHA
         — The current deployment identity
         — The current evidence state

Step 3: Assess the overlay need:
         — Does the historical record need a current overlay to be interpretable today?
         — Is the historical record clearly marked as historical, or is it at risk of
           being read as current?
         — Would a current overlay change how the record should be interpreted?

Step 4: Report:
         — Whether an overlay is needed
         — What the overlay should convey (current interpretation of historical material)
         — That the overlay is a separate artifact from the historical record
         — That Continuum does not rewrite historical records
```

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Artifact metadata unavailable (run deleted, artifact expired) | Report "lineage incomplete: artifact metadata unavailable" with the artifact ID; do not fabricate identifiers |
| Sidecar references a file that does not exist | Report "stale sidecar: accompanying file not found" with the sidecar path |
| SHA reference is ambiguous (could be candidate, commit, or artifact) | Report the SHA and the ambiguity; do not assume which it is |
| Orchestrator asks Continuum to close a gate or authorize evidence | Continuum states it does not close gates or authorize; refers to Apogee or the appropriate authority |
| Orchestrator asks Continuum to produce or modify evidence | Continuum states it only assesses provenance; refers to the appropriate agent for evidence production |
| Orchestrator asks Continuum to rewrite a historical record | Continuum states it does not rewrite historical records; reports the overlay need as a separate finding |

---

*Classification: T1 PUBLIC*
