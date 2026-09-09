# Read-only GitHub pull-request evidence reconciliation

`scripts/reconcile_github_pr_evidence.py` converts a bounded GitHub pull-request evidence snapshot into a deterministic report.

## Safety boundary

- It makes no network calls.
- It writes only an explicitly requested local output file.
- It never writes to GitHub, Notion, Drive, deployment platforms, or any control record.
- It rejects secret-bearing field names.
- Its `PASS` result has `authorization_effect: NONE` and `scientific_state_effect: NONE`.

## Input

The input JSON has exactly these top-level fields:

```json
{
  "repository": "owner/repository",
  "pull_request": {
    "number": 123,
    "head_sha": "40-or-64-character-lowercase-SHA",
    "state": "open"
  },
  "workflow_runs": [
    {
      "name": "Governance CI",
      "status": "completed",
      "conclusion": "success",
      "head_sha": "same expected SHA"
    }
  ]
}
```

## Run

```bash
python3 scripts/reconcile_github_pr_evidence.py snapshot.json \
  --expected-head-sha <exact-pr-head-sha> \
  --output reconciliation-report.json
```

A changed pull-request head or a workflow bound to another head is reported as `STALE`; incomplete work is `BLOCKED`; failed/cancelled work is `FAIL`. The report is evidence for a human or existing repository control, never an authorization decision.
