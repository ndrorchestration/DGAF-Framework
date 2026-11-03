'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchDashboardSnapshot } from '../lib/api'
import { DEFAULT_REQUEST_TIMEOUT_MS, MIN_RUNTIME_FRESHNESS_MS, RuntimePollEvidence, scheduleRuntimeRequestDeadline } from '../lib/runtime-poll-evidence'
import type { DashboardSnapshot } from '../lib/types'

export type DashboardPhase = 'loading' | 'fresh' | 'stale' | 'error'

export function useDashboardData(refreshMs = 10_000) {
  const intervalMs = Math.max(250, refreshMs)
  const requestTimeoutMs = Math.min(DEFAULT_REQUEST_TIMEOUT_MS, Math.max(100, intervalMs * 0.8))
  const maxEvidenceAgeMs = Math.max(MIN_RUNTIME_FRESHNESS_MS, intervalMs * 3)
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(null)
  const [phase, setPhase] = useState<DashboardPhase>('loading')
  const [error, setError] = useState<string | null>(null)
  const [lastSuccessAt, setLastSuccessAt] = useState<Date | null>(null)
  const controllerRef = useRef<AbortController | null>(null)
  const cancelDeadlineRef = useRef<(() => void) | null>(null)
  const evidenceRef = useRef(new RuntimePollEvidence())
  const hasSnapshotRef = useRef(false)

  const refresh = useCallback(async () => {
    const generation = evidenceRef.current.beginRequest()
    cancelDeadlineRef.current?.()
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    const cancelDeadline = scheduleRuntimeRequestDeadline(controller, requestTimeoutMs, () => {
      if (!evidenceRef.current.isCurrent(generation)) return
      setError('Runtime telemetry request timed out; fresh evidence is unavailable.')
      setPhase(hasSnapshotRef.current ? 'stale' : 'error')
    })
    cancelDeadlineRef.current = cancelDeadline
    try {
      const next = await fetchDashboardSnapshot(controller.signal)
      if (controller.signal.aborted || !evidenceRef.current.acceptSuccess(generation, performance.now())) return
      setSnapshot(next)
      hasSnapshotRef.current = true
      setLastSuccessAt(new Date())
      setError(null)
      setPhase('fresh')
    } catch (caught) {
      // Superseded, unmounted, or timed-out requests cannot overwrite current evidence.
      if (controller.signal.aborted || !evidenceRef.current.isCurrent(generation)) return
      const message = caught instanceof Error ? caught.message : String(caught)
      setError(message)
      setPhase(hasSnapshotRef.current ? 'stale' : 'error')
    } finally {
      cancelDeadline()
      if (evidenceRef.current.isCurrent(generation)) {
        cancelDeadlineRef.current = null
        controllerRef.current = null
      }
    }
  }, [requestTimeoutMs])

  useEffect(() => {
    const expireOldEvidence = () => {
      if (!evidenceRef.current.isExpired(performance.now(), maxEvidenceAgeMs)) return
      setError(previous => previous ?? 'Cached runtime telemetry exceeded the freshness deadline.')
      setPhase('stale')
    }
    void refresh()
    const interval = window.setInterval(() => {
      expireOldEvidence()
      void refresh()
    }, intervalMs)
    const onFocus = () => expireOldEvidence()
    const onVisibility = () => { if (!document.hidden) expireOldEvidence() }
    window.addEventListener('focus', onFocus)
    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      window.clearInterval(interval)
      window.removeEventListener('focus', onFocus)
      document.removeEventListener('visibilitychange', onVisibility)
      evidenceRef.current.invalidate()
      cancelDeadlineRef.current?.()
      cancelDeadlineRef.current = null
      controllerRef.current?.abort()
      controllerRef.current = null
    }
  }, [refresh, intervalMs, maxEvidenceAgeMs])

  return { snapshot, phase, error, lastSuccessAt, refresh }
}
