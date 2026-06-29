"""
api/ahg_herald.py — P-01 Herald Fan-Out Trace Endpoint
Vercel Serverless Function (Python runtime)
Version: 1.0
Author: Amethyst | 2026-06-29

Route: POST /api/ahg_herald

Receives batched AHGTraceRecord payloads from HeraldHTTPSink
(components/ahg_herald_trace.py) and fans out to:
  1. Vercel KV (if configured) — latest phi/regime per session, for dashboard
  2. Structured JSON log (always) — stdout, captured by Vercel runtime logs
  3. Tribunal alert webhook (if AHG_TRIBUNAL_WEBHOOK_URL set)

Auth:
  Requests must include header: Authorization: Bearer <AHG_HERALD_API_KEY>
  Set AHG_HERALD_API_KEY as a Vercel environment variable.
  If not set, auth is bypassed (dev/open mode — not recommended for production).

Expected request body:
  {
    "records": [ <AHGTraceRecord dict>, ... ],
    "count": <int>
  }

Response:
  200 OK  — { "accepted": <int>, "tribunal_alerts": <int>, "session_id": <str> }
  400     — malformed body
  401     — missing or invalid API key
  405     — method not allowed

Environment variables:
  AHG_HERALD_API_KEY          — Bearer token (required in production)
  AHG_KV_REST_API_URL         — Vercel KV REST URL (optional)
  AHG_KV_REST_API_TOKEN       — Vercel KV REST token (optional)
  AHG_TRIBUNAL_WEBHOOK_URL    — Slack/webhook URL for Tribunal alerts (optional)
  AHG_LOG_FULL_RECORDS        — "true" to log all record fields (default: false)
"""

import json
import logging
import os
import urllib.request
from http.server import BaseHTTPRequestHandler
from typing import Any

logger = logging.getLogger("p01.herald")

NDR_STASIS_PHI = 1.6180339887498949
NDR_STASIS_TOLERANCE = 0.02


# ---------------------------------------------------------------------------
# Vercel KV helpers (optional — no-op if env vars not set)
# ---------------------------------------------------------------------------

def _kv_set(key: str, value: Any) -> bool:
    """Write a value to Vercel KV via REST API. Returns True on success."""
    url = os.environ.get("AHG_KV_REST_API_URL")
    token = os.environ.get("AHG_KV_REST_API_TOKEN")
    if not url or not token:
        return False
    try:
        payload = json.dumps(["SET", key, json.dumps(value)]).encode()
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            return resp.status == 200
    except Exception as exc:
        logger.warning(f"[Herald] KV write failed: {exc}")
        return False


def _post_webhook(url: str, payload: dict) -> bool:
    """POST a JSON payload to a webhook URL. Returns True on success."""
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return resp.status in (200, 204)
    except Exception as exc:
        logger.warning(f"[Herald] Webhook post failed: {exc}")
        return False


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def _check_auth(headers: dict) -> bool:
    """Validate Bearer token against AHG_HERALD_API_KEY env var.
    If env var not set, passes in open/dev mode.
    """
    expected = os.environ.get("AHG_HERALD_API_KEY")
    if not expected:
        return True  # open mode — dev only
    auth = headers.get("authorization", headers.get("Authorization", ""))
    if not auth.startswith("Bearer "):
        return False
    return auth[len("Bearer "):].strip() == expected.strip()


# ---------------------------------------------------------------------------
# Record processing
# ---------------------------------------------------------------------------

