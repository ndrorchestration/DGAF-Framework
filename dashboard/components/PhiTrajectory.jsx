// dashboard/components/PhiTrajectory.jsx
// SVG sparkline of only observed effective confidence; missing values are never fabricated.
import { normalizeOrchestrateResponse, confidenceSegments } from '../lib/orchestrate-presentation.mjs';
export default function PhiTrajectory({ turns }) {
  const W = 560, H = 200, PAD = 32;
  const data = (Array.isArray(turns) ? turns : []).map(normalizeOrchestrateResponse).reverse();
  const n    = data.length;

  const xScale = i  => PAD + (i / Math.max(n - 1, 1)) * (W - PAD * 2);
  const yScale = v  => H - PAD - (v * (H - PAD * 2));
  const phiY   = yScale(0.618);

  const observed = data.map((t, i) => ({ t, i }))
    .filter(({ t }) => t.effective_confidence !== null);
  // Missing observations split the line; do not visually bridge evidence gaps.
  const segments = confidenceSegments(data);
  const blocked = data.map((t, i) => ({ t, i }))
    .filter(({ t }) => ['KILL', 'REJECT', 'BLOCKED'].includes(t.decision));

  return (
    <div style={styles.card}>
      <div style={styles.header}>Effective Confidence Trajectory</div>
      <svg width={W} height={H} style={{ display: 'block' }}>
        {/* φ* reference line */}
        <line x1={PAD} y1={phiY} x2={W - PAD} y2={phiY}
              stroke="#7c3aed" strokeWidth={1} strokeDasharray="4 3" opacity={0.6} />
        <text x={W - PAD + 4} y={phiY + 4} fill="#7c3aed" fontSize={10}>φ*</text>

        {/* Confidence sparkline */}
        {segments.filter(segment => segment.length > 1).map((segment, i) => (
          <polyline key={i}
            points={segment.map(({ index, confidence }) => `${xScale(index)},${yScale(confidence)}`).join(' ')}
            fill="none" stroke="#2563eb" strokeWidth={2} />
        ))}
        {/* Data points */}
        {observed.map(({ t, i }) => (
          <circle key={i} cx={xScale(i)} cy={yScale(t.effective_confidence)}
                  r={3} fill="#2563eb" />
        ))}
        {/* KILL markers */}
        {blocked.map(({ t, i }) => (
          <text key={i} x={xScale(i) - 5}
                y={(t.effective_confidence === null ? H - PAD : yScale(t.effective_confidence)) - 8}
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
        <span style={styles.dot('#2563eb')} /> Observed confidence &nbsp;
        <span style={{ color: '#dc2626', fontSize: 11 }}>✕ Blocked / rejected</span>
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
