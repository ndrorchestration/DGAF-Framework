# P-01 Herald Endpoint — `/api/ahg_herald`

**Version:** 1.0 | **File:** `api/ahg_herald.py` | **Date:** 2026-06-29

Vercel serverless function that receives AHG trace batches from
`HeraldHTTPSink` (in `components/ahg_herald_trace.py`) and fans out to
Vercel KV, structured runtime logs, and an optional Tribunal alert webhook.

---

## Quick Setup

### 1. Set Vercel environment variables

```bash
# Required in production
vercel env add AHG_HERALD_API_KEY production
# e.g. value: sk-herald-<random-32-chars>

# Optional: Vercel KV (for dashboard real-time state)
vercel env add AHG_KV_REST_API_URL production
vercel env add AHG_KV_REST_API_TOKEN production

# Optional: Slack/webhook Tribunal alerts
vercel env add AHG_TRIBUNAL_WEBHOOK_URL production

# Optional: log all record fields (verbose — dev only)
vercel env add AHG_LOG_FULL_RECORDS production  # value: "true"
```

### 2. Configure HeraldHTTPSink on the Python side

Set these on the machine running the AHG ensemble:

```bash
export AHG_HERALD_ENDPOINT=https://<your-vercel-domain>/api/ahg_herald
export AHG_HERALD_API_KEY=sk-herald-<same-value-as-above>
export AHG_HERALD_TIMEOUT=2.0
export AHG_HERALD_MAX_RETRIES=3
export AHG_HERALD_BATCH_SIZE=10
```

Or in Python:

```python
from components.ahg_herald_trace import AHGHeraldTrace, HeraldSinkConfig

config = HeraldSinkConfig(
    endpoint="https://<your-vercel-domain>/api/ahg_herald",
    api_key="sk-herald-...",
    timeout=2.0,
    max_retries=3,
    batch_size=10,
)
trace = AHGHeraldTrace(session_id="S077", sink_config=config)
sidecar.wire_herald_trace(trace.on_intent)
```

### 3. Verify

```bash
# Health check (no auth required)
curl https://<your-vercel-domain>/api/ahg_herald

# Test push
curl -X POST https://<your-vercel-domain>/api/ahg_herald \
  -H "Authorization: Bearer sk-herald-..." \
  -H "Content-Type: application/json" \
  -d '{"records":[{"session_id":"S077","turn_id":1,"timestamp_utc":"2026-06-29T03:10:00","archetype":"INTEGRATION","regime":"Integration","phi":1.618,"v_phi":0.01,"a_phi":0.001,"tribunal_active":false,"ttl":5,"message":"test","ndr_stasis_delta":0.0001}],"count":1}'
```

Expected response:
```json
{ "accepted": 1, "tribunal_alerts": 0, "ndr_stasis_events": 1, "session_id": "S077" }
```

---

## Fan-Out Map

| Sink | Condition | Detail |
|---|---|---|
| Vercel runtime logs | Always | Structured JSON per record via `print()` |
| Vercel KV `ahg:session:<id>:latest` | Always (if KV configured) | Latest phi, regime, archetype, tribunal flag |
| Tribunal webhook | If `tribunal_active=true` in any record | Slack-compatible JSON with all tribunal events |
| NDR-STASIS detection | phi within 0.02 of 1.6180339... | Counted in response; no external push (logged) |

---

## KV Schema

Key: `ahg:session:<session_id>:latest`

```json
{
  "session_id": "S077",
  "turn_id": 42,
  "phi": 1.618,
  "regime": "Integration",
  "archetype": "INTEGRATION",
  "tribunal_active": false,
  "timestamp_utc": "2026-06-29T03:10:00",
  "batch_size": 10,
  "tribunal_alerts_in_batch": 0
}
```

This is the primary data source for a real-time governance dashboard.
Read it from any Vercel route via:
```typescript
import { kv } from '@vercel/kv'
const state = await kv.get(`ahg:session:${sessionId}:latest`)
```

---

## Response Schema

| Field | Type | Meaning |
|---|---|---|
| `accepted` | int | Records successfully processed |
| `tribunal_alerts` | int | Records with `tribunal_active=true` in batch |
| `ndr_stasis_events` | int | Records with phi within NDR-STASIS tolerance |
| `session_id` | string | Session ID from first record |

---

## Security Notes

- Set `AHG_HERALD_API_KEY` in Vercel env before going to production.
- Without it, the endpoint is open (dev mode only).
- The API key should match `AHG_HERALD_API_KEY` on the Python/ensemble side.
- Rotate keys via `vercel env rm AHG_HERALD_API_KEY` + re-add.
- The endpoint does not store records itself — KV holds only the **latest** state per session. Full record history lives in JSONL files on the ensemble host.
