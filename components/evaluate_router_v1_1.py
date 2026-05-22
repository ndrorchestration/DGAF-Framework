"""evaluate_router v1.1 — Sentinel integration patch.

Adds sentinel_review() at 3 hook points.
P-10 deontic gate at hook point 1.
Per-record audit log for EU AI Act Art.9 / NIST RMF Measure.
Core routing math unchanged from v1.0.
"""
from datetime import datetime, timezone

RISK_OK    = 'risk_ok'
RISK_WARN  = 'risk_warn'
RISK_BLOCK = 'risk_block'

def p10_deontic_gate(record: dict) -> dict:
    """P-10 Normative Constraint gate — permitted / obligated / forbidden."""
    category = record.get('category', 'unknown')
    if category == 'adversarial' and record.get('confidence', 1.0) < 0.1:
        return {'gate': 'forbidden', 'reason': 'adversarial below detection floor'}
    if category == 'governance':
        return {'gate': 'obligated', 'reason': 'governance record: strong weights required'}
    return {'gate': 'permitted', 'reason': 'within normative bounds'}

def sentinel_review(record: dict, routing: dict, hook_point: str) -> dict:
    """Side-effect-free Sentinel review at defined hook points.
    
    Hook points:
      1. after_category_detection
      2. after_weight_selection
      3. before_report_emission

    Returns per-record audit log entry.
    EU AI Act Article 9 | NIST AI RMF: Measure, Govern
    """
    ts         = datetime.now(timezone.utc).isoformat()
    category   = routing.get('category', 'unknown')
    policy     = routing.get('policy', 'unknown')
    confidence = routing.get('confidence', 0.0)
    deontic    = p10_deontic_gate(record) if hook_point == 'after_category_detection' else {'gate': 'skipped'}

    risk  = RISK_OK
    notes = []

    if category == 'adversarial' and policy != 'apply_strong':
        risk = RISK_BLOCK
        notes.append('ADVERSARIAL input reached non-strong policy — hard block')
    elif confidence < 0.20:
        risk = RISK_WARN
        notes.append('Confidence below floor 0.20 — low signal input')
    elif deontic.get('gate') == 'forbidden':
        risk = RISK_BLOCK
        notes.append(f"P-10 deontic gate: {deontic['reason']}")
    elif policy == 'fallback_balanced' and category not in ['entropy', 'kappa_heuristic']:
        risk = RISK_WARN
        notes.append('Fallback reached for non-entropy category — review routing')

    if not notes:
        notes.append('All checks nominal')

    return {
        'audit_type':       'sentinel_review',
        'timestamp':        ts,
        'hook_point':       hook_point,
        'record_id':        record.get('id', 'unknown'),
        'category':         category,
        'confidence':       round(confidence, 4),
        'policy':           policy,
        'deontic_gate':     deontic,
        'risk':             risk,
        'notes':            notes,
        'eu_ai_act_art9':   True,
        'nist_rmf_function':'Measure'
    }
