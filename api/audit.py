# api/audit.py — Vercel Python serverless route
# GET /api/audit
from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler

# Import shared state from orchestrate (same module scope on warm instances)
try:
    from api.orchestrate import _state
except ImportError:
    _state = {}

VERSION = os.environ.get("ENSEMBLE_VERSION", "1.7.0")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "status":        "ok",
            "version":       VERSION,
            "turn_count":    _state.get("turn_count", 0),
            "stable_turns":  _state.get("stable_turns", 0),
            "prune_events":  _state.get("prune_events", 0),
            "axiom_count":   _state.get("axiom_count", 3),
            "consec_phi_fail": _state.get("consec_phi_fail", 0),
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
