// dashboard/components/OrchestratePanel.jsx
// POST form to /api/orchestrate; appends result to turn table.
import { useState } from 'react';

const DEFAULT = {
  payload:              'Validate schema hash against SSoT. Mode: governance.',
  confidence:           '0.80',
  claim:                'Schema hash validated.',
  entropy_score:        '0.25',
  kappa_score_hint:     '0.50',
  artifact_description: '',
};

export default function OrchestratePanel({ onNewTurn }) {
  const [form, setForm]   = useState(DEFAULT);
  const [busy, setBusy]   = useState(false);
  const [last, setLast]   = useState(null);
  const [err, setErr]     = useState(null);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const submit = async () => {
    setBusy(true); setErr(null);
    try {
      const res = await fetch('/api/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          confidence:       parseFloat(form.confidence),
          entropy_score:    parseFloat(form.entropy_score),
          kappa_score_hint: parseFloat(form.kappa_score_hint),
        }),
      });
      const data = await res.json();
      setLast(data);
      onNewTurn(data);
    } catch (e) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={styles.card}>
      <div style={styles.header}>Orchestrate Turn</div>

      <label style={styles.lbl}>Payload</label>
      <textarea style={styles.ta} rows={3} value={form.payload} onChange={set('payload')} />

      <div style={styles.row}>
        <div style={styles.field}>
          <label style={styles.lbl}>Confidence</label>
          <input style={styles.inp} value={form.confidence} onChange={set('confidence')} />
        </div>
        <div style={styles.field}>
          <label style={styles.lbl}>Entropy</label>
          <input style={styles.inp} value={form.entropy_score} onChange={set('entropy_score')} />
        </div>
        <div style={styles.field}>
          <label style={styles.lbl}>KAPPA hint</label>
          <input style={styles.inp} value={form.kappa_score_hint} onChange={set('kappa_score_hint')} />
        </div>
      </div>

      <label style={styles.lbl}>Claim</label>
      <input style={styles.inp} value={form.claim} onChange={set('claim')} />

      <label style={styles.lbl}>Artifact description (optional)</label>
      <input style={styles.inp} value={form.artifact_description} onChange={set('artifact_description')} />

      <button style={{ ...styles.btn, opacity: busy ? 0.6 : 1 }} onClick={submit} disabled={busy}>
        {busy ? 'Sending…' : '▶ Fire Turn'}
      </button>

      {err && <div style={styles.err}>Error: {err}</div>}

      {last && (
        <div style={styles.result}>
          <div style={styles.resultRow}>
            <span style={styles.k}>DGAF</span>
            <span style={dgafColor(last.dgaf_decision)}>{last.dgaf_decision}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>Φ-Gate</span>
            <span>{last.phi_decision ?? '—'}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>KAPPA</span>
            <span>{last.kappa_category} / {last.kappa_policy}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>Eff. Conf</span>
            <span>{typeof last.effective_confidence === 'number' ? last.effective_confidence.toFixed(4) : '—'}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>Apogee</span>
            <span>{last.apogee_grade} {last.gold_star ? '⭐' : ''}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>SCPE</span>
            <span>{typeof last.scpe_compression === 'number' ? (last.scpe_compression * 100).toFixed(1) + '%' : '—'}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.k}>Seal</span>
            <code style={styles.code}>{String(last.seal_hash ?? '—').slice(0,16)}…</code>
          </div>
        </div>
      )}
    </div>
  );
}

const dgafColor = (d) => ({
  color: d === 'KILL' ? '#dc2626' : d === 'REPROMPT' ? '#d97706' : '#059669',
  fontWeight: 700,
});

const styles = {
  card:      { background: '#111118', border: '1px solid #1f2937', borderRadius: 10, padding: 16, display: 'flex', flexDirection: 'column', gap: 8 },
  header:    { fontSize: 13, fontWeight: 600, color: '#9ca3af', marginBottom: 4 },
  lbl:       { fontSize: 11, color: '#6b7280' },
  ta:        { width: '100%', background: '#0d0d12', border: '1px solid #1f2937', borderRadius: 6, color: '#e5e7eb', fontSize: 12, padding: '6px 8px', resize: 'vertical', boxSizing: 'border-box' },
  inp:       { width: '100%', background: '#0d0d12', border: '1px solid #1f2937', borderRadius: 6, color: '#e5e7eb', fontSize: 12, padding: '5px 8px', boxSizing: 'border-box' },
  row:       { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8 },
  field:     { display: 'flex', flexDirection: 'column', gap: 4 },
  btn:       { marginTop: 4, padding: '8px 0', borderRadius: 6, border: 'none', cursor: 'pointer', background: '#7c3aed', color: '#fff', fontSize: 13, fontWeight: 600 },
  err:       { color: '#dc2626', fontSize: 12 },
  result:    { marginTop: 4, background: '#0d0d12', border: '1px solid #1f2937', borderRadius: 8, padding: '10px 12px', display: 'flex', flexDirection: 'column', gap: 4 },
  resultRow: { display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#d1d5db' },
  k:         { color: '#6b7280' },
  code:      { fontSize: 11, color: '#7c3aed', fontFamily: 'monospace' },
};
