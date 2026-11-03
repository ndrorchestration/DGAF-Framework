// Presentation-only polling evidence: a successful response is current only for its request generation.
export const DEFAULT_REQUEST_TIMEOUT_MS = 8_000
export const MIN_RUNTIME_FRESHNESS_MS = 30_000

export class RuntimePollEvidence {
  private generation = 0
  private lastObservedAt: number | null = null

  beginRequest(): number {
    return ++this.generation
  }

  isCurrent(generation: number): boolean {
    return generation === this.generation
  }

  acceptSuccess(generation: number, monotonicNow: number): boolean {
    if (!this.isCurrent(generation) || !Number.isFinite(monotonicNow)) return false
    this.lastObservedAt = monotonicNow
    return true
  }

  isExpired(monotonicNow: number, maxAgeMs: number): boolean {
    if (this.lastObservedAt === null) return false
    return !Number.isFinite(monotonicNow) || !Number.isFinite(maxAgeMs) ||
      maxAgeMs <= 0 || monotonicNow < this.lastObservedAt ||
      monotonicNow - this.lastObservedAt >= maxAgeMs
  }

  invalidate(): void {
    this.generation++
  }
}

type DeadlineTimers = {
  set: (callback: () => void, milliseconds: number) => unknown
  clear: (handle: unknown) => void
}

const defaultTimers: DeadlineTimers = {
  set: (callback, milliseconds) => setTimeout(callback, milliseconds),
  clear: handle => clearTimeout(handle as ReturnType<typeof setTimeout>),
}

// A never-settling fetch must still revoke the visible fresh state after its deadline.
export function scheduleRuntimeRequestDeadline(
  controller: AbortController,
  milliseconds: number,
  onTimeout: () => void,
  timers: DeadlineTimers = defaultTimers,
): () => void {
  const handle = timers.set(() => {
    if (controller.signal.aborted) return
    controller.abort()
    onTimeout()
  }, milliseconds)
  return () => timers.clear(handle)
}
