/**
 * AKDC Gate 13: official MCP SDK v2 signed MRTR + atomic SQLite receipt.
 *
 * No external network, verified principal, real user consent, side effects,
 * production key custody, or distributed exactly-once execution.
 */
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { createHash, randomBytes } from 'node:crypto';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';
import { Client, isInputRequiredResult, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { acceptedContent, createMcpHandler, createRequestStateCodec, inputRequired, McpServer } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

const execAsync = promisify(execFile);
const output = new URL('./evidence/', import.meta.url);
mkdirSync(output, { recursive: true });
const root = mkdtempSync(join(tmpdir(), 'akdc-gate13-synthetic-'));
const dbPath = join(root, 'shared-mrtr.sqlite');
const receiptKey = randomBytes(32);
const tokenCodec = createRequestStateCodec({ key: randomBytes(32), ttlSeconds: 120 });
const frames = [];
const receiptOutcomes = [];
const confirmedSchema = z.object({ confirm: z.boolean() });
const operationDigest = createHash('sha256').update('akdc-confirm-fixture:{}', 'utf8').digest('hex');
let entered = 0;

async function receipt(nonce) {
    // Do NOT supply user secrets or real bearer tokens on argv. This is a
    // synthetic decoded SDK nonce, after SDK requestState verification.
    const args = [
        '-m', 'experiments.akdc.mrtr_receipt_ledger_research',
        '--db', dbPath, '--nonce', nonce,
        '--principal', 'fixture-claimed-not-verified',
        '--action', 'akdc-confirm-fixture',
        '--operation-digest', operationDigest
    ];
    const { stdout } = await execAsync('python', args, {
        env: { ...process.env, AKDC_RESEARCH_RECEIPT_KEY_HEX: receiptKey.toString('hex') },
        timeout: 20000
    });
    const response = JSON.parse(stdout);
    assert.equal(response.authority, 'NOT_GRANTED');
    assert.equal(response.outcome, 'SYNTHETIC_COMPLETE');
    assert.ok(['FIRST_RECORDED', 'DUPLICATE_RECORDED'].includes(response.receipt));
    receiptOutcomes.push(response.receipt);
    return response.receipt;
}

function makeServer() {
    const server = new McpServer(
        { name: 'akdc-mrtr-ledger-fixture', version: '1.0.0' },
        { capabilities: { tools: {} }, requestState: { verify: tokenCodec.verify } }
    );
    server.registerTool(
        'akdc-confirm-fixture',
        { description: 'Synthetic no-effect confirmation', inputSchema: z.object({}) },
        async (_args, ctx) => {
            entered++;
            const state = ctx.mcpReq.requestState();
            const accepted = acceptedContent(ctx.mcpReq.inputResponses, 'confirm', confirmedSchema);
            if (state?.step === 'awaiting-confirm' && accepted?.confirm === true) {
                await receipt(state.nonce);
                return { content: [{ type: 'text', text: 'SYNTHETIC-RECORD-ONLY-COMPLETE' }] };
            }
            return inputRequired({
                inputRequests: {
                    confirm: inputRequired.elicit({
                        message: 'Accept synthetic no-effect fixture only?',
                        requestedSchema: confirmedSchema
                    })
                },
                requestState: await tokenCodec.mint({
                    step: 'awaiting-confirm', nonce: randomBytes(16).toString('hex')
                })
            });
        }
    );
    return server;
}

function responseFrames(body, contentType) {
    if (contentType.includes('text/event-stream')) {
        return body.split(/\r?\n/).filter(l => l.startsWith('data:')).map(l => JSON.parse(l.slice(5).trim()));
    }
    if (contentType.includes('json')) return body ? [JSON.parse(body)] : [];
    return [];
}
const handler = createMcpHandler(makeServer);
const transport = new StreamableHTTPClientTransport(new URL('http://test.local/mcp'), {
    fetch: async (url, init) => {
        const request = new Request(url, init);
        const body = await request.clone().text();
        const req = body ? JSON.parse(body) : null;
        const resp = await handler.fetch(request);
        const responses = responseFrames(await resp.clone().text(), resp.headers.get('content-type') ?? '');
        if (req?.method === 'tools/call') {
            const response = responses.find(x => x?.jsonrpc === '2.0' && x.id === req.id &&
                ('result' in x || 'error' in x));
            assert.ok(response, 'SDK response must correlate with raw JSON-RPC request');
            frames.push({ request: req, response });
        }
        return resp;
    }
});
const client = new Client(
    { name: 'akdc-ledger-fixture-client', version: '1.0.0' },
    {
        versionNegotiation: { mode: 'auto' },
        capabilities: { elicitation: { form: {} } },
        inputRequired: { autoFulfill: false }
    }
);
async function toolsCall(extra = {}) {
    return client.request(
        { method: 'tools/call', params: { name: 'akdc-confirm-fixture', arguments: {}, ...extra } },
        { allowInputRequired: true }
    );
}

try {
    await client.connect(transport);
    assert.equal(client.getNegotiatedProtocolVersion(), '2026-07-28');

    const first = await toolsCall();
    assert.ok(isInputRequiredResult(first));
    assert.equal(first.inputRequests.confirm.method, 'elicitation/create');
    assert.equal(entered, 1);

    const damaged = first.requestState.slice(0, -2) + (first.requestState.endsWith('zz') ? 'ab' : 'zz');
    const accepted = { confirm: { action: 'accept', content: { confirm: true } } };
    await assert.rejects(
        () => toolsCall({ requestState: damaged, inputResponses: accepted }),
        /Invalid or expired requestState|32602|requestState/
    );
    assert.equal(entered, 1, 'invalid HMAC state must not enter handler or ledger');
    assert.deepEqual(receiptOutcomes, []);

    const args = { requestState: first.requestState, inputResponses: accepted };
    const admitted = await toolsCall(args);
    assert.equal(admitted.content?.[0]?.text, 'SYNTHETIC-RECORD-ONLY-COMPLETE');
    const duplicate = await toolsCall(args);
    assert.equal(duplicate.content?.[0]?.text, 'SYNTHETIC-RECORD-ONLY-COMPLETE');

    // Real asynchronous SDK RPCs invoke separate Python processes writing the
    // same SQLite DB. BEGIN IMMEDIATE serializes their receipt transactions.
    const concurrent = await Promise.all(Array.from({ length: 4 }, () => toolsCall(args)));
    assert.equal(concurrent.length, 4);
    for (const reply of concurrent) {
        assert.equal(reply.content?.[0]?.text, 'SYNTHETIC-RECORD-ONLY-COMPLETE');
    }

    assert.equal(frames.length, 8);
    assert.equal(entered, 7); // 1 initial + 2 sequential valid + 4 concurrent
    assert.equal(receiptOutcomes.length, 6);
    assert.equal(receiptOutcomes.filter(x => x === 'FIRST_RECORDED').length, 1);
    assert.equal(receiptOutcomes.filter(x => x === 'DUPLICATE_RECORDED').length, 5);

    const { stdout: countOutput } = await execAsync('python', [
        '-c', 'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); print(c.execute("SELECT COUNT(*) FROM mrtr_receipt").fetchone()[0]); c.close()',
        dbPath
    ]);
    assert.equal(Number(countOutput.trim()), 1, 'one persistent receipt across all valid retry attempts');

    const kinds = frames.map(p => p.response.error ? 'protocol_error' : p.response.result?.resultType);
    assert.deepEqual(kinds, ['input_required', 'protocol_error', ...Array(6).fill('complete')]);
    assert.equal(frames[1].response.error?.code, -32602);
    for (const p of frames) {
        assert.equal(p.request.method, 'tools/call');
        assert.equal(p.request.jsonrpc, '2.0');
        assert.equal(p.response.id, p.request.id);
    }

    const wire = {
        schema: 'AKDC-SDK-MRTR-LEDGER-RESEARCH-V1',
        negotiated_version: '2026-07-28',
        synthetic_only: true,
        authority: 'NOT_GRANTED',
        raw_frame_pairs: frames
    };
    const bytes = Buffer.from(JSON.stringify(wire, null, 2) + '\n', 'utf8');
    writeFileSync(new URL('sdk_mrtr_ledger_synthetic.json', output), bytes);
    const manifest = {
        schema: 'AKDC-SDK-MRTR-LEDGER-MANIFEST-V1',
        negotiated_version: '2026-07-28',
        request_count: frames.length,
        categories: kinds,
        invalid_state_rejected_before_ledger: true,
        ledger_first_records: 1,
        ledger_duplicate_records: 5,
        persistent_receipts: 1,
        authority: 'NOT_GRANTED',
        scientific_n_increment: 0,
        wire_sha256: createHash('sha256').update(bytes).digest('hex')
    };
    writeFileSync(new URL('mrtr_ledger_manifest.json', output), JSON.stringify(manifest, null, 2) + '\n');
    console.log('AKDC Gate 13 SDK + atomic receipt research PASS:', JSON.stringify(manifest));
} finally {
    await client.close();
    await handler.close();
    rmSync(root, { recursive: true, force: true });
}
