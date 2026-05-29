# api/health.py  GET /api/health
# Returns PSI cubic integrity check + ensemble version.
import json
import math
import sys
from http.server import BaseHTTPRequestHandler

PSI = (1 + math.sqrt(5)) / 2


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        psi_ok = abs(PSI**3 - (PSI**2 + 1)) < 1e-10
        body = json.dumps({
            "status":        "ok" if psi_ok else "psi_fail",
            "version":       "1.7.0",
            "psi_cubic":     psi_ok,
            "phi_star":      round(PSI - 1, 6),
            "python":        sys.version,
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
