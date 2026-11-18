const { test } = require('node:test');
const assert = require('node:assert/strict');
const { operations, code, draft } = require('./build-draft.cjs');

class ApiError extends Error { constructor(message, code, status) { super(message); this.code = code; this.status = status; } }
class ThrottledError extends Error { constructor(message, delay) { super(message); this.delay = delay; } }
const success = { ok: true, schemaVersion: '4', data: { valuation: null }, currency: null, quality: { state: 'partial', reasons: ['Missing snapshot'] }, warnings: ['Synthetic sample'], asOf: null, page: { truncated: false } };

function run(operation, response = {}, inputData = {}) {
  const requests = [];
  const z = { errors: { Error: ApiError, ThrottledError }, request: async request => {
    requests.push(request);
    const result = { status: 200, headers: {}, data: success, throwForStatus() { if (this.status >= 400) throw new ApiError('HTTP failure', 'HTTP_ERROR', this.status); }, ...response };
    if (!request.skipThrowForStatus) result.throwForStatus();
    return result;
  } };
  const result = Promise.resolve().then(() => new Function('z', 'bundle', code(operation))(z, { authData: { api_token: 'test-only' }, inputData }));
  return { requests, result };
}

test('only the two approved reads are callable, with no dynamic tool or destination', async () => {
  assert.deepEqual(draft.authentication.requiredScopes, ['accounts:read', 'networth:read']);
  assert.deepEqual(draft.requestTemplate, { params: { source: 'zapier' }, headers: {} });
  assert.deepEqual(operations.map(o => o.tool), ['betteroff_get_overview', 'betteroff_get_net_worth_history']);
  for (const operation of operations) {
    const { requests, result } = run(operation, {}, { tool: 'betteroff_propose_category_change', url: 'https://example.invalid', category: 'ENTERTAINMENT' });
    assert.deepEqual(await result, success);
    assert.equal(requests[0].url, `https://api.betteroff.finance/v1/tools/${operation.tool}`);
    assert.deepEqual(requests[0].body, operation.key === 'get_overview' ? {} : { period: '30d' });
    assert.equal(requests[0].headers.Authorization, 'Bearer test-only');
  }
});
test('preserves incomplete-data and freshness qualifications', async () => assert.deepEqual(await run(operations[0]).result, success));
test('rejects invalid periods before sending a request', async () => {
  const { result, requests } = run(operations[1], {}, { period: 'invalid' });
  await assert.rejects(result, { code: 'INVALID_INPUT' });
  assert.equal(requests.length, 0);
});
test('uses the selected valid period', async () => {
  const { result, requests } = run(operations[1], {}, { period: '90d' });
  await result;
  assert.deepEqual(requests[0].body, { period: '90d' });
});
test('refuses expired and denied credentials', async () => {
  await assert.rejects(run(operations[0], { status: 401 }).result, { code: 'AUTHENTICATION_FAILED' });
  await assert.rejects(run(operations[0], { status: 403 }).result, { code: 'ACCESS_DENIED' });
});
test('respects throttling without treating it as a successful read', async () => {
  await assert.rejects(run(operations[0], { status: 429, headers: { 'retry-after': '37' } }).result, { delay: 37 });
});
test('propagates service errors', async () => await assert.rejects(run(operations[0], { status: 503 }).result, { status: 503 }));
test('rejects malformed and tool-error responses', async () => {
  for (const data of [null, {}, { ok: false }, { ...success, schemaVersion: 'unknown' }]) await assert.rejects(run(operations[0], { data }).result, { code: 'INVALID_RESPONSE' });
});
