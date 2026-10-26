/**
 * Gate 11: official MCP TypeScript v2 SDK, real in-process 2026-07-28 HTTP
 * wire frames. No remote MCP server, credentials, user tools or mutations.
 * The fixture values are synthetic and intentionally non-sensitive.
 */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { Client, isInputRequiredResult, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { McpServer, createMcpHandler, inputRequired } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

const output = new URL('./evidence/', import.meta.url);
mkdirSync(output, { recursive: true });
const framePairs = [];

function makeServer() {
    const server = new McpServer({ name: 'akdc-test-only', version: '1.0.0' });
    server.registerTool(
        'akdc-read-only',
        { description: 'Return a synthetic fixture string only', inputSchema: z.object({}) },
        async () => ({ content: [{ type: 'text', text: 'TEST-FIXTURE-COMPLETE' }] })
    );
    server.registerTool(
        'akdc-mrtr-state-only',
        { description: 'Return an opaque synthetic MRTR state (not executable)', inputSchema: z.object({}) },
        async () => inputRequired({ requestState: 'SYNTHETIC-MRTR-STATE-ONLY' })
    );
    return server;
}

function messagesFromResponse(body, contentType) {
    if (contentType.includes('text/event-stream')) {
        return body.split(/\r?\n/)
            .filter(line => line.startsWith('data:'))
            .map(line => JSON.parse(line.slice(5).trim()));
    }
    if (contentType.includes('json')) {
        return body ? [JSON.parse(body)] : [];
    }
    return [];
}

const handler = createMcpHandler(makeServer);
const transport = new StreamableHTTPClientTransport(new URL('http://test.local/mcp'), {
    fetch: async (url, init) => {
        const request = new Request(url, init);
        const reqText = await request.clone().text();
        const outbound = reqText ? JSON.parse(reqText) : null;
        // This is a real SDK request submitted to the official handler,
        // not an object made up by AKDC.
        const response = await handler.fetch(request);
        const body = await response.clone().text();
        const frames = messagesFromResponse(body, response.headers.get('content-type') ?? '');
        if (outbound?.method === 'tools/call') {
            const reply = frames.find(frame =>
                frame && frame.id === outbound.id && frame.jsonrpc === '2.0' &&
                ('result' in frame || 'error' in frame)
            );
            assert.ok(reply, 'SDK response must correlate to request JSON-RPC id');
            framePairs.push({ request: outbound, response: reply });
        }
        return response;
    }
});
const client = new Client(
    { name: 'akdc-test-only', version: '1.0.0' },
    { versionNegotiation: { mode: 'auto' }, inputRequired: { autoFulfill: false } }
);

try {
    await client.connect(transport);
    assert.equal(client.getNegotiatedProtocolVersion(), '2026-07-28');

    const complete = await client.callTool({ name: 'akdc-read-only', arguments: {} });
    assert.equal(complete.content?.[0]?.text, 'TEST-FIXTURE-COMPLETE');
    assert.equal('resultType' in complete, false, 'wire-only resultType must be consumed by public SDK');

    const mrtr = await client.request(
        { method: 'tools/call', params: { name: 'akdc-mrtr-state-only', arguments: {} } },
        { allowInputRequired: true }
    );
    assert.ok(isInputRequiredResult(mrtr), 'manual SDK MRTR request must expose its neutral result');
    assert.equal(mrtr.requestState, 'SYNTHETIC-MRTR-STATE-ONLY');
    assert.equal(framePairs.length, 2, 'expected exactly two tools/call exchanges');

    const completePair = framePairs.find(pair => pair.request.params.name === 'akdc-read-only');
    const mrtrPair = framePairs.find(pair => pair.request.params.name === 'akdc-mrtr-state-only');
    assert.ok(completePair && mrtrPair);
    assert.equal(completePair.response.result?.resultType, 'complete');
    assert.equal(mrtrPair.response.result?.resultType, 'input_required');
    assert.equal(mrtrPair.response.result.requestState, 'SYNTHETIC-MRTR-STATE-ONLY');

    for (const pair of framePairs) {
        assert.equal(pair.request.method, 'tools/call');
        assert.equal(pair.request.jsonrpc, '2.0');
        assert.ok(pair.request.params?._meta, '2026 SDK request meta required');
        assert.equal(pair.response.id, pair.request.id);
        assert.equal(pair.response.jsonrpc, '2.0');
    }

    const wire = { schema: 'AKDC-SDK-WIRE-FIXTURE-RESEARCH-V1', negotiated_version: '2026-07-28', framePairs };
    const bytes = Buffer.from(JSON.stringify(wire, null, 2) + '\n', 'utf8');
    writeFileSync(new URL('sdk_wire_synthetic.json', output), bytes);
    const manifest = {
        kind: 'IN_PROCESS_OFFICIAL_SDK_SYNTHETIC_WIRE',
        sdk_packages: JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8')).dependencies,
        negotiated_version: '2026-07-28',
        tools_call_pair_count: framePairs.length,
        result_types: framePairs.map(pair => pair.response.result?.resultType),
        wire_sha256: createHash('sha256').update(bytes).digest('hex'),
        source_capture_attestation: 'IN_PROCESS_TEST_ONLY_NOT_EXTERNAL',
        dgaf_authority: 'NOT_GRANTED',
        scientific_n_increment: 0
    };
    writeFileSync(new URL('trace_manifest.json', output), JSON.stringify(manifest, null, 2) + '\n');
    console.log('AKDC Gate 11 SDK probe PASSED:', JSON.stringify(manifest));
} finally {
    await client.close();
    await handler.close();
}
