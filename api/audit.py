# api/audit.py  GET /api/audit
# Returns the session audit summary from the warm singleton.
# Full per-turn audit records are written to sim_drift_v17_audit.json by the sim.
import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "components"))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Lazy import so cold-start cost is only paid on first audit request.
        from ensemble_v17 import AgentAmethyst  # noqa: F401

        # Import the live singleton from orchestrate (shared module cache on warm instances).
        try:
            from api.orchestrate import _amethyst, _scpe  # type: ignore
            prune_log   = _scpe.prune_log
            turn_count  = _amethyst.turn_counter
            phi_events  = _amethyst.phi_closure_events
            pdmal_events = _amethyst.pdmal_events
            body = json.dumps({
                "status":         "ok",
                "turn_count":     turn_count,
                "prune_events":   len(prune_log),
                "phi_events":     phi_events,
                "pdmal_events":   pdmal_events,
                "note":           "Full audit: POST /api/orchestrate then re-check here.",
            })
        except Exception as exc:
            body = json.dumps({
                "status": "warm_singleton_unavailable",
                "detail": str(exc),
                "note":   "Fire at least one POST to /api/orchestrate first.",
            })

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())
