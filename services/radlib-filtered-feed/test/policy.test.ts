import test from 'node:test'
import assert from 'node:assert/strict'
import {
  DEFAULT_CONTENT_FILTER_POLICY,
  evaluateCandidate,
  matchAnyTerm,
  normalizePolicy,
  rankCandidates,
} from '../src/policy.ts'
import type {FeedCandidate} from '../src/types.ts'

const viewerDid = 'did:plc:viewer'
const now = new Date('2026-08-18T12:00:00.000Z')
test('provider starts with a neutral policy and preserves an explicit empty pack selection', () => {
  assert.deepEqual(DEFAULT_CONTENT_FILTER_POLICY.termPacks, [])
  assert.deepEqual(normalizePolicy({enabled: true, termPacks: []}).termPacks, [])
})

test('disabled policy leaves ordinary candidates included', () => {
  const candidate = post('1', 'did:plc:author', 'An ordinary organizing post')
  const trace = evaluateCandidate(candidate, DEFAULT_CONTENT_FILTER_POLICY, {viewerDid, now})
  assert.equal(trace.included, true)
})

test('legacy pack identifiers do not carry provider vocabulary', () => {
  const policy = normalizePolicy({enabled: true, termPacks: ['legacy-pack']})
  assert.equal(evaluateCandidate(post('1', 'did:plc:a', 'legacy pack content'), policy, {viewerDid, now}).included, true)
})

test('custom terms filter only the terms explicitly supplied by the viewer', () => {
  const policy = normalizePolicy({enabled: true, customTerms: ['field recording']})
  assert.equal(evaluateCandidate(post('1', 'did:plc:a', 'field recording notes'), policy, {viewerDid, now}).included, false)
  assert.equal(evaluateCandidate(post('2', 'did:plc:a', 'recording notes'), policy, {viewerDid, now}).included, true)
})

test('strict legacy algorithm does not add an implicit term', () => {
  const strict = normalizePolicy({enabled: true, algorithm: 'strict'})
  assert.equal(evaluateCandidate(post('1', 'did:plc:a', 'ordinary organizing'), strict, {viewerDid, now}).included, true)
})

test('hard content exclusion beats explicit more preference', () => {
  const policy = normalizePolicy({enabled: true, customTerms: ['blocked phrase']})
  const ranked = rankCandidates([
    post('bad', 'did:plc:a', 'blocked phrase with excellent craft notes'),
    post('good', 'did:plc:b', 'excellent craft notes'),
  ], policy, {viewerDid, now, moreTerms: ['excellent craft notes']})

  assert.deepEqual(ranked.map(item => item.post), ['at://did:plc:b/app.bsky.feed.post/good'])
})

test('explicit author exclusion is attention-only and creates no relationship mutation', () => {
  const policy = normalizePolicy({enabled: true, excludedAuthorDids: ['did:plc:a']})
  const trace = evaluateCandidate(post('1', 'did:plc:a', 'ordinary text'), policy, {viewerDid, now})
  assert.equal(trace.included, false)
  assert.equal(trace.exclusion?.code, 'explicit-author-exclusion')
})

test('selected labeler hide outranks ranking signals', () => {
  const candidate = {
    ...post('1', 'did:plc:a', 'ordinary text'),
    labels: [{src: 'did:plc:labeler' as const, val: 'hide-pol'}],
  }
  const trace = evaluateCandidate(candidate, DEFAULT_CONTENT_FILTER_POLICY, {
    viewerDid,
    now,
    hiddenLabels: [{src: 'did:plc:labeler', val: 'hide-pol'}],
    moreTerms: ['ordinary'],
  })
  assert.equal(trace.included, false)
  assert.equal(trace.exclusion?.code, 'selected-labeler-hide')
})

test('less demotes and more boosts surviving candidates', () => {
  const ranked = rankCandidates([
    post('less', 'did:plc:a', 'boring neutral text'),
    post('more', 'did:plc:b', 'delightful neutral text'),
  ], DEFAULT_CONTENT_FILTER_POLICY, {viewerDid, now, lessTerms: ['boring'], moreTerms: ['delightful']})

  assert.deepEqual(ranked.map(item => item.post), [
    'at://did:plc:b/app.bsky.feed.post/more',
    'at://did:plc:a/app.bsky.feed.post/less',
  ])
})

test('term matcher requires word boundaries', () => {
  assert.equal(matchAnyTerm('field-recording-kit', ['recording']), undefined)
  assert.equal(matchAnyTerm('recording critique', ['recording']), 'recording')
})

function post(rkey: string, authorDid: FeedCandidate['authorDid'], text: string): FeedCandidate {
  return {
    uri: `at://${authorDid}/app.bsky.feed.post/${rkey}`,
    authorDid,
    text,
    createdAt: '2026-08-18T11:00:00.000Z',
    indexedAt: '2026-08-18T11:00:00.000Z',
  }
}