def _process_records(records: list) -> dict:
    """Process a batch of AHGTraceRecord dicts. Returns fan-out summary."""
    if not records:
        return {"accepted": 0, "tribunal_alerts": 0, "ndr_stasis_events": 0, "session_id": "unknown"}

    log_full = os.environ.get("AHG_LOG_FULL_RECORDS", "").lower() == "true"
    tribunal_alerts = 0
    ndr_stasis_events = 0
    session_id = records[0].get("session_id", "unknown")
    latest = records[-1]  # most recent record in batch for KV update

    for rec in records:
        # 1. Structured stdout log (always — captured by Vercel runtime)
        log_entry = {
            "p01": "ahg_trace",
            "session": rec.get("session_id"),
            "turn": rec.get("turn_id"),
            "ts": rec.get("timestamp_utc"),
            "archetype": rec.get("archetype"),
            "regime": rec.get("regime"),
            "phi": rec.get("phi"),
            "tribunal": rec.get("tribunal_active"),
        }
        if log_full:
            log_entry["full"] = rec
        print(json.dumps(log_entry))  # Vercel captures stdout as runtime logs

        # 2. Tribunal alert counting
        if rec.get("tribunal_active"):
            tribunal_alerts += 1

        # 3. NDR-STASIS proximity
        phi = rec.get("phi", 0.0)
        if abs(phi - NDR_STASIS_PHI) <= NDR_STASIS_TOLERANCE:
            ndr_stasis_events += 1

    # 4. Vercel KV — update latest session state (for dashboard)
    kv_key = f"ahg:session:{session_id}:latest"
    _kv_set(kv_key, {
        "session_id": session_id,
        "turn_id": latest.get("turn_id"),
        "phi": latest.get("phi"),
        "regime": latest.get("regime"),
        "archetype": latest.get("archetype"),
        "tribunal_active": latest.get("tribunal_active"),
        "timestamp_utc": latest.get("timestamp_utc"),
        "batch_size": len(records),
        "tribunal_alerts_in_batch": tribunal_alerts,
    })

    # 5. Tribunal webhook (if any tribunal alerts in batch)
    webhook_url = os.environ.get("AHG_TRIBUNAL_WEBHOOK_URL")
    if tribunal_alerts > 0 and webhook_url:
        tribunal_recs = [r for r in records if r.get("tribunal_active")]
        _post_webhook(webhook_url, {
            "text": (
                f"⚠️ *AHG TRIBUNAL ACTIVE* — Session `{session_id}`\n"
                f"> {tribunal_alerts} Tribunal event(s) in batch of {len(records)}\n"
                f"> Latest: turn={latest.get('turn_id')} "
                f"phi={latest.get('phi', 0):.4f} "
                f"regime={latest.get('regime')} "
                f"archetype={latest.get('archetype')}"
            ),
            "session_id": session_id,
            "tribunal_events": tribunal_recs,
        })

    return {
        "accepted": len(records),
        "tribunal_alerts": tribunal_alerts,
        "ndr_stasis_events": ndr_stasis_events,
        "session_id": session_id,
    }


# ---------------------------------------------------------------------------
# Vercel handler
# ---------------------------------------------------------------------------

class handler(BaseHTTPRequestHandler):
    """Vercel Python serverless function handler for POST /api/ahg_herald."""

    def log_message(self, format, *args):  # suppress default access log
        pass

    def _send_json(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        # Preflight — CORS headers set by vercel.json
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        # Auth check
        headers = dict(self.headers)
        if not _check_auth(headers):
            self._send_json(401, {"error": "Unauthorized"})
            return

        # Parse body
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            body = json.loads(raw)
            records = body.get("records", [])
            if not isinstance(records, list):
                raise ValueError("records must be a list")
        except Exception as exc:
            self._send_json(400, {"error": f"Bad request: {exc}"})
            return

        # Process
        result = _process_records(records)
        self._send_json(200, result)

    def do_GET(self):
        # Health probe for Herald endpoint
        self._send_json(200, {
            "status": "ok",
            "endpoint": "P-01 AHG Herald Fan-Out",
            "version": "1.0",
            "kv_configured": bool(os.environ.get("AHG_KV_REST_API_URL")),
            "auth_required": bool(os.environ.get("AHG_HERALD_API_KEY")),
            "tribunal_webhook": bool(os.environ.get("AHG_TRIBUNAL_WEBHOOK_URL")),
        })

    def do_DELETE(self):
        self._send_json(405, {"error": "Method not allowed"})
