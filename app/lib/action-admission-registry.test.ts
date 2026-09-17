import assert from 'node:assert/strict'
import test from 'node:test'

import * as admission from './action-admission.ts'

test('Action Admission coverage report exposes exact bounded #755 enforcement without implying broader coverage', () => {
  const reportFn = (admission as unknown as Record<string, unknown>).actionAdmissionCoverageReport
  assert.equal(typeof reportFn, 'function')

  const report = (reportFn as () => Record<string, unknown>)()
  assert.equal(report.version, 'AAR_COVERAGE_V1')
  assert.equal(report.complete, false)
  assert.deepEqual(report.registered_action_classes, ['AUDIT_COUNTER_UPDATE_V1'])

  const entries = report.entries as Array<Record<string, unknown>>
  assert.equal(entries.length, 1)
  assert.deepEqual(entries[0], {
    action_class: 'AUDIT_COUNTER_UPDATE_V1',
    target: '/api/audit',
    aar_required: true,
    enforcement_state: 'ENFORCED_BOUNDED',
    replay_class: 'PROCESS_LOCAL',
    revocation_class: 'RECORD_LOCAL',
    trust_anchor_class: 'SERVER_HMAC_ENV',
    issuer_class: 'NOT_ESTABLISHED',
    decision_effect: 'NON_SCIENTIFIC_EPHEMERAL_AUDIT_COUNTER_UPDATE_ONLY',
    limitations: [
      'NO_DURABLE_CROSS_INSTANCE_REPLAY_PREVENTION',
      'NO_AUTHORITATIVE_POST_ISSUANCE_REVOCATION',
      'NO_PRODUCTION_AAR_ISSUER',
      'NO_TRUST_ANCHOR_CUSTODY_ROTATION_POLICY',
      'NO_DURABLE_ACTION_LEDGER',
      'NO_OTHER_ACTION_CLASS_COVERAGE',
    ],
  })
})
