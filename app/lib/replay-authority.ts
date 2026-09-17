import { createHash } from 'node:crypto'

export type ReplayAuthorityResult = 'CONSUMED' | 'REPLAY' | 'UNAVAILABLE' | 'CONFLICTED'

export type ReplayEffectIdentity = {
  version: string
  action_class: string
  target: string
  policy_id: string
  authorization_id: string
  action_digest: string
}

export type ReplayIdentityInput = ReplayEffectIdentity & {
  record_id?: string
}

export type ReplayAuthority = {
  consumeOnce: (effect: ReplayEffectIdentity) => Promise<ReplayAuthorityResult>
}

export type ConditionalSetOptions = {
  nx: true
}

export type UpstashReplayTransport = {
  set: (key: string, value: string, options: ConditionalSetOptions) => Promise<unknown>
}

function canonicalEffectIdentity(effect: ReplayEffectIdentity): ReplayEffectIdentity {
  return {
    version: effect.version,
    action_class: effect.action_class,
    target: effect.target,
    policy_id: effect.policy_id,
    authorization_id: effect.authorization_id,
    action_digest: effect.action_digest,
  }
}

export function effectIdentityKey(effect: ReplayIdentityInput): string {
  const payload = JSON.stringify(canonicalEffectIdentity(effect))
  const digest = createHash('sha256').update(payload).digest('hex')
  return `aar:effect:${digest}`
}

export function createUpstashReplayAuthority(transport: UpstashReplayTransport): ReplayAuthority {
  return {
    async consumeOnce(effect: ReplayEffectIdentity): Promise<ReplayAuthorityResult> {
      try {
        const result = await transport.set(effectIdentityKey(effect), 'CONSUMED', { nx: true })
        if (result === 'OK') return 'CONSUMED'
        if (result === null) return 'REPLAY'
        return 'CONFLICTED'
      } catch {
        return 'UNAVAILABLE'
      }
    },
  }
}
