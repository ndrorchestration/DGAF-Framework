import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import { validateProjection } from '../../public/evidence/tektite-containment-view.mjs'

function fixture() {
  return JSON.parse(readFileSync(new URL('../../public/evidence/tektite-containment-v0.json', import.meta.url), 'utf8'))
}

test('accepts five bounded historical synthetic cases', async () => {
  const value = await validateProjection(fixture())
  assert.equal(value.cases.length, 5)
  assert.equal(value.evaluation_mode, 'FIXED_TIME_SNAPSHOT_REPLAY')
})

test('rejects malformed roots and missing or duplicated cases', async () => {
  for (const value of [null, [], {}, { ...fixture(), cases: [] }]) {
    await assert.rejects(() => validateProjection(value))
  }
  const value = fixture()
  value.cases[1] = value.cases[0]
  await assert.rejects(() => validateProjection(value))
})

test('rejects promoted authority and evidence ceilings', async () => {
  for (const key of ['execution_permitted', 'scientific_n_increment', 'high_assurance', 'source_authenticity']) {
    const value = fixture()
    value.claim_boundary[key] = key === 'execution_permitted' ? true : 'ESTABLISHED'
    await assert.rejects(() => validateProjection(value), key)
  }
  for (const [key, changed] of [['authority_effect', 'GRANTED'], ['execution_permitted', true],
    ['follow_on_authority', 'INHERITED'], ['source_authenticity', 'VERIFIED']] as const) {
    const value = fixture()
    value.cases[0].assessment[key] = changed
    await assert.rejects(() => validateProjection(value), key)
  }
})

test('rejects inconsistent positive claims and receipt linkage', async () => {
  for (const mutate of [
    (v: ReturnType<typeof fixture>) => { v.cases[0].assessment.predicate_results.workers_covered = 'UNKNOWN' },
    (v: ReturnType<typeof fixture>) => { v.cases[0].assessment.reasons = ['STALE'] },
    (v: ReturnType<typeof fixture>) => { v.cases[0].assessment.observed_at = '2026-10-11T08:01:00Z' },
    (v: ReturnType<typeof fixture>) => { v.cases[4].dispatcher_calls = 1 },
    (v: ReturnType<typeof fixture>) => { v.cases[4].prior_assessment_digest = 'sha256:' + 'a'.repeat(64) },
  ]) {
    const value = fixture()
    mutate(value)
    await assert.rejects(() => validateProjection(value))
  }
})

test('checks content digests for evidence IDs and retained binding fields', async () => {
  for (const [key, changed] of [['contract_digest', 'sha256:' + '0'.repeat(64)],
    ['observation_digest', 'sha256:' + '0'.repeat(64)], ['evidence_ids', ['forged:anything']]] as const) {
    const value = fixture()
    value.cases[0].assessment[key] = changed
    await assert.rejects(async () => validateProjection(value), /assessment digest mismatch/)
  }
})
