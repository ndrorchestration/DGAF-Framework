// pages/api/mandate.ts — Triumvirate mandate issuance (POST) and retrieval (GET)
// Implements Triumvirate Governance Contract #1: Prime issues signed mandate
import type { NextApiRequest, NextApiResponse } from 'next'
import { createHash } from 'crypto'

export interface Mandate {
  mandate_id:  string
  task:        string
  scope:       string
  constraints: string[]
  issued_by:   string        // must be 'amethyst'
  prefects:    string[]      // must be exactly 2
  triad_type:  'triumvirate' | 'conducted' | 'consensus'
  issued_at:   string
  sha256:      string
  status:      'open' | 'aggregating' | 'signed_off'
}

// In-memory store — replace with Vercel KV for persistence
const mandates: Map<string, Mandate> = new Map()

function signMandate(m: Omit<Mandate, 'sha256'>): string {
  return createHash('sha256')
    .update(JSON.stringify({ mandate_id: m.mandate_id, task: m.task, issued_at: m.issued_at }))
    .digest('hex')
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  // GET  /api/mandate?id=xxx  or  /api/mandate  (list all)
  if (req.method === 'GET') {
    const { id } = req.query
    if (id) {
      const m = mandates.get(String(id))
      if (!m) return res.status(404).json({ error: 'mandate not found', id })
      return res.status(200).json(m)
    }
    return res.status(200).json({
      count:    mandates.size,
      mandates: [...mandates.values()],
    })
  }

  // POST /api/mandate — issue a new mandate
  if (req.method === 'POST') {
    const { task, scope, constraints = [], issued_by, prefects = [], triad_type = 'triumvirate' } = req.body ?? {}

    // Governance Contract #1: Prime must be amethyst
    if (issued_by !== 'amethyst') {
      return res.status(403).json({ error: 'Mandate may only be issued by Prime (amethyst)', received: issued_by })
    }
    // Triumvirate: exactly 2 prefects
    if (triad_type === 'triumvirate' && prefects.length !== 2) {
      return res.status(400).json({ error: 'Triumvirate requires exactly 2 prefects', received: prefects })
    }
    if (!task || !scope) {
      return res.status(400).json({ error: 'task and scope are required' })
    }

    const mandate_id = `M-${Date.now()}-${Math.random().toString(36).slice(2,7).toUpperCase()}`
    const issued_at  = new Date().toISOString()
    const partial: Omit<Mandate, 'sha256'> = {
      mandate_id, task, scope, constraints, issued_by, prefects, triad_type, issued_at, status: 'open',
    }
    const mandate: Mandate = { ...partial, sha256: signMandate(partial) }
    mandates.set(mandate_id, mandate)
    return res.status(201).json(mandate)
  }

  // PATCH /api/mandate — update status (aggregating | signed_off)
  if (req.method === 'PATCH') {
    const { mandate_id, status } = req.body ?? {}
    const m = mandates.get(mandate_id)
    if (!m) return res.status(404).json({ error: 'mandate not found', mandate_id })
    if (!['aggregating','signed_off'].includes(status)) {
      return res.status(400).json({ error: 'status must be aggregating or signed_off' })
    }
    m.status = status
    return res.status(200).json(m)
  }

  res.status(405).json({ error: 'Method not allowed' })
}
