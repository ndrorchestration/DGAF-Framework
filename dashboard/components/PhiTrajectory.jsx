// dashboard/components/PhiTrajectory.jsx
// SVG sparkline of effective_confidence over turns, with φ* = 0.618 reference line.
export default function PhiTrajectory({ turns }) {
  const W = 560, H = 200, PAD = 32;
  const data = [...turns].reverse();
  const n    = data.length;

  const xScale = i  => PAD + (i / Math.max(n - 1, 1)) * (W - PAD * 2);
  const yScale = v  => H - PAD - (v * (H - PAD * 2));
  const phiY   = yScale(0.618);

  const points = data.map((t, i) =>
    `${xScale(i)},${yScale(t.effective_confidence ?? 0.5)}`
  ).join(' ');

  const dgafKillPoints = data
    .map((t, i) => ({ t, i }))
    .filter(({ t }) => t.dgaf_decision === 'KILL');

  return (
    <div style={styles.card}>
      <div style={styles.header}>Effective Confidence Trajectory</div>
      <svg width={W} height={H} style={{ display: 'block' }}>
        {/* φ* reference line */}
        <line x1={PAD} y1={phiY} x2={W - PAD} y2={phiY}
              stroke="#7c3aed" strokeWidth={1} strokeDasharray="4 3" opacity={0.6} />
        <text x={W - PAD + 4} y={phiY + 4} fill="#7c3aed" fontSize={10}>φ*</text>

        {/* Confidence sparkline */}
        {n > 1 && (
          <polyline points={points} fill="none" stroke="#2563eb" strokeWidth={2} />
        )}
        {/* Data points */}
        {data.map((t, i) => (
          <circle key={i} cx={xScale(i)} cy={yScale(t.effective_confidence ?? 0.5)}
                  r={3} fill={t.gold_star ? '#f59e0b' : '#2563eb'} />
        ))}
        {/* KILL markers */}
        {dgafKillPoints.map(({ t, i }) => (
          <text key={i} x={xScale(i) - 5} y={yScale(t.effective_confidence ?? 0.5) - 8}
                fill="#dc2626" fontSize={10} fontWeight="bold">✕</text>
        ))}

        {/* Axes */}
        <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} stroke="#374151" strokeWidth={1} />
        <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} stroke="#374151" strokeWidth={1} />
        <text x={PAD - 4} y={PAD + 4} fill="#6b7280" fontSize={9} textAnchor="end">1.0</text>
        <text x={PAD - 4} y={H - PAD + 4} fill="#6b7280" fontSize={9} textAnchor="end">0.0</text>
        <text x={W / 2} y={H - 6} fill="#6b7280" fontSize={9} textAnchor="middle">Turns (newest right)</text>
      </svg>
      <div style={styles.legend}>
        <span style={styles.dot('#f59e0b')} /> Gold Star &nbsp;
        <span style={styles.dot('#2563eb')} /> Normal &nbsp;
        <span style={{ color: '#dc2626', fontSize: 11 }}>✕ DGAF Kill</span>
      </div>
    </div>
  );
}

const styles = {
  card:   { background: '#111118', border: '1px solid #1f2937', borderRadius: 10, padding: 16 },
  header: { fontSize: 13, fontWeight: 600, marginBottom: 12, color: '#9ca3af' },
  legend: { fontSize: 11, color: '#6b7280', marginTop: 8, display: 'flex', alignItems: 'center', gap: 4 },
  dot:    (bg) => ({
    display: 'inline-block', width: 8, height: 8,
    borderRadius: '50%', background: bg, marginRight: 3
  }),
};
