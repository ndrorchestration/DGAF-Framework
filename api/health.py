# api/health.py — Vercel Python serverless route
# GET /api/health
from __future__ import annotations
import json, math, os, sys
from http.server import BaseHTTPRequestHandler

PSI      = 1.4655712318767682
PHI      = (1 + math.sqrt(5)) / 2
PHI_STAR = PHI - 1
VERSION  = os.environ.get("ENSEMBLE_VERSION", "1.7.0")
PSI_ON   = os.environ.get("PSI_CHECK", "enabled").lower() == "enabled"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        psi_cubic = abs(PSI**3 - (PSI**2 + 1)) < 1e-10
        body = json.dumps({
            "status":           "ok",
            "psi_cubic":        psi_cubic and PSI_ON,
            "version":          VERSION,
            "phi_star":         round(PHI_STAR, 6),
            "psi":              round(PSI, 10),
            "runtime":          f"python-{sys.version_info.major}.{sys.version_info.minor}",
            "scpe_threshold":   0.15,
            "phi_checkpoints":  [13, 21, 34, 55],
            "phi_tolerance":    0.05,
            "t0_axiom_guard":   True,
            "adapters":         ["raw", "langchain", "langgraph", "autogen", "crewai"],
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
