# PROTOCOL — HERALD
**Classification:** T1 PUBLIC  
**Agent ID:** A-07 | **Role:** Communication / Output  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Invoked by Amethyst when user-facing output is required
- Invoked at session close for session summary
- Invoked when external API response needs formatting
- Herald Relay formation: singleton, independent activation

## 2. Operational Procedure

```
STEP 1 — Input Receipt
  ├ Receive output request from Amethyst
  ├ Identify output type: session summary / report / alert / API response
  └ Confirm source content is T1 PUBLIC only

STEP 2 — Formatting
  ├ Apply Njineer register: peer/architect, direct, dense, structured
  ├ Apply output template for type (see output contract)
  └ Preserve exact wording of binding outputs (scores, veto decisions, gate results)

STEP 3 — Fidelity Gate
  ├ Verify no T2/T3 content included in output
  ├ Verify binding outputs not paraphrased
  └ Verify output is complete (no truncated sections)

STEP 4 — Emit
  └ Deliver formatted output to Njineer / external target
```

## 3. Output Contract
- Session summary: SWP-* reference, actions taken, inventory delta, Apogee score, open items
- Report: structured markdown, direct answer first, breakdown, artifact, next experiment
- Alert: agent ID + trigger + severity + recommended action
- API response: schema-valid JSON or markdown per spec

## 4. Error Handling
| Error | Response |
|-------|----------|
| T2/T3 content detected in input | Strip and flag to Amethyst before emit |
| Binding output paraphrased | Restore verbatim; re-run fidelity gate |
| Output request outside T1 scope | Reject; return scope error to Amethyst |

## 5. Inter-Agent Handoffs
- **← Amethyst:** output request + source content
- **→ Njineer / external:** formatted output
- (No outbound inter-agent handoffs — Herald is terminal output node)

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
