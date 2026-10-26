/**
 * AKDC Gate 12: actual MCP SDK v2 MRTR manual retry and adversarial control.
 * Synthetic, in-process, no network, no real side effects or authentic principal.
 */
import assert from 'node:assert/strict';
import { createHash, randomBytes } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { Client, isInputRequiredResult, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { acceptedContent, createMcpHandler, createRequestStateCodec, inputRequired, McpServer } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

const output = new URL('./evidence/', import.meta.url);
mkdirSync(output, { recursive: true });
const framePairs = [];
let handlerEntrances = 0;
const confirmationSchema = z.object({ confirm: z.boolean() });
const stateCodec = createRequestStateCodec({ key: randomBytes(32), ttlSeconds: 120 });

function makeServer() {
    const server = new McpServer(
        { name: 'akdc-mrtr-retry-fixture', version: '1.0.0' },
        { capabilities: { tools: {} }, requestState: { verify: stateCodec.verify } }
    );
    server.registerTool(
        'akdc-confirm-fixture',
        { description: 'Confirm a synthetic label without side effects', inputSchema: z.object({}) },
        async (_args, ctx) => {
            handlerEntrances++;
            const state = ctx.mcpReq.requestState();
            const confirmation = acceptedContent(ctx.mcpReq.inputResponses, 'confirm', confirmationSchema);
            if (state?.step === 'awaiting-confirm' && confirmation?.confirm === true) {
                return { content: [{ type: 'text', text: 'SYNTHETIC-CONFIRMATION-ONLY' }] };
            }
            return inputRequired({
                inputRequests: {
                    confirm: inputRequired.elicit({
                        message: 'Confirm a no-effect synthetic fixture?',
                        requestedSchema: confirmationSchema
                    })
                },
                requestState: await stateCodec.mint({ step: 'awaiting-confirm' })
            });
        }
    );
    return server;
}

function framesFromHTTP(body, contentType) {
    if (contentType.includes('text/event-stream')) {
        return body.split(/\r?\n/).filter(line => line.startsWith('data:'))
            .map(line => JSON.parse(line.slice(5).trim()));
    }
    if (contentType.includes('json')) return body ? [JSON.parse(body)] : [];
    return [];
}
const handler = createMcpHandler(makeServer);
const transport = new StreamableHTTPClientTransport(new URL('http://test.local/mcp'), {
    fetch: async (url, init) => {
        const request = new Request(url, init);
        const reqBody = await request.clone().text();
        const outbound = reqBody ? JSON.parse(reqBody) : null;
        const response = await handler.fetch(request);
        const body = await response.clone().text();
        const inbound = framesFromHTTP(body, response.headers.get('content-type') ?? '');
        if (outbound?.method === 'tools/call') {
            const correlated = inbound.find(x => x?.jsonrpc === '2.0' && x.id === outbound.id &&
                ('result' in x || 'error' in x));
            assert.ok(correlated, 'missing typed-ID-correlated JSON-RPC SDK response');
            framePairs.push({ request: outbound, response: correlated });
        }
        return response;
    }
});
const client = new Client(
    { name: 'akdc-mrtr-fixture-client', version: '1.0.0' },
    {
        versionNegotiation: { mode: 'auto' },
        capabilities: { elicitation: { form: {} } },
        inputRequired: { autoFulfill: false }
    }
);

async function callTool(extraParams = {}) {
    return client.request(
        { method: 'tools/call', params: { name: 'akdc-confirm-fixture', arguments: {}, ...extraParams } },
        { allowInputRequired: true }
    );
}

try {
    await client.connect(transport);
    assert.equal(client.getNegotiatedProtocolVersion(), '2026-07-28');

    const initial = await callTool();
    assert.ok(isInputRequiredResult(initial), 'first SDK response must require input');
    assert.equal(initial.inputRequests?.confirm?.method, 'elicitation/create');
    assert.equal(typeof initial.requestState, 'string');
    assert.ok(initial.requestState.length > 30);
    assert.equal(handlerEntrances, 1, 'first call entered handler once');

    // Tampered opaque requestState MUST be refused by SDK's verification seam.
    const corrupt = initial.requestState.slice(0, -2) +
        (initial.requestState.endsWith('zz') ? 'ab' : 'zz');
    await assert.rejects(() => callTool({
        requestState: corrupt,
        inputResponses: { confirm: { action: 'accept', content: { confirm: true } } }
    }), /Invalid or expired requestState|32602|requestState/);
    assert.equal(handlerEntrances, 1, 'tampered state must not reach handler');

    const accepted = { confirm: { action: 'accept', content: { confirm: true } } };
    const approved = await callTool({ requestState: initial.requestState, inputResponses: accepted });
    assert.equal(approved.content?.[0]?.text, 'SYNTHETIC-CONFIRMATION-ONLY');
    assert.equal(handlerEntrances, 2);

    // Negative control: verified HMAC state DOES NOT imply single-use.
    // This fixture has no real action; repeat acceptance is expected.
    const repeated = await callTool({ requestState: initial.requestState, inputResponses: accepted });
    assert.equal(repeated.content?.[0]?.text, 'SYNTHETIC-CONFIRMATION-ONLY');
    assert.equal(handlerEntrances, 3);

    assert.equal(framePairs.length, 4);
    const kinds = framePairs.map(p => p.response.error ? 'protocol_error' : p.response.result?.resultType);
    assert.deepEqual(kinds, ['input_required', 'protocol_error', 'complete', 'complete']);
    assert.equal(framePairs[1].response.error?.code, -32602, 'tampered requestState must be Invalid Params');
    for (const pair of framePairs) {
        assert.equal(pair.request.method, 'tools/call');
        assert.equal(pair.request.jsonrpc, '2.0');
        assert.equal(pair.response.id, pair.request.id);
    }
    assert.equal(framePairs[2].request.params.requestState, initial.requestState);
    assert.equal(framePairs[3].request.params.requestState, initial.requestState);
    const trace = {
        schema: 'AKDC-SDK-MRTR-RETRY-RESEARCH-V1',
        negotiated_version: '2026-07-28',
        fixture_data: 'SYNTHETIC_ONLY',
        request_state_attestation: 'SDK_HMAC_INTEGRITY_ONLY_NOT_SINGLE_USE_NOT_AUTHENTICATED',
        raw_frame_pairs: framePairs
    };
    const bytes = Buffer.from(JSON.stringify(trace, null, 2) + '\n', 'utf8');
    writeFileSync(new URL('sdk_mrtr_retry_synthetic.json', output), bytes);
    const manifest = {
        schema: 'AKDC-SDK-MRTR-RETRY-EVIDENCE-V1',
        negotiated_version: '2026-07-28',
        request_count: framePairs.length,
        classifications: kinds,
        tampered_state_refused_before_handler: true,
        valid_state_replay_accepted_negative_control: true,
        handler_entrances: handlerEntrances,
        trace_sha256: createHash('sha256').update(bytes).digest('hex'),
        scientific_n_increment: 0,
        authority: 'NOT_GRANTED'
    };
    writeFileSync(new URL('mrtr_retry_manifest.json', output), JSON.stringify(manifest, null, 2) + '\n');
    console.log('AKDC Gate 12 official SDK MRTR retry probe PASS:', JSON.stringify(manifest));
} finally {
    await client.close();
    await handler.close();
}
