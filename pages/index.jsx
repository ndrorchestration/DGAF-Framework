// pages/index.jsx  — DGAF Audit Dashboard
import { useState, useEffect, useCallback } from 'react';
import TurnTable from '../dashboard/components/TurnTable';
import AuditSummary from '../dashboard/components/AuditSummary';
import PhiTrajectory from '../dashboard/components/PhiTrajectory';
import OrchestratePanel from '../dashboard/components/OrchestratePanel';

export default function Dashboard() {
  const [audit, setAudit]         = useState(null);
  const [turns, setTurns]         = useState([]);
  const [loading, setLoading]     = useState(false);
  const [autoRefresh, setAuto]    = useState(false);
  const [lastUpdated, setUpdated] = useState(null);

  const fetchAudit = useCallback(async () => {
    setLoading(true);
    try {
      const res  = await fetch('/api/audit');
      const data = await res.json();
      setAudit(data);
      setUpdated(new Date().toLocaleTimeString());
    } catch (e) {
      console.error('audit fetch failed', e);
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-refresh every 5 s when toggled on
  useEffect(() => {
    if (!autoRefresh) return;
    const id = setInterval(fetchAudit, 5000);
    return () => clearInterval(id);
  }, [autoRefresh, fetchAudit]);

  // Initial load
  useEffect(() => { fetchAudit(); }, [fetchAudit]);

  const onNewTurn = (rec) => setTurns(prev => [rec, ...prev].slice(0, 50));

  return (
    <div style={styles.root}>
      <header style={styles.header}>
        <div style={styles.headerLeft}>
          <span style={styles.logo}>⬡</span>
          <span style={styles.title}>DGAF Ensemble v1.7 — Audit Dashboard</span>
        </div>
        <div style={styles.headerRight}>
          {lastUpdated && <span style={styles.ts}>Last updated: {lastUpdated}</span>}
          <button style={styles.btn} onClick={fetchAudit} disabled={loading}>
            {loading ? 'Refreshing…' : 'Refresh'}
          </button>
          <button
            style={{ ...styles.btn, background: autoRefresh ? '#7c3aed' : '#374151' }}
            onClick={() => setAuto(v => !v)}
          >
            {autoRefresh ? '⏸ Auto' : '▶ Auto'}
          </button>
        </div>
      </header>

      <main style={styles.main}>
        {/* Top row: summary cards */}
        <AuditSummary audit={audit} />

        {/* Middle row: phi trajectory + orchestrate panel side by side */}
        <div style={styles.row}>
          <PhiTrajectory turns={turns} />
          <OrchestratePanel onNewTurn={onNewTurn} />
        </div>

        {/* Bottom: turn table */}
        <TurnTable turns={turns} />
      </main>
    </div>
  );
}

const styles = {
  root:        { minHeight: '100vh', background: '#0f0f14', color: '#e5e7eb', fontFamily: "'Inter', system-ui, sans-serif" },
  header:      { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid #1f2937', background: '#111118' },
  headerLeft:  { display: 'flex', alignItems: 'center', gap: 10 },
  headerRight: { display: 'flex', alignItems: 'center', gap: 10 },
  logo:        { fontSize: 24, color: '#7c3aed' },
  title:       { fontSize: 15, fontWeight: 600, letterSpacing: '0.02em' },
  ts:          { fontSize: 12, color: '#6b7280' },
  btn:         { padding: '6px 14px', borderRadius: 6, border: 'none', cursor: 'pointer', fontSize: 13, fontWeight: 500, background: '#1f2937', color: '#e5e7eb' },
  main:        { padding: '24px', display: 'flex', flexDirection: 'column', gap: 24 },
  row:         { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 },
};
