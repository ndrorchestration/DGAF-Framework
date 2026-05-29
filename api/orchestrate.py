# api/orchestrate.py  POST /api/orchestrate
# Single-turn gate: SCPE → COLLEEN → DemiJoule → Phi-Closure → HPG → PRODIGY → APOGEE → Amethyst seal.
import json
import sys
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "components"))

from ensemble_v17 import (  # noqa: E402
    AgentAmethyst,
    ContextToken,
    StructuralContextPruningEngine,
    Tier,
)

# Module-level singletons — persist across warm Vercel invocations.
_scpe = StructuralContextPruningEngine(threshold=0.15)
_amethyst = AgentAmethyst(_scpe)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        payload    = body.get("payload", "")
        state      = body.get("state", {"schema": "v1.7", "mode": "governance"})
        confidence = float(body.get("confidence", 0.80))
        claim      = body.get("claim", "")
        artifact   = body.get("artifact_description", "")
        entropy    = float(body.get("entropy_score", 0.5))
        kappa_hint = float(body.get("kappa_score_hint", 0.5))

        # Ingest payload as operational token before orchestration.
        _scpe.ingest(ContextToken(
            token_id=f"req_{int(time.time() * 1000)}",
            content=payload[:300],
            tier=Tier.OPERATIONAL,
        ))

        rec = _amethyst.orchestrate_turn(
            payload=payload,
            state=state,
            confidence=confidence,
            claim=claim,
            artifact_description=artifact,
            entropy_score=entropy,
            kappa_score_hint=kappa_hint,
        )

        resp = json.dumps({
            "turn_id":               rec.turn_id,
            "dgaf_decision":         rec.dgaf_decision,
            "phi_decision":          rec.phi_decision,
            "kappa_category":        rec.kappa_category,
            "kappa_policy":          rec.kappa_policy,
            "hpg_routing_mode":      rec.hpg_routing_mode,
            "hpg_applied":           rec.hpg_applied,
            "hpg_step_locked":       rec.hpg_step_locked,
            "effective_confidence":  rec.hpg_effective_confidence,
            "apogee_grade":          rec.apogee_grade,
            "gold_star":             rec.gold_star,
            "scpe_compression":      rec.scpe_compression_ratio,
            "pdmal_status":          rec.pdmal_convergence_status,
            "seal_hash":             rec.seal_hash,
        }).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(resp)
