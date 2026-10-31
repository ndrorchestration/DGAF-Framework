// Presentation-only adapter for the actual Pages Router /api/orchestrate contract.
// This data is not an authorization grant and must not be treated as an audit seal.
const API_DECISIONS = new Set(['PASS', 'KILL', 'REJECT', 'BLOCKED']);
const EVIDENCE_STATUSES = new Set(['PASS', 'PARTIAL', 'BLOCKED', 'NOT_IMPLEMENTED']);
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);

export function normalizeOrchestrateResponse(value, httpOk = true) {
  const data = object(value) ? value : {};
  const evidence = object(data.evidence) ? data.evidence : {};
  const rawStatus = data.evidence_status ?? evidence.status;
  const rawDecision = API_DECISIONS.has(data.decision) ? data.decision : 'UNKNOWN';
  // A failed HTTP exchange is never a successful admission, even if the body says PASS.
  const decision = httpOk === false && rawDecision === 'PASS' ? 'UNKNOWN' : rawDecision;
  const evidenceStatus = EVIDENCE_STATUSES.has(rawStatus) ? rawStatus : 'UNKNOWN';
  return {
    decision,
    evidence_status: evidenceStatus,
    turn: Number.isSafeInteger(data.turn) && data.turn > 0 ? data.turn : null,
    reason: httpOk === false && rawDecision === 'PASS'
      ? 'Conflicting PASS response on an unsuccessful HTTP request'
      : (typeof data.reason === 'string' ? data.reason : null),
    phi_gate: typeof data.phi_gate === 'string' ? data.phi_gate : null,
    effective_confidence:
      typeof data.effective_confidence === 'number' &&
      Number.isFinite(data.effective_confidence) &&
      data.effective_confidence >= 0 &&
      data.effective_confidence <= 1 ? data.effective_confidence : null,
    hpg_fired: typeof data.hpg_fired === 'boolean' ? data.hpg_fired : null,
  };
}

export function decisionColor(value) {
  const row = normalizeOrchestrateResponse(value);
  if (row.decision === 'KILL' || row.decision === 'BLOCKED') return '#b91c1c';
  if (row.decision === 'REJECT') return '#b45309';
  if (row.evidence_status === 'BLOCKED') return '#b91c1c';
  // This diagnostic endpoint never grants governance admission, even when
  // both its local decision and evidence status happen to say PASS.
  if (row.decision === 'PASS') return '#b45309';
  return '#6b7280'; // Unknown/missing values must never turn green.
}

// A gap is unobserved evidence, not an instruction to interpolate a confidence line.
// Retain absolute plot positions and split only on missing, malformed or out-of-range readings.
export function confidenceSegments(values) {
  if (!Array.isArray(values)) return [];
  const segments = [];
  let current = [];
  values.forEach((value, index) => {
    const row = normalizeOrchestrateResponse(value);
    if (row.effective_confidence === null) {
      if (current.length) segments.push(current);
      current = [];
      return;
    }
    current.push({ index, confidence: row.effective_confidence });
  });
  if (current.length) segments.push(current);
  return segments;
}
