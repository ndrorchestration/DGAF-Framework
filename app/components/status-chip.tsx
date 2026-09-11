import { statusMeta } from '../lib/status'
import type { UiState } from '../lib/types'

export function StatusChip({ state, label, compact = false }: { state: UiState; label?: string; compact?: boolean }) {
  const meta = statusMeta(state)
  return <span className="status-chip" data-tone={meta.tone} data-compact={compact ? 'true' : 'false'} title={meta.description}><span className="status-dot" aria-hidden="true" />{label ?? meta.label}</span>
}
