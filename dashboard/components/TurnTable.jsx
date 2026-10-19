// Current /api/orchestrate presentation; schema-limited, no inferred approval.
import { normalizeOrchestrateResponse, decisionColor } from '../lib/orchestrate-presentation.mjs';

const COLS = [
  { key: 'turn', label: 'Turn', w: 60 },
  { key: 'decision', label: 'API decision', w: 130 },
  { key: 'evidence_status', label: 'Evidence', w: 100 },
  { key: 'phi_gate', label: 'Φ-Gate', w: 100 },
  { key: 'effective_confidence', label: 'Eff. Conf', w: 100 },
  { key: 'hpg_fired', label: 'HPG', w: 60 },
  { key: 'reason', label: 'Reason', w: 240 },
];

const cell = (row, key) => {
  const val = row[key];
  if (key === 'decision') {
    return <span style={{ ...styles.badge, background: decisionColor(row) }}>{val}</span>;
  }
  if (key === 'effective_confidence') return val === null ? '—' : val.toFixed(3);
  if (key === 'hpg_fired') return val === null ? '—' : (val ? 'Yes' : 'No');
  return val ?? '—';
};

export default function TurnTable({ turns }) {
  const rows = Array.isArray(turns) ? turns.map(normalizeOrchestrateResponse) : [];
  if (!rows.length) return (
    <div style={styles.empty}>No responses yet — submit a request above.</div>
  );
  return (
    <div style={styles.wrap}>
      <div style={styles.heading}>Turn responses — not authorization evidence</div>
      <div style={{ overflowX: 'auto' }}>
        <table style={styles.table}>
          <thead>
            <tr>{COLS.map(c => <th key={c.key} style={{ ...styles.th, width: c.w }}>{c.label}</th>)}</tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} style={i % 2 === 0 ? styles.rowEven : styles.rowOdd}>
                {COLS.map(c => <td key={c.key} style={styles.td}>{cell(row, c.key)}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const styles = {
  wrap:    { background: '#111118', border: '1px solid #1f2937', borderRadius: 10, padding: 16 },
  heading: { fontSize: 13, fontWeight: 600, color: '#9ca3af', marginBottom: 12 },
  table:   { width: '100%', borderCollapse: 'collapse', fontSize: 12 },
  th:      { textAlign: 'left', padding: '6px 10px', color: '#6b7280', borderBottom: '1px solid #1f2937', whiteSpace: 'nowrap' },
  td:      { padding: '6px 10px', borderBottom: '1px solid #1a1a24', color: '#d1d5db', whiteSpace: 'nowrap' },
  rowEven: { background: 'transparent' },
  rowOdd:  { background: '#0d0d12' },
  badge:   { display: 'inline-block', padding: '2px 7px', borderRadius: 4, fontSize: 11, fontWeight: 600, color: '#fff' },
  empty:   { padding: 24, color: '#6b7280', textAlign: 'center', fontSize: 13 },
};
