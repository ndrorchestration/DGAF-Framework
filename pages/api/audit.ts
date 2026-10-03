// pages/api/audit.ts — Pages Router API
// ⚠️  STATE RESETS ON COLD START — in-memory only.
// Production upgrade path: bind `state` to an admitted durable store after dependency admission.
import { timingSafeEqual } from 'node:crypto'

import type { NextApiRequest, NextApiResponse } from 'next'

import { consumeAuditAdmission, validateAuditAdmission } from '../../app/lib/action-admission.ts'

export const COLD_START_WARNING =
  'Audit counters are in-memory and reset on each serverless cold start. ' +
  'Configure an admitted durable store before relying on persistent audit state.'

const state = {
  turn_count: 0,
  stable_turns: 0,
  prune_events: 0,
  axiom_count: 1, // T0 axiom guard
  consec_phi_fail: 0,
  cold_start: true,
  cold_start_at: new Date().toISOString(),
}

function demoTrustKey(req: NextApiRequest): string | undefined {
  const expectedToken = process.env.TEKTITE_DEMO_INTERNAL_TOKEN
  const trustKey = process.env.TEKTITE_DEMO_AAR_HMAC_KEY
  const supplied = req.headers?.['x-tektite-demo-token']
  if (!expectedToken || !trustKey || typeof supplied !== 'string') return undefined

  const expected = Buffer.from(expectedToken)
  const actual = Buffer.from(supplied)
  if (expected.length !== actual.length || !timingSafeEqual(expected, actual)) return undefined
  return trustKey
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const admission = validateAuditAdmission(req.body, Date.now(), demoTrustKey(req))
    if (!admission.ok) {
      return res.status(403).json({ status: 'denied', reason: admission.reason, _warning: COLD_START_WARNING })
    }

    if (!consumeAuditAdmission(admission.record.record_id)) {
      return res.status(403).json({ status: 'denied', reason: 'AAR_REPLAY', _warning: COLD_START_WARNING })
    }

    const b = admission.parameters
    if (b.turn_count !== undefined) {
      state.turn_count = b.turn_count
      state.cold_start = false
    }
    if (b.stable_turns !== undefined) state.stable_turns = b.stable_turns
    if (b.prune_events !== undefined) state.prune_events = b.prune_events
    if (b.axiom_count !== undefined) state.axiom_count = b.axiom_count
    if (b.consec_phi_fail !== undefined) state.consec_phi_fail = b.consec_phi_fail

    const postconditionVerified = Object.entries(b).every(
      ([key, value]) => state[key as keyof typeof state] === value,
    )
    const executionReceipt = {
      version: 'AAR_EXECUTION_RECEIPT_V1',
      record_id: admission.record.record_id,
      action_class: admission.record.action_class,
      target: admission.record.target,
      action_digest: admission.record.action_digest,
      executed_at: new Date().toISOString(),
      postcondition: postconditionVerified ? 'VERIFIED' : 'FAILED',
      authority_effect: 'NONE',
      follow_on_authority: 'FRESH_ADJUDICATION_REQUIRED',
    }

    if (!postconditionVerified) {
      return res.status(500).json({
        status: 'postcondition_failed',
        ...state,
        execution_receipt: executionReceipt,
        _warning: COLD_START_WARNING,
      })
    }

    return res.status(200).json({
      status: 'updated',
      ...state,
      execution_receipt: executionReceipt,
      _warning: COLD_START_WARNING,
    })
  }

  return res.status(200).json({
    status: 'ok',
    version: process.env.ENSEMBLE_VERSION ?? '1.8.0',
    ...state,
    _warning: state.cold_start ? COLD_START_WARNING : null,
  })
}
