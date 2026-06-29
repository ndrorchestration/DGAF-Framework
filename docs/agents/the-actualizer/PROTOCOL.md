# The Actualizer — Operational Protocol

**Agent:** The Actualizer (A-08)
**Classification:** T1 PUBLIC
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. Artifact Generation Procedure

**Trigger:** Formation requests code or artifact generation (post-Auditor constraint verify).

```
Step 1:  Receive generation request
         Contents: artifact type, spec reference, target path, session ID

Step 2:  Confirm Auditor gate cleared
         Check: The Auditor constraint verify = PASSED for this request?
         YES → Step 3
         NO  → block; notify requesting agent; await Auditor clearance

Step 3:  Check for version collision
         Does artifact conflict with an existing canonical doc at target path?
         YES → halt; invoke Reciprocity rollback (Section 3)
         NO  → Step 4

Step 4:  Execute generation
         Write code/artifact to target path
         Log: ARTIFACT_WRITTEN | Actualizer | [artifact name] | [target path]

Step 5:  Mandatory post-write handoff to The Librarian
         Route decision package to Librarian (NDR-Protocol-01 step 3 trigger)
         Confirm archive entry created before marking write COMPLETE
```

---

## 2. L5 Executor Artifact Delivery Procedure

**Trigger:** COLLEEN L5 Executor gate cleared (TUE condition 1 met); L5 delivery artifacts required.

```
Step 1:  Receive L5 delivery request from COLLEEN
         Confirm TUE condition 1 cleared (COLLEEN L5 Executor status)

Step 2:  Confirm Auditor gate cleared for L5 artifacts
         (Full constraint verify required for L5 Executor artifacts)

Step 3:  Generate L5 artifacts
         Includes: CITATION.cff, governance templates, schema files, YAML configs
         Per L5 Executor Roadmap spec

Step 4:  Route to Librarian → Apogee scoring → Amethyst seal
         Chain: Actualizer write → Librarian archive → Apogee score → Amethyst seal → CANONICAL

Step 5:  Log in SWEEP_LOG
         Entry: L5_ARTIFACT_DELIVERED | Actualizer | [artifact list] | [chain status]
```

---

## 3. Version Collision / Reciprocity Rollback Procedure

**Trigger:** Artifact conflicts with existing canonical doc (version collision detected at Step 3 of Section 1).

```
Step 1:  Halt generation
         Do not overwrite existing canonical doc

Step 2:  Invoke Reciprocity rollback authority
         Notify Reciprocity: collision description + artifact + target path + current HEAD

Step 3:  Await Reciprocity rollback
         Reciprocity restores clean HEAD state

Step 4:  Re-generate against clean HEAD
         Return to Section 1 Step 2 (Auditor gate re-confirmed)

Step 5:  Log in SWEEP_LOG
         Entry: VERSION_COLLISION | Actualizer | [artifact] | RECIPROCITY_INVOKED | [resolution]
```

---

*Classification: T1 PUBLIC*
