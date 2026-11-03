import test from 'node:test'
import assert from 'node:assert/strict'
import { RuntimePollEvidence, scheduleRuntimeRequestDeadline } from './runtime-poll-evidence.ts'

test('observed runtime freshness expires at the monotonic deadline, without inventing initial evidence', () => {
  const evidence = new RuntimePollEvidence()
  assert.equal(evidence.isExpired(100_000, 30_000), false)
  const generation = evidence.beginRequest()
  assert.equal(evidence.acceptSuccess(generation, 100), true)
  assert.equal(evidence.isExpired(30_099, 30_000), false)
  assert.equal(evidence.isExpired(30_100, 30_000), true)
  assert.equal(evidence.isExpired(99, 30_000), true)
})

test('superseded and unmounted responses cannot restore current status', () => {
  const evidence = new RuntimePollEvidence()
  const first = evidence.beginRequest()
  const second = evidence.beginRequest()
  assert.equal(evidence.acceptSuccess(first, 100), false)
  assert.equal(evidence.acceptSuccess(second, 200), true)
  assert.equal(evidence.isExpired(30_200, 30_000), true)
  evidence.invalidate()
  assert.equal(evidence.acceptSuccess(second, 30_300), false)
  assert.equal(evidence.isExpired(30_300, 30_000), true)
})

test('a successful later refresh recovers freshness after expiry', () => {
  const evidence = new RuntimePollEvidence()
  const first = evidence.beginRequest()
  assert.equal(evidence.acceptSuccess(first, 100), true)
  assert.equal(evidence.isExpired(40_000, 30_000), true)
  const newer = evidence.beginRequest()
  assert.equal(evidence.acceptSuccess(newer, 40_001), true)
  assert.equal(evidence.isExpired(40_002, 30_000), false)
})

test('never-resolving request has a timeout callback that aborts even without a fetch rejection', () => {
  const controller = new AbortController()
  const callbacks = new Map<number, () => void>()
  let nextId = 0
  let timeouts = 0
  const timers = {
    set: (fn: () => void, milliseconds: number) => {
      assert.equal(milliseconds, 8_000)
      callbacks.set(++nextId, fn)
      return nextId
    },
    clear: (handle: unknown) => { callbacks.delete(Number(handle)) },
  }
  const cancel = scheduleRuntimeRequestDeadline(controller, 8_000, () => { timeouts++ }, timers)
  assert.equal(controller.signal.aborted, false)
  callbacks.get(1)?.()
  assert.equal(controller.signal.aborted, true)
  assert.equal(timeouts, 1)
  callbacks.get(1)?.()
  assert.equal(timeouts, 1)
  cancel()
  assert.equal(callbacks.size, 0)
})

test('superseded request deadline can be cancelled without producing false timeout', () => {
  const controller = new AbortController()
  const callbacks = new Map<number, () => void>()
  let counter = 0
  const timers = {
    set: (fn: () => void, _milliseconds: number) => { callbacks.set(++counter, fn); return counter },
    clear: (handle: unknown) => { callbacks.delete(Number(handle)) },
  }
  let failures = 0
  const cancel = scheduleRuntimeRequestDeadline(controller, 8_000, () => failures++, timers)
  cancel()
  for (const callback of callbacks.values()) callback()
  assert.equal(failures, 0)
  assert.equal(controller.signal.aborted, false)
})

test('invalid success timestamps do not establish evidence', () => {
  const evidence = new RuntimePollEvidence()
  assert.equal(evidence.acceptSuccess(evidence.beginRequest(), Number.NaN), false)
  assert.equal(evidence.isExpired(10, 30_000), false)
})
