'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchDashboardSnapshot } from '../lib/api'
import type { DashboardSnapshot } from '../lib/types'

export type DashboardPhase = 'loading' | 'fresh' | 'stale' | 'error'

export function useDashboardData(refreshMs = 10_000) {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(null)
  const [phase, setPhase] = useState<DashboardPhase>('loading')
  const [error, setError] = useState<string | null>(null)
  const [lastSuccessAt, setLastSuccessAt] = useState<Date | null>(null)
  const controllerRef = useRef<AbortController | null>(null)
  const hasSnapshotRef = useRef(false)

  const refresh = useCallback(async () => {
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    try {
      const next = await fetchDashboardSnapshot(controller.signal)
      setSnapshot(next)
      hasSnapshotRef.current = true
      setLastSuccessAt(new Date())
      setError(null)
      setPhase('fresh')
    } catch (caught) {
      if (controller.signal.aborted) return
      const message = caught instanceof Error ? caught.message : String(caught)
      setError(message)
      setPhase(hasSnapshotRef.current ? 'stale' : 'error')
    }
  }, [])

  useEffect(() => {
    void refresh()
    const interval = window.setInterval(() => void refresh(), refreshMs)
    return () => {
      window.clearInterval(interval)
      controllerRef.current?.abort()
    }
  }, [refresh, refreshMs])

  return { snapshot, phase, error, lastSuccessAt, refresh }
}
