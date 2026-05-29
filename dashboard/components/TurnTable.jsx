// dashboard/components/TurnTable.jsx
// Per-turn audit table: newest rows at top, 50-row max.
const COLS = [
  { key: 'turn_id',              label: 'Turn ID',       w: 180 },
  { key: 'kappa_category',      label: 'KAPPA',         w: 100 },
  { key: 'dgaf_decision',       label: 'DGAF',          w: 90  },
  { key: 'phi_decision',        label: 'Φ-Gate',        w: 90  },
  { key: 'effective_confidence',label: 'Eff. Conf',     w: 90  },
  { key: 'hpg_applied',         label: 'HPG',           w: 60  },
  { key: 'hpg_step_locked',     label: 'Step↓',         w: 60  },
  { key: 'apogee_grade',        label: 'Apogee',        w: 80  },
  { key: 'gold_star',           label: '★',             w: 40  },
  { key: 'scpe_compression',    label: 'SCPE%',         w: 80  },
  { key: 'seal_hash',           label: 'Seal',          w: 120 },
];

const badge = (val, key) => {
  if (key === 'dgaf_decision') {
    const c = val === 'KILL' ? '#dc2626' : val === 'REPROMPT' ? '#d97706' : '#059669';
    return <span style={{ ...styles.badge, background: c }}>{val}</span>;
  }
  if (key === 'phi_decision') {
    const c = val === 'PASS' ? '#059669' : val === 'REPROMPT' ? '#d97706' : '#374151';
    return <span style={{ ...styles.badge, background: c }}>{val ?? '—'}</span>;
  }
  if (key === 'gold_star') return val ? '⭐' : '·';
  if (key === 'hpg_applied' || key === 'hpg_step_locked') return val ? '✓' : '·';
  if (key === 'seal_hash') return <code style={styles.code}>{String(val ?? '—').slice(0,10)}…</code>;
  if (key === 'effective_confidence') return typeof val === 'number' ? val.toFixed(3) : '—';
  if (key === 'scpe_compression') return typeof val === 'number' ? (val * 100).toFixed(1) + '%' : '—';
  return String(val ?? '—');
};

export default function TurnTable({ turns }) {
  if (!turns.length) return (
    <div style={styles.empty}>No turns yet — fire a request via the Orchestrate panel above.</div>
  );
  return (
    <div style={styles.wrap}>
      <div style={styles.heading}>Turn Audit Log</div>
      <div style={{ overflowX: 'auto' }}>
        <table style={styles.table}>
          <thead>
            <tr>{COLS.map(c => <th key={c.key} style={{ ...styles.th, width: c.w }}>{c.label}</th>)}</tr>
          </thead>
          <tbody>
            {turns.map((row, i) => (
              <tr key={i} style={i % 2 === 0 ? styles.rowEven : styles.rowOdd}>
                {COLS.map(c => <td key={c.key} style={styles.td}>{badge(row[c.key], c.key)}</td>)}
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
  code:    { fontSize: 11, color: '#7c3aed', fontFamily: 'monospace' },
  empty:   { padding: 24, color: '#6b7280', textAlign: 'center', fontSize: 13 },
};
