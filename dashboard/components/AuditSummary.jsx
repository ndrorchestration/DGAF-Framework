// dashboard/components/AuditSummary.jsx
// 4 stat cards: turn count, prune events, phi events, PDMAL alerts
export default function AuditSummary({ audit }) {
  const cards = [
    { label: 'Turns',         value: audit?.turn_count     ?? '—', color: '#7c3aed' },
    { label: 'Prune Events',  value: audit?.prune_events   ?? '—', color: '#2563eb' },
    { label: 'Phi Events',    value: audit?.phi_events != null ? JSON.stringify(audit.phi_events).slice(0,40) : '—', color: '#059669' },
    { label: 'PDMAL Alerts',  value: audit?.pdmal_events   ?? '—', color: '#dc2626' },
  ];

  return (
    <div style={styles.grid}>
      {cards.map(c => (
        <div key={c.label} style={styles.card}>
          <div style={{ ...styles.dot, background: c.color }} />
          <div>
            <div style={styles.val}>{String(c.value)}</div>
            <div style={styles.lbl}>{c.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  grid:  { display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 16 },
  card:  { background: '#111118', border: '1px solid #1f2937', borderRadius: 10, padding: '16px 20px', display: 'flex', alignItems: 'center', gap: 14 },
  dot:   { width: 10, height: 10, borderRadius: '50%', flexShrink: 0 },
  val:   { fontSize: 22, fontWeight: 700, color: '#f3f4f6' },
  lbl:   { fontSize: 12, color: '#6b7280', marginTop: 2 },
};
