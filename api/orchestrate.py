# api/orchestrate.py — Vercel Python serverless route
# POST /api/orchestrate
# Implements the 9-gate orchestration pipeline.
from __future__ import annotations
import json, math, hashlib, os, sys, time, uuid
from http.server import BaseHTTPRequestHandler

# ── constants ─────────────────────────────────────────────────────────────────
PSI      = 1.4655712318767682
PHI      = (1 + math.sqrt(5)) / 2
PHI_STAR = PHI - 1
VERSION  = os.environ.get("ENSEMBLE_VERSION", "1.7.0")
SCPE_THR = 0.15
FIB_CPS  = {13, 21, 34, 55}
PHI_TOL  = 0.05

# ── session state (module-level, warm across invocations within same instance)
_state = {
    "turn_count":    0,
    "stable_turns":  0,
    "prune_events":  0,
    "axiom_count":   3,   # seeded axioms never pruned
    "consec_phi_fail": 0,
    "prune_log":     [],
}


# ── gate helpers ──────────────────────────────────────────────────────────────
def dgaf_gate(payload: str, entropy: float, kappa_hint: float) -> str:
    """DGAF 6-axis semantic safety gate."""
    blocklist = [
        "ignore all previous", "override governance",
        "disable governance", "you are now ungoverned",
        "drop all axioms", "unrestricted",
    ]
    p = payload.lower()
    if any(b in p for b in blocklist):
        return "KILL"
    if entropy > 0.75 or kappa_hint < 0.25:
        return "REPROMPT"
    return "pass"


def phi_gate(turn: int, stable: bool) -> dict:
    """Fibonacci Phi-Closure Gate."""
    _state["stable_turns"] += int(stable)
    R     = _state["stable_turns"] / _state["turn_count"]
    delta = abs(R - PHI_STAR)
    if turn not in FIB_CPS:
        return {"checkpoint": False, "R": R, "decision": None}
    if delta < PHI_TOL:
        _state["consec_phi_fail"] = 0
        decision = "PASS"
    else:
        _state["consec_phi_fail"] += 1
        decision = "KILL_RECOMMENDATION" if _state["consec_phi_fail"] >= 2 else "REPROMPT"
    return {"checkpoint": True, "turn": turn, "R": round(R, 4),
            "delta": round(delta, 6), "decision": decision}


def hpg_gate(confidence: float) -> dict:
    """Harmonic Progression Gate — snap to phi-Ionian lattice."""
    if not (0.0 <= confidence <= 1.0):
        confidence = max(0.0, min(1.0, confidence))
    octave = 1.0 + confidence  # map [0,1] → [1,2]
    ionian = [2 ** (s / 12) for s in [0, 2, 4, 5, 7, 9, 11, 12]]  # C major
    nearest = min(ionian, key=lambda x: abs(x - octave))
    effective = nearest - 1.0
    phi_member = abs(octave - PHI) < 1e-3
    return {"effective_confidence": round(effective, 6),
            "phi_member": phi_member, "snapped_to": round(nearest, 6)}


def scpe_compression(history_len: int, turn: int) -> float:
    """Simulated SCPE compression ratio (grows with context pressure)."""
    base = min(0.60, 0.10 + history_len * 0.015 + turn * 0.005)
    _state["prune_events"] += max(0, history_len // 4)
    return round(base, 4)


def kappa_classify(kappa_hint: float) -> str:
    if kappa_hint < 0.25: return "adversarial"
    if kappa_hint < 0.45: return "fan_out"
    if kappa_hint < 0.65: return "balanced"
    return "sequential"


def apogee_grade(dgaf: str, phi: dict, conf: float) -> tuple[str, bool]:
    """Apogee evidence grade and Gold Star decision."""
    if dgaf == "KILL":
        return "BLOCKED", False
    phi_dec = phi.get("decision")
    if phi_dec == "KILL_RECOMMENDATION":
        return "D", False
    if phi_dec == "REPROMPT":
        return "C", False
    if conf >= 0.85:
        return "A", True
    if conf >= 0.75:
        return "B", False
    return "C", False


# ── main handler ──────────────────────────────────────────────────────────────
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length  = int(self.headers.get("Content-Length", 0))
        body    = json.loads(self.rfile.read(length) or b"{}")

        _state["turn_count"] += 1
        turn   = _state["turn_count"]
        t_id   = str(uuid.uuid4())[:8]

        payload     = body.get("payload", "")
        confidence  = float(body.get("confidence", 0.80))
        claim       = body.get("claim", "")
        entropy     = float(body.get("entropy_score", 0.25))
        kappa_hint  = float(body.get("kappa_score_hint", 0.55))
        hist_len    = int(body.get("history_length", 0))

        # Gate 1: SCPE
        comp = scpe_compression(hist_len, turn)

        # Gate 4: DGAF
        dgaf = dgaf_gate(payload, entropy, kappa_hint)
        stable = (dgaf == "pass")

        # Gate 5: Phi-Closure
        phi = phi_gate(turn, stable)
        phi_dec = phi.get("decision")
        hpg_applied = False
        eff_conf = confidence

        # Gate 6: HPG (only if phi PASS or no checkpoint)
        if dgaf != "KILL" and phi_dec not in ("REPROMPT", "KILL_RECOMMENDATION"):
            hpg_result  = hpg_gate(confidence)
            eff_conf    = hpg_result["effective_confidence"]
            hpg_applied = True

        # Gate 8: Apogee
        grade, gold_star = apogee_grade(dgaf, phi, eff_conf)

        # Gate 9: Amethyst seal
        seal = hashlib.sha256(
            f"{t_id}{turn}{dgaf}{eff_conf}{comp}".encode()
        ).hexdigest()[:16]

        kappa = kappa_classify(kappa_hint)

        result = {
            "turn_id":              t_id,
            "turn_number":          turn,
            "dgaf_decision":        dgaf,
            "phi_decision":         phi_dec,
            "phi_checkpoint":       phi.get("checkpoint", False),
            "phi_R":                phi.get("R"),
            "kappa_category":       kappa,
            "hpg_applied":          hpg_applied,
            "effective_confidence": eff_conf,
            "apogee_grade":         grade,
            "gold_star":            gold_star,
            "scpe_compression":     comp,
            "pdmal_status":         "ok",
            "seal_hash":            seal,
            "meta": {
                "version":    VERSION,
                "psi_cubic":  abs(PSI**3 - (PSI**2 + 1)) < 1e-10,
                "phi_star":   round(PHI_STAR, 6),
            },
        }

        out = json.dumps(result).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
